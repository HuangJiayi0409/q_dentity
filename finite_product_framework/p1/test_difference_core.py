"""Synthetic algorithm tests; no Train, Test split, or Lean files are read."""
import unittest
import sympy as s
from core import CoreBudget, compute, solve, rational_input
from expressions import X, q
from qgosper import UnsupportedDomain
from ore import OreResourceLimit
from qdifference import (Tower, product_lattice, constant_signature, laurent_coefficients,
                         rational_read, verify_relation)

H,J,K,P,R = s.symbols('H J K P R')
a,b = s.symbols('a b')
B = CoreBudget(seconds=60)


def tree(value):
    value = s.sympify(value)
    if value.is_Integer: return int(value)
    if value.is_Rational: return ['div', int(value.p), int(value.q)]
    if value.is_Symbol: return str(value)
    if value.is_Add: return ['add', *map(tree, value.args)]
    if value.is_Mul: return ['mul', *map(tree, value.args)]
    if value.is_Pow and value.exp.is_Integer: return ['pow', tree(value.base), int(value.exp)]
    raise ValueError(value)


def request(extensions, rhs):
    return dict(schema_version=1, solver='difference_ring', input=dict(
        extensions=[dict(name=str(t), kind=kind, **{'increment' if kind=='sum' else 'ratio':tree(v)})
                    for t,kind,v in extensions], rhs_basis=list(map(tree,rhs))))


class DifferenceCoreTests(unittest.TestCase):
    def tower(self, products=(), sums=(), budget=B):
        t = Tower(budget)
        for p, ratio in products: self.assertTrue(t.add_product(p, ratio))
        for h, increment in sums: t.add_sum(h, increment)
        return t

    def recovered(self, tower, known):
        rhs = tower.sigma(known)-known
        basis = tower.solve([rhs])
        cs,g = next((cs,g) for cs,g in basis if cs[0] != 0)
        self.assertEqual(s.cancel(tower.sigma(g/cs[0]-known)-(g/cs[0]-known)),0)
        tower.check_basis([rhs],basis,len(tower.sums))
        return basis

    def checked_output(self, extensions, rhs):
        output = compute(request(extensions,rhs),B)
        self.assertEqual(output['status'],'constructed')
        substitutions = {X:q*X, **{t:t+v if kind=='sum' else t*v for t,kind,v in extensions}}
        for item in [output['result'], *output['result']['solution_basis']]:
            cs=list(map(rational_read,item['original_coefficients']));g=rational_read(item['original_certificate'])
            self.assertEqual(s.cancel(g.xreplace(substitutions)-g-sum(c*f for c,f in zip(cs,rhs))),0)
            self.assertTrue(all(s.cancel(c.xreplace(substitutions)-c)==0 for c in cs))
        return output

    def test_base_rational_exact_poles_and_negative_powers(self):
        self.recovered(self.tower(), X**-3+1/(1-X)**2)

    def test_base_negative_result_preserves_homogeneous_solution(self):
        basis=self.tower().solve([1/(1-X)])
        self.assertEqual(basis,[((0,),1)])

    def test_sum_extension_checks_no_primitive(self):
        t=self.tower(sums=[(H,1/(1-X))])
        self.assertEqual(t.records[0]['action'],'sigma_star_extension')
        self.assertEqual(t.records[0]['obstruction_basis'][0]['coefficients'],['0'])

    def test_nonlinear_single_sum_requires_degree_increase(self):
        t=self.tower(sums=[(H,1/(1-X))]);self.recovered(t,H**5)
        self.assertTrue(any(r.get('kind')=='sigma_degree' and r['upper']==5 for r in t.trace))

    def test_parameterized_coefficients_solved_jointly(self):
        t=self.tower(sums=[(H,1/(1-X))]);basis=t.solve([2*H/(1-X),1/(1-X)**2])
        self.assertEqual(basis,[((1,1),H**2),((0,0),1)])

    def test_sum_rhs_without_primitive_returns_only_constant(self):
        t=self.tower(sums=[(H,1/(1-X))])
        self.assertEqual(t.solve([H]),[((0,),1)])

    def test_two_genuine_nested_sum_extensions(self):
        t=self.tower(sums=[(H,1/(1-X)),(J,H/(1-2*X))])
        self.assertEqual([r['action'] for r in t.records],['sigma_star_extension']*2)
        self.recovered(t,J**2+H*J)

    def test_two_independent_sum_increments(self):
        t=self.tower(sums=[(H,1/(1-X)),(J,1/(1-2*X))])
        self.recovered(t,H*J+J**3)

    def test_three_nested_levels(self):
        t=self.tower(sums=[(H,1/(1-X)),(J,H/(1-2*X)),(K,J/(1-3*X))])
        self.assertEqual(len(t.sums),3);self.recovered(t,H+J+K)

    def test_redundant_base_sum_retains_integration_constant(self):
        out=compute(request([(H,'sum',X)],[H]),B)
        # H=X/(q-1)+C. The missing primitive of C must not be silently dropped.
        self.assertEqual(out['status'],'no_relation_in_declared_basis')
        self.assertEqual(out['tower'][0]['action'],'constant_reduction')
        self.assertIn('DRConstant0',out['tower'][0]['alias'])

    def test_redundant_nested_sum_retains_constant(self):
        out=self.checked_output([(H,'sum',1/(1-X)),(J,'sum',2*H/(1-X)+1/(1-X)**2)],
                                [2*H/(1-X)+1/(1-X)**2])
        self.assertEqual(out['tower'][1]['action'],'constant_reduction')
        self.assertEqual(s.cancel(rational_read(out['tower'][1]['primitive'])-H**2),0)

    def test_chain_of_redundant_sum_constants_restores_original_equation(self):
        out=self.checked_output([(H,'sum',X),(J,'sum',H-H+X),(K,'sum',J-H)], [K,1])
        self.assertGreaterEqual(len(out['result']['constant_field_extensions']),2)

    def test_zero_increment_is_constant_not_sigma_star(self):
        out=self.checked_output([(H,'sum',0)],[H,1])
        self.assertEqual(out['tower'][0]['action'],'constant_reduction')
        self.assertEqual(out['result']['certificate'],'0')

    def test_zero_rhs_full_solution_basis(self):
        t=self.tower(sums=[(H,1/(1-X))]);basis=t.solve([0,0])
        self.assertEqual(len(basis),3)
        self.assertIn(((0,0),s.Integer(1)),basis)

    def test_repeated_rhs_linear_dependency_is_not_lost(self):
        t=self.tower(sums=[(H,1/(1-X))]);basis=t.solve([H,H])
        self.assertEqual(len(basis),2)
        self.assertTrue(any(cs[0]!=0 and cs[0]+cs[1]==0 and g==0 for cs,g in basis))

    def test_q_pochhammer_product(self):
        t=self.tower(products=[(P,1-a*X)]);self.recovered(t,P/(1-X))

    def test_product_laurent_positive_and_negative_powers(self):
        t=self.tower(products=[(P,2)]);self.recovered(t,P**-3/(1-X)+P**4)

    def test_mixed_products_and_nested_sum(self):
        t=self.tower(products=[(P,1-X)],sums=[(H,P/(1-2*X))])
        self.assertEqual(t.records[-1]['action'],'sigma_star_extension')
        self.recovered(t,H**2+H/P)

    def test_product_weighted_harmonic_square(self):
        t=self.tower(products=[(P,2)],sums=[(H,1/(1-X))]);self.recovered(t,P*H**2)

    def test_multi_product_shared_parameter_space(self):
        t=self.tower(products=[(P,2),(R,3)])
        basis=t.solve([P+R,P+2*R]);self.assertEqual(len(basis),3)
        self.recovered(t,P/R+P*R)

    def test_product_primitive_makes_sum_redundant(self):
        out=self.checked_output([(P,'product',1-X),(H,'sum',-X*P)],[-X*P])
        self.assertEqual(out['tower'][-1]['action'],'constant_reduction')

    def test_product_orbit_dependency_and_witness(self):
        trace,dep=product_lattice([1-X,1-q**3*X],B)
        self.assertEqual(trace['rank'],1);self.assertEqual(dep['exponents'],[-1,1])
        g=rational_read(dep['rational_witness'])
        self.assertEqual(s.cancel(g.subs(X,q*X)/g-(1-q**3*X)/(1-X)),0)

    def test_product_reverse_orbit_and_nonlinear_factor(self):
        _,dep=product_lattice([1+q**4*X**2,1+X**2],B)
        g=rational_read(dep['rational_witness'])
        self.assertEqual(s.cancel(g.subs(X,q*X)/g-(1+X**2)/(1+q**4*X**2)),0)

    def test_product_multiplicities_and_constant_unit_combined(self):
        trace,dep=product_lattice([2*(1-X)**2,4*(1-q*X)**4],B)
        self.assertEqual(trace['rank'],1);self.assertEqual(dep['exponents'],[-2,1])

    def test_integer_and_parameter_units_independent(self):
        trace,dep=product_lattice([2,3,a,1-a,X],B)
        self.assertIsNone(dep);self.assertEqual(trace['rank'],5)

    def test_parameter_pochhammer_orbits_are_independent(self):
        trace,dep=product_lattice([1-X,1-a*X],B)
        self.assertIsNone(dep);self.assertEqual(trace['rank'],2)

    def test_product_constant_alias_for_q_power(self):
        out=self.checked_output([(P,'product',q**7)],[P])
        self.assertEqual(out['tower'][0]['action'],'constant_reduction')
        self.assertTrue(out['tower'][0]['constant_must_be_nonzero'])

    def test_product_rational_dependency_restored(self):
        out=self.checked_output([(P,'product',2),(R,'product',4)],[P+R])
        self.assertEqual(out['tower'][1]['action'],'constant_reduction')
        self.assertEqual(out['tower'][1]['dependency']['exponents'],[-2,1])

    def test_product_q_shift_alias_restored(self):
        self.checked_output([(P,'product',1-X),(R,'product',1-q*X)],[-X*P])

    def test_torsion_and_algebraic_product_dependency_are_explicit(self):
        for extensions in [[(P,'product',-1)],[(P,'product',4),(R,'product',2)]]:
            out=compute(request(extensions,[1]),B)
            self.assertEqual(out['status'],'unsupported_domain')
            self.assertEqual(out['tower'][-1]['action'],'algebraic_or_torsion_dependency')
            self.assertEqual(out['tower'][-1]['dependency']['residual'],'0')

    def test_constant_signature_ignores_only_sign_and_q_power(self):
        self.assertEqual(constant_signature(-q**17),{})
        self.assertEqual(constant_signature(4/((1-q)**2*a)),
                         {'rational_prime:2':2,'constant_factor:q - 1':-2,'constant_factor:a':-1})

    def test_sum_denominator_is_not_reported_as_no_solution(self):
        with self.assertRaises(UnsupportedDomain): compute(request([(H,'sum',1/(1-X))],[1/H]),B)

    def test_product_non_laurent_denominator_is_rejected(self):
        with self.assertRaises(UnsupportedDomain): compute(request([(P,'product',2)],[1/(1+P)]),B)

    def test_simplification_before_class_membership(self):
        req=request([(H,'sum',1/(1-X))],[2*H/(1-X)+1/(1-X)**2])
        req['input']['rhs_basis'][0]=['add',['div',['mul',2,['pow','H',3]],
            ['mul',['pow','H',2],['sub',1,'X']]],['pow',['sub',1,'X'],-2]]
        out=compute(req,B)
        self.assertEqual(out['status'],'constructed')

    def test_product_depending_on_sum_is_rejected(self):
        with self.assertRaises(UnsupportedDomain): compute(request([(H,'sum',1),(P,'product',H)],[P]),B)

    def test_forward_self_reference_and_duplicate_name_rejected(self):
        for exts in [[(H,'sum',J),(J,'sum',1)],[(H,'sum',H)],[(H,'sum',1),(H,'sum',2)]]:
            with self.assertRaises(ValueError): compute(request(exts,[1]),B)

    def test_reserved_names_and_extra_certificate_rejected(self):
        with self.assertRaises(ValueError): compute(request([(X,'sum',1)],[1]),B)
        req=request([], [X]);req['input']['certificate']=tree(X/(q-1))
        with self.assertRaises(ValueError): compute(req,B)

    def test_symbol_names_do_not_collide_with_sympy_builtins(self):
        I,S,E=s.symbols('I S E')
        self.checked_output([(I,'product',2),(S,'sum',1),(E,'sum',S)],[I+S+E])

    def test_fresh_constant_names_do_not_capture_parameters(self):
        C=s.Symbol('DRConstant0')
        out=self.checked_output([(H,'sum',X)],[H,C])
        self.assertEqual(out['tower'][0]['new_constant'],'DRConstant1')

    def test_three_certificate_tamperings_rejected(self):
        t=self.tower(sums=[(H,1/(1-X))]);rhs=[t.sigma(H**2)-H**2]
        for cs,g in [([1],H**2+X),([2],H**2),([X],H**2)]:
            with self.assertRaises(ValueError): verify_relation(t,rhs,cs,g)

    def test_derived_degree_and_product_support_resource_limits(self):
        t=self.tower(sums=[(H,1)],budget=CoreBudget(max_normal_form_degree=3))
        with self.assertRaises(OreResourceLimit): t.solve([H**4])
        t=self.tower(products=[(P,2)],budget=CoreBudget(max_states=2))
        with self.assertRaises(OreResourceLimit): t.solve([P+P**2])

    def test_large_product_orbit_guard_before_expansion(self):
        with self.assertRaises(OreResourceLimit):
            product_lattice([1-X,1-q**1000*X],CoreBudget(max_normal_form_degree=5))

    def test_public_timeout_and_metadata(self):
        req=request([(H,'sum',1)], [H**2])
        out=solve(req,CoreBudget(seconds=30))
        self.assertEqual(out['status'],'constructed');self.assertFalse(out['original_identity_proved'])
        self.assertEqual(out['benchmark_files_read'],0);self.assertIn('qdifference.py',out['source_sha256'])
        self.assertEqual(solve(req,CoreBudget(seconds=0.000001))['status'],'resource_exhausted')

    def test_public_failure_labels(self):
        for req,status in [(request([], [1/(1-X)]),'no_relation_in_declared_basis'),
                           (request([(H,'sum',1)],[1/H]),'unsupported_domain'),
                           (request([(P,'product',0)],[P]),'invalid_input')]:
            self.assertEqual(solve(req,B)['status'],status)


if __name__ == '__main__': unittest.main()
