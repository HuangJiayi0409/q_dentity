"""Tests for input-driven construction and prevention of preset-proof fallback."""
import copy
import inspect
import json
from pathlib import Path
import unittest
import sympy as s
from expressions import derive, X, q
from search import Budget, search
from run import HERE, run
from qgosper import antidifference, coefficient_field, dispersion, q_power, UnsupportedDomain


def fixture():
    return json.loads((HERE/'examples/finite_q_binomial.formula.json').read_text())


class InputDrivenTests(unittest.TestCase):
    def test_shifts_derived_and_changed_with_input(self):
        first = fixture()
        second = copy.deepcopy(first)
        second['summand'] = ['mul', first['summand'], ['pow', 'a', 'k']]
        second['target'] = ['poch', ['mul', 'a', 'z'], 'q', 'n']
        left, right = derive(first), derive(second)
        self.assertEqual(s.cancel(right['k_shift']/left['k_shift']), s.Symbol('a'))
        self.assertNotEqual(left['target_coefficient'], right['target_coefficient'])

    def test_metadata_does_not_select_mathematics(self):
        first = fixture()
        second = dict(first, source_id='metadata-only')
        self.assertEqual(derive(first), derive(second))

    def test_proof_hints_rejected(self):
        for key in ('certificate', 'denominator', 'degree', 'lean_proof', 'recurrence'):
            with self.assertRaisesRegex(ValueError, 'invalid_problem'):
                derive(dict(fixture(), **{key: 'preset'}))

    def test_q_gosper_normal_form_and_residual(self):
        shifts = derive(fixture())
        result = search(shifts['n_shift'], shifts['k_shift'], shifts['target_coefficient'],
                        X, q)
        self.assertEqual(result['status'], 'constructed')
        self.assertEqual(result['rational_residual'], '0')
        self.assertEqual(result['algorithm'], 'q-Gosper')
        self.assertEqual(result['normal_form']['remaining_dispersion'], [])
        self.assertEqual(result['q_wz_residual'], '0')
        self.assertNotIn('denominator', inspect.signature(search).parameters)

    def test_changed_base_requires_different_search(self):
        problem = fixture()
        def change(node):
            if node == 'q':
                return ['pow', 'q', 2]
            return [change(x) for x in node] if isinstance(node, list) else node
        problem['summand'], problem['target'] = change(problem['summand']), change(problem['target'])
        shifts = derive(problem)
        result = search(shifts['n_shift'], shifts['k_shift'], shifts['target_coefficient'],
                        X, q)
        self.assertEqual(result['status'], 'constructed')
        self.assertEqual(result['q_wz_residual'], '0')

    def test_budget_exhaustion_is_not_unsummability(self):
        shifts = derive(fixture())
        result = search(shifts['n_shift'], shifts['k_shift'], shifts['target_coefficient'],
                        X, q, Budget(max_unknowns=0))
        self.assertEqual(result['status'], 'resource_exhausted')
        self.assertNotIn('certificate', result)

    def test_native_synthesis_does_not_use_archive(self):
        source = (HERE/'lean_pipeline.py').read_text()
        self.assertNotIn('archive/', source)
        self.assertNotIn('Identity005', source)
        self.assertNotIn('FQI-FINITE-Q-BINOMIAL', source)
        self.assertNotIn('Binomial.lean', source)


class QGosperTests(unittest.TestCase):
    def check_term(self, term):
        ratio = s.cancel(term/term.subs(X, X/q))
        result = antidifference(ratio, X, q)
        self.assertEqual(result['status'], 'constructed')
        certificate = result['antidifference_ratio']
        primitive = s.cancel(certificate*term)
        self.assertEqual(s.cancel(primitive.subs(X, q*X)-primitive-term), 0)
        return result

    def test_exact_q_power_recognition(self):
        a = s.Symbol('a')
        for i in (-13, 0, 17):
            self.assertEqual(q_power(q**i, q), i)
        self.assertEqual(q_power((q**3+q**2)/(q+1), q), 2)
        self.assertIsNone(q_power(a*q**3, q))
        self.assertIsNone(q_power(-q**3, q))

    def test_dispersion_beyond_old_radius(self):
        a = s.Symbol('a')
        A, B = (1-a*q**13*X)**2, (1-a*X)**3
        field = coefficient_field(A/B, X, q)
        self.assertEqual(dispersion(A, B, X, q, field), [13])

    def test_independently_constructed_rational_differences(self):
        a = s.Symbol('a')
        for primitive in (X**9, X**(-7), 1/(1-a*X),
                          1/(1-a*X)**2, X**3/(1-a*X)):
            with self.subTest(primitive=primitive):
                self.check_term(s.cancel(primitive.subs(X, q*X)-primitive))

    def test_laurent_negative_degrees(self):
        a = s.Symbol('a')
        ratio = q**7*(1-a*X/q)/(1-X)
        result = antidifference(ratio, X, q)
        self.assertEqual(result['status'], 'constructed')
        self.assertLess(result['laurent_bounds']['lower'], 0)
        self.assertLess(result['laurent_bounds']['upper'], 0)
        R = result['antidifference_ratio']
        self.assertEqual(s.cancel(ratio.subs(X,q*X)*R.subs(X,q*X)-R-1), 0)

    def test_derived_degree_exceeds_old_budget(self):
        result = self.check_term(X**13+X**2)
        self.assertGreater(result['laurent_bounds']['upper'], 6)

    def test_q_pochhammer_example(self):
        # REDUCE QSUM manual: (a;q)_k q^k/(q;q)_k, not a preset answer.
        a = s.Symbol('a')
        ratio = (q-a*X)/(1-X)
        result = antidifference(ratio, X, q)
        self.assertEqual(result['status'], 'constructed')
        R = result['antidifference_ratio']
        self.assertEqual(s.cancel(ratio.subs(X,q*X)*R.subs(X,q*X)-R-1), 0)

    def test_no_antidifference_is_decided_not_timed_out(self):
        for term in (s.Integer(1), 1+X):
            ratio = s.cancel(term/term.subs(X, X/q))
            result = antidifference(ratio, X, q)
            self.assertEqual(result['status'], 'no_q_hypergeometric_antidifference')
            self.assertEqual(result['reason'], 'inconsistent Laurent system')

    def test_generic_q_pochhammer_nonsummability(self):
        a, z = s.symbols('a z')
        result = antidifference(z*(1-a*X/q)/(1-X), X, q)
        self.assertEqual(result['status'], 'no_q_hypergeometric_antidifference')

    def test_unsupported_domains_are_not_negative_decisions(self):
        with self.assertRaises(UnsupportedDomain):
            antidifference(s.sqrt(q)+X, X, q)
        with self.assertRaises(UnsupportedDomain):
            antidifference(1+X, X, s.Integer(2))

    def test_zero_wz_difference(self):
        result = search(s.Integer(1), q, s.Integer(1), X, q)
        self.assertEqual(result['certificate'], '0')


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestSuite([
            unittest.defaultTestLoader.loadTestsFromTestCase(InputDrivenTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(QGosperTests)]))
    (HERE/'generated/test_results.json').write_text(json.dumps({
        'tests_run': result.testsRun, 'failures': len(result.failures),
        'errors': len(result.errors), 'passed': result.wasSuccessful(),
    }, indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
