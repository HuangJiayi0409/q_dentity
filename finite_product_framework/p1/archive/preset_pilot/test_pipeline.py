if __name__ == "__main__":
    raise SystemExit("Retired preset pilot: use ../../run.py; this archive is not an automatic pipeline.")

"""Failure-mode tests for the first pilot; run after check.py."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import sympy as sp
from run import HERE, ROOT, load_target
from search import search_linear_numerator


class PipelineFailureTests(unittest.TestCase):
    def test_wrong_recurrence_has_no_solution_in_ansatz(self):
        q, Q, X, z = sp.symbols('q Q X z')
        with self.assertRaisesRegex(ValueError, 'search_exhausted'):
            search_linear_numerator((1-q*Q)/(1-q*Q/X),
                                    -z*X*(1-Q/X)/(1-q*X),
                                    1-2*z*Q, X-q*Q, X, q)

    def test_unsupported_train_identity_is_not_reported_proved(self):
        with self.assertRaisesRegex(ValueError, 'no adapter'):
            load_target('FQI-CHU-VANDERMONDE-Q')

    def test_wrong_lower_boundary_is_rejected_by_lean(self):
        source = (HERE/'generated/FiniteQBinomial.lean').read_text()
        needle = '  | 0 => 0\n  | k+1 => z*q^n*binomialTerm q z n k'
        self.assertEqual(source.count(needle), 1)
        mutated = source.replace(needle, needle.replace('| 0 => 0', '| 0 => 1'))
        env = os.environ.copy()
        env['LEAN_PATH'] = str(HERE/'generated/deps')
        with tempfile.TemporaryDirectory(prefix='p1-negative-') as directory:
            path = Path(directory)/'WrongBoundary.lean'
            path.write_text(mutated)
            result = subprocess.run(['lake', 'env', 'lean', str(path)], cwd=ROOT/'project',
                                    env=env, text=True, capture_output=True, timeout=180)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unsolved goals', result.stdout + result.stderr)
        self.assertNotIn('unknown module', result.stdout + result.stderr)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PipelineFailureTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    (HERE/'generated/negative_checks.json').write_text(json.dumps({
        'tests_run': result.testsRun, 'failures': len(result.failures),
        'errors': len(result.errors), 'passed': result.wasSuccessful(),
        'cases': ['wrong_recurrence', 'unsupported_train_adapter', 'wrong_lower_boundary'],
    }, indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
