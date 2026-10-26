"""Structural recurrence regressions, independent of Train identity names."""
import unittest
import sympy as s
from expressions import n,k,q,Q,X,Poch
from poch_intervals import plan,compact
from general_summation import frontend,construct,parse,validate_local
from core import CoreBudget
from source_ir import node,var,nat


class RecurrenceClosureTests(unittest.TestCase):
    def test_zero_side_does_not_raise_order_or_accept_false_initial(self):
        body=node('HMul.hMul',node('FiniteQBenchmark.poch',var('a'),var('q'),var('n')),
                  node('HPow.hPow',var('q'),var('j')))
        raw=node('Eq',node('Finset.sum',node('Finset.range',node('HAdd.hAdd',var('n'),nat(1))),
                          dict(op='lambda',name='j',body=body)),nat(0))
        problem,model=frontend(raw,'synthetic:zero-side')
        result=construct(problem,CoreBudget(seconds=20,max_order=2))['construction']
        self.assertEqual(result['status'],'constructed')
        self.assertEqual(result['order'],1)
        self.assertEqual(result['sides'][1]['seed_coefficients'],['1'])
        from general_sum_emit import emit
        with self.assertRaisesRegex(ValueError,'initial_value_mismatch'):
            emit(model,result)

    def test_square_base_shift_and_residue(self):
        a=s.Symbol('a')
        p=plan([Poch(a*q,q**2,k+1),Poch(a*q**3,q**2,k)])
        self.assertEqual(len(p['cores']),1)
        self.assertEqual(next(iter(p['cores'].values())),Poch(a*q**3,q**2,k))
        self.assertEqual(compact(p['normalized'][0]-(1-a*q)*p['normalized'][1]),0)

    def test_bases_and_residue_classes_stay_distinct(self):
        a=s.Symbol('a')
        p=plan([Poch(a,q,k),Poch(a,q**2,k),Poch(a*q,q**2,k)])
        self.assertEqual(len(p['cores']),3)

    def test_quadratic_power_shift_in_candidate_algebra(self):
        self.assertEqual(compact(q**((k+1)**2)-q**(k*k)*q**(2*k+1)),0)
        self.assertNotEqual(compact(q**((k+1)**2)-q**(k*k)*q**(2*k+2)),0)

    def test_compact_keeps_unrelated_nonlinear_powers(self):
        a=s.Symbol('a');f=Poch(a,q,n-k)
        self.assertEqual(compact(f*q**(k*k)),f*q**(k*k))
        self.assertNotEqual(compact(q**(k*k)-q**(n*n)),0)

    def test_nonintegral_or_nonpositive_product_base_rejected(self):
        a=s.Symbol('a')
        for base in (q**s.Rational(1,2),q**-1,s.S.One,a):
            with self.subTest(base=base),self.assertRaisesRegex(ValueError,'positive integral'):
                plan([Poch(a,base,k)])


if __name__=='__main__':unittest.main()
