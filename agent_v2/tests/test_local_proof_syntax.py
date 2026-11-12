"""Direct trusted-parser unit checks; production acceptance is tested separately."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from agent_v2.lean_checker import LeanChecker, _lean_environment


class LocalProofSyntaxTests(unittest.TestCase):
    def run_driver(self, terms):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        checker = LeanChecker()
        driver = checker.repository / 'agent_v2/lean/LocalProofCheck.lean'
        code = driver.read_text() + '\n'
        for index, (prop, proof) in enumerate(terms):
            code += f'agent_v2_local_declaration Proof{index} {json.dumps(prop, ensure_ascii=False)} {json.dumps(proof, ensure_ascii=False)}\n'
        path = root / 'Probe.lean'; path.write_text(code)
        return subprocess.run([str(checker.binary), '-j', '1', str(path)], cwd=root,
            env=_lean_environment(checker.binary), text=True, capture_output=True, timeout=30)

    def test_basic_pure_tactics_have_cases_and_combinators(self):
        result = self.run_driver([
            ('True ∧ True', 'by constructor <;> exact True.intro'),
            ('True → True', 'by intro h; have h2 : True := h; exact h2'),
            ('True ∧ True → True', 'by intro h; rcases h with ⟨a, b⟩; exact a'),
            ('(0 : Nat) = 0', 'by calc (0 : Nat) = 0 := rfl'),
        ])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_executable_term_and_tactic_extensions_never_elaborate(self):
        for proof in ('by run_tac throwError "execution escaped"',
                      'by_elab throwError "execution escaped"',
                      'by native_decide',
                      'by exact True.intro\naxiom bad : False'):
            result = self.run_driver([('True', proof)])
            self.assertNotEqual(result.returncode, 0, proof)
            self.assertTrue('not permitted' in result.stdout or 'invalid complete local term' in result.stdout,
                            result.stdout + result.stderr)
            self.assertNotIn('error: execution escaped', result.stdout)

    def test_reflexivity_modulo_conditional_and_negation(self):
        for proposition, proof in [
            ('(0 : Nat) = 0', 'by rfl'),
            ('∀ n : Nat, n % 2 = n % 2', 'by intro n; exact Eq.refl (n % 2)'),
            ('∀ n : Nat, (if n = 0 then 1 else 0) = (if n = 0 then 1 else 0)',
             'by intro n; exact Eq.refl (if n = 0 then 1 else 0)'),
            ('∀ n : Int, -n = -n', 'by intro n; exact Eq.refl (-n)'),
        ]:
            with self.subTest(proposition=proposition):
                result = self.run_driver([(proposition, proof)])
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__': unittest.main()
