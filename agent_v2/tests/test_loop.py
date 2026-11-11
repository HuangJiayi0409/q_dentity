import importlib.util
import tempfile
import unittest
from pathlib import Path

from agent_v2.models import Budget, Candidate, Obligation, initial_state, thaw
from agent_v2.storage import RunStore, freeze_source, IntegrityError
from agent_v2.tests.test_executor import RecordingChecker, result


class QueueAdapter:
    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    def execute(self, identity, method, source, attempt_dir, seconds):
        self.calls.append((identity, method, seconds))
        return self.results.pop(0).to_dict()


class FinalChecker(RecordingChecker):
    def __init__(self, final=True):
        super().__init__(); self.final = final; self.final_calls = []

    def accept_original(self, report, source, attempt_dir):
        self.final_calls.append(report)
        return {'accepted': self.final, 'status': 'original_theorem_proved' if self.final else 'incomplete',
                'evidence': {'source_sha256': source['sha256'], 'theorem': source['theorem']},
                'sigma': {'code': 'checked' if self.final else 'final_rejected'}}


class LoopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); root = Path(self.tmp.name)
        src = root / 'source.lean'; src.write_text('theorem demo : True := by sorry\n')
        self.store = RunStore.create(root / 'runs', 'run')
        self.source = freeze_source(src, 'synthetic', 'demo', self.store, proposition='True')
        self.state, self.rep = initial_state(self.source, Budget(100, 5))

    def tearDown(self): self.tmp.cleanup()

    def graph(self):
        from agent_v2.graph import Graph, Outlet
        graph = Graph(self.source.sha256); graph.add_node(self.rep)
        graph.add_outlet(Outlet('outlet', 'original', 'CAS', 'method',
            {'method': 'telescoping', 'seconds': 10.0}, ('closed_prop',)))
        return graph

    def candidate(self, closes='original', name='c', proposition='True', replaces=()):
        return Candidate(name, proposition, 'by trivial', 'AgentV2Candidate.proof',
                         self.source.sha256, (), closes, tuple(replaces))

    def run_loop(self, results, checker=None, state=None):
        from agent_v2.executor import Executor
        from agent_v2.loop import run
        adapter = QueueAdapter(results)
        state = run(state or self.state, self.graph(), self.store,
                    Executor({'method': adapter}), checker or FinalChecker())
        return state, adapter

    def test_reselect_after_one_action_using_changed_residual(self):
        from agent_v2.executor import Executor
        from agent_v2.loop import run
        from agent_v2.router import RuleBasedRouter
        child = Obligation('leaf', 'subgoal', 'True', 'True', self.source.sha256, 'a')
        bridge = self.candidate('original', 'bridge', '(True) → (True)', [child])
        adapter = QueueAdapter([result([bridge], [child]), result([self.candidate('leaf', 'leaf_proof')])])
        observations = []
        class Router(RuleBasedRouter):
            def choose(inner, state, legal):
                observations.append(tuple(o.id for o in state.O))
                return super().choose(state, legal)
        final = run(self.state, self.graph(), self.store, Executor({'method': adapter}),
                    FinalChecker(), Router())
        self.assertEqual(observations, [('original',), ('leaf',)])
        self.assertEqual(final.round_index, 2)
        self.assertEqual(len(adapter.calls), 2)
        self.assertEqual(final.status, 'original_theorem_proved')

    def test_repeated_failed_action_stops_and_checkpoints(self):
        final, adapter = self.run_loop([result()])
        self.assertEqual(len(adapter.calls), 1)
        self.assertEqual(final.status, 'incomplete')
        self.assertEqual(final.O, self.state.O)
        self.assertEqual(self.store.load_checkpoint()['state']['round_index'], 1)
        self.assertLess(final.b.seconds, self.state.b.seconds)

    def test_budget_zero_executes_nothing(self):
        import dataclasses
        final, adapter = self.run_loop([], state=dataclasses.replace(self.state, b=Budget(100, 0)))
        self.assertEqual(adapter.calls, [])
        self.assertEqual(final.status, 'budget_exhausted')
        self.assertTrue(self.store.path('checkpoint.json').exists())

    def test_empty_O_still_requires_final_acceptance(self):
        checker = FinalChecker(False)
        final, _ = self.run_loop([result([self.candidate()])], checker)
        self.assertEqual(len(checker.final_calls), 1)
        self.assertEqual(final.status, 'incomplete')
        self.assertEqual(final.O, self.state.O)
        self.assertEqual(len(final.C), 1)
        self.assertEqual(final.links, ())

    def test_source_tampering_rejects_before_adapter(self):
        Path(self.source.path).write_text('changed')
        with self.assertRaises(IntegrityError): self.run_loop([])

    def test_resume_rechecks_proofs_instead_of_trusting_saved_flags(self):
        from agent_v2.loop import resume
        final, _ = self.run_loop([result([self.candidate(closes=None)])])
        with self.assertRaises(IntegrityError): resume(self.store, RecordingChecker(False))

    def test_final_checker_exception_reopens_and_charges_before_stopping(self):
        import time
        class CrashingChecker(FinalChecker):
            def accept_original(self, *args):
                time.sleep(0.02)
                raise RuntimeError('checker unavailable')
        final, _ = self.run_loop([result([self.candidate()])], CrashingChecker())
        self.assertEqual(final.O, self.state.O)
        self.assertNotEqual(final.status, 'original_theorem_proved')
        self.assertLess(final.b.seconds, 99.98)
        self.assertFalse(self.store.read_json('run.json')['original_identity_proved'])

    def test_failed_resume_charges_replay_cost_and_saves_checkpoint(self):
        import time
        from agent_v2.loop import resume
        self.run_loop([result([self.candidate(closes=None)])])
        before = self.store.load_checkpoint()['state']['b']['seconds']
        class SlowReject(RecordingChecker):
            def check_partial(self, *args):
                time.sleep(0.02)
                return {'accepted': False, 'status': 'incomplete'}
        with self.assertRaises(IntegrityError): resume(self.store, SlowReject())
        after = self.store.load_checkpoint()['state']['b']['seconds']
        self.assertLess(after, before - 0.02)

    def test_environment_failure_reselects_another_available_route(self):
        from agent_v2.executor import Executor
        from agent_v2.graph import Outlet
        from agent_v2.loop import run
        graph = self.graph()
        graph.add_outlet(Outlet('second', 'original', 'CAS', 'method',
            {'method': 'alternative', 'seconds': 20.0}, ('closed_prop',)))
        adapter = QueueAdapter([result(status='environment_blocked'), result([self.candidate()])])
        final = run(self.state, graph, self.store, Executor({'method': adapter}), FinalChecker())
        self.assertEqual(final.status, 'original_theorem_proved')
        self.assertEqual([call[1] for call in adapter.calls], ['telescoping', 'alternative'])
        self.assertEqual(final.round_index, 2)

    def test_resume_replaces_old_receipts_with_fresh_evidence(self):
        from agent_v2.loop import resume
        self.run_loop([result([self.candidate(closes=None)])])
        class FreshChecker(RecordingChecker):
            def check_partial(self, candidate, context):
                checked = super().check_partial(candidate, context)
                checked['evidence']['replay_marker'] = 'fresh'
                return checked
        state, graph = resume(self.store, FreshChecker())
        self.assertEqual(state.C[0].evidence.get('replay_marker'), 'fresh')
        legal, reasons = graph.legal_candidates(state)
        self.assertEqual(legal, [], 'fresh evidence for the same lemma must not unlock a repeated action')
        self.assertIn('duplicate_action', str(reasons))


if __name__ == '__main__': unittest.main()
