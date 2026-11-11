"""Independent controller fault-injection checks; no mathematical claims."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from agent_v2.executor import Executor
from agent_v2.graph import Graph, Outlet
from agent_v2.loop import ReplayFailure, resume, run
from agent_v2.models import Budget, Candidate, Obligation, initial_state
from agent_v2.storage import RunStore, freeze_source
from agent_v2.tests.test_executor import RecordingChecker, result
from agent_v2.tests.test_loop import FinalChecker, QueueAdapter


class ClosureReviewTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        original = root / 'Source.lean'
        original.write_text('theorem demo : True := by sorry\n')
        self.store = RunStore.create(root / 'runs')
        self.source = freeze_source(original, 'synthetic-independent-review', 'demo',
                                    self.store, proposition='True')
        self.state, node = initial_state(self.source, Budget(100, 4))
        self.graph = Graph(self.source.sha256)
        self.graph.add_node(node)
        self.graph.add_outlet(Outlet('one', 'original', 'CAS', 'method',
            {'method': 'telescoping', 'produces_certificate': 'proved'}, ('closed_prop',)))

    def failed_final(self):
        class Blocked(FinalChecker):
            def accept_original(self, report, source, attempt):
                return {'accepted': False, 'status': 'environment_blocked', 'evidence': {},
                        'sigma': {'code': 'lean_start_failed'}}
        candidate = Candidate('proved', 'True', 'by exact True.intro', 'AgentV2Candidate.proof',
                              self.source.sha256, closes='original')
        return run(self.state, self.graph, self.store,
                   Executor({'method': QueueAdapter([result([candidate])])}), Blocked())

    def test_retry_tree_is_not_used_when_fresh_certificate_check_fails(self):
        failed = self.failed_final()
        with self.assertRaises(ReplayFailure):
            resume(self.store, RecordingChecker(False))
        checkpoint = self.store.load_checkpoint()['state']
        self.assertEqual(checkpoint['O'], failed.to_dict()['O'])
        self.assertEqual(checkpoint['links'], [])
        self.assertEqual(checkpoint['b']['actions'], failed.b.actions)

    def test_retry_rejects_changed_certificate_even_after_fresh_check(self):
        self.failed_final()
        retry = self.store.read_json('final/retry.json')
        retry['state']['C'][0]['proof_term'] = 'by rfl'
        self.store.write_json('final/retry.json', retry)
        fresh = RecordingChecker()
        with self.assertRaises(ReplayFailure) as raised:
            resume(self.store, fresh)
        self.assertEqual(len(fresh.seen), 1)
        self.assertEqual(raised.exception.status, 'integrity_error')
        self.assertEqual(self.store.load_checkpoint()['state']['links'], [])

    def test_retry_rejects_a_link_to_an_unverified_certificate(self):
        self.failed_final()
        retry = self.store.read_json('final/retry.json')
        retry['state']['links'][0]['certificate_id'] = 'unknown'
        self.store.write_json('final/retry.json', retry)
        with self.assertRaises(ReplayFailure) as raised:
            resume(self.store, RecordingChecker())
        self.assertEqual(raised.exception.status, 'integrity_error')
        self.assertEqual(self.store.load_checkpoint()['state']['links'], [])

    def test_retry_rejects_a_changed_original_context(self):
        self.failed_final()
        retry = self.store.read_json('final/retry.json')
        retry['state']['G']['Gamma'] += '\n-- changed context\n'
        self.store.write_json('final/retry.json', retry)
        with self.assertRaises(ReplayFailure) as raised:
            resume(self.store, RecordingChecker())
        self.assertEqual(raised.exception.status, 'integrity_error')
        self.assertEqual(self.store.load_checkpoint()['state']['G'], self.source.to_dict())
        self.assertEqual(self.store.load_checkpoint()['state']['links'], [])

    def test_retry_restoration_does_not_refund_budget_or_repeat_a_method(self):
        failed = self.failed_final()
        state, graph = resume(self.store, RecordingChecker())
        self.assertEqual(state.b.actions, failed.b.actions)
        self.assertLess(state.b.seconds, failed.b.seconds)
        self.assertEqual(state.O, ())
        adapter, checker = QueueAdapter([]), FinalChecker()
        final = run(state, graph, self.store, Executor({'method': adapter}), checker)
        self.assertEqual(final.status, 'original_theorem_proved')
        self.assertEqual(adapter.calls, [])
        self.assertEqual(len(checker.final_calls), 1)
        self.assertEqual(final.b.actions, failed.b.actions)

    def test_ordinary_bridge_proof_rejection_is_not_integrity_corruption(self):
        endpoint = Obligation('endpoint', 'boundary', 'True', 'True', self.source.sha256, 'a')
        bridge = Candidate('bridge', '(True) → (True)', 'by rfl', 'AgentV2Candidate.proof',
                           self.source.sha256, (), 'original', (endpoint,))
        outcome = replace(result([bridge], [endpoint], status='symbolic_constructed'),
                          raw_result={'execution_scope': 'certificate_chain'})
        final = run(self.state, self.graph, self.store,
            Executor({'method': QueueAdapter([outcome])}), RecordingChecker(False))
        self.assertEqual(final.O, self.state.O)
        self.assertEqual(final.links, ())
        self.assertEqual(final.C, ())
        self.assertEqual(final.status, 'incomplete')


if __name__ == '__main__':
    unittest.main()
