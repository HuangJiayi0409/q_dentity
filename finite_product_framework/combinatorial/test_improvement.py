"""Structural admission regressions, without invoking other proof solvers."""
import unittest
from combinatorial.pipeline import plans, diagnostics, proof_script

def var(n):return dict(op='var',name=n)
def num(n):return dict(op='nat',value=n)
def app(op,*args,**kw):return dict(op=op,args=list(args),**kw)
def total(domain):return app('Finset.sum',domain,app('lambda',body=var('x')))
def eq(a,b):return app('Eq',a,b)

class Admission(unittest.TestCase):
    def test_wrong_range_length(self):
        self.assertEqual(plans(eq(total(app('Finset.range',var('n'))),total(app('Finset.range',var('m'))))),[])

    def test_cross_index_type(self):
        self.assertEqual(plans(eq(total(app('Finset.range',var('n'))),
            total(app('Finset.Icc',num(0),var('n'),type='Finset ℤ')))),[])

    def test_same_domain_both_orientations(self):
        s=total(app('Finset.range',var('n')))
        self.assertEqual(len(plans(eq(s,s))),2)

    def test_conjunction_requires_all_leaves(self):
        s=total(app('Finset.range',var('n')))
        raw=app('And',eq(s,s),eq(var('x'),var('y')))
        self.assertEqual(plans(raw),[])
        self.assertEqual([r['status'] for r in diagnostics(raw)],['candidate','unsupported_representation_or_map'])

    def test_nested_conjunction_proof_assembly(self):
        s=total(app('Finset.range',var('n')));e=eq(s,s)
        p=plans(app('And',e,app('And',e,e)))[0]
        self.assertEqual(proof_script(p).count('constructor'),2)
        self.assertEqual(proof_script(p).count('range_bijection'),3)

    def test_non_equality_is_explicit(self):
        self.assertEqual(diagnostics(app('Exists'))[0]['status'],'unsupported_representation_or_map')

if __name__=='__main__':unittest.main()
