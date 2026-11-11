"""Real, isolated Lean checks; all sources here are synthetic, never Test data."""
import hashlib
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class LeanCheckerTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.lean_checker'),
                             'new independent Lean checker is not implemented')
        from agent_v2.lean_checker import LeanChecker
        self.checker = LeanChecker()
        self.tmp = tempfile.TemporaryDirectory(prefix='agent-v2-lean-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.run = self.root / 'run'; self.run.mkdir()
        self.attempt = self.run / 'attempt'; self.attempt.mkdir()
        self.context = {'source_sha256': 'a' * 64, 'run_dir': str(self.run),
                        'attempt_dir': str(self.attempt), 'seconds': 20.0}
        self.candidate = {'id': 'local_1', 'proposition': '(2 + 2 : Nat) = 4',
                          'proof_term': 'by rfl', 'theorem': 'AgentV2Candidate.proof',
                          'source_sha256': 'a' * 64, 'dependencies': []}

    def check(self, **changes):
        return self.checker.check_partial(dict(self.candidate, **changes), self.context)

    def make_source(self, proposition='True'):
        from agent_v2.lean_checker import init_original_template
        text = init_original_template('Synthetic.statement', proposition)
        path = self.root / 'original.lean'; path.write_text(text)
        snapshot = self.run / 'original.lean'; snapshot.write_text(text)
        return {'identity': 'synthetic', 'path': str(path), 'snapshot_path': str(snapshot),
                'sha256': hashlib.sha256(text.encode()).hexdigest(),
                'theorem': 'Synthetic.statement', 'declaration': text,
                'Gamma': text, 'proposition': proposition, 'dependencies': []}

    def original(self, source, **report):
        return self.checker.accept_original(dict(proof_term='True.intro', seconds=20,
                  run_dir=str(self.run), **report), source, str(self.attempt))

    def test_real_lean_positive_has_bound_artifacts(self):
        result = self.check()
        self.assertTrue(result['accepted'], result)
        self.assertEqual(result['status'], 'partial_lean_verified')
        evidence = result['evidence']
        for key in ('proposition', 'source_sha256', 'proof_term', 'theorem'):
            self.assertEqual(evidence[key], self.candidate[key])
        self.assertEqual(evidence['axioms'], [])
        self.assertGreater(len(evidence['artifacts']), 2)
        self.assertTrue(any(a['path'].endswith('.olean') for a in evidence['artifacts']))
        for artifact in evidence['artifacts']:
            path = Path(artifact['path']); path.relative_to(self.run)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), artifact['sha256'])

    def test_real_lean_rejects_incorrect_term(self):
        result = self.check(proposition='False', proof_term='True.intro')
        self.assertFalse(result['accepted'])
        self.assertEqual(result['sigma']['code'], 'lean_check_failed')
        self.assertTrue(result['evidence']['artifacts'])

    def test_real_lean_rejects_non_prop_and_free_variable(self):
        for prop, term in [('Nat', '0'), ('n = n', 'by rfl')]:
            with self.subTest(prop=prop):
                result = self.check(proposition=prop, proof_term=term)
                self.assertFalse(result['accepted'])
                self.assertEqual(result['sigma']['code'], 'lean_check_failed')

    def test_source_hash_and_theorem_binding(self):
        for change in [{'source_sha256': 'b' * 64}, {'theorem': 'Wrong.proof'}]:
            with self.subTest(change=change):
                result = self.check(**change)
                self.assertFalse(result['accepted'])
                self.assertEqual(result['status'], 'integrity_error')

    def test_unsafe_terms_never_reach_lean(self):
        for term in ['by sorry', 'by admit', 'by run_tac Lean.logInfo "forged"',
                     'by exact (unsafeCast True.intro)',
                     'by rfl\naxiom bad : False', 'by native_decide',
                     'by exact (IO.println "Test")', 'by exact?']:
            with self.subTest(term=term):
                result = self.check(proof_term=term)
                self.assertFalse(result['accepted'])
                self.assertEqual(result['sigma']['code'], 'unsupported_term_syntax')
        self.assertEqual(list(self.attempt.iterdir()), [])

    def test_unverified_dependency_and_extra_claim_rejected(self):
        self.assertFalse(self.check(dependencies=['unverified'])['accepted'])
        self.assertFalse(self.check(accepted=True)['accepted'])

    def test_attempt_escape_and_test_path_rejected_before_writes(self):
        for path in [self.root / 'escape', self.run / 'Test' / 'forbidden']:
            self.context['attempt_dir'] = str(path)
            result = self.check()
            self.assertFalse(result['accepted'])
            self.assertEqual(result['status'], 'integrity_error')
            self.assertFalse(path.exists())

    def test_zero_budget_and_missing_binary(self):
        self.context['seconds'] = 0
        self.assertEqual(self.check()['status'], 'budget_exhausted')
        self.context['seconds'] = 20
        from agent_v2.lean_checker import LeanChecker
        result = LeanChecker(lean_binary=self.root / 'missing').check_partial(self.candidate, self.context)
        self.assertEqual(result['status'], 'environment_blocked')

    def test_original_exact_template_is_verified(self):
        result = self.original(self.make_source())
        self.assertTrue(result['accepted'], result)
        self.assertEqual(result['status'], 'original_theorem_proved')
        self.assertEqual(result['evidence']['theorem'], 'Synthetic.statement')

    def test_original_tampering_and_context_change_rejected(self):
        for field, value in [('sha256', 'f' * 64), ('theorem', 'Other.statement'),
                             ('declaration', 'theorem evil : True := by sorry'),
                             ('Gamma', {'assumption': 'False'}), ('proposition', 'False')]:
            with self.subTest(field=field):
                source = self.make_source(); source[field] = value
                self.assertFalse(self.original(source)['accepted'])
        source = self.make_source()
        Path(source['snapshot_path']).write_text('tampered')
        self.assertEqual(self.original(source)['status'], 'integrity_error')

    def test_original_dependency_hash_and_path_checked(self):
        source = self.make_source()
        dep = self.root / 'dependency.lean'; dep.write_text('import Init\n')
        source['dependencies'] = [{'schema_version': 1, 'path': str(dep), 'sha256': 'b' * 64}]
        self.assertEqual(self.original(source)['status'], 'integrity_error')
        source['dependencies'][0]['path'] = str(self.root / 'Test' / 'not_read.lean')
        self.assertEqual(self.original(source)['status'], 'integrity_error')

    def test_original_unsupported_source_fails_closed(self):
        source = self.make_source()
        source['declaration'] = 'import Benchmark.Batch3Proofs\ntheorem statement : True := by sorry\n'
        source['Gamma'] = source['declaration']
        source['sha256'] = hashlib.sha256(source['declaration'].encode()).hexdigest()
        for key in ('path', 'snapshot_path'): Path(source[key]).write_text(source['declaration'])
        result = self.original(source)
        self.assertFalse(result['accepted'])
        self.assertEqual(result['status'], 'environment_blocked')
        self.assertEqual(result['sigma']['code'], 'unsupported_original_translation')

    def test_fabricated_original_logs_or_name_cannot_pass(self):
        source = self.make_source()
        result = self.checker.accept_original({'status': 'proved', 'accepted': True,
                    'stdout': 'AgentV2 accepted', 'run_dir': str(self.run)}, source, str(self.attempt))
        self.assertFalse(result['accepted'])
        self.assertFalse(self.original(source, theorem='Other.statement')['accepted'])

    def test_incomplete_context_returns_structured_error(self):
        del self.context['run_dir']
        result = self.check()
        self.assertFalse(result['accepted'])
        self.assertEqual(result['status'], 'integrity_error')

    def fault_injection_process(self, mutate):
        """Only a boundary fault fixture, never evidence of Lean success."""
        binary = self.root / 'toolchain/bin/lean'; binary.parent.mkdir(parents=True)
        binary.write_bytes(b'fault-fixture'); binary.chmod(0o700)
        lib = self.root / 'toolchain/lib/lean'; lib.mkdir(parents=True)
        (lib / 'Init.olean').write_bytes(b'initial-standard-library')
        runtime = lib / 'libCustom.so'; runtime.write_bytes(b'initial-runtime-library')
        src = self.root / 'toolchain/src/lean'; src.mkdir(parents=True)
        for module in ['Init', 'Lean.Elab.Command', 'Lean.Elab.ElabRules', 'Lean.Util.CollectAxioms']:
            path = src / (module.replace('.', '/') + '.lean'); path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('prelude\n')
            artifact = lib / (module.replace('.', '/') + '.olean'); artifact.parent.mkdir(parents=True, exist_ok=True)
            if not artifact.exists(): artifact.write_bytes(b'fixture-module')
        config = self.root / 'repository/benchmark/lean/lean-toolchain'
        config.parent.mkdir(parents=True); config.write_text('leanprover/lean4:v4.35.0-rc4\n')
        from agent_v2.lean_checker import LeanChecker
        checker = LeanChecker(repository=self.root / 'repository', lean_binary=binary)
        checker.expected_binary = binary

        class Process:
            returncode = 0
            def __init__(self, args, **kwargs):
                src = Path(args[-1]); out = Path(args[args.index('-o') + 1])
                nonce = re.search(r'nonce "([0-9a-f]+)"', src.read_text()).group(1)
                record = {'agent_v2_audit_v1': nonce, 'theorem': 'AgentV2Candidate.proof', 'axioms': [],
                          'modules': sorted(['Init', 'Lean.Elab.Command', 'Lean.Elab.ElabRules', 'Lean.Util.CollectAxioms'])}
                kwargs['stdout'].write((json.dumps({'severity': 'information', 'data': json.dumps(record)}) + '\n').encode())
                out.write_bytes(b'not-a-real-olean')
                mutate(lib, config, out)
            def wait(self, timeout=None): return self.returncode

        with patch('agent_v2.lean_checker.subprocess.Popen', Process):
            with patch('agent_v2.lean_checker._runtime_libraries', return_value=[runtime], create=True):
                return checker.check_partial(self.candidate, self.context)

    def test_runtime_dependency_mutation_is_rejected(self):
        def mutate(lib, config, out):
            (lib / 'Init.olean').write_bytes(b'modified-standard-library')
            config.write_text('leanprover/lean4:v0.0.0\n')
        result = self.fault_injection_process(mutate)
        self.assertFalse(result['accepted'])
        self.assertEqual(result['status'], 'integrity_error')

    def test_output_symlink_escape_is_rejected_before_hashing(self):
        external = self.root / 'outside.bin'; external.write_bytes(b'outside')
        def mutate(lib, config, out):
            out.unlink(); out.symlink_to(external)
        result = self.fault_injection_process(mutate)
        self.assertFalse(result['accepted'])
        self.assertEqual(result['status'], 'integrity_error')

    def test_actual_loader_resolved_library_mutation_is_rejected(self):
        def mutate(lib, config, out):
            (lib / 'libCustom.so').write_bytes(b'modified-runtime-library')
        result = self.fault_injection_process(mutate)
        self.assertFalse(result['accepted'])
        self.assertEqual(result['status'], 'integrity_error')


if __name__ == '__main__':
    unittest.main()
