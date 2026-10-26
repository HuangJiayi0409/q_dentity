"""Exact synthetic tests for symbolic-bound Omega input construction."""
from pathlib import Path
import sys
import unittest
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'p1'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core import compute,CoreBudget
from check_omega_core import replay
from macmahon.adapter import Parser,source_sums,encode,reconstruct,OmegaInputGap


class AdapterTests(unittest.TestCase):
    def run_sum(self,text,types=None):
        types=types or {'n':'ℕ','q':'K','z':'K'}
        candidate=dict(ast=Parser(text,types).parse(),parameter_types=types,source_span=[0,len(text)],source_fragment=text)
        requests,binding=encode(candidate)
        outputs=[compute(req,CoreBudget()) for req in requests]
        for req,out in zip(requests,outputs):replay(req,out)
        return reconstruct(outputs,binding),binding,requests

    def assert_formula(self,text,formula,types=None):
        value,binding,requests=self.run_sum(text,types)
        substitutions={str(name):s.Symbol(symbol) for name,symbol in {**binding['coefficient_variables'],**binding['scalar_parameters']}.items()}
        expected=s.sympify(formula,locals=substitutions)
        self.assertEqual(s.cancel(value-expected),0)
        return value,binding,requests

    def test_symbolic_geometric_prefix(self):
        self.assert_formula('∑ j ∈ Finset.range (n+1), q^j','1/((1-n)*(1-n*q))')

    def test_signed_weight(self):
        self.assert_formula('∑ k ∈ Finset.range (n+1), z^((n:ℤ)-2*k)','1/((1-n*z)*(1-n/z))')

    def test_twice_bound(self):
        self.assert_formula('∑ k ∈ Finset.range (2*n+1), z^((n:ℤ)-(k:ℤ))','(1+n)/((1-n*z)*(1-n/z))')

    def test_alternating_weight(self):
        self.assert_formula('∑ k ∈ Finset.range (2*n+1), (-1:K)^(k:ℤ)*z^((n:ℤ)-(k:ℤ))','(1-n)/((1-n*z)*(1-n/z))')

    def test_empty_prefix_at_zero(self):
        self.assert_formula('∑ j ∈ Finset.range n, q^j','n/((1-n)*(1-n*q))')

    def test_natural_interval(self):
        self.assert_formula('∑ j ∈ Finset.Icc 1 n, q^j','n*q/((1-n)*(1-n*q))')

    def test_signed_interval(self):
        self.assert_formula('∑ j ∈ Finset.Icc (-(n:ℤ)) (n:ℤ), z^j','(1+n)/((1-n*z)*(1-n/z))')

    def test_nested_triangle(self):
        self.assert_formula('∑ j ∈ Finset.range (n+1), ∑ k ∈ Finset.range (j+1), q^j*z^k',
                            '1/((1-n)*(1-n*q)*(1-n*q*z))')

    def test_natural_subtraction_certified_by_outer_bound(self):
        self.assert_formula('∑ j ∈ Finset.range (n+1), ∑ k ∈ Finset.range (n-j+1), q^j*z^k',
                            '1/((1-n)*(1-n*q)*(1-n*z))')

    def test_unjustified_natural_truncation_rejected(self):
        with self.assertRaisesRegex(OmegaInputGap,'may truncate'):
            self.run_sum('∑ j ∈ Finset.range (n-1), q^j')

    def test_weight_branch_linearity(self):
        self.assert_formula('∑ j ∈ Finset.range (n+1), q^j-z^j',
                            '1/((1-n)*(1-n*q))-1/((1-n)*(1-n*z))')

    def test_constant_rational_prefactor(self):
        self.assert_formula('∑ j ∈ Finset.range (n+1), q^j/(1-q)',
                            '1/((1-q)*(1-n)*(1-n*q))')

    def test_two_symbolic_bounds(self):
        self.assert_formula('∑ j ∈ Finset.range (n+1), ∑ k ∈ Finset.range (m+1), q^j*z^k',
                            '1/((1-n)*(1-n*q)*(1-m)*(1-m*z))',{'n':'ℕ','m':'ℕ','q':'K','z':'K'})

    def test_literal_dimension_is_not_parameter_sampling(self):
        value,_,_=self.assert_formula('∑ j ∈ Finset.range 4, q^j','1+q+q**2+q**3',{'q':'K'})
        self.assertTrue(value.free_symbols)

    def test_literal_empty_interval(self):
        self.assert_formula('∑ j ∈ Finset.Icc 3 1, q^j','0',{'q':'K'})

    def test_nonlinear_weight_rejected(self):
        with self.assertRaises(OmegaInputGap):self.run_sum('∑ j ∈ Finset.range (n+1), q^(j*j)')

    def test_fractional_floor_rejected(self):
        with self.assertRaises(OmegaInputGap):self.run_sum('∑ j ∈ Finset.range (n/2+1), q^j')

    def test_index_rational_denominator_rejected(self):
        with self.assertRaises(OmegaInputGap):self.run_sum('∑ j ∈ Finset.range (n+1), 1/(1-q^j)')

    def test_arbitrary_function_rejected(self):
        with self.assertRaises(OmegaInputGap):self.run_sum('∑ j ∈ Finset.range (n+1), gaussian q n j')

    def test_no_natural_index_cast_erasure(self):
        with self.assertRaises(OmegaInputGap):self.run_sum('∑ j ∈ Finset.range (n+1), (j:K)*q^j')

    def test_symbolic_integer_bound_chamber_required(self):
        with self.assertRaises(OmegaInputGap):self.run_sum('∑ j ∈ Finset.Icc 0 n, q^j',{'n':'ℤ','q':'K'})

    def test_source_binding_and_hypothesis_exclusion(self):
        source='''theorem statement (q z : K) (n : ℕ)
 (h : (∑ j ∈ Finset.range n, q^j) = 0) :
 (∑ k ∈ Finset.range (n+1), z^((n:ℤ)-2*k)) = 0 := by
  sorry'''
        accepted,rejected=source_sums(source)
        self.assertEqual(len(accepted),1);self.assertFalse(rejected)
        row=accepted[0];a,b=row['source_span']
        self.assertEqual(source[a:b].strip(),row['source_fragment'])
        self.assertIn('z^',row['source_fragment'])

    def test_source_variable_renaming(self):
        source='theorem statement (u : K) (size : ℕ) : (∑ count ∈ Finset.range (size+1), u^count) = 0 := by\n  sorry'
        accepted,_=source_sums(source);requests,binding=encode(accepted[0])
        self.assertIn('size',binding['coefficient_variables'])
        self.assertEqual(requests[0]['solver'],'rational_omega')

    def test_source_multiple_sums_and_conjunction(self):
        source='theorem statement (q z : K) (n : ℕ) : (∑ j ∈ Finset.range n, q^j) = 0 ∧ (∑ k ∈ Finset.range n, z^k) = 0 := by\n  sorry'
        accepted,_=source_sums(source);self.assertEqual(len(accepted),2)

    def test_independent_numeric_coefficients(self):
        value,binding,_=self.run_sum('∑ k ∈ Finset.Icc (-(n:ℤ)) (n:ℤ), z^k')
        t=s.Symbol(binding['coefficient_variables']['n']);z=s.Symbol(binding['scalar_parameters']['z'])
        polynomial=s.series(value.subs(z,2),t,0,9).removeO().expand()
        for n in range(9):
            self.assertEqual(polynomial.coeff(t,n),sum(s.Integer(2)**j for j in range(-n,n+1)))

    def test_all_branches_required(self):
        _,binding,requests=self.run_sum('∑ j ∈ Finset.range (n+1), q^j-z^j')
        with self.assertRaises(ValueError):reconstruct([compute(requests[0],CoreBudget())],binding)


if __name__=='__main__':unittest.main()
