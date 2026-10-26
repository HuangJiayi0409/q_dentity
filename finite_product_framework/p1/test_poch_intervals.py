import unittest
import sympy as s
from expressions import n,k,q,Q,X,Poch
from poch_intervals import plan,backward_certificate,compact

class IntervalTests(unittest.TestCase):
 def test_shift_intersection_without_new_denominators(self):
  a=s.Symbol('a')
  p=plan([Poch(a/q,q,k+1),Poch(a,q,k)])
  self.assertEqual(len(p['cores']),1)
  self.assertEqual(next(iter(p['cores'].values())),Poch(a,q,k))
  self.assertEqual(s.cancel(p['normalized'][0]/p['normalized'][1]-(1-a/q)),0)
 def test_negative_n_parameter(self):
  p=plan([Poch(q**(-n-1),q,k),Poch(q**(-n),q,k)])
  core=next(iter(p['cores'].values()))
  self.assertEqual(core,Poch(q**(-n),q,k-1))
  self.assertTrue(all(r['prefix']>=0 and r['suffix']>=0 for r in p['rows']))
 def test_keeps_distinct_product_families(self):
  a,b=s.symbols('a b');p=plan([Poch(a,q,k),Poch(b,q,k),Poch(a,q,n)])
  self.assertEqual(len(p['cores']),3)
 def test_affine_power_denominator_factorization(self):
  c=s.Symbol('c')
  expanded=1-c*q**(n+1)-c*q**(n+2)+c**2*q**(2*n+3)
  factored=compact(expanded,s.factor)
  self.assertTrue(factored.is_Mul)
  self.assertEqual(compact(factored-(1-c*q**(n+1))*(1-c*q**(n+2))),0)
 def test_compact_keeps_product_atoms(self):
  a=s.Symbol('a');atom=Poch(a*q**n,q,k)
  value=compact(atom*(1-q**(n+1))/(1-q*q**n))
  self.assertEqual(value,atom)
 def test_backward_endpoint_cancellation(self):
  a,c=s.symbols('a c')
  F=Poch(a,q,k)*Poch(q**(-n),q,k)*q**k/(Poch(q,q,k)*Poch(c,q,k))
  R=(-Q*X**2*c+Q*X*c+Q*X*q-Q*q)/(Q**2*X*c*q-Q*X**2*c-Q*X*q+X**2)
  B=backward_certificate(F,R)
  self.assertFalse(s.denom(B).subs(X,Q).equals(0))
  self.assertEqual(s.cancel(R.subs(X,q*X)*q*(1-a*X)*(1-X/Q)/((1-q*X)*(1-c*X))-B),0)

if __name__=='__main__':unittest.main()
