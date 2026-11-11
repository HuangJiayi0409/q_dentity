"""Integration checks on one real Train source; never held-out Test input."""
from pathlib import Path
import hashlib
import tempfile
import unittest
from unittest.mock import patch

from agent_v2.lean_checker import LeanChecker
from agent_v2.storage import RunStore, load_train


class TelescopingCheckerIntegrationTests(unittest.TestCase):
    integration = True

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='agent-v2-telescoping-')
        self.addCleanup(self.temporary.cleanup)
        self.store = RunStore.create(Path(self.temporary.name), 'run')
        self.source = load_train('FQI-SRC-AP-3.3.9', self.store)
        self.checker = LeanChecker()
        self.context = {'source_sha256': self.source.sha256,
                        'source': self.source.to_dict(), 'run_dir': str(self.store.root),
                        'attempt_dir': str(self.store.path('check')), 'seconds': 300.0}

    def candidate(self):
        from agent_v2.formal_frontend import analyze_source
        from agent_v2.telescoping_translation import local_proof
        front = analyze_source(self.source.to_dict(), self.store.root)
        proposition, proof = front['local_proposition'], local_proof(front)
        return {'id': 'telescoping_local', 'proposition': proposition, 'proof_term': proof,
                'theorem': 'AgentV2Candidate.proof', 'source_sha256': self.source.sha256,
                'dependencies': []}

    def require_environment(self):
        if self.checker.binary is None or not self.checker.binary.is_file():
            self.skipTest('integration: lean_environment_unavailable')
        root = self.checker.repository / 'project/.lake/packages/mathlib/.lake/build/lib/lean'
        if not root.is_dir():
            self.skipTest('integration: lean_environment_unavailable (Mathlib cache missing)')

    def test_real_train_local_proof_with_original_context_and_universe(self):
        self.require_environment()
        candidate = self.candidate()
        checked = self.checker.check_partial(candidate, self.context)
        self.assertTrue(checked['accepted'], checked)
        self.assertEqual(checked['status'], 'partial_lean_verified')
        evidence = checked['evidence']
        self.assertEqual(evidence['proposition'], candidate['proposition'])
        self.assertEqual(evidence['source_sha256'], self.source.sha256)
        self.assertEqual(evidence['audit']['universe_parameters'], ['u'])
        self.assertTrue(set(evidence['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'})
        self.assertNotIn(self.source.theorem.rpartition('.')[0], evidence['audit']['modules'])
        self.assertTrue(all('Statements' not in module for module in evidence['audit']['modules']))
        self.assertIn('Benchmark.Gaussian', evidence['audit']['modules'])
        self.assertTrue(any(a['path'].endswith('Candidate.olean') for a in evidence['artifacts']))
        for artifact in evidence['artifacts']:
            self.assertEqual(hashlib.sha256(Path(artifact['path']).read_bytes()).hexdigest(), artifact['sha256'])

    def test_real_wrong_proof_reaches_lean_and_is_rejected(self):
        self.require_environment()
        candidate = dict(self.candidate(), proof_term='by rfl')
        checked = self.checker.check_partial(candidate, self.context)
        self.assertFalse(checked['accepted'])
        self.assertEqual(checked['status'], 'incomplete', checked)
        self.assertEqual(checked['sigma']['code'], 'lean_check_failed', checked)
        self.assertNotEqual(checked['evidence']['returncode'], 0)
        self.assertTrue(any(a['path'].endswith('candidate/stdout.jsonl') for a in checked['evidence']['artifacts']))

    def test_uncontrolled_proof_commands_are_rejected_before_lean(self):
        for proof in ['by sorry', 'by admit', 'by rfl\naxiom bad : False',
                      'by rfl\nimport Benchmark.Train', 'by native_decide',
                      'by run_tac Lean.logInfo "forged"']:
            with self.subTest(proof=proof):
                checked = self.checker.check_partial(dict(self.candidate(), proof_term=proof), self.context)
                self.assertFalse(checked['accepted'])
                self.assertEqual(checked['sigma']['code'], 'unsupported_term_syntax')
        self.assertFalse(Path(self.context['attempt_dir']).exists())

    def test_wrong_proposition_is_rejected_against_independent_source_anchor(self):
        for proposition in ['True', self.candidate()['proposition'].replace('Type u', 'Type 0'),
                            self.candidate()['proposition'].replace('h_domain : True', 'h_domain : False')]:
            with self.subTest(proposition=proposition):
                candidate = dict(self.candidate(), proposition=proposition, proof_term='by exact True.intro')
                checked = self.checker.check_partial(candidate, self.context)
                self.assertEqual(checked['status'], 'integrity_error', checked)
                self.assertEqual(checked['sigma']['code'], 'proposition_binding_mismatch', checked)
        self.assertFalse(Path(self.context['attempt_dir']).exists())

    def test_candidate_or_context_foreign_hash_is_rejected(self):
        candidate = self.candidate()
        checked = self.checker.check_partial(dict(candidate, source_sha256='0' * 64), self.context)
        self.assertEqual(checked['status'], 'integrity_error')
        altered = dict(self.context, source=dict(self.source.to_dict(), sha256='1' * 64))
        self.assertEqual(self.checker.check_partial(candidate, altered)['status'], 'integrity_error')

    def test_tampered_original_snapshot_is_rejected(self):
        candidate = self.candidate()
        Path(self.source.snapshot_path).write_text(self.source.declaration + '\n-- changed\n')
        self.assertEqual(self.checker.check_partial(candidate, self.context)['status'], 'integrity_error')

    def test_missing_environment_and_zero_budget_have_distinct_diagnostics(self):
        candidate = self.candidate()
        missing = LeanChecker(lean_binary=self.store.root / 'missing-lean')
        blocked = missing.check_partial(candidate, self.context)
        self.assertEqual(blocked['status'], 'environment_blocked', blocked)
        self.assertEqual(blocked['sigma']['code'], 'lean_environment_unavailable')
        budget = self.checker.check_partial(candidate, dict(self.context, seconds=0))
        self.assertEqual(budget['status'], 'budget_exhausted')
        self.assertEqual(budget['sigma']['code'], 'budget_exhausted')

    def test_timeout_fault_fixture_is_classified_without_accepting_candidate(self):
        # Fault injection tests classification only; no claim of Lean success.
        from agent_v2 import math_lean_profile
        with patch.object(math_lean_profile, '_inventory', return_value={'modules': [], 'files': []}), \
             patch.object(math_lean_profile, '_compile', return_value={'timed_out': True,
                          'returncode': -9, 'environment_error': None}):
            checked = self.checker.check_partial(self.candidate(), self.context)
        self.assertFalse(checked['accepted'])
        self.assertEqual(checked['status'], 'budget_exhausted')
        self.assertEqual(checked['sigma']['code'], 'lean_timeout')

    def test_candidate_cannot_select_imports_or_profile(self):
        candidate = dict(self.candidate(), imports=['Benchmark.Train'])
        self.assertEqual(self.checker.check_partial(candidate, self.context)['status'], 'integrity_error')
        candidate = dict(self.candidate(), profile='unrestricted')
        self.assertEqual(self.checker.check_partial(candidate, self.context)['status'], 'integrity_error')

    def test_standard_library_test_named_exception_cannot_read_benchmark_or_arbitrary_paths(self):
        from agent_v2.math_lean_profile import _guard_dependency
        from agent_v2.storage import IntegrityError, guard_path
        fixed = self.checker.expected_binary.parent.parent / 'src/lean/Std/Http/Test/Helpers.lean'
        self.assertEqual(_guard_dependency(fixed, self.checker, 'Std.Http.Test.Helpers'), fixed.resolve())
        # Check rejection before reading or creating any alleged Test source.
        forbidden = [self.checker.repository / 'benchmark/lean/Benchmark/Statements/Test/Identity272.lean',
                     self.store.root / 'Std/Http/Test/Helpers.lean',
                     self.store.root / 'Test/not_read.lean']
        for path in forbidden:
            with self.subTest(path=path):
                with self.assertRaises(IntegrityError):
                    _guard_dependency(path, self.checker, 'Std.Http.Test.Helpers')
                with self.assertRaises(IntegrityError):
                    guard_path(path)
        with self.assertRaises(IntegrityError):
            guard_path(fixed)  # The global guard remains strict.

    def test_source_changed_during_compilation_keeps_failure_evidence(self):
        # Boundary fault injection: no fabricated success is accepted as Lean.
        from agent_v2 import math_lean_profile
        def compile_and_mutate(binary, source, output, source_root, environment, logs, deadline):
            output.write_bytes(b'fault-fixture-not-a-real-olean')
            if source.name == 'Candidate.lean':
                Path(self.source.snapshot_path).write_text(self.source.declaration + '\n-- changed during compile\n')
            return {'timed_out': False, 'returncode': 0, 'environment_error': None}
        with patch.object(math_lean_profile, '_inventory', return_value={'modules': [], 'files': []}), \
             patch.object(math_lean_profile, '_compile', side_effect=compile_and_mutate):
            checked = self.checker.check_partial(self.candidate(), self.context)
        self.assertFalse(checked['accepted'])
        self.assertEqual(checked['status'], 'integrity_error', checked)
        self.assertEqual(checked['sigma']['code'], 'verification_input_changed', checked)
        self.assertTrue(checked['evidence']['artifacts'])

    def test_package_object_without_source_cannot_shadow_toolchain(self):
        from agent_v2 import math_lean_profile
        from agent_v2.storage import IntegrityError
        fake = self.store.path('package-shadow')
        objects = fake / 'objects'
        objects.mkdir(parents=True)
        (objects / 'Init.olean').write_bytes(b'not-a-standard-Init-object')
        with patch.object(math_lean_profile, '_hash', return_value='0' * 64), \
             patch('agent_v2.lean_checker._runtime_libraries', return_value=[]):
            with self.assertRaisesRegex(IntegrityError, 'shadow'):
                math_lean_profile._inventory(self.checker, ('Init',), [(fake, objects)], [], float('inf'))

    def test_new_build_object_shadow_is_detected_on_reinventory(self):
        from agent_v2 import math_lean_profile
        from agent_v2.storage import IntegrityError
        build = self.store.path('build-shadow')
        build.mkdir()
        with patch.object(math_lean_profile, '_hash', return_value='0' * 64), \
             patch('agent_v2.lean_checker._runtime_libraries', return_value=[]):
            before = math_lean_profile._inventory(self.checker, ('Init',), [], [], float('inf'), build)
            self.assertIn(str(build), before['object_search_roots'])
            (build / 'Init.olean').write_bytes(b'new-shadow-after-first-inventory')
            with self.assertRaisesRegex(IntegrityError, 'shadow'):
                math_lean_profile._inventory(self.checker, ('Init',), [], [], float('inf'), build)

    def test_object_symlink_alias_is_rejected(self):
        from agent_v2.math_lean_profile import _assert_object_resolution
        from agent_v2.storage import IntegrityError
        root = self.store.path('module-root'); root.mkdir()
        outside = self.store.path('outside.olean'); outside.write_bytes(b'not-a-module')
        (root / 'Init.olean').symlink_to(outside)
        with self.assertRaisesRegex(IntegrityError, 'symlink'):
            _assert_object_resolution('Init', root, [root])

    def test_resume_environment_drift_or_missing_digest_rejected_before_compilation(self):
        from agent_v2 import math_lean_profile
        for prior in [{}, {'external_environment_sha256': '0' * 64}]:
            with self.subTest(prior=prior), \
                 patch.object(math_lean_profile, '_inventory', return_value={'modules': [], 'files': []}), \
                 patch.object(math_lean_profile, '_compile', return_value={'timed_out': True,
                              'returncode': -9, 'environment_error': None}) as compiler:
                checked = self.checker.check_partial(self.candidate(), dict(self.context, prior_evidence=prior))
                self.assertEqual(checked['status'], 'integrity_error', checked)
                self.assertEqual(checked['sigma']['code'], 'external_environment_changed', checked)
                compiler.assert_not_called()

    def test_external_environment_digest_ignores_only_fresh_build_paths(self):
        from agent_v2.math_lean_profile import external_environment_digest
        before = {'modules': ['Init'], 'files': [{'path': '/fixed/module.olean', 'sha256': 'a' * 64}],
                  'object_search_roots': ['/run/first/build', '/fixed']}
        replay = dict(before, object_search_roots=['/run/replay/build', '/fixed'])
        self.assertEqual(external_environment_digest(before), external_environment_digest(replay))
        changed = dict(replay, files=[{'path': '/fixed/module.olean', 'sha256': 'b' * 64}])
        self.assertNotEqual(external_environment_digest(before), external_environment_digest(changed))


if __name__ == '__main__':
    unittest.main()
