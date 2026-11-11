"""Controller unit tests with explicitly fake kernels; real mathematics is integration-tested separately."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from agent_v2.executor import Executor, verify_and_update
from agent_v2.graph import Graph, Outlet
from agent_v2.loop import resume, run
from agent_v2.models import Budget, Candidate, JointAction, initial_state
from agent_v2.storage import RunStore, freeze_source
from agent_v2.tests.test_executor import RecordingChecker, result
from agent_v2.tests.test_loop import QueueAdapter


class LocalScopeFlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='agent-v2-local-flow-')
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        original = root / 'source.lean'
        original.write_text('theorem demo : True := by sorry\n')
        self.store = RunStore.create(root / 'runs')
        self.source = freeze_source(original, 'synthetic-controller-unit-only', 'demo', self.store,
                                    proposition='True')
        self.state, node = initial_state(self.source, Budget(100, 1))
        self.graph = Graph(self.source.sha256)
        self.graph.add_node(node)
        self.graph.add_outlet(Outlet('local', node.id, 'CAS', 'method',
            {'method': 'telescoping'}, ('closed_prop',)))
        self.candidate = Candidate('local-difference', 'True', 'by trivial',
                                   'AgentV2Candidate.proof', self.source.sha256)

    def outcome(self):
        return replace(result([self.candidate], status='symbolic_constructed'),
                       raw_result={'execution_scope': 'local_certificate_only'})

    def execute(self, checker):
        return run(self.state, self.graph, self.store,
                   Executor({'method': QueueAdapter([self.outcome()])}), checker)

    def test_verified_local_scope_finishes_incomplete_with_original_open(self):
        checker = RecordingChecker()
        state = self.execute(checker)
        self.assertEqual(state.status, 'incomplete')
        self.assertEqual(len(state.C), 1)
        self.assertEqual(state.O, self.state.O)
        self.assertEqual(state.links, ())
        self.assertEqual(state.b.actions, 0)
        self.assertGreater(state.b.seconds, 0)
        self.assertEqual(self.store.read_json('run.json')['stop_reason'],
                         'local_certificate_verified_original_open')

    def test_full_source_is_passed_to_partial_verifier(self):
        checker = RecordingChecker()
        self.execute(checker)
        self.assertEqual(checker.seen[0][1].get('source'), self.source.to_dict())

    def test_resume_reverifies_full_source_and_does_not_repeat_completed_local_scope(self):
        self.execute(RecordingChecker())
        checker = RecordingChecker()
        state, graph = resume(self.store, checker)
        self.assertEqual(len(checker.seen), 1)
        self.assertEqual(checker.seen[0][1].get('source'), self.source.to_dict())
        empty = QueueAdapter([])
        final = run(state, graph, self.store, Executor({'method': empty}), checker)
        self.assertEqual(empty.calls, [])
        self.assertEqual(final.status, 'incomplete')
        self.assertEqual(final.O, self.state.O)

    def test_rejected_local_candidate_keeps_C_empty_and_O_open(self):
        state = self.execute(RecordingChecker(False))
        self.assertEqual(state.C, ())
        self.assertEqual(state.O, self.state.O)
        self.assertEqual(state.status, 'incomplete')
        self.assertEqual(self.store.read_json('run.json')['stop_reason'], 'local_verification_failed')

    def test_partial_technical_failure_keeps_its_category(self):
        for status, code in [('environment_blocked', 'lean_environment_unavailable'),
                             ('budget_exhausted', 'lean_timeout'),
                             ('integrity_error', 'candidate_source_hash_mismatch')]:
            with self.subTest(status=status):
                store = RunStore.create(Path(self.tmp.name) / 'runs')
                source = freeze_source(self.source.path, self.source.identity, self.source.theorem,
                                       store, proposition='True')
                state, _ = initial_state(source, Budget(100, 1))
                class Failure(RecordingChecker):
                    def check_partial(self, candidate, context):
                        return {'accepted': False, 'status': status, 'sigma': {'code': code},
                                'evidence': {}}
                final = run(state, self.graph, store,
                    Executor({'method': QueueAdapter([self.outcome()])}), Failure())
                self.assertEqual(final.status, status)
                self.assertEqual(store.read_json('run.json')['stop_reason'], code)
                self.assertEqual(final.C, ())
                self.assertEqual(final.O, state.O)

    def test_raw_local_scope_claim_alone_cannot_add_C_or_close_O(self):
        empty = replace(self.outcome(), C_partial=())
        action = JointAction('a', 'identity', 'original', 'original', 'CAS', 'method', {})
        state, _ = verify_and_update(self.state, action, empty, RecordingChecker(),
            {'run_dir': str(self.store.root), 'attempt_dir': str(self.store.root / 'attempt'),
             'seconds': 10.0, 'source_sha256': self.source.sha256})
        self.assertEqual(state.C, ())
        self.assertEqual(state.O, self.state.O)

    def test_resume_failure_preserves_category_and_full_receipt(self):
        import json
        from agent_v2.storage import IntegrityError
        self.execute(RecordingChecker())
        original_checkpoint = self.store.load_checkpoint()
        for status, code in [('environment_blocked', 'lean_environment_unavailable'),
                             ('budget_exhausted', 'lean_timeout'),
                             ('incomplete', 'lean_check_failed')]:
            with self.subTest(status=status):
                self.store.save_checkpoint(original_checkpoint)
                class Failure:
                    def check_partial(self, candidate, context):
                        return {'accepted': False, 'status': status, 'sigma': {'code': code},
                                'evidence': {'replay_diagnostic_marker': code}}
                with self.assertRaises(IntegrityError):
                    resume(self.store, Failure())
                report = self.store.read_json('run.json')
                self.assertEqual(report['status'], status)
                self.assertEqual(report['stop_reason'], code)
                self.assertIn('replay_diagnostic_marker', json.dumps(report['diagnostics']))

    def test_resume_without_recheck_budget_is_not_integrity_failure(self):
        from agent_v2.storage import IntegrityError
        self.execute(RecordingChecker())
        saved = self.store.load_checkpoint()
        saved['state']['b']['seconds'] = 0.0
        self.store.save_checkpoint(saved)
        with self.assertRaises(IntegrityError):
            resume(self.store, RecordingChecker())
        self.assertEqual(self.store.read_json('run.json')['status'], 'budget_exhausted')

    def test_cli_preserves_replay_failure_exit_code_and_run_location(self):
        import contextlib
        import io
        import json
        from unittest.mock import patch
        from agent_v2 import cli
        from agent_v2.loop import ReplayFailure
        for status, exit_code in [('incomplete', 2), ('budget_exhausted', 3),
                                  ('environment_blocked', 3), ('integrity_error', 4)]:
            failure = ReplayFailure(status, 'replay_rejected', 'test-only failure', self.store.root)
            output, error = io.StringIO(), io.StringIO()
            with patch.object(cli, 'resume_run', side_effect=failure), \
                    contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
                returned = cli.main(['resume', '--run-dir', str(self.store.root)])
            self.assertEqual(returned, exit_code)
            summary = json.loads(output.getvalue().splitlines()[-1])
            self.assertEqual(summary['status'], status)
            self.assertEqual(summary['run_dir'], str(self.store.root))


if __name__ == '__main__':
    unittest.main()
