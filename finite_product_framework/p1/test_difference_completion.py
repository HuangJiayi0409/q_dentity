"""Original-equation regression tests for the stage-four extensions.

Fixtures construct their RHS independently; the solver sees only equations,
never the known certificate. Tests replay every returned basis vector.
"""
import unittest
import sympy as s
from core import CoreBudget,compute,solve
from qgosper import UnsupportedDomain
from ore import OreResourceLimit
from qfinite import FiniteAlgebra
from qdifference import rational_read
from test_difference_core import tree,request,H,J,K,P,R
from test_difference_full import field_request,finite_request,X,q,E,Z,C,a,B


def system_request(extensions,V,rows):
    data=request(extensions,[0])['input']
    data['matrix']=[[tree(v) for v in row] for row in V.tolist()]
    data['rhs_basis']=[[tree(v) for v in row] for row in rows]
    return dict(schema_version=1,solver='difference_system',input=data)


class CompletionTests(unittest.TestCase):
    def field(self,exts,A,D,g):
        A,D=map(s.sympify,(A,D));shift={X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in exts}}
        rhs=s.cancel(A*g.xreplace(shift)+D*g)
        out=compute(field_request(exts,[rhs],[A,D]),B)
        self.assertEqual(out['status'],'constructed')
        for row in [out['result'],*out['result']['solution_basis']]:
            cs=list(map(rational_read,row['original_coefficients']));h=rational_read(row['original_certificate'])
            self.assertTrue(all(s.cancel(c.xreplace(shift)-c)==0 for c in cs))
            self.assertEqual(s.cancel(A*h.xreplace(shift)+D*h-cs[0]*rhs),0)
        return out

    def finite(self,exts,alg,g,A=1,D=-1):
        A,D=map(s.sympify,(A,D));F=FiniteAlgebra(alg,{X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in exts}},B,
                                                          set().union(*(v.free_symbols for v in (A,D,g))))
        rhs=F.normal(A*F.sigma(g)+D*g);req=finite_request(exts,alg,[rhs])
        req['input']['operator']=list(map(tree,(A,D)))
        out=compute(req,B);self.assertEqual(out['status'],'constructed')
        for row in [out['result'],*out['result']['solution_basis']]:
            cs=list(map(rational_read,row['coefficients']));h=rational_read(row['certificate'])
            self.assertTrue(all(F.normal(F.sigma(c)-c)==0 for c in cs))
            self.assertEqual(F.normal(A*F.sigma(h)+D*h-cs[0]*rhs),0)
        return out,F

    def system(self,V,g,exts=None):
        exts=exts or [(H,'sum',1)];shift={X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in exts}}
        g=s.Matrix([g]);rhs=(g.applyfunc(lambda v:v.xreplace(shift))*V-g).applyfunc(s.cancel)
        out=compute(system_request(exts,V,[list(rhs)]),B)
        self.assertEqual(out['status'],'constructed')
        for row in [out['result'],*out['result']['solution_basis']]:
            cs=list(map(rational_read,row['coefficients']));h=s.Matrix([list(map(rational_read,row['certificate_row']))])
            self.assertTrue(all(s.cancel(c.xreplace(shift)-c)==0 for c in cs))
            self.assertEqual((h.applyfunc(lambda v:v.xreplace(shift))*V-h-cs[0]*rhs).applyfunc(s.cancel),s.zeros(1,V.rows))
        return out

    def test_weighted_sign_rational_coefficients(self):
        self.field([(P,'product',-1),(H,'sum',1)],H+P,1/H,1/(H+P))

    def test_weighted_sign_dependent_nested_sum(self):
        self.field([(P,'product',-1),(H,'sum',P/(1-X))],H+1,P,1/(H+P))

    def test_weighted_sign_followed_by_product(self):
        self.field([(P,'product',-1),(H,'sum',1),(R,'product',H+P)],1,-2,1/R)

    def test_weighted_periodic_homogeneous_direction_retained(self):
        out=compute(field_request([(P,'product',-1)],[0],[1,1]),B)
        basis=out['result']['solution_basis']
        self.assertTrue(any(rational_read(r['original_certificate'])!=0 for r in basis))
        for r in basis:
            h=rational_read(r['original_certificate']);self.assertEqual(s.cancel(h.xreplace({P:-P,X:q*X})+h),0)

    def test_periodic_one_term_multiplication(self):self.field([(P,'product',-1)],0,P+1,1/(P+2))
    def test_periodic_one_term_shift(self):self.field([(P,'product',-1),(H,'sum',1)],H+P,0,1/(H+P))

    def test_periodic_no_relation_is_decided(self):
        out=compute(field_request([(P,'product',-1),(H,'sum',1)],[1/H],[1,2]),B)
        self.assertEqual(out['status'],'no_relation_in_declared_basis')

    def test_upper_triangular_coupled_system(self):self.system(s.Matrix([[2,H],[0,1]]),[1/H,X/(H+1)])
    def test_lower_triangular_coupled_system(self):self.system(s.Matrix([[2,0],[H,1]]),[1/H,X/(H+1)])
    def test_semilinear_weighted_cycle(self):self.system(s.Matrix([[0,H],[1,0]]),[1/H,X/(H+1)])
    def test_nondiagonal_finite_order_block(self):self.system(s.Matrix([[0,-1],[1,-1]]),[1/H,X/(H+1)])
    def test_projectively_periodic_block(self):self.system((H+1)*s.Matrix([[0,-1],[1,-1]]),[1/H,X/(H+1)])
    def test_coupled_interleaved_tower(self):
        self.system(s.Matrix([[2,P],[0,H+1]]),[1/(P+H),1/H],[(H,'sum',1),(P,'product',H+1)])

    def test_shared_rhs_parameters_and_homogeneous_vectors(self):
        V=s.eye(2);rows=[[1/H,0],[-1/(H+1),0],[0,X]]
        out=compute(system_request([(H,'sum',1)],V,rows),B)
        pairs=out['result']['solution_basis']
        self.assertTrue(any(all(rational_read(c)==0 for c in r['coefficients']) and any(rational_read(h)!=0 for h in r['certificate_row']) for r in pairs))
        self.assertTrue(any(rational_read(r['coefficients'][0])!=0 and rational_read(r['coefficients'][1])!=0 for r in pairs))

    def test_coupled_redundant_sums_keep_invariant(self):
        self.system(s.Matrix([[1,H-J],[0,2]]),[1/H,1/J],[(H,'sum',1),(J,'sum',1)])

    def test_previous_matrix_block_gap_is_constructed(self):
        V=s.Matrix([[H,1],[1,H+1]]);g=s.Matrix([[1/H,X]])
        f=(g.applyfunc(lambda v:v.xreplace({X:q*X,H:H+1}))*V-g).applyfunc(s.cancel)
        result=compute(system_request([(H,'sum',1)],V,[list(f)]),B)
        self.assertEqual(result['status'],'constructed')
        for row in result['result']['solution_basis']:
            c=rational_read(row['coefficients'][0]);h=s.Matrix([list(map(rational_read,row['certificate_row']))])
            self.assertEqual((h.applyfunc(lambda v:v.xreplace({X:q*X,H:H+1}))*V-h-c*f).applyfunc(s.cancel),s.zeros(1,2))

    def test_matrix_validation_and_resource(self):
        with self.assertRaises(ValueError):compute(system_request([(H,'sum',1)],s.zeros(2),[[0,0]]),B)
        with self.assertRaises(OreResourceLimit):compute(system_request([(H,'sum',1)],s.eye(2),[[0,0]]),CoreBudget(max_states=1))

    def test_nonsplit_invariant_unit_gauge(self):
        self.finite([(H,'sum',Z/(1-X))],[(Z,Z**2+Z+1,Z)],1/H)

    def test_nonsplit_affine_gauge_removes_exact_coordinate(self):
        self.finite([(H,'sum',Z/(1-X)+(q-1)*X)],[(Z,Z**2+Z+1,Z)],H**2)

    def test_nonsplit_gauge_preserves_redundant_sum_constant(self):
        out,F=self.finite([(H,'sum',Z)],[(Z,Z**2+Z+1,Z)],H**2)
        self.assertTrue(out['result']['solution_basis'])

    def test_nonsplit_two_gauged_sums(self):
        self.finite([(H,'sum',Z/(1-X)),(J,'sum',Z*H)],[(Z,Z**2+Z+1,Z)],J/H)

    def test_nonsplit_product_unit_gauge(self):
        self.finite([(H,'sum',1),(P,'product',(H+1+Z)/(H+Z))],[(Z,Z**2+Z+1,Z)],1/P)

    def test_nonperiodic_nonsplit_module_over_sum(self):
        self.finite([(H,'sum',1)],[(E,E**2-C*X**2,q*E)],E/H)

    def test_weighted_nonperiodic_nonsplit_module(self):
        self.finite([(H,'sum',1)],[(E,E**2-C*X**2,q*E)],E/H,H+2,-2)

    def test_weighted_nonsplit_periodic_module(self):
        self.finite([(H,'sum',1)],[(E,E**2-C,-E)],E/H,H+2,-2)

    def test_weighted_split_component_cycle(self):
        self.finite([(H,'sum',E/(1-X))],[(E,E**2-1,-E)],1/(H+E),H+E,2+E)

    def test_weighted_finite_base(self):self.finite([],[(Z,Z**2-2,Z)],Z/(1-X),1+X,-2)

    def test_finite_one_term_multiplication(self):
        self.finite([(H,'sum',Z/(1-X))],[(Z,Z**2+Z+1,Z)],1/H,0,H+Z)

    def test_finite_one_term_inverse_independent_free_shift(self):
        self.finite([(H,'sum',1)],[(E,E**2-C*X**2,q*E)],E/H,H+2,0)

    def test_finite_one_term_inverse_dependent_free_shift(self):
        self.finite([(H,'sum',E/(1-X))],[(E,E**2-1,-E)],1/(H+E),H+E,0)

    def test_operator_zero_in_quotient_rejected(self):
        req=finite_request([],[(Z,Z**2+Z+1,Z)],[X]);req['input']['operator']=[tree(Z**2+Z+1),0]
        with self.assertRaisesRegex(ValueError,'nonzero operator'):compute(req,B)

    def test_zero_divisor_product_ratio_rejected(self):
        req=finite_request([(P,'product',E-1)],[(E,E**2-1,-E)],[X])
        with self.assertRaisesRegex(ValueError,'nonunit product ratio'):compute(req,B)

    def test_triangular_remainder_matches_groebner_form(self):
        F=FiniteAlgebra([(Z,Z**2-2,Z),(E,E**3-Z*E-1,E)],{X:q*X},B)
        for value in [E**7+Z**6*E**4,(X+Z)*E**5+Z**3/(1-X)]:
            self.assertEqual(s.cancel(F.remainder(value)-F.G.reduce(s.expand(value))[1]),0)

    def test_nonsplit_free_product_constant_normalization(self):
        self.finite([(P,'product',4),(R,'product',2)],[(Z,Z**2+Z+1,Z)],1/R)

    def test_nonsplit_free_sum_constant_normalization(self):
        self.finite([(H,'sum',1),(J,'sum',1)],[(Z,Z**2+Z+1,Z)],Z*(H-J)/H)

    def test_two_algebraic_summation_classes_descend(self):
        exts=[(H,'sum',Z/(1-X)+1/(1-2*X))];alg=[(Z,Z**2+Z+1,Z)]
        out,F=self.finite(exts,alg,H**2)
        self.assertIn('algebraic-number',out['result']['reduction_trace']['algorithm'])

    def test_previously_unsupported_algebraic_product_is_constructed(self):
        exts=[(H,'sum',1),(P,'product',H+Z)];alg=[(Z,Z**2+Z+1,Z)]
        F=FiniteAlgebra(alg,{X:q*X,H:H+1,P:(H+Z)*P},B);f=F.normal(F.sigma(1/P)-1/P)
        result=compute(finite_request(exts,alg,[f]),B)
        self.assertEqual(result['status'],'constructed')
        for row in result['result']['solution_basis']:
            cs=list(map(rational_read,row['coefficients']));g=rational_read(row['certificate'])
            self.assertEqual(F.normal(F.sigma(g)-g-cs[0]*f),0)

    def test_new_solver_public_process_and_provenance(self):
        req=system_request([(H,'sum',1)],s.Matrix([[1]]),[[1/(H+1)-1/H]])
        out=solve(req,B);self.assertEqual(out['status'],'constructed')
        self.assertIn('qpisigma_system.py',out['source_sha256']);self.assertFalse(out['original_identity_proved'])
        self.assertEqual(solve(req,CoreBudget(seconds=0.00001))['status'],'resource_exhausted')


if __name__=='__main__':unittest.main()
