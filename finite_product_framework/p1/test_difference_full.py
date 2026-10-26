"""Independent synthetic tests for rational towers and finite difference algebras."""
import unittest
import sympy as s
from core import CoreBudget,compute,solve,rational_input
from expressions import X,q
from qpisigma import PiSigma,column_basis
from qfinite import FiniteAlgebra,finite_order
from qgosper import UnsupportedDomain
from ore import OreResourceLimit
from qdifference import rational_read
from test_difference_core import tree,request,H,J,K,P,R

E,Z,C,a=s.symbols('E Z C a')
B=CoreBudget(seconds=90)


def field_request(extensions,rhs,operator=None):
    result=request(extensions,rhs);result['solver']='difference_field'
    if operator is not None:result['input']['operator']=list(map(tree,operator))
    return result


def finite_request(extensions,algebraic,rhs):
    result=request(extensions,rhs);result['solver']='finite_difference_ring'
    result['input']['algebraic_extensions']=[dict(name=str(z),polynomial=tree(p),shift=tree(v)) for z,p,v in algebraic]
    return result


class RationalTowerTests(unittest.TestCase):
    def tower(self,extensions,budget=B):
        t=PiSigma(budget)
        for row in extensions:self.assertTrue(t.add(*row))
        return t

    def recovered(self,extensions,g,A=1,Bb=-1):
        t=self.tower(extensions);rhs=s.cancel(A*t.sigma(g)+Bb*g)
        basis=t.solve(A,Bb,[rhs]);self.assertTrue(any(cs[0]!=0 for cs,h in basis))
        for cs,h in basis:self.assertEqual(s.cancel(A*t.sigma(h)+Bb*h-cs[0]*rhs),0)
        return t,basis

    def public(self,extensions,rhs,operator=None):
        out=compute(field_request(extensions,rhs,operator),B)
        self.assertEqual(out['status'],'constructed')
        sigma={X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in extensions}}
        A,Bb=operator or (1,-1)
        for row in [out['result'],*out['result']['solution_basis']]:
            cs=list(map(rational_read,row['original_coefficients']));g=rational_read(row['original_certificate'])
            self.assertTrue(all(s.cancel(c.xreplace(sigma)-c)==0 for c in cs))
            self.assertEqual(s.cancel(A*g.xreplace(sigma)+Bb*g-sum(c*f for c,f in zip(cs,rhs))),0)
        return out

    def test_sum_denominator(self):self.recovered([(H,'sum',1)],1/H)
    def test_harmonic_sum_denominator(self):self.recovered([(H,'sum',1/(1-X))],1/H)
    def test_product_non_laurent_denominator(self):self.recovered([(P,'product',2)],1/(1+P))
    def test_sum_denominator_multiplicity(self):self.recovered([(H,'sum',1)],1/H**3+1/(H+1)**2)
    def test_irreducible_quadratic_denominator(self):self.recovered([(H,'sum',1)],1/(H**2+1))
    def test_two_variable_denominator(self):self.recovered([(H,'sum',1),(P,'product',H+1)],1/(H+P))
    def test_sum_product_interleaving(self):self.recovered([(H,'sum',1),(P,'product',H+1),(J,'sum',P)],J/H)
    def test_product_sum_product_interleaving(self):self.recovered([(P,'product',2),(H,'sum',P/(1-X)),(R,'product',H)],R/(H+1))
    def test_weighted_first_order_rational_operator(self):self.recovered([(H,'sum',1)],1/(H+1),(H+2)/H,H-1)
    def test_weighted_equation_interleaved(self):self.recovered([(H,'sum',1),(P,'product',H+1)],P/H,H+P,1/H)

    def test_high_degree_homogeneous_resonance(self):
        t=self.tower([(H,'sum',1)]);g=H**7
        basis=t.solve(1,-((H+1)/H)**7,[0])
        self.assertTrue(any(cs[0]==0 and h!=0 and s.cancel(t.sigma(h/g)-h/g)==0 for cs,h in basis))

    def test_positive_and_negative_product_resonances(self):
        t=self.tower([(P,'product',2)])
        for exponent in (11,-9):
            basis=t.solve(1,-2**s.Integer(exponent),[0])
            self.assertTrue(any(h!=0 and s.cancel(t.sigma(h/P**exponent)-h/P**exponent)==0 for cs,h in basis))

    def test_exact_large_sum_orbit_offset(self):
        t=self.tower([(H,'sum',1)]);self.assertEqual(t.orbit(H,H+37,2),37)
        self.assertEqual(t.orbit(H+37,H,2),-37)

    def test_harmonic_orbit_match_uses_lower_telescoping(self):
        t=self.tower([(H,'sum',1/(1-X))]);p=H+X
        self.assertEqual(t.orbit(p,t.sigma(p,j=3),2),3)

    def test_nested_product_factor_orbit(self):
        t=self.tower([(H,'sum',1),(P,'product',H+1)])
        self.assertEqual(t.orbit(P+H,P+1,3),1)

    def test_different_orbits_are_decided(self):
        t=self.tower([(H,'sum',1)])
        self.assertIsNone(t.orbit(H,H+s.Rational(1,2),2))

    def test_rational_unsummability_is_not_unsupported(self):
        for exts,f in [([(H,'sum',1)],1/H),([(P,'product',2)],1/(1+P))]:
            out=compute(field_request(exts,[f]),B)
            self.assertEqual(out['status'],'no_relation_in_declared_basis')
            self.assertTrue(out['result']['solution_basis'])

    def test_multiple_rhs_shared_coefficients(self):
        self.public([(H,'sum',1)],[1/H,1/(H+1)])

    def test_parameter_names_and_rational_weights(self):
        self.public([(H,'sum',a)],[1/H-1/(H+a)])

    def test_unimodular_product_basis_reverses_nonprimitive_order(self):
        self.public([(P,'product',4),(R,'product',2)],[P+R])

    def test_unimodular_basis_needs_combination_of_inputs(self):
        out=self.public([(P,'product',4),(R,'product',8)],[P+R])
        self.assertTrue(any(r['action']=='unimodular_product_basis' for r in out['tower']))

    def test_dependent_products_separated_by_sum_are_reordered(self):
        self.public([(P,'product',4),(H,'sum',P),(R,'product',2)],[P+R])

    def test_integer_column_operations_are_unimodular(self):
        M=s.Matrix([[2,3,0],[4,6,5]]);U,rank=column_basis(M)
        self.assertEqual(abs(U.det()),1);self.assertEqual(rank,2);self.assertEqual((M*U)[:,-1],s.zeros(2,1))

    def test_automatic_sign_preserves_initial_value(self):
        out=self.public([(P,'product',-1)],[P/(1+P**2)])
        self.assertEqual(out['result']['unrolling_order'],2)
        # P is fixed by sigma^2; only the descended coefficients must be fixed by sigma.
        self.assertIn('P',out['result']['unrolled_constant_definitions'].values())
        self.assertIn('P**2',out['result']['certificate'])

    def test_sign_followed_by_redundant_sum(self):self.public([(P,'product',-1),(H,'sum',P)],[P])
    def test_sign_followed_by_genuine_harmonic_sum(self):
        self.public([(P,'product',-1),(H,'sum',P/(1-X))],[2*H*P/(1-X)+P**2/(1-X)**2])
    def test_sign_in_later_product_ratio(self):
        self.public([(P,'product',-1),(H,'sum',1),(R,'product',H+P)],[1/((H+P)*R)-1/R])

    def test_sign_product_with_geometric_factor(self):self.public([(P,'product',2),(R,'product',-2)],[P+R])

    def test_resource_bounds_are_not_no_solution(self):
        t=self.tower([(H,'sum',1)],CoreBudget(max_normal_form_degree=3))
        with self.assertRaises(OreResourceLimit):t.orbit(H,H+100,2)

    def test_malformed_operator_and_forward_reference(self):
        for req in [field_request([(H,'sum',H)],[H]),field_request([], [X],[0,0])]:
            with self.assertRaises(ValueError):compute(req,B)

    def test_process_timeout_and_new_source_provenance(self):
        req=field_request([(H,'sum',1)],[1/H-1/(H+1)])
        out=solve(req,B);self.assertEqual(out['status'],'constructed')
        self.assertIn('qpisigma.py',out['source_sha256']);self.assertIn('qfinite.py',out['source_sha256'])
        self.assertFalse(out['original_identity_proved'])
        self.assertEqual(solve(req,CoreBudget(seconds=0.00001))['status'],'resource_exhausted')


class FiniteRingTests(unittest.TestCase):
    def check(self,extensions,algebraic,rhs):
        out=compute(finite_request(extensions,algebraic,rhs),B)
        self.assertEqual(out['status'],'constructed')
        alg=FiniteAlgebra(algebraic,{X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in extensions}},B,
                          set().union(*(f.free_symbols for f in map(s.sympify,rhs))))
        for row in [out['result'],*out['result']['solution_basis']]:
            cs=list(map(rational_read,row['coefficients']));g=rational_read(row['certificate'])
            self.assertTrue(all(alg.normal(alg.sigma(c)-c)==0 for c in cs))
            self.assertEqual(alg.normal(alg.sigma(g)-g-sum(c*f for c,f in zip(cs,rhs))),0)
        return out,alg

    def test_order_two_root_of_unity(self):self.check([],[(E,E**2-1,-E)],[E])
    def test_preserved_nonspecialized_square(self):self.check([],[(E,E**2-C,-E)],[E])
    def test_order_three_root_of_unity(self):self.check([],[(Z,Z**2+Z+1,Z),(E,E**3-1,Z*E)],[E])
    def test_order_four_root_of_unity(self):self.check([],[(Z,Z**2+1,Z),(E,E**4-1,Z*E)],[E])
    def test_root_of_unity_declaration_constructs_relations(self):
        req=finite_request([],[(E,E**2-1,-E)],[E])
        req['input']['algebraic_extensions']=[dict(kind='root_unity',name='E',order=3)]
        out=compute(req,B);self.assertEqual(out['status'],'constructed')
        self.assertEqual(len(out['algebra']['basis']),6)
    def test_algebraic_constant_field(self):self.check([],[(Z,Z**2-2,Z)],[Z*X])

    def test_general_algebraic_shift_over_q_base(self):
        # E^2=X^2*C is preserved by sigma(E)=q*E.
        self.check([],[(E,E**2-C*X**2,q*E)],[E])

    def test_arbitrary_rhs_parameter_is_in_coefficient_field(self):self.check([],[(E,E**2-1,-E)],[a*E])
    def test_rational_quotient_denominator_unit(self):self.check([],[(E,E**2-1,-E)],[1/(2+E)-1/(2-E)])

    def test_zero_divisor_denominator_rejected(self):
        with self.assertRaisesRegex(ValueError,'nonunit'):
            compute(finite_request([],[(E,E**2-1,-E)],[1/(E-1)]),B)

    def test_nonreduced_quotient_rejected(self):
        with self.assertRaises(UnsupportedDomain):compute(finite_request([],[(E,E**2,E)],[E]),B)

    def test_shift_ideal_and_invertibility_checked(self):
        for image in (2*E,s.Integer(1)):
            with self.assertRaises(ValueError):compute(finite_request([],[(E,E**2-1,image)],[E]),B)

    def test_nonmonic_and_duplicate_algebraic_names_rejected(self):
        for alg in [[(E,2*E**2-2,-E)],[(E,E**2-1,-E),(E,E**3-1,E)]]:
            with self.assertRaises(ValueError):compute(finite_request([],alg,[E]),B)

    def test_constant_ring_nonunits_not_used_for_normalization(self):
        out,alg=self.check([],[(E,E**2-1,E)],[X*(1+E),X*(1-E)])
        for row in out['result']['solution_basis']:
            for index in row['unit_coefficient_indices']:
                self.assertNotEqual(alg.multiplication(rational_read(row['coefficients'][index])).det(),0)

    def test_root_of_unity_with_rational_sum_denominator(self):
        self.check([(H,'sum',1)],[(E,E**2-1,-E)],[E/H+E/(H+1)])

    def test_nonsplit_periodic_module_over_sum(self):
        self.check([(H,'sum',1)],[(Z,Z**2+Z+1,Z),(E,E**3-1,Z*E)],[Z*E/(H+1)-E/H])

    def test_sign_dependent_harmonic_sum_components(self):
        self.check([(H,'sum',E/(1-X))],[(E,E**2-1,-E)],[2*H*E/(1-X)+1/(1-X)**2])

    def test_sign_dependent_product_components(self):
        self.check([(H,'sum',1),(P,'product',H+E)],[(E,E**2-1,-E)],[1/((H+E)*P)-1/P])

    def test_component_constant_extension(self):
        self.check([(H,'sum',E)],[(E,E**2-1,-E)],[2*H*E+1])

    def test_finite_dimension_budget(self):
        with self.assertRaises(OreResourceLimit):
            compute(finite_request([],[(E,E**5-1,E)],[E]),CoreBudget(max_states=3))

    def test_public_negative_result_and_metadata(self):
        out=solve(finite_request([],[(E,E**2-1,-E)],[1/(1-X)]),B)
        self.assertEqual(out['status'],'no_relation_in_declared_basis');self.assertFalse(out['original_identity_proved'])

    def test_previous_nonsplit_gap_is_constructed_and_checked(self):
        alg=FiniteAlgebra([(Z,Z**2+Z+1,Z)],{X:q*X,H:H+Z/(1-X)},B)
        f=alg.normal(alg.sigma(1/H)-1/H)
        self.assertEqual(alg.normal(alg.sigma(1/H)-1/H-f),0)
        out=solve(finite_request([(H,'sum',Z/(1-X))],[(Z,Z**2+Z+1,Z)],[f]),B)
        self.assertEqual(out['status'],'constructed')
        cs=list(map(rational_read,out['result']['coefficients']));g=rational_read(out['result']['certificate'])
        self.assertEqual(alg.normal(alg.sigma(g)-g-cs[0]*f),0)


if __name__=='__main__':unittest.main()
