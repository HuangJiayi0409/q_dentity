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

    def test_no_affordable_action_stops_for_budget_without_execution(self):
        from agent_v2.executor import Executor
        from agent_v2.graph import Graph, Outlet
        from agent_v2.loop import run
        graph = Graph(self.source.sha256); graph.add_node(self.rep)
        graph.add_outlet(Outlet('expensive', 'original', 'CAS', 'method',
            {'method': 'telescoping'}, ('closed_prop',), estimated_seconds=101.0))
        adapter = QueueAdapter([])
        final = run(self.state, graph, self.store, Executor({'method': adapter}), FinalChecker())
        self.assertEqual(final.status, 'budget_exhausted')
        self.assertEqual(self.store.read_json('run.json')['stop_reason'], 'no_affordable_action')
        self.assertEqual(adapter.calls, [])
        self.assertEqual(final.O, self.state.O)
        self.assertEqual(final.b.actions, self.state.b.actions)

    def test_no_route_distinguishes_contract_and_missing_capability(self):
        from agent_v2.executor import Executor
        from agent_v2.graph import Graph, Outlet
        from agent_v2.loop import run
        for kind, reason in [('contract', 'input_contract_mismatch'), ('empty', 'graph_capability_missing')]:
            with self.subTest(kind=kind):
                graph = Graph(self.source.sha256); graph.add_node(self.rep)
                if kind == 'contract':
                    graph.add_outlet(Outlet('wrong-domain', 'original', 'CAS', 'method', {},
                        ('closed_prop',), semantic_domain='Field'))
                store = RunStore.create(Path(self.tmp.name) / 'runs', kind)
                # A frozen source snapshot must belong to this run.
                source = freeze_source(self.source.path, 'synthetic', 'demo', store, proposition='True')
                state, _ = initial_state(source, Budget(100, 5))
                final = run(state, graph, store, Executor({'method': QueueAdapter([])}), FinalChecker())
                self.assertEqual(final.status, 'incomplete')
                self.assertEqual(store.read_json('run.json')['stop_reason'], reason)

    def test_duplicate_failure_has_its_own_stop_reason(self):
        self.run_loop([result()])
        self.assertEqual(self.store.read_json('run.json')['stop_reason'], 'repeated_actions_exhausted')

    def test_disabled_only_route_is_environment_blocked(self):
        from agent_v2.executor import Executor
        from agent_v2.graph import Graph, Outlet
        from agent_v2.loop import run
        graph = Graph(self.source.sha256); graph.add_node(self.rep)
        graph.add_outlet(Outlet('disabled', 'original', 'LLM', 'llm', {}, ('closed_prop',)))
        final = run(self.state, graph, self.store, Executor({}), FinalChecker())
        self.assertEqual(final.status, 'environment_blocked')
        self.assertEqual(self.store.read_json('run.json')['stop_reason'], 'environment_unavailable')

    def assert_final_classification(self, status, code, exception=None, evidence_mismatch=False):
        class Checker(FinalChecker):
            def accept_original(inner, report, source, attempt_dir):
                if exception is not None: raise exception
                if evidence_mismatch:
                    return {'accepted': True, 'status': 'original_theorem_proved',
                            'evidence': {'source_sha256': '0' * 64, 'theorem': source['theorem']},
                            'sigma': {'code': 'claimed_success'}}
                return {'accepted': False, 'status': status, 'evidence': {}, 'sigma': {'code': code}}
        final, _ = self.run_loop([result([self.candidate()])], Checker())
        self.assertEqual(final.status, status)
        self.assertEqual(final.O, self.state.O)
        self.assertEqual(final.links, ())
        self.assertEqual(len(final.C), 1)
        self.assertFalse(self.store.read_json('run.json')['original_identity_proved'])
        self.assertEqual(self.store.read_json('run.json')['stop_reason'], code)
        self.assertEqual(self.store.load_checkpoint()['state']['status'], status)
        self.assertGreater(final.b.seconds, 0, 'explicit failure must survive even with time left')

    def test_final_integrity_result_keeps_integrity_category(self):
        self.assert_final_classification('integrity_error', 'hash_mismatch')

    def test_final_budget_result_keeps_budget_category(self):
        self.assert_final_classification('budget_exhausted', 'lean_timeout')

    def test_final_environment_result_keeps_environment_category(self):
        self.assert_final_classification('environment_blocked', 'dependency_missing')

    def test_final_integrity_exception_keeps_integrity_category(self):
        self.assert_final_classification('integrity_error', 'final_integrity_error',
                                         IntegrityError('hash_mismatch'))

    def test_final_timeout_exception_keeps_budget_category(self):
        self.assert_final_classification('budget_exhausted', 'final_checker_timeout',
                                         TimeoutError('deadline'))

    def test_final_false_success_binding_is_integrity_error(self):
        self.assert_final_classification('integrity_error', 'original_evidence_binding_mismatch',
                                         evidence_mismatch=True)

    def test_source_changed_during_final_check_stops_as_integrity_error(self):
        class ChangingChecker(FinalChecker):
            def accept_original(inner, report, source, attempt_dir):
                Path(source['path']).write_text('changed during final verification')
                return super().accept_original(report, source, attempt_dir)
        final, _ = self.run_loop([result([self.candidate()])], ChangingChecker())
        self.assertEqual(final.status, 'integrity_error')
        self.assertEqual(final.O, self.state.O)
        self.assertFalse(self.store.read_json('run.json')['original_identity_proved'])

    def test_late_success_reports_wall_budget_not_lean_verified_as_stop_reason(self):
        from unittest.mock import patch
        from agent_v2.executor import verify_and_update
        from agent_v2.models import JointAction
        from agent_v2.loop import _final
        action = JointAction('a', 'identity', 'original', 'original', 'CAS', 'method', {})
        closed, _ = verify_and_update(self.state, action, result([self.candidate()]), RecordingChecker(),
            {'source_sha256': self.source.sha256, 'run_dir': str(self.store.root),
             'attempt_dir': str(self.store.root / 'attempt'), 'seconds': 10.0})
        with patch('agent_v2.loop.time.monotonic', side_effect=[100.0, 201.0]):
            final = _final(closed, self.graph(), self.store, FinalChecker())
        self.assertEqual(final.status, 'budget_exhausted')
        self.assertEqual(self.store.read_json('run.json')['stop_reason'], 'wall_budget_exhausted')

    def test_stop_classification_uses_relevant_current_blockers(self):
        from agent_v2.recovery import classify_stop
        cases = [
            (['budget_insufficient', 'semantic_domain_mismatch', 'no_transition_from_current'],
             ('budget_exhausted', 'no_affordable_action')),
            (['duplicate_action', 'no_transition_from_current'],
             ('incomplete', 'repeated_actions_exhausted')),
            (['semantic_domain_mismatch', 'index_ranges_mismatch'],
             ('incomplete', 'input_contract_mismatch')),
            (['bridge_not_verified', 'semantic_domain_mismatch'],
             ('incomplete', 'graph_capability_missing')),
            (['original_binding_mismatch', 'budget_insufficient'],
             ('integrity_error', 'graph_integrity_error')),
        ]
        for codes, expected in cases:
            with self.subTest(codes=codes):
                self.assertEqual(classify_stop(self.state, [], [{'code': c} for c in codes]), expected)

    def test_old_unrelated_environment_failure_does_not_reclassify_current_duplicate(self):
        from dataclasses import replace
        from agent_v2.models import Attempt
        from agent_v2.recovery import classify_stop
        state = replace(self.state, attempts=(Attempt('f1', 'current', 'search_exhausted', 1),
            Attempt('f2', 'irrelevant', 'formal_frontend_unavailable', 2)))
        reasons = [{'route_id': 'current', 'code': 'duplicate_action',
                    'attempt_action_id': 'current', 'attempt_code': 'search_exhausted'}]
        self.assertEqual(classify_stop(state, [], reasons), ('incomplete', 'repeated_actions_exhausted'))
        reasons[0]['attempt_code'] = 'formal_frontend_unavailable'
        self.assertEqual(classify_stop(state, [], reasons), ('environment_blocked', 'environment_unavailable'))

    def test_malformed_final_result_is_recorded_without_losing_terminal_checkpoint(self):
        class NonJSONChecker(FinalChecker):
            def accept_original(inner, report, source, attempt_dir):
                return {'accepted': False, 'status': 'integrity_error', 'evidence': {},
                        'sigma': {'code': 'hash_mismatch'}, 'extra': object()}
        final, _ = self.run_loop([result([self.candidate()])], NonJSONChecker())
        self.assertEqual(final.status, 'integrity_error')
        self.assertEqual(final.O, self.state.O)
        self.assertEqual(self.store.load_checkpoint()['state']['status'], 'integrity_error')
        self.assertFalse(self.store.read_json('run.json')['original_identity_proved'])


if __name__ == '__main__': unittest.main()
