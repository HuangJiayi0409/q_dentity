"""Controller contracts; fake kernels here are never mathematical evidence."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from agent_v2.executor import Executor
from agent_v2.graph import Graph, Outlet
from agent_v2.loop import resume, run
from agent_v2.models import Budget, Candidate, JointAction, Obligation, initial_state
from agent_v2.storage import RunStore, freeze_source
from agent_v2.tests.test_executor import RecordingChecker, result
from agent_v2.tests.test_loop import FinalChecker, QueueAdapter


class ClosureFlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        source = root / 'Source.lean'
        source.write_text('theorem demo : True := by sorry\n')
        self.store = RunStore.create(root / 'runs')
        self.source = freeze_source(source, 'synthetic-flow-only', 'demo', self.store,
                                    proposition='True')
        self.state, node = initial_state(self.source, Budget(100, 5))
        self.graph = Graph(self.source.sha256)
        self.graph.add_node(node)
        self.graph.add_outlet(Outlet('local', node.id, 'CAS', 'method',
            {'method': 'telescoping', 'produces_certificate': 'local'}, ('closed_prop',)))

    def candidate(self, name, dependencies=(), closes=None):
        return Candidate(name, 'True', 'by trivial', 'AgentV2Candidate.proof',
                         self.source.sha256, dependencies, closes)

    def test_completed_certificate_outlet_is_not_reexecuted_after_state_changes(self):
        adapter = QueueAdapter([result([self.candidate('local')])])
        final = run(self.state, self.graph, self.store, Executor({'method': adapter}), FinalChecker())
        self.assertEqual(len(adapter.calls), 1)
        legal, filtered = self.graph.legal_candidates(final)
        self.assertEqual(legal, [])
        self.assertIn('task_already_completed', [r['code'] for r in filtered])

    def test_resume_passes_only_fresh_predecessor_receipts(self):
        self.graph.add_outlet(Outlet('child', 'original', 'CAS', 'method',
            {'method': 'telescoping', 'produces_certificate': 'child'}, ('closed_prop',),
            required_certificates=('local',)))
        adapter = QueueAdapter([result([self.candidate('local')]),
                                result([self.candidate('child', ('local',))])])
        run(self.state, self.graph, self.store, Executor({'method': adapter}), FinalChecker())
        class Fresh(RecordingChecker):
            def check_partial(self, candidate, context):
                response = super().check_partial(candidate, context)
                response['evidence']['fresh'] = True
                return response
        checker = Fresh()
        resume(self.store, checker)
        self.assertEqual(checker.seen[0][1]['approved_certificates'], {})
        self.assertEqual(set(checker.seen[1][1]['approved_certificates']), {'local'})
        self.assertTrue(checker.seen[1][1]['approved_certificates']['local']['evidence']['fresh'])

    def test_final_receives_exact_tree_and_each_attempt_preserves_evidence(self):
        checker = FinalChecker()
        final = run(self.state, self.graph, self.store,
            Executor({'method': QueueAdapter([result([self.candidate('local', closes='original')])])}),
            checker)
        self.assertEqual(checker.final_calls[0]['state']['links'], final.to_dict()['links'])
        first = set(self.store.path('final').glob('*/checked.json'))
        state, graph = resume(self.store, RecordingChecker())
        run(state, graph, self.store, Executor({'method': QueueAdapter([])}), checker)
        self.assertEqual(len(set(self.store.path('final').glob('*/checked.json')) - first), 1)

    def test_final_environment_failure_can_retry_from_freshly_verified_tree(self):
        class Blocked(FinalChecker):
            def accept_original(self, report, source, attempt):
                return {'accepted': False, 'status': 'environment_blocked', 'evidence': {},
                        'sigma': {'code': 'lean_environment_unavailable'}}
        failed = run(self.state, self.graph, self.store,
            Executor({'method': QueueAdapter([result([self.candidate('local', closes='original')])])}),
            Blocked())
        self.assertEqual(failed.O, self.state.O)
        self.assertEqual(failed.links, ())
        fresh = RecordingChecker()
        state, graph = resume(self.store, fresh)
        self.assertEqual(len(fresh.seen), 1)
        checker = FinalChecker()
        adapter = QueueAdapter([])
        final = run(state, graph, self.store, Executor({'method': adapter}), checker)
        self.assertEqual(final.status, 'original_theorem_proved')
        self.assertEqual(len(checker.final_calls), 1)
        self.assertEqual(adapter.calls, [])
        self.assertEqual(final.b.actions, failed.b.actions)

    def test_explicit_task_receives_state_action_in_adapter(self):
        self.graph = Graph(self.source.sha256)
        self.graph.add_node(initial_state(self.source, self.state.b)[1])
        self.graph.add_outlet(Outlet('task', 'original', 'CAS', 'method',
            {'method': 'telescoping', 'task': 'bridge'}, ('closed_prop',)))
        action = self.graph.legal_candidates(self.state)[0][0]
        seen = []
        class Adapter:
            def execute_action(inner, state, selected, path, seconds):
                seen.append((state, selected))
                return result().to_dict()
        Executor({'method': Adapter()}).execute(self.state, action, self.graph,
                                               self.store.root / 'attempt')
        self.assertEqual(seen, [(self.state, action)])

    def test_chain_partial_failure_keeps_diagnostic_category_and_original(self):
        class Failure(RecordingChecker):
            def check_partial(self, candidate, context):
                return {'accepted': False, 'status': 'environment_blocked',
                        'sigma': {'code': 'lean_environment_unavailable'}, 'evidence': {}}
        outcome = replace(result([self.candidate('local')], status='symbolic_constructed'),
                          raw_result={'execution_scope': 'certificate_chain'})
        final = run(self.state, self.graph, self.store,
                    Executor({'method': QueueAdapter([outcome])}), Failure())
        self.assertEqual(final.status, 'environment_blocked')
        self.assertEqual(final.O, self.state.O)
        self.assertEqual(self.store.read_json('run.json')['stop_reason'], 'lean_environment_unavailable')

    def test_chain_backend_failures_keep_their_categories(self):
        for status in ('integrity_error', 'budget_exhausted', 'environment_blocked'):
            with self.subTest(status=status):
                store = RunStore.create(Path(self.tmp.name) / 'runs')
                source = freeze_source(self.source.path, self.source.identity, self.source.theorem,
                                       store, proposition='True')
                state, _ = initial_state(source, self.state.b)
                outcome = replace(result(status=status), raw_result={'execution_scope': 'certificate_chain'})
                final = run(state, self.graph, store,
                    Executor({'method': QueueAdapter([outcome])}), FinalChecker())
                self.assertEqual(final.status, status)

    def test_task_connection_cannot_forge_child_origin(self):
        from agent_v2.executor import verify_and_update
        action = JointAction('actual', 'identity', 'original', 'original', 'CAS', 'method',
                             {'task': 'bridge', 'scope': 'full'})
        child = Obligation('endpoint', 'boundary', 'True', 'True', self.source.sha256, 'forged')
        bridge = Candidate('bridge', '(True) → (True)', 'fun h => h', 'AgentV2Candidate.proof',
                           self.source.sha256, (), 'original', (child,))
        after, diagnostics = verify_and_update(self.state, action, result([bridge], [child]),
            RecordingChecker(), {'run_dir': str(self.store.root), 'seconds': 10,
                                 'attempt_dir': str(self.store.path('attempt'))})
        self.assertEqual(after.O, self.state.O)
        self.assertEqual(after.links, ())
        self.assertEqual(len(after.C), 1)  # independent proof survives metadata rollback
        self.assertIn('invariant_update_rejected', str(diagnostics))


if __name__ == '__main__':
    unittest.main()
