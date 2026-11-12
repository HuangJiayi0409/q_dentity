"""Public profile boundaries; fixtures never constitute mathematical evidence."""
from dataclasses import replace
import hashlib
import importlib.util
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from agent_v2.executor import _candidate_request
from agent_v2.formal_frontend import analyze_source
from agent_v2.lean_checker import LeanChecker
from agent_v2.models import Budget, Candidate, Source, initial_state
from agent_v2.storage import IntegrityError, RunStore, load_train
from agent_v2.telescoping_translation import local_proof


class ProofProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='qv2-profiles-')
        self.addCleanup(self.temp.cleanup)
        self.store = RunStore.create(Path(self.temp.name), 'run')
        raw = load_train('FQI-SRC-AP-3.3.9', self.store)
        self.front = analyze_source(raw.to_dict(), self.store.root)
        self.source = replace(raw, proposition=self.front['original_proposition'])
        self.front = analyze_source(self.source.to_dict(), self.store.root)
        self.candidate = Candidate('telescoping-local-' + self.source.sha256[:20],
            self.front['local_proposition'], local_proof(self.front),
            'AgentV2Candidate.proof', self.source.sha256)
        self.context = {'source': self.source.to_dict(), 'source_sha256': self.source.sha256,
            'run_dir': str(self.store.root), 'attempt_dir': str(self.store.path('check')), 'seconds': 0}
        self.checker = LeanChecker()

    def profiles(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.proof_profiles'),
                             'The common source/profile boundary is not implemented.')
        from agent_v2 import proof_profiles
        return proof_profiles

    def test_arbitrary_local_certificate_id_is_rejected_before_budget_check(self):
        result = self.checker.check_partial(_candidate_request(replace(self.candidate, id='foreign-local')),
                                             self.context)
        self.assertEqual(result['status'], 'integrity_error', result)

    def test_legacy_local_alias_is_bounded_and_not_a_bridge_dependency(self):
        profiles = self.profiles()
        bound = profiles.resolve_source_profile(self.source, self.store.root)
        alias = replace(self.candidate, id='telescoping_local')
        rebuilt = profiles.reconstruct_bound_candidate(bound, _candidate_request(alias), {})
        self.assertEqual(rebuilt.id, 'telescoping_local')
        from agent_v2.telescoping_closure import closure_blueprint
        plan = closure_blueprint(self.front)
        request = {'id': plan['bridge_id'], 'proposition': plan['bridge_proposition'],
            'proof_term': 'by rfl', 'theorem': 'AgentV2Candidate.proof',
            'source_sha256': self.source.sha256, 'dependencies': ['telescoping_local']}
        with self.assertRaises(IntegrityError):
            profiles.reconstruct_bound_candidate(bound, request, {})

    def test_multiple_source_profiles_are_rejected_even_with_zero_budget(self):
        # Fault injection represents a second registered frontend claiming the
        # same frozen syntax; no compiler or successful audit is fabricated.
        duplicate = dict(self.front, profile='gaussian_geometric_recurrence_v1')
        with patch('agent_v2.recurrence_frontend.analyze_source', return_value=duplicate):
            result = self.checker.check_partial(_candidate_request(self.candidate), self.context)
        self.assertEqual(result['status'], 'integrity_error', result)
        self.assertIn('ambiguous', result['sigma']['message'].lower())

    def test_frontend_cannot_change_its_registered_profile(self):
        with patch('agent_v2.formal_frontend.analyze_source',
                   return_value=dict(self.front, profile='unregistered')):
            result = self.checker.check_partial(_candidate_request(self.candidate), self.context)
        self.assertEqual(result['status'], 'integrity_error', result)

    def test_unknown_frozen_source_does_not_fall_through_to_init_checker(self):
        text = 'import Mathlib\ntheorem unsupported : True := by sorry\n'
        path = self.store.path('unsupported.lean'); path.write_text(text)
        digest = hashlib.sha256(text.encode()).hexdigest()
        source = Source('synthetic-unsupported', str(path), str(path), digest,
                        'unsupported', text, text, 'True')
        candidate = Candidate('unknown', 'True', 'by exact True.intro', 'AgentV2Candidate.proof', digest)
        context = dict(self.context, source=source.to_dict(), source_sha256=digest)
        result = self.checker.check_partial(_candidate_request(candidate), context)
        self.assertFalse(result['accepted'])
        self.assertEqual(result['sigma']['code'], 'unsupported_source_profile', result)

    def test_exact_init_original_retains_its_existing_empty_context_forms(self):
        from agent_v2.lean_checker import init_original_template
        text = init_original_template('Synthetic.statement', 'True')
        path = self.store.path('init-original.lean'); path.write_text(text)
        digest = hashlib.sha256(text.encode()).hexdigest()
        source = Source('synthetic-init', str(path), str(path), digest,
                        'Synthetic.statement', text, text, 'True').to_dict()
        report = {'proof_term': 'by exact True.intro', 'run_dir': str(self.store.root), 'seconds': 0}
        for gamma in ('', {}, []):
            with self.subTest(gamma=gamma):
                result = self.checker.accept_original(report, dict(source, Gamma=gamma), self.store.path('init-final'))
                self.assertEqual(result['status'], 'budget_exhausted', result)

    def test_resolved_profiles_have_separate_fixed_rule_sets(self):
        profiles = self.profiles()
        bound = profiles.resolve_source_profile(self.source, self.store.root)
        self.assertEqual(bound.profile.id, 'gaussian_weighted_range_v1')
        raw = load_train('FQI-GAUSS-ALTERNATING', self.store)
        recurrence = profiles.resolve_source_profile(raw, self.store.root)
        self.assertEqual(recurrence.profile.id, 'gaussian_geometric_recurrence_v1')
        self.assertNotIn('finite_product_framework/p1/lean/Shared.lean', bound.profile.rules)
        self.assertIn('finite_product_framework/p1/lean/Shared.lean', recurrence.profile.rules)

    def test_recurrence_original_uses_its_own_parser_before_tree_validation(self):
        from agent_v2.recurrence_frontend import analyze_source as recurrence_frontend
        raw = load_train('FQI-GAUSS-ALTERNATING', self.store)
        front = recurrence_frontend(raw.to_dict(), self.store.root)
        source = replace(raw, proposition=front['original_proposition'])
        state, _ = initial_state(source, Budget(60, 5))
        report = {'state': replace(state, O=()).to_dict(), 'proof_term': 'by rfl',
                  'run_dir': str(self.store.root), 'seconds': 0}
        result = self.checker.accept_original(report, source.to_dict(), self.store.path('final'))
        self.assertEqual(result['status'], 'integrity_error', result)
        self.assertIn('open obligations', result['sigma']['message'])

    def test_malformed_recurrence_proof_returns_a_classified_rejection(self):
        raw = load_train('FQI-GAUSS-ALTERNATING', self.store)
        context = dict(self.context, source=raw.to_dict(), source_sha256=raw.sha256)
        request = {'id': 'unknown', 'proposition': 'True', 'proof_term': None,
                   'theorem': 'AgentV2Candidate.proof', 'source_sha256': raw.sha256, 'dependencies': []}
        try:
            result = self.checker.check_partial(request, context)
        except Exception as error:
            self.fail('Malformed proof escaped the checker boundary: ' + repr(error))
        self.assertFalse(result['accepted'])
        self.assertIn(result['status'], ('integrity_error', 'incomplete'))

    def test_bound_candidate_does_not_replace_negative_proof_sent_to_lean(self):
        profiles = self.profiles()
        bound = profiles.resolve_source_profile(self.source, self.store.root)
        negative = _candidate_request(replace(self.candidate, proof_term='by rfl'))
        rebuilt = profiles.reconstruct_bound_candidate(bound, negative, {}, allow_negative=True)
        self.assertEqual(rebuilt.proof_term, self.candidate.proof_term)
        self.assertEqual(negative['proof_term'], 'by rfl')
        with self.assertRaises(ValueError):
            profiles.reconstruct_bound_candidate(bound, negative, {}, allow_negative=False)

    def test_dependency_receipt_wrong_profile_is_not_reclassified_as_math_success(self):
        # A deliberately incomplete receipt must fail before artifact reads.
        profiles = self.profiles()
        from agent_v2.models import VerifiedCertificate
        bound = profiles.resolve_source_profile(self.source, self.store.root)
        request = _candidate_request(self.candidate)
        evidence = {**request, 'certificate_id': request['id'], 'profile': 'gaussian_geometric_recurrence_v1',
                    'profile_version': '1', 'returncode': 0,
                    'audit': {'theorem': 'AgentV2Candidate.proof', 'universe_parameters': ['u'], 'axioms': []}}
        cert = VerifiedCertificate(self.candidate.id, self.candidate.proposition, self.candidate.proof_term,
                                   self.source.sha256, (), evidence)
        with self.assertRaisesRegex(IntegrityError, 'profile'):
            profiles.check_certificate_binding(cert, bound, self.store.root, {})

    def test_final_rejects_predecessor_environment_drift_before_compilation(self):
        from agent_v2 import math_lean_profile
        import time
        profiles = self.profiles()
        bound = profiles.resolve_source_profile(self.source, self.store.root)
        request = {'id': 'original', 'proposition': self.source.proposition,
            'proof_term': 'by rfl', 'theorem': self.source.theorem,
            'source_sha256': self.source.sha256, 'dependencies': []}
        context = dict(self.context, seconds=300,
                       approved_certificates={'previous': {'evidence': {'external_environment_sha256': '0' * 64}}})
        with patch.object(math_lean_profile, '_inventory', return_value={'modules': [], 'files': []}), \
             patch.object(math_lean_profile, '_compile', return_value={'timed_out': True,
                          'returncode': -9, 'environment_error': None}):
            result = math_lean_profile._verify_train(self.checker, request, context, time.monotonic(),
                self.source, self.front, self.source.proposition, original=True, bound=bound)
        self.assertEqual(result['status'], 'integrity_error', result)
        self.assertEqual(result['sigma']['code'], 'external_environment_changed', result)

    def test_optional_wire_schema_does_not_change_retained_candidate_semantics(self):
        from agent_v2 import math_lean_profile
        request = dict(_candidate_request(self.candidate), schema_version=1)
        with patch.object(math_lean_profile, '_inventory', return_value={'modules': [], 'files': []}), \
             patch.object(math_lean_profile, '_compile', return_value={'timed_out': True,
                          'returncode': -9, 'environment_error': None}):
            result = self.checker.check_partial(request, dict(self.context, seconds=300))
        self.assertEqual(result['status'], 'budget_exhausted')
        retained = [a for a in result['evidence']['artifacts'] if a['path'].endswith('/request.json')]
        self.assertEqual(len(retained), 1)
        self.assertEqual(json.loads(Path(retained[0]['path']).read_text()), _candidate_request(self.candidate))

    def test_partial_and_original_freeze_same_complete_audit_drivers(self):
        from agent_v2 import math_lean_profile
        import time
        profiles = self.profiles()
        bound = profiles.resolve_source_profile(self.source, self.store.root)
        inventories = []

        def fixed_inventory(checker, imports, packages, fixed_paths, deadline, build, **kwargs):
            # Exercise the production fixed-path selection with real bytes;
            # only expensive transitive import scanning is replaced here.
            inventory = {'modules': [], 'files': [
                {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                for path in sorted(set(fixed_paths))]}
            inventories.append(inventory)
            return inventory

        with patch.object(math_lean_profile, '_inventory', side_effect=fixed_inventory), \
             patch.object(math_lean_profile, '_compile', return_value={'timed_out': True,
                          'returncode': -9, 'environment_error': None}):
            local = self.checker.check_partial(_candidate_request(self.candidate), dict(self.context, seconds=300))
            request = {'id': 'original', 'proposition': self.source.proposition,
                'proof_term': 'by rfl', 'theorem': self.source.theorem,
                'source_sha256': self.source.sha256, 'dependencies': []}
            context = dict(self.context, seconds=300, attempt_dir=str(self.store.path('driver-final')),
                           approved_certificates={'local': {'evidence': local['evidence']}})
            final = math_lean_profile._verify_train(self.checker, request, context, time.monotonic(),
                self.source, self.front, self.source.proposition, original=True, bound=bound)
        self.assertEqual(local['status'], 'budget_exhausted', local)
        self.assertEqual(final['status'], 'budget_exhausted', final)
        for inventory in inventories:
            driver_names = {Path(item['path']).name for item in inventory['files']
                            if Path(item['path']).name in {'TelescopingCheck.lean', 'OriginalTrainCheck.lean'}}
            self.assertEqual(driver_names, {'TelescopingCheck.lean', 'OriginalTrainCheck.lean'})
        self.assertEqual(local['evidence']['external_environment_sha256'],
                         final['evidence']['external_environment_sha256'])


class ProofProfileReceiptIntegrationTests(unittest.TestCase):
    """Fresh Lean artifact binding, independently of source-parser unit tests."""
    integration = True
    setUp = ProofProfileTests.setUp

    def test_changed_receipt_audit_is_rejected_even_when_artifact_hashes_match(self):
        from agent_v2.models import VerifiedCertificate
        from agent_v2.proof_profiles import check_certificate_binding, resolve_source_profile
        if self.checker.binary is None or not self.checker.binary.is_file():
            self.skipTest('integration: fixed Lean toolchain unavailable')
        result = self.checker.check_partial(_candidate_request(self.candidate), dict(self.context, seconds=300))
        self.assertTrue(result['accepted'], result)
        certificate = VerifiedCertificate(self.candidate.id, self.candidate.proposition,
            self.candidate.proof_term, self.source.sha256, (), result['evidence'])
        bound = resolve_source_profile(self.source, self.store.root)
        check_certificate_binding(certificate, bound, self.store.root, {})
        changed = copy.deepcopy(result['evidence'])
        changed['audit']['agent_v2_audit_v1'] = 'not-the-compiled-audit'
        with self.assertRaisesRegex(IntegrityError, 'audit'):
            check_certificate_binding(replace(certificate, evidence=changed), bound, self.store.root, {})
        for key, value in [('profile', 'gaussian_geometric_recurrence_v1'), ('profile_version', '999')]:
            changed = copy.deepcopy(result['evidence']); changed[key] = value
            with self.assertRaisesRegex(IntegrityError, 'profile'):
                check_certificate_binding(replace(certificate, evidence=changed), bound, self.store.root, {})


if __name__ == '__main__':
    unittest.main()
