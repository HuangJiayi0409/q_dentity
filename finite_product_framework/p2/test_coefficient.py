"""Branch safety and certificate boundaries; no Train/Test inputs."""
import unittest
from p2.run import construct, preparation

def atom(key=0, display='x'):
    return {'op':'atom','key':key,'display':display}

def integer(n):
    return {'op':'integer','value':n}

def eq(a,b):
    return {'lhs':a,'rhs':b}

class CoefficientCertificateTests(unittest.TestCase):
    def test_all_branches_required(self):
        r=construct({'goals':[eq(atom(),atom()),eq(integer(0),integer(1))]})
        self.assertEqual(r['status'],'coefficient_obligations_open')
        self.assertEqual(r['closed_goal_count'],1)
    def test_unsupported_branch_cannot_be_dropped(self):
        r=construct({'goals':[eq(atom(),atom()),{'unsupported_goal':'False'}]})
        self.assertNotEqual(r['status'],'constructed')
    def test_empty_list_is_not_closed_certificate(self):
        self.assertNotEqual(construct({'goals':[]})['status'],'constructed')
    def test_separate_branch_atom_namespaces(self):
        r=construct({'goals':[eq(atom(0,'x'),atom(0,'x')),eq(atom(0,'y'),atom(0,'y'))]})
        self.assertEqual(r['status'],'constructed')
        self.assertEqual(r['goals'][0]['atoms'][0]['display'],'x')
        self.assertEqual(r['goals'][1]['atoms'][0]['display'],'y')
    def test_inverse_not_cancelled(self):
        r=construct(eq({'op':'HMul.hMul','args':[atom(0,'x'),atom(1,'x⁻¹')]},integer(1)))
        self.assertNotEqual(r['status'],'constructed')
        self.assertFalse(r['denominator_cancellation'])
    def test_unknown_sum_remains_obligation(self):
        r=construct(eq(atom(0,'∑ k ∈ s, f k'),atom(1,'candidate closed form')))
        self.assertNotEqual(r['status'],'constructed')
    def test_closed_preparation_marker(self):
        self.assertEqual(construct({'closed_by_preparation':True})['status'],'constructed')
    def test_local_ring_normalization(self):
        a,b=atom(),atom(1,'y')
        r=construct(eq({'op':'HAdd.hAdd','args':[a,b]},{'op':'HAdd.hAdd','args':[b,a]}))
        self.assertEqual(r['status'],'constructed')
    def test_view_is_explicit(self):
        with self.assertRaises(ValueError):preparation(view='recurrence')
        self.assertIn('FiniteQBenchmark.phiTerm',preparation(view='finite'))
        self.assertNotIn('FiniteQBenchmark.phiTerm',preparation(view='series'))

if __name__=='__main__':unittest.main()
