"""Closure checks reject unbound certificates and forged complete proof trees."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from agent_v2.formal_frontend import analyze_source
from agent_v2.lean_checker import LeanChecker
from agent_v2.models import Budget, initial_state
from agent_v2.storage import RunStore, load_train


class ClosureCheckerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='qv2-closure-checker-')
        self.addCleanup(self.temp.cleanup)
        self.store = RunStore.create(Path(self.temp.name), 'run')
        raw = load_train('FQI-SRC-AP-3.3.9', self.store)
        self.front = analyze_source(raw.to_dict(), self.store.root)
        self.source = replace(raw, proposition=self.front['original_proposition'])
        self.front = analyze_source(self.source.to_dict(), self.store.root)
        self.checker = LeanChecker()
        self.context = {'source': self.source.to_dict(), 'source_sha256': self.source.sha256,
                        'run_dir': str(self.store.root), 'attempt_dir': str(self.store.path('check')),
                        'seconds': 300.0}

    def test_mathematical_final_requires_complete_bound_state(self):
        report = {'proof_term': 'by exact True.intro', 'run_dir': str(self.store.root),
                  'theorem': self.source.theorem, 'proposition': self.source.proposition,
                  'seconds': 300.0, 'accepted': True, 'status': 'original_theorem_proved'}
        checked = self.checker.accept_original(report, self.source.to_dict(), self.store.path('final'))
        self.assertEqual(checked['status'], 'integrity_error', checked)
        self.assertFalse(checked['accepted'])
        self.assertFalse(self.store.path('final').exists())

    def test_mathematical_final_rejects_fake_empty_obligation_set(self):
        state, _ = initial_state(self.source, Budget(300, 4))
        state = replace(state, O=())
        report = {'state': state.to_dict(), 'proof_term': 'by exact True.intro',
                  'run_dir': str(self.store.root), 'seconds': 300.0}
        checked = self.checker.accept_original(report, self.source.to_dict(), self.store.path('final'))
        self.assertEqual(checked['status'], 'integrity_error', checked)
        self.assertFalse(checked['accepted'])

    def test_original_renderer_preserves_declaration_and_ignores_comment_sorry(self):
        from agent_v2.math_lean_profile import _original_declaration
        original = self.source.declaration.replace('theorem statement',
                         '/- nested /- sorry := by -/ comment -/ theorem statement')
        source = replace(self.source, declaration=original)
        rendered = _original_declaration(source, self.front)
        self.assertIn('/- nested /- sorry := by -/ comment -/', rendered)
        expected = original.replace('import Benchmark.Batch3Proofs\n', '').replace('  sorry',
            '  exact _root_.AgentV2Assembled q m n h_domain')
        self.assertEqual(rendered, expected)
        self.assertNotIn('import Benchmark', rendered)

    def test_bridge_missing_local_dependency_is_rejected_before_lean(self):
        from agent_v2.telescoping_closure import closure_blueprint
        blueprint = closure_blueprint(self.front)
        request = {'id': blueprint['bridge_id'], 'proposition': blueprint['bridge_proposition'],
                   'proof_term': 'by rfl', 'theorem': 'AgentV2Candidate.proof',
                   'source_sha256': self.source.sha256, 'dependencies': [blueprint['local_id']]}
        checked = self.checker.check_partial(request, self.context)
        self.assertEqual(checked['status'], 'integrity_error', checked)
        self.assertIn('missing', checked['sigma']['message'])
        self.assertFalse(Path(self.context['attempt_dir']).exists())

    def test_endpoint_has_independent_contract_and_cannot_claim_dependencies(self):
        from agent_v2.executor import _candidate_request
        from agent_v2.telescoping_closure import make_closure_candidate
        endpoint = make_closure_candidate(self.front, 'zero_endpoint', {}, 'test-action')
        request = _candidate_request(endpoint)
        checked = self.checker.check_partial(request, dict(self.context, seconds=0))
        self.assertEqual(checked['status'], 'budget_exhausted', checked)
        checked = self.checker.check_partial(dict(request, dependencies=['invented']), self.context)
        self.assertEqual(checked['status'], 'integrity_error', checked)
        self.assertFalse(Path(self.context['attempt_dir']).exists())

    def test_real_bridge_endpoints_and_exact_original_reject_tampering(self):
        from agent_v2.executor import _candidate_request, assemble_term, validate_invariant, verify_and_update
        from agent_v2.models import Candidate, Cost, ExecutionResult, FailureSignature, JointAction, thaw
        from agent_v2.telescoping_closure import closure_blueprint, make_closure_candidate
        from agent_v2.telescoping_translation import local_proof
        if self.checker.binary is None or not self.checker.binary.is_file():
            self.skipTest('integration: lean_environment_unavailable')
        blueprint = closure_blueprint(self.front)
        local = Candidate(blueprint['local_id'], self.front['local_proposition'], local_proof(self.front),
                          'AgentV2Candidate.proof', self.source.sha256)
        state, _ = initial_state(self.source, Budget(900, 6))
        action = JointAction('checker-test', 'identity', 'original', 'original', 'CAS', 'telescoping', {})

        def execute(state, candidate, attempt):
            result = ExecutionResult('symbolic_constructed', (candidate,), candidate.replaces,
                FailureSignature('construction', 'checker_integration', 'Controlled checker test.', None),
                Cost(0.0, 1), {}, (), (), False)
            context = dict(self.context, attempt_dir=str(self.store.path(attempt)))
            return verify_and_update(state, action, result, self.checker, context)

        state, diagnostics = execute(state, local, 'local')
        self.assertEqual(len(state.C), 1, diagnostics)
        approved = {cert.id: cert.to_dict() for cert in state.C}
        bridge = make_closure_candidate(self.front, 'bridge', approved, action.id)
        request = _candidate_request(bridge)
        for context, altered in [
            (self.context, request),
            (dict(self.context, approved_certificates=approved), dict(request, dependencies=[])),
        ]:
            checked = self.checker.check_partial(altered, context)
            self.assertEqual(checked['status'], 'integrity_error', checked)
        changed = thaw(approved)
        changed[local.id]['evidence']['proof_term'] = 'by sorry'
        checked = self.checker.check_partial(request, dict(self.context, approved_certificates=changed))
        self.assertEqual(checked['status'], 'integrity_error', checked)
        changed = thaw(approved)
        changed[local.id]['evidence']['artifacts'][0]['sha256'] = '0' * 64
        checked = self.checker.check_partial(request, dict(self.context, approved_certificates=changed))
        self.assertEqual(checked['status'], 'integrity_error', checked)

        rejected, diagnostics = execute(state, replace(bridge, proof_term='by rfl'), 'wrong-bridge')
        self.assertEqual(rejected.O, state.O)
        self.assertEqual(rejected.links, ())
        self.assertIn('lean_check_failed', str(diagnostics))
        state, diagnostics = execute(state, bridge, 'bridge')
        self.assertEqual(len(state.O), 2, diagnostics)
        self.assertEqual(len(state.links), 1)
        validate_invariant(state)
        for task in ('zero_endpoint', 'upper_endpoint'):
            approved = {cert.id: cert.to_dict() for cert in state.C}
            endpoint = make_closure_candidate(self.front, task, approved, action.id)
            state, diagnostics = execute(state, endpoint, task)
            self.assertIn(endpoint.id, [cert.id for cert in state.C], diagnostics)
        self.assertEqual(state.O, ())
        validate_invariant(state)
        report = {'state': state.to_dict(), 'proof_term': assemble_term(state),
                  'theorem': self.source.theorem, 'proposition': self.source.proposition,
                  'run_dir': str(self.store.root), 'seconds': 300.0}
        for tampered in [dict(report, proof_term='by exact True.intro'),
                         dict(report, theorem='Other.statement'), dict(report, proposition='True')]:
            checked = self.checker.accept_original(tampered, self.source.to_dict(), self.store.path('bad-final'))
            self.assertEqual(checked['status'], 'integrity_error', checked)
        broken = state.to_dict()
        broken['C'][1]['dependencies'] = []
        checked = self.checker.accept_original(dict(report, state=broken), self.source.to_dict(), self.store.path('bad-final'))
        self.assertEqual(checked['status'], 'integrity_error', checked)
        checked = self.checker.accept_original(report, self.source.to_dict(), self.store.path('final'))
        self.assertTrue(checked['accepted'], checked)
        self.assertEqual(checked['status'], 'original_theorem_proved')
        audit = checked['evidence']['audit']
        self.assertEqual(audit['theorem'], self.source.theorem)
        self.assertEqual(audit['universe_parameter_count'], 1)
        self.assertTrue(all('Statements' not in name for name in audit['modules']))
        code = next(Path(a['path']).read_text() for a in checked['evidence']['artifacts']
                    if a['path'].endswith('/sources/Candidate.lean'))
        self.assertIn(self.source.declaration.split('namespace ', 1)[1].split(':= by', 1)[0], code)
        self.assertNotIn('sorry', code)


if __name__ == '__main__':
    unittest.main()
