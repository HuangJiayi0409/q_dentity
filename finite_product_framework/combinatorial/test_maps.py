"""Map admission must use structure and retain full statement obligations."""
import unittest
from combinatorial.pipeline import plans, map_certificate
from combinatorial.test_improvement import var, num, app, total, eq

class Maps(unittest.TestCase):
    def test_complement_same_ground(self):
        s=total(app('Finset.powerset',var('s')))
        self.assertEqual({p['rule'] for p in plans(eq(s,s))},{'subset_complement'})
        self.assertEqual(plans(eq(s,total(app('Finset.powerset',var('t'))))),[])

    def test_union_ranked_blocks(self):
        ground=app('Union.union',var('s'),var('t'))
        lhs=total(app('Finset.powersetCard',var('h'),ground))
        rhs=total(app('Finset.powerset',var('s')))
        pp=plans(eq(lhs,rhs))
        self.assertEqual(pp[0]['rule'],'subset_blocks_rank')
        self.assertIn('rank_condition',map_certificate(pp[0]))

    def test_reciprocal_requires_same_base_and_rank(self):
        roger=lambda z,q,n:app('FiniteQBenchmark.rogersSzego',var(z),var(q),var(n))
        lhs=roger('vinv','q','n')
        self.assertEqual(plans(eq(lhs,app('HMul.hMul',var('c'),roger('v','p','n')))),[])
        self.assertEqual(plans(eq(lhs,app('HMul.hMul',var('c'),roger('v','q','m')))),[])
        p=plans(eq(lhs,app('HMul.hMul',var('c'),roger('v','q','n'))))[0]
        self.assertEqual(p['rule'],'gaussian_reciprocal')
        self.assertIn('shared_lemmas',map_certificate(p))

    def test_parity_candidate_is_not_acceptance(self):
        body=app('lambda',body=app('HMul.hMul',var('weight'),app('FiniteQBenchmark.gaussian',var('q'),var('n'),var('k'))))
        lhs=app('Finset.sum',app('Finset.range',var('bound')),body)
        pp=plans(eq(lhs,num(0)))
        self.assertEqual(pp[0]['rule'],'gaussian_odd_cancel')
        self.assertEqual(map_certificate(pp[0])['fixed_points'],'none by odd parity')

if __name__=='__main__': unittest.main()
