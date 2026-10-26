"""Independent-component telescoping tests; no Train/Test data or Lean."""
import unittest
import sympy as s
from core import CoreBudget,compute,solve
from expressions import q,Q,X
from qgosper import Budget,UnsupportedDomain
from qparameterized import solve as scalar,solve_joint
from qjoint import search


def request(components):
    return dict(schema_version=1,solver='q_zeilberger_joint',input=dict(components=components))


class JointCoreTests(unittest.TestCase):
    def check_joint(self,components,result):
        self.assertEqual(result['status'],'constructed')
        symbols={str(t):t for t in set().union(*(s.sympify(v).free_symbols for c in components for v in c.values()),{q,Q,X})}
        parse=lambda v:s.sympify(v,locals=symbols)
        for relation in (result,result['primitive_relation']):
            cs=list(map(parse,relation['coefficients']))
            self.assertTrue(any(c!=0 for c in cs))
            self.assertTrue(all(not c.has(X) for c in cs))
            self.assertEqual(len(relation['certificates']),len(components))
            for c,Rtext in zip(components,relation['certificates']):
                U,V=map(s.sympify,(c['n_shift'],c['k_shift']))
                R=parse(Rtext);basis=[s.Integer(1)]
                for j in range(len(cs)-1):basis.append(s.cancel(basis[-1]*U.subs(Q,q**j*Q)))
                self.assertEqual(s.cancel(V*R.subs(X,q*X)-R-sum(a*b for a,b in zip(cs,basis))),0)

    def test_joint_space_keeps_alternatives_discarded_by_scalar_choice(self):
        b1,b2=[1,0,X],[0,1,X]
        first=scalar(1,b1,X,q);second=scalar(1,b2,X,q)
        self.assertEqual(first['coefficients'],['0','1','0'])
        self.assertEqual(second['coefficients'],['1','0','0'])
        joint=solve_joint([1,1],[b1,b2],X,q)
        self.assertEqual(joint['coefficients'],['0','0','1'])
        for Rtext in joint['certificates']:
            R=s.sympify(Rtext,locals={'q':q,'X':X})
            self.assertEqual(s.cancel(R.subs(X,q*X)-R-X),0)

    def test_two_geometric_components_need_shared_order_two(self):
        a,b=s.symbols('a b')
        components=[dict(n_shift=a,k_shift=1),dict(n_shift=b,k_shift=1)]
        self.assertEqual(search(components,max_order=1)['status'],'search_exhausted')
        r=search(components,max_order=2);self.check_joint(components,r)
        self.assertEqual(r['order'],2)
        self.assertEqual(r['primitive_relation']['coefficients'],['a*b','-a - b','1'])

    def test_three_components_and_reordering(self):
        components=[dict(n_shift=a,k_shift=1) for a in (2,3,5)]
        r=search(components,max_order=3);self.check_joint(components,r)
        self.assertEqual(r['primitive_relation']['coefficients'],['-30','31','-10','1'])
        reverse=search(components[::-1],max_order=3)
        self.assertEqual(r['primitive_relation']['coefficients'],reverse['primitive_relation']['coefficients'])

    def test_duplicate_components_do_not_raise_order(self):
        components=[dict(n_shift=2,k_shift=1)]*3
        r=search(components,max_order=1);self.check_joint(components,r)
        self.assertEqual(r['order'],1)

    def test_q_binomial_components_have_computed_nonzero_certificates(self):
        U=X*(1-q*Q)/(X-q*Q)
        components=[dict(n_shift=U,k_shift=z*(X-Q)/(1-q*X)) for z in (2,3)]
        r=search(components,max_order=2);self.check_joint(components,r)
        self.assertEqual(r['order'],2)
        self.assertTrue(all(R!='0' for R in r['certificates']))
        self.assertEqual(r['attempts'][0]['status'],'no_relation_in_joint_system')
        self.assertEqual(r['attempts'][1]['status'],'no_relation_in_joint_system')

    def test_order_zero_summable_components(self):
        components=[dict(n_shift=2,k_shift=q),dict(n_shift=3,k_shift=q**2)]
        r=search(components,max_order=0);self.check_joint(components,r)
        self.assertEqual(r['order'],0)

    def test_primitive_normalization_scales_every_certificate(self):
        a=s.Symbol('a')
        components=[dict(n_shift=X,k_shift=Q*(1-a*X**2))]*2
        r=search(components,max_order=2);self.check_joint(components,r)
        self.assertEqual(r['primitive_relation']['coefficients'],['1 - Q','0','Q*a'])
        self.assertEqual(r['primitive_relation']['certificates'],['-1','-1'])
        self.assertNotEqual(r['primitive_relation']['scaling_factor'],'1')

    def test_rational_and_negative_laurent_certificate_blocks(self):
        R1=1/(1-X);R2=X**-3
        bases=[[s.cancel(R1.subs(X,q*X)-R1)],[s.cancel(R2.subs(X,q*X)-R2)]]
        r=solve_joint([1,1],bases,X,q)
        self.assertEqual(r['status'],'constructed')
        for rhs,Rtext in zip(bases,r['certificates']):
            R=s.sympify(Rtext,locals={'q':q,'X':X})
            self.assertEqual(s.cancel(R.subs(X,q*X)-R-rhs[0]),0)
        # The common denominator can absorb X^-3, so f's Laurent lower bound
        # need not be negative. Check the resulting certificate's pole instead.
        R=s.sympify(r['certificates'][1],locals={'q':q,'X':X})
        self.assertEqual(s.cancel(R*X**3).subs(X,0),1)
        self.assertNotEqual(r['blocks'][0]['common_denominator'],'1')

    def test_homogeneous_only_is_not_nonzero_telescoper(self):
        r=solve_joint([1,1],[[1],[1]],X,q)
        self.assertEqual(r['status'],'no_relation_in_joint_system')
        self.assertNotIn('certificates',r)

    def test_zero_rhs_blocks_preserve_free_shared_coefficients(self):
        r=solve_joint([1,1],[[0,0],[0,0]],X,q,normalize_index=1)
        self.assertEqual(r['coefficients'],['0','1'])
        self.assertEqual(r['certificates'],['0','0'])

    def test_aggregate_unknown_budget(self):
        budget=Budget(max_unknowns=4)
        self.assertEqual(scalar(1,[X],X,q,budget)['status'],'constructed')
        r=solve_joint([1,1],[[X],[X]],X,q,budget)
        self.assertEqual(r['status'],'resource_exhausted')
        self.assertEqual(r['failed_component'],1)

    def test_normal_form_budget_is_propagated(self):
        r=solve_joint([q**1000*(X-q**-1000)/(X-1)],[[1]],X,q,Budget(max_normal_form_degree=5))
        self.assertEqual(r['status'],'resource_exhausted')

    def test_input_shape_and_compatibility(self):
        for components in ([],[dict(n_shift=Q,k_shift=Q)],
                           [dict(n_shift=0,k_shift=1)],[dict(n_shift=1,k_shift=1,certificate=0)]):
            with self.assertRaises(ValueError):search(components,max_order=1)
        for shifts,rhs in (([],[]),([1],[[1],[1]]),([1,1],[[1],[1,2]])):
            with self.assertRaises(ValueError):solve_joint(shifts,rhs,X,q)
        with self.assertRaises(ValueError):solve_joint([1],[[1]],X,q,normalize_index=True)
        with self.assertRaises(UnsupportedDomain):search([dict(n_shift=s.Float(0.5),k_shift=1)])

    def test_expression_ir_and_zero_component_indexing(self):
        r=compute(request([dict(summand=0),dict(summand=['pow',2,'n']),
                           dict(summand=['pow',3,'n'])]),CoreBudget(max_order=2))
        self.assertEqual(r['status'],'constructed')
        self.assertEqual(r['active_component_indices'],[1,2])
        self.assertEqual(r['operator']['coefficients'],['6','-5','1'])
        self.assertEqual(r['result']['certificates'],['0','0','0'])
        self.assertEqual(len(r['operator_certificate_term_expressions']),3)

    def test_all_zero_components(self):
        r=compute(request([dict(summand=0),dict(summand=0)]),CoreBudget())
        self.assertEqual(r['operator']['coefficients'],['1'])
        self.assertEqual(r['result']['certificates'],['0','0'])
        self.assertEqual(r['active_component_indices'],[])

    def test_cancellation_between_components_is_not_claimed(self):
        # 2^n - 2^n is zero, but the independent-component solver still needs E-2.
        req=request([dict(summand=['pow',2,'n']),dict(summand=['mul',-1,['pow',2,'n']])])
        r=compute(req,CoreBudget(max_order=0))
        self.assertEqual(r['status'],'search_exhausted')
        self.assertIn('not exploited',r['domain']['component_dependence_policy'])

    def test_public_input_rejections_and_resource_status(self):
        cases=[request([]),request([dict(n_shift=1,k_shift=0)]),
               request([dict(n_shift='__import__',k_shift=1)]),request([dict(n_shift=1,k_shift=1,hint=0)])]
        for req in cases:self.assertEqual(solve(req)['status'],'invalid_input')
        r=solve(request([dict(n_shift=2,k_shift=1)]*2),CoreBudget(max_states=1))
        self.assertEqual(r['status'],'resource_exhausted')

    def test_public_contract_source_hashes_and_mixed_inputs(self):
        r=solve(request([dict(summand=['pow',2,'n']),dict(n_shift=3,k_shift=1)]),CoreBudget(max_order=2))
        self.assertEqual(r['status'],'constructed')
        self.assertFalse(r['original_identity_proved'])
        self.assertEqual(r['benchmark_files_read'],0)
        self.assertIn('qjoint.py',r['source_sha256'])
        self.assertEqual(r['operator_certificate_term_expressions'],['0',None])


if __name__=='__main__':unittest.main()
