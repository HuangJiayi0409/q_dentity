import dataclasses
import importlib.util
import tempfile
import unittest
from pathlib import Path

from agent_v2.models import (Budget, Candidate, ContractError, Cost, ExecutionResult, FailureSignature,
                             JointAction, Obligation, ProofLink, VerifiedCertificate,
                             initial_state)
from agent_v2.storage import RunStore, freeze_source


class RecordingChecker:
    """Test-only kernel boundary. It never appears in CLI construction."""
    def __init__(self, accepted=True):
        self.accepted = accepted
        self.seen = []

    def check_partial(self, candidate, context):
        self.seen.append((candidate, context))
        return {'accepted': self.accepted, 'status': 'partial_lean_verified' if self.accepted else 'incomplete',
                'evidence': {'test_only': True, 'proposition': candidate['proposition'],
                             'source_sha256': candidate['source_sha256']},
                'sigma': {'code': 'checked' if self.accepted else 'lean_rejected'}}


def result(candidates=(), obligations=(), status='incomplete'):
    return ExecutionResult(status, tuple(candidates), tuple(obligations),
        FailureSignature('construction', 'candidate_generated', 'test-only candidate', None),
        Cost(0.01, 1), {}, (), (), False)


class ExecutorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name); src = root / 'source.lean'
        src.write_text('theorem demo : True := by sorry\n')
        self.store = RunStore.create(root / 'runs', 'test-run')
        self.source = freeze_source(src, 'synthetic', 'demo', self.store, proposition='True')
        self.state, self.rep = initial_state(self.source, Budget(100, 5))
        self.action = JointAction('a', 'identity', 'original', 'original', 'CAS', 'method', {})
        self.context = {'source_sha256': self.source.sha256, 'run_dir': str(self.store.root),
                        'attempt_dir': str(self.store.root / 'rounds/1'), 'seconds': 5.0}

    def tearDown(self): self.tmp.cleanup()

    def candidate(self, name='c', proposition='True', closes=None, replaces=()):
        return Candidate(name, proposition, 'by trivial', 'AgentV2Candidate.proof',
                         self.source.sha256, (), closes, tuple(replaces))

    def test_state_update_rejects_noncurrent_identity_before_checking_candidates(self):
        from agent_v2.executor import verify_and_update
        checker = RecordingChecker()
        rogue = dataclasses.replace(self.action, source='child', target='child')
        with self.assertRaises(ContractError):
            verify_and_update(self.state, rogue, result([self.candidate()]), checker, self.context)
        self.assertEqual(checker.seen, [])
        self.assertEqual(self.state.r, 'original')

    def test_state_update_rejects_identity_that_changes_target(self):
        from agent_v2.executor import verify_and_update
        rogue = dataclasses.replace(self.action, target='child')
        with self.assertRaises(ContractError):
            verify_and_update(self.state, rogue, result(), RecordingChecker(), self.context)

    def test_state_update_rejects_noncurrent_nonidentity_source(self):
        from agent_v2.executor import verify_and_update
        rogue = dataclasses.replace(self.action, T='child-to-grandchild', source='child', target='grandchild')
        with self.assertRaises(ContractError):
            verify_and_update(self.state, rogue, result(), RecordingChecker(), self.context)

    def test_executor_rejects_stale_origin_even_if_a_route_list_includes_it(self):
        from agent_v2.executor import Executor
        rogue = dataclasses.replace(self.action, source='child', target='child')
        class StaleRoutes:
            def legal_candidates(self, *args, **kwargs): return [rogue], []
        class Adapter:
            calls = 0
            def execute(inner, *args):
                inner.calls += 1
                return result().to_dict()
        adapter = Adapter()
        with self.assertRaises(ContractError):
            Executor({'method': adapter}).execute(self.state, rogue, StaleRoutes(), self.store.root / 'attempt')
        self.assertEqual(adapter.calls, 0)

    def test_checked_current_edge_can_execute_and_update_representation(self):
        from agent_v2.executor import Executor, verify_and_update
        from agent_v2.graph import Edge, Graph, Outlet
        bridge = VerifiedCertificate('bridge', '(True) → (True)', 'fun h => h',
            self.source.sha256, (), {'test_only': True, 'source_sha256': self.source.sha256,
                                    'proposition': '(True) → (True)'})
        state = dataclasses.replace(self.state, C=(bridge,))
        graph = Graph(self.source.sha256)
        original = dataclasses.replace(self.rep, semantic_domain='Prop')
        graph.add_node(original)
        graph.add_node(dataclasses.replace(original, id='child', payload={'proposition': 'True'}))
        graph.add_edge(Edge('forward', 'original', 'child', 'bridge', bridge_certificate='bridge'))
        graph.add_outlet(Outlet('child-method', 'child', 'CAS', 'method', {}, ('closed_prop',)))
        legal, _ = graph.legal_candidates(state)
        self.assertEqual([(a.T, a.source, a.target) for a in legal], [('forward', 'original', 'child')])
        class Adapter:
            def execute(self, *args): return result().to_dict()
        outcome = Executor({'method': Adapter()}).execute(state, legal[0], graph, self.store.root / 'attempt')
        updated, _ = verify_and_update(state, legal[0], outcome, RecordingChecker(), self.context)
        self.assertEqual(updated.r, 'child')
        self.assertEqual(updated.O, state.O)
        self.assertEqual(updated.C, state.C)

    def test_unverified_candidate_cannot_close_obligation(self):
        from agent_v2.executor import verify_and_update
        new, diagnostics = verify_and_update(self.state, self.action,
            result([self.candidate(closes='original')]), RecordingChecker(False), self.context)
        self.assertEqual(new.C, ())
        self.assertEqual(new.O, self.state.O)
        self.assertIn('lean_rejected', str(diagnostics))

    def test_verified_unrelated_progress_and_original_remain_separate(self):
        from agent_v2.executor import verify_and_update, validate_invariant
        new, _ = verify_and_update(self.state, self.action, result([self.candidate()]),
                                  RecordingChecker(), self.context)
        self.assertEqual([c.id for c in new.C], ['c'])
        self.assertEqual(new.O, self.state.O)
        validate_invariant(new)

    def test_bridge_then_leaf_reconstructs_exact_original(self):
        from agent_v2.executor import verify_and_update, validate_invariant, assemble_term
        child = Obligation('leaf', 'subgoal', 'True', 'True', self.source.sha256, 'a')
        bridge = self.candidate('bridge', '(True) → (True)', 'original', [child])
        first, _ = verify_and_update(self.state, self.action, result([bridge], [child]),
                                    RecordingChecker(), self.context)
        self.assertEqual([o.id for o in first.O], ['leaf'])
        self.assertEqual(len(first.C), 1)
        second, _ = verify_and_update(first, self.action,
            result([self.candidate('leaf_proof', 'True', 'leaf')]), RecordingChecker(), self.context)
        self.assertEqual(second.O, ())
        self.assertEqual(second.status, 'running')
        validate_invariant(second)
        self.assertIn('by trivial', assemble_term(second))

    def test_unjustified_new_obligation_rolls_back_but_keeps_independent_proof(self):
        from agent_v2.executor import verify_and_update
        forged = Obligation('new', 'subgoal', 'False', 'False', self.source.sha256)
        new, diagnostics = verify_and_update(self.state, self.action,
            result([self.candidate()], [forged]), RecordingChecker(), self.context)
        self.assertEqual(new.O, self.state.O)
        self.assertEqual([c.id for c in new.C], ['c'])
        self.assertIn('invariant_update_rejected', str(diagnostics))

    def test_wrong_bridge_cannot_close_or_replace(self):
        from agent_v2.executor import verify_and_update
        child = Obligation('child', 'subgoal', 'False', 'False', self.source.sha256)
        new, _ = verify_and_update(self.state, self.action,
            result([self.candidate('bad', 'True', 'original', [child])], [child]),
            RecordingChecker(), self.context)
        self.assertEqual(new.O, self.state.O)
        self.assertEqual(new.links, ())

    def test_invariant_rejects_forged_empty_open_set(self):
        from agent_v2.executor import validate_invariant
        with self.assertRaises(ValueError): validate_invariant(dataclasses.replace(self.state, O=()))

    def test_cas_constructed_is_not_a_proof(self):
        from agent_v2.executor import verify_and_update
        new, _ = verify_and_update(self.state, self.action, result(status='symbolic_constructed'),
                                  RecordingChecker(), self.context)
        self.assertEqual(new.O, self.state.O)
        self.assertEqual(new.C, ())
        self.assertNotEqual(new.status, 'original_theorem_proved')

    def test_structured_core_diagnostics_are_not_formal_obligations(self):
        from agent_v2.executor import normalize_result
        data = result(status='symbolic_constructed').to_dict()
        data['diagnostics'] = [{'code': 'translation_pending', 'formal_obligations_exported': False}]
        normalized = normalize_result(data)
        self.assertEqual(normalized.O_res, ())
        self.assertEqual(normalized.C_partial, ())
        self.assertEqual(normalized.diagnostics[0]['code'], 'translation_pending')

    def test_later_checker_crash_preserves_earlier_independent_certificate(self):
        from agent_v2.executor import verify_and_update
        class LaterCrash(RecordingChecker):
            def check_partial(self, candidate, context):
                if self.seen: raise RuntimeError('second check process failed')
                return super().check_partial(candidate, context)
        new, diagnostics = verify_and_update(self.state, self.action,
            result([self.candidate('one'), self.candidate('two')]), LaterCrash(), self.context)
        self.assertEqual([c.id for c in new.C], ['one'])
        self.assertEqual(new.O, self.state.O)
        self.assertIn('partial_checker_exception', str(diagnostics))


if __name__ == '__main__': unittest.main()
