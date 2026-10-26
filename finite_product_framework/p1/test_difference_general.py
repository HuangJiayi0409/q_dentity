"""Higher-order and algebraic coefficient tests; no benchmark inputs."""
import json
from pathlib import Path
import unittest
import sympy as s
from core import CoreBudget,compute,rational_input
from qpisigma import PiSigma
from qplde import solve,apply,candidates,specialized_kernel
from qnumberfield import NumberFieldTower,s_unit_coordinates,fixed_constant_solve
from qpisigma_system import solve as system_solve
from qfinite import FiniteAlgebra
from qdifference import rational_read
from expressions import X,q
from test_difference_core import tree
from test_difference_completion import system_request
from test_difference_full import finite_request
from ore import OreResourceLimit

H,J,P,R,Z,C=s.symbols('H J P R Z C')
B=CoreBudget(seconds=120)


class GeneralTests(unittest.TestCase):
    def tower(self,exts):
        tower=PiSigma(B)
        for t,k,v in exts:self.assertTrue(tower.add(t,k,s.sympify(v)))
        return tower

    def equation(self,exts,operator,g,extra=()):
        tower=self.tower(exts);rhs=[apply(tower,operator,g,len(tower.nodes)),*map(s.sympify,extra)]
        basis=solve(tower,operator,rhs)
        self.assertTrue(any(cs[0]!=0 for cs,h in basis),basis)
        for cs,h in basis:
            self.assertEqual(apply(tower,operator,h,len(tower.nodes)),tower.normal(sum(c*f for c,f in zip(cs,rhs))))
            self.assertTrue(all(tower.sigma(c)==c for c in cs))
        # Check that the known input-independent solution belongs to the entire
        # returned space, not merely that some unrelated RHS relation exists.
        rows=[[*cs,h] for cs,h in basis]+[[s.Integer(1),*[s.Integer(0)]*len(extra),g]]
        from qpisigma_system import constant_nullspace
        relations=constant_nullspace(rows,[t for t,k,v in tower.nodes],len(rhs)+1,tower)
        self.assertTrue(any(v[-1]!=0 for v in relations),(g,basis))
        return tower,basis

    def test_second_difference_full_homogeneous_basis(self):
        t,b=self.equation([(H,'sum',1)],[1,-2,1],H**4)
        self.assertEqual(len(b),3)

    def test_high_degree_is_derived(self):
        t,b=self.equation([(H,'sum',1)],[1,-2,1],H**19)
        self.assertGreaterEqual(max(v.get('upper',0) for v in t.trace),19)

    def test_third_order_homogeneous_dimension(self):
        t,b=self.equation([(H,'sum',1)],[-1,3,-3,1],H**5)
        self.assertEqual(len(b),4)

    def test_variable_leading_sigma_operator(self):
        self.equation([(H,'sum',1)],[H,-2*H-1,H+1],H**2)

    def test_sigma_ordinary_poles(self):
        self.equation([(H,'sum',1)],[H+2,-H,1],1/(H*(H+4)))

    def test_nested_sigma(self):
        self.equation([(H,'sum',1),(J,'sum',1/H)],[1,-2,1],J**2)

    def test_pi_laurent_resonances(self):
        self.equation([(H,'sum',1),(P,'product',H)],[1,-2,1],P+1/P)

    def test_pi_ordinary_poles(self):
        self.equation([(H,'sum',1),(P,'product',H)],[H,1,P],(H+P)/(P+1))

    def test_nonconstant_pi_leading_multiplier(self):
        self.equation([(H,'sum',1),(P,'product',H)],[H*(H+1),-(2*H+1),1],P)

    def test_q_base_order_four(self):
        self.equation([],[1,2,-1,0,1],X**-3/(X-1))

    def test_zero_endpoint_shift(self):
        self.equation([(H,'sum',1)],[0,0,1,-2,1],1/H+H**3)

    def test_order_zero(self):
        self.equation([(H,'sum',1)],[H+X],1/(H+1))

    def test_rhs_shared_parameters(self):
        t,b=self.equation([(H,'sum',1)],[1,-2,1],H**4,[H**2,1/H])
        self.assertTrue(all(cs[2]==0 for cs,g in b))

    def test_proved_no_relation(self):
        t=self.tower([(H,'sum',1)])
        result=solve(t,[1,-2,1],[1/H])
        self.assertTrue(result)
        self.assertTrue(all(cs==(0,) for cs,g in result))
        self.assertEqual(len(result),2)

    def test_coupled_previous_failure(self):
        req=json.loads(Path(__file__).with_name('examples').joinpath('core_difference_completion_remaining_coupled.json').read_text())
        result=compute(req,B)
        self.assertEqual(result['status'],'constructed')
        self.assertEqual(result['result']['certificate_row'],['1/H','X/(H + 1)'])

    def test_coupled_pi_block(self):
        t=self.tower([(H,'sum',1),(P,'product',H)])
        V=s.Matrix([[P,1],[1,H+1]]);g=s.Matrix([[1/P,P]])
        rhs=list((g.applyfunc(t.sigma)*V-g).applyfunc(t.normal))
        pairs,trace=system_solve(t,V,[rhs])
        self.assertTrue(any(cs[0]!=0 for cs,h in pairs))
        for cs,h in pairs:self.assertEqual((h.applyfunc(t.sigma)*V-h-cs[0]*s.Matrix([rhs])).applyfunc(t.normal),s.zeros(1,2))

    def test_degree_specialization_exception(self):
        t=self.tower([]);d=s.Symbol('d')
        basis,exceptions=specialized_kernel(t,s.Matrix([[d-37,1],[0,d-37]]),d)
        self.assertEqual(basis,[]);self.assertEqual(exceptions,[37])

    def test_degree_specialization_retains_kernel(self):
        t=self.tower([]);d=s.Symbol('d');M=s.Matrix([[d-9,1,0]])
        basis,exceptions=specialized_kernel(t,M,d)
        self.assertIn(9,exceptions);self.assertEqual(len(basis),2)
        self.assertTrue(all(M*v==s.zeros(1,1) for v in basis))

    def test_hypergeometric_candidates_quotient_class(self):
        t=self.tower([(H,'sum',1)])
        ratios=candidates(t,[-H,1],len(t.nodes))
        self.assertTrue(any(t.hyper(H/r,len(t.nodes)) is not None for r in ratios))

    def test_number_field_units_norm_one_not_torsion(self):
        t=NumberFieldTower(B,s.Poly(Z**2-2,Z));z=t.root
        M=s_unit_coordinates(t,[1+z,3+2*z,1-z,2])
        self.assertNotEqual(M[:,0],s.zeros(M.rows,1))
        self.assertEqual(M[:,1],2*M[:,0]);self.assertEqual(M[:,2],-M[:,0])

    def test_number_field_split_primes(self):
        t=NumberFieldTower(B,s.Poly(Z**2+1,Z));z=t.root
        M=s_unit_coordinates(t,[(2+z)/(2-z),5])
        self.assertEqual(M.rank(),2)

    def test_number_field_torsion_removed_only_in_signature(self):
        t=NumberFieldTower(B,s.Poly(Z**2+Z+1,Z));z=t.root
        self.assertFalse(any(t.signature([z],0)));self.assertIsNone(t.hyper(z,0))

    def test_number_field_polynomial_factorization(self):
        t=NumberFieldTower(B,s.Poly(Z**2+Z+1,Z))
        self.assertEqual(len(t.poly(H**2+H+1,H).factor_list()[1]),2)

    def test_algebraic_pi_previous_failure(self):
        req=json.loads(Path(__file__).with_name('examples').joinpath('core_difference_completion_remaining_algebraic_product.json').read_text())
        result=compute(req,B);self.assertEqual(result['status'],'constructed')
        self.assertEqual(result['result']['certificate'],'1/P')

    def native(self,exts,poly,g,A=1,D=-1):
        algebra=FiniteAlgebra([(Z,poly,Z)],{X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in exts}},B)
        rhs=algebra.normal(A*algebra.sigma(g)+D*g)
        answer,trace=fixed_constant_solve(algebra,exts,[rhs],B,s.sympify(A),s.sympify(D))
        self.assertTrue(any(cs[0]!=0 for cs,h in answer))
        for cs,h in answer:
            self.assertEqual(algebra.normal(A*algebra.sigma(h)+D*h-cs[0]*rhs),0)
            self.assertEqual(algebra.normal(algebra.sigma(cs[0])-cs[0]),0)
        return answer

    def test_algebraic_sigma_with_following_pi(self):
        self.native([(H,'sum',Z/(1-X)+1/(1-2*X)),(P,'product',H+Z)],Z**2+Z+1,H/P)

    def test_algebraic_pi_denominator(self):
        self.native([(H,'sum',1),(P,'product',H+Z)],Z**2+Z+1,1/(P+Z))

    def test_algebraic_nested_sigma_after_pi(self):
        self.native([(H,'sum',1),(P,'product',H+Z),(J,'sum',1/P)],Z**2+Z+1,J/P)

    def test_algebraic_redundant_sum_keeps_constant(self):
        pairs=self.native([(H,'sum',1),(J,'sum',Z)],Z**2-2,H*(J-Z*H))
        self.assertTrue(pairs)

    def test_algebraic_product_unit(self):
        self.native([(P,'product',1+Z)],Z**2-2,P+1/P)

    def test_algebraic_crt_components(self):
        self.native([(H,'sum',1),(P,'product',H+Z)],(Z**2+1)*(Z**2-2),1/P)

    def test_number_field_high_order(self):
        t=NumberFieldTower(B,s.Poly(Z**2-2,Z));z=t.root
        t.add(H,'sum',s.Integer(1));t.add(P,'product',H+z)
        a=[H+z,1,P];g=(P+z)/(H+z);f=apply(t,a,g,len(t.nodes))
        pairs=solve(t,a,[f]);self.assertTrue(any(cs[0]!=0 for cs,h in pairs))

    def test_number_field_coupled(self):
        t=NumberFieldTower(B,s.Poly(Z**2-2,Z));z=t.root;t.add(H,'sum',s.Integer(1))
        V=s.Matrix([[H+z,1],[1,H+1]]);g=s.Matrix([[1/(H+z),X]])
        f=list((g.applyfunc(t.sigma)*V-g).applyfunc(t.normal))
        pairs,trace=system_solve(t,V,[f]);self.assertTrue(any(cs[0]!=0 for cs,h in pairs))

    def test_public_higher_order(self):
        req=dict(schema_version=1,solver='difference_equation',input=dict(
            extensions=[dict(name='H',kind='sum',increment=1)],operator=[1,-2,1],rhs_basis=[tree(12*H**2+24*H+14)]))
        result=compute(req,B);self.assertEqual(result['status'],'constructed');self.assertEqual(len(result['result']['solution_basis']),3)

    def test_no_guessed_degree_input(self):
        req=dict(schema_version=1,solver='difference_equation',input=dict(extensions=[],operator=[1,-2,1],rhs_basis=[0],degree=10))
        with self.assertRaises(ValueError):compute(req,B)

    def test_no_certificate_input(self):
        req=dict(schema_version=1,solver='difference_equation',input=dict(extensions=[],operator=[1,-2,1],rhs_basis=[0],certificate=1))
        with self.assertRaises(ValueError):compute(req,B)

    def test_degree_resource_limit_is_not_no_relation(self):
        t=self.tower([(H,'sum',1)]);t.budget=CoreBudget(max_normal_form_degree=2)
        with self.assertRaises(OreResourceLimit):solve(t,[1,-2,1],[H**20])

    def finite_case(self,exts,relations,g):
        algebra=FiniteAlgebra(relations,{X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in exts}},B)
        f=algebra.normal(algebra.sigma(g)-g);result=compute(finite_request(exts,relations,[f]),B)
        self.assertEqual(result['status'],'constructed')
        for row in result['result']['solution_basis']:
            c=rational_read(row['coefficients'][0]);h=rational_read(row['certificate'])
            self.assertEqual(algebra.normal(algebra.sigma(h)-h-c*f),0)
            self.assertEqual(algebra.normal(algebra.sigma(c)-c),0)
        return result

    def test_number_field_periodic_product(self):
        r=self.finite_case([(H,'sum',1),(P,'product',Z)],[(Z,Z**2+Z+1,Z)],H/P)
        self.assertTrue(any('P' in row['coefficients'][0] for row in r['result']['solution_basis']))

    def test_number_field_conjugation(self):
        self.finite_case([(H,'sum',1),(P,'product',H+Z)],[(Z,Z**2-2,-Z)],1/P)

    def test_number_field_periodic_sum_constant(self):
        self.finite_case([(P,'product',Z),(H,'sum',P)],[(Z,Z**2+Z+1,Z)],H/P)

    def test_constant_parameter_elimination(self):
        self.finite_case([(H,'sum',1),(P,'product',H+Z)],[(Z,Z**2-C,Z)],1/P)

    def test_algebraic_base_q_normalization(self):
        self.finite_case([(P,'product',Z)],[(Z,Z**2-q,Z)],X/P)

    def test_crt_with_rational_component(self):
        self.native([(H,'sum',1),(P,'product',H+Z)],(Z-1)*(Z**2+1),1/P)

    def test_multiple_algebraic_generators(self):
        self.finite_case([(H,'sum',1),(P,'product',H+Z+R)],[(Z,Z**2-2,Z),(R,R**2-3,R)],1/P)

    def test_public_algebraic_higher_order(self):
        req=finite_request([(H,'sum',1)],[(Z,Z**2-2,Z)],[2*Z]);req['solver']='difference_equation';req['input']['operator']=[1,-2,1]
        out=compute(req,B);self.assertEqual(out['status'],'constructed')
        self.assertEqual(len(out['result']['solution_basis']),3)

    def test_public_algebraic_matrix(self):
        V=s.Matrix([[H+Z,1],[1,H+1]]);g=s.Matrix([[1/(H+Z),X]])
        F=FiniteAlgebra([(Z,Z**2-2,Z)],{X:q*X,H:H+1},B)
        f=(g.applyfunc(F.sigma)*V-g).applyfunc(F.normal)
        req=system_request([(H,'sum',1)],V,[list(f)])
        req['input']['algebraic_extensions']=finite_request([],[(Z,Z**2-2,Z)],[0])['input']['algebraic_extensions']
        out=compute(req,B);self.assertEqual(out['status'],'constructed')
        for row in out['result']['solution_basis']:
            c=rational_read(row['coefficients'][0]);h=s.Matrix([list(map(rational_read,row['certificate_row']))])
            self.assertEqual((h.applyfunc(F.sigma)*V-h-c*f).applyfunc(F.normal),s.zeros(1,2))

    def test_zero_operator_on_component_is_not_no_relation(self):
        from qgosper import UnsupportedDomain
        req=finite_request([(H,'sum',1)],[(Z,(Z-1)*(Z**2+1),Z)],[1]);req['solver']='difference_equation'
        req['input']['operator']=[tree(Z-1),tree(1-Z),tree(Z-1)]
        with self.assertRaisesRegex(UnsupportedDomain,'vanishes on a finite component'):compute(req,B)

    def test_order_zero_algebraic_operator(self):
        req=finite_request([],[(Z,Z**2-2,Z)],[X]);req['solver']='difference_equation';req['input']['operator']=[tree(Z+X)]
        out=compute(req,B);self.assertEqual(out['status'],'constructed')

    def test_sigma_exceptional_homogeneous_degree(self):
        self.equation([(H,'sum',1)],[H+1,-2*H+6,H-7],s.prod(H-j for j in range(9)))

    def test_repeated_ordinary_poles(self):
        self.equation([(H,'sum',1)],[1,1,1],1/H**3)

    def test_interleaved_radical_product_normalization(self):
        from test_difference_full import field_request
        exts=[(P,'product',4),(H,'sum',1),(R,'product',2*(H+1)/H)]
        out=compute(field_request(exts,[-H/(2*R)]),B)
        self.assertEqual(out['status'],'constructed')
        self.assertTrue(any(row['action']=='primitive_radical_product_normalization' for row in out['tower']))
        self.assertIn(str(R**2/(H**2*P)),out['result']['constant_definitions'].values())

    def test_interleaved_radical_constant_preserved_in_rhs(self):
        from test_difference_full import field_request
        exts=[(P,'product',8),(H,'sum',1),(R,'product',2*(H+1)/H)]
        invariant=R**3/(H**3*P);g=invariant*H/R
        shift={P:8*P,H:H+1,R:2*(H+1)/H*R,X:q*X}
        f=s.cancel(g.xreplace(shift)-g);out=compute(field_request(exts,[f]),B)
        self.assertEqual(out['status'],'constructed')
        for row in out['result']['solution_basis']:
            c=rational_read(row['original_coefficients'][0]);h=rational_read(row['original_certificate'])
            self.assertEqual(s.cancel(h.xreplace(shift)-h-c*f),0)

    def test_radical_relation_with_dependent_sum_rebuild(self):
        from test_difference_full import field_request
        exts=[(P,'product',4),(H,'sum',P),(R,'product',2*(H+P)/H)]
        shift={P:4*P,H:H+P,R:2*(H+P)/H*R,X:q*X};g=H/R
        f=s.cancel(g.xreplace(shift)-g);out=compute(field_request(exts,[f]),B)
        self.assertEqual(out['status'],'constructed')
        for row in out['result']['solution_basis']:
            c=rational_read(row['original_coefficients'][0]);h=rational_read(row['original_certificate'])
            self.assertEqual(s.cancel(h.xreplace(shift)-h-c*f),0)

    def test_algebraic_unit_radical_normalization(self):
        self.finite_case([(P,'product',3+2*Z),(H,'sum',1),(R,'product',(1+Z)*(H+1)/H)],[(Z,Z**2-2,Z)],H/R)

    def test_periodic_high_order_descent_keeps_parameter(self):
        req=json.loads(Path(__file__).with_name('examples').joinpath('core_difference_general_periodic_high_order.json').read_text())
        out=compute(req,B);self.assertEqual(out['status'],'constructed')
        self.assertTrue(any(rational_read(row['coefficients'][0])!=0 for row in out['result']['solution_basis']))
        from check_difference_general import replay
        replay(req,out)

    def test_conjugate_high_order_descent(self):
        req=json.loads(Path(__file__).with_name('examples').joinpath('core_difference_general_conjugate_high_order.json').read_text())
        out=compute(req,B);self.assertEqual(out['status'],'constructed')
        from check_difference_general import replay
        replay(req,out)

    def test_periodic_coupled_system(self):
        V=s.Matrix([[H,1],[1,H+1]]);g=s.Matrix([[P,H*P]]);shift={X:q*X,P:-P,H:H+1}
        f=(g.applyfunc(lambda v:v.xreplace(shift))*V-g).applyfunc(s.cancel)
        req=system_request([(P,'product',-1),(H,'sum',1)],V,[list(f)])
        out=compute(req,B);self.assertEqual(out['status'],'constructed')
        from check_difference_general import replay
        replay(req,out)

    def test_periodic_high_order_root_three(self):
        F=FiniteAlgebra([(Z,Z**2+Z+1,Z)],{X:q*X,P:Z*P,H:H+1},B);g=H/P
        f=F.normal(F.sigma(F.sigma(g))-2*F.sigma(g)+g)
        req=finite_request([(P,'product',Z),(H,'sum',1)],[(Z,Z**2+Z+1,Z)],[f]);req['solver']='difference_equation';req['input']['operator']=[1,-2,1]
        out=compute(req,B);self.assertEqual(out['status'],'constructed')
        from check_difference_general import replay
        replay(req,out)

    def test_crt_outputs_only_original_symbols(self):
        from check_difference_general import replay
        req=json.loads(Path(__file__).with_name('examples').joinpath('core_difference_general_algebraic_crt.json').read_text())
        out=compute(req,B);self.assertEqual(out['status'],'constructed');replay(req,out)
        for row in out['result']['solution_basis']:
            for value in [*row['coefficients'],row['certificate']]:self.assertFalse(rational_read(value).free_symbols-{Z,P,H,X,q})
        self.assertTrue(all(row['unit_coefficient_indices']==[] for row in out['result']['solution_basis']))

    def test_parameter_constant_matrix(self):
        V=s.Matrix([[H+Z,1],[1,H+1]]);F=FiniteAlgebra([(Z,Z**2-C,Z)],{X:q*X,H:H+1},B);g=s.Matrix([[1/(H+Z),X]])
        f=(g.applyfunc(F.sigma)*V-g).applyfunc(F.normal);req=system_request([(H,'sum',1)],V,[list(f)])
        req['input']['algebraic_extensions']=finite_request([],[(Z,Z**2-C,Z)],[0])['input']['algebraic_extensions']
        out=compute(req,B);self.assertEqual(out['status'],'constructed')
        from check_difference_general import replay
        replay(req,out)

    def test_parameter_conjugate_product(self):
        self.finite_case([(H,'sum',1),(P,'product',H+Z)],[(Z,Z**2-C,-Z)],1/P)


if __name__=='__main__':unittest.main()
