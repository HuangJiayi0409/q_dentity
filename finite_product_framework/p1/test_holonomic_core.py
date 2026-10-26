"""Algorithmic bounds, coupled rational solve, and q-module telescoping.

All examples are synthetic. No benchmark files or Lean invocation.
"""
import unittest
import sympy as s
from core import CoreBudget,compute,solve
from expressions import q,Q,X
from qgosper import Budget,UnsupportedDomain
from ore import OreResourceLimit
from qrational_system import scalar_bounds,power_roots,solve_system,uncouple_coordinate
from qholonomic import search,validate_module,verify_relation,module_from_summands


def parse(value):return s.sympify(value,locals={'q':q,'Q':Q,'X':X,'a':s.Symbol('a')})


def req(solver,**data):return dict(schema_version=1,solver=solver,input=data)


class HolonomicCoreTests(unittest.TestCase):
    def contained(self,coefficients,y):
        rhs=s.cancel(sum(a*y.subs(X,q**j*X) for j,a in enumerate(coefficients)))
        D,lo,hi,trace=scalar_bounds(coefficients,[rhs],X,q)
        f=s.cancel(D*y);numerator,denominator=s.fraction(f)
        # A rational solution after multiplication by D can have poles only at 0.
        denominator=s.Poly(denominator,X)
        self.assertEqual(len(denominator.terms()),1)
        exponent=denominator.monoms()[0][0]
        polynomial=s.Poly(numerator,X)
        self.assertGreaterEqual(min(m[0] for m in polynomial.monoms())-exponent,lo)
        self.assertLessEqual(polynomial.degree()-exponent,hi)
        return trace

    def check_system(self,V,rhs,r):
        self.assertEqual(r['status'],'constructed')
        row=s.Matrix([list(map(parse,r['certificate_row']))])
        cs=list(map(parse,r['coefficients']))
        residual=row.subs(X,q*X)*V-row-sum((c*s.Matrix([h]) for c,h in zip(cs,rhs)),s.zeros(1,V.rows))
        self.assertEqual(residual.applyfunc(s.cancel),s.zeros(1,V.rows))
        for basis in r.get('solution_basis',[]):
            row=s.Matrix([list(map(parse,basis['certificate_row']))]);cs=list(map(parse,basis['coefficients']))
            check=row.subs(X,q*X)*V-row-sum((c*s.Matrix([h]) for c,h in zip(cs,rhs)),s.zeros(1,V.rows))
            self.assertEqual(check.applyfunc(s.cancel),s.zeros(1,V.rows))

    def check_telescoper(self,U,V,h,r):
        self.assertEqual(r['status'],'constructed')
        for relation in (r,r['primitive_relation']):
            cs=list(map(parse,relation['coefficients']));R=s.Matrix([list(map(parse,relation['certificate_row']))])
            row=s.Matrix([h]);total=s.zeros(1,U.rows)
            for c in cs:
                total+=c*row;row=(row.subs(Q,q*Q)*U).applyfunc(s.cancel)
            self.assertEqual((R.subs(X,q*X)*V-R-total).applyfunc(s.cancel),s.zeros(1,U.rows))

    def test_universal_denominator_orbit_direction(self):
        D=s.prod(1-q**j*X for j in range(5));y=1/D
        a=[-D,D.subs(X,q*X)]
        bound,lo,hi,trace=scalar_bounds(a,[0],X,q)
        self.assertEqual(trace['pole_radius'],4)
        self.assertEqual(trace['denominator_degree'],5)
        self.assertFalse(s.cancel(bound*y).has(X))
        self.assertEqual((lo,hi),(0,0))

    def test_pole_multiplicities_and_irreducible_factors(self):
        for D in ((1-X)**3*(1-q*X)**2,(1+X**2)*(1+q**2*X**2),
                  (1-X)*(1-2*X),(1-X)*(1-q**-2*X)):
            self.contained([-D,D.subs(X,q*X)],1/D)

    def test_higher_order_scalar_bounds_known_rational_solutions(self):
        cases=[([1,X,1+X],X**-3/(1-X)),([X-1,1,-X**2],(1+X**4)/(1+X**2)),
               ([1,0,X,1],1/((1-X)**2*(1-q*X))),([1+X,2,1],X**7+X**-4)]
        for coefficients,y in cases:self.contained(coefficients,y)

    def test_exact_large_positive_and_negative_resonances(self):
        for exponent in (23,-19):
            _,lo,hi,trace=scalar_bounds([-q**exponent,1],[0],X,q)
            self.assertEqual((lo,hi),(exponent,exponent))
            self.assertEqual(trace['low_resonances'],[exponent])
            self.assertEqual(trace['high_resonances'],[exponent])

    def test_indicial_roots_over_parameter_field(self):
        a,t=s.symbols('a t');field=s.QQ.frac_field(q,a)
        poly=(t-q**7)*(t-q**-4)*(t-a)*(t+q)*(t**2+1)
        self.assertEqual(power_roots(poly,t,q,field),[-4,7])

    def test_no_homogeneous_rational_solution_has_empty_interval(self):
        _,lo,hi,_=scalar_bounds([-2,1],[0],X,q)
        self.assertGreater(lo,hi)

    def test_denominator_limit_precedes_large_expansion(self):
        with self.assertRaises(OreResourceLimit):
            scalar_bounds([1-X,-(1-q**1000*X)],[0],X,q,Budget(max_normal_form_degree=5))

    def test_uncoupling_identity_including_forcing(self):
        A=s.Matrix([[0,1],[1+X,0]]);G=s.Matrix([[X,1],[1,X**2]])
        cs,rhs,trace=uncouple_coordinate(A,G,0,X,q)
        self.assertEqual(len(cs),3)
        rows=[s.Matrix([[1,0]])];forcing=[s.zeros(1,2)]
        for _ in range(2):
            forcing.append((forcing[-1].subs(X,q*X)+rows[-1].subs(X,q*X)*G).applyfunc(s.cancel))
            rows.append((rows[-1].subs(X,q*X)*A).applyfunc(s.cancel))
        self.assertEqual(sum((c*r for c,r in zip(cs,rows)),s.zeros(1,2)).applyfunc(s.cancel),s.zeros(1,2))
        self.assertEqual(sum((c*f for c,f in zip(cs,forcing)),s.zeros(1,2)).applyfunc(s.cancel),s.Matrix([rhs]))

    def test_genuinely_coupled_rational_certificate(self):
        V=s.Matrix([[0,1],[1+X,0]]);known=s.Matrix([[1/(1-X),X**2]])
        rhs=[list((known.subs(X,q*X)*V-known).applyfunc(s.cancel))]
        r=solve_system(V,rhs,X,q,include_basis=True);self.check_system(V,rhs,r)
        self.assertTrue(all(s.cancel(a-b)==0 for a,b in zip(map(parse,r['certificate_row']),known)))

    def test_triangular_coupling_and_negative_powers(self):
        V=s.Matrix([[1,X],[0,1]]);known=s.Matrix([[X**-2,1/(1-X)]])
        rhs=[list((known.subs(X,q*X)*V-known).applyfunc(s.cancel))]
        r=solve_system(V,rhs,X,q,include_basis=True);self.check_system(V,rhs,r)
        self.assertLess(r['coordinate_bounds'][0]['lower'],0)

    def test_rank_three_cyclic_coupling(self):
        V=s.Matrix([[0,1,0],[0,0,1],[1+X,0,0]])
        known=s.Matrix([[1,X,X**2]])
        rhs=[list((known.subs(X,q*X)*V-known).applyfunc(s.cancel))]
        r=solve_system(V,rhs,X,q,include_basis=True);self.check_system(V,rhs,r)
        self.assertTrue(all(t['uncoupling']['order']==3 for t in r['coordinate_bounds']))

    def test_complete_solution_basis_includes_homogeneous_vectors(self):
        V=s.eye(2);rhs=[[0,0]]
        r=solve_system(V,rhs,X,q,include_basis=True);self.check_system(V,rhs,r)
        vectors=[list(map(parse,v['coefficients']+v['certificate_row'])) for v in r['solution_basis']]
        self.assertEqual(len(vectors),3);self.assertEqual(s.Matrix(vectors).rank(),3)

    def test_shared_parameters_across_coupled_coordinates(self):
        V=s.eye(2);rhs=[[1,0],[0,1],[X,X]]
        r=solve_system(V,rhs,X,q,include_basis=True);self.check_system(V,rhs,r)
        self.assertEqual(r['coefficients'],['0','0','1'])
        self.assertEqual(solve_system(V,rhs,X,q,normalize_index=0)['status'],'no_relation_in_declared_basis')

    def test_unsummable_rhs_keeps_homogeneous_basis(self):
        r=solve_system(s.eye(1),[[1]],X,q,include_basis=True)
        self.assertEqual(r['status'],'no_relation_in_declared_basis')
        self.assertEqual(r['solution_basis'],[dict(coefficients=['0'],certificate_row=['1'],residual='0')])

    def test_non_diagonal_module_creative_telescoping(self):
        U=s.Matrix([[0,1],[1+Q*X,0]])
        r=search(U,U,[1,0],CoreBudget(),max_order=1);self.check_telescoper(U,U,[1,0],r)
        self.assertEqual(r['primitive_relation']['coefficients'],['-1','1'])
        self.assertEqual(r['certificate_row'],['1','0'])
        self.assertEqual(r['attempts'][0]['status'],'no_relation_in_declared_basis')

    def test_rational_gauge_of_coupled_module(self):
        A=s.Matrix([[0,1],[1+Q*X,0]]);P=s.diag(1-X,1)
        U=(P*A*P.inv()).applyfunc(s.cancel);V=(P.subs(X,q*X)*A*P.inv()).applyfunc(s.cancel)
        h=[1/(1-X),0]
        r=search(U,V,h,CoreBudget(),max_order=1);self.check_telescoper(U,V,h,r)
        self.assertTrue(parse(r['certificate_row'][0]).has(X))
        self.assertGreater(r['attempts'][-1]['coordinate_bounds'][0]['denominator_degree'],0)

    def test_primitive_scaling_keeps_nonconstant_leading_polynomial(self):
        a=s.Symbol('a');U=s.Matrix([[X]]);V=s.Matrix([[Q*(1-a*X**2)]])
        r=search(U,V,[1],CoreBudget(),max_order=2);self.check_telescoper(U,V,[1],r)
        self.assertEqual(r['primitive_relation']['coefficients'],['1 - Q','0','Q*a'])
        self.assertEqual(r['primitive_relation']['certificate_row'],['-1'])

    def test_zero_observable(self):
        U=s.Matrix([[0,1],[1+Q*X,0]])
        r=search(U,U,[0,0],CoreBudget(),max_order=0);self.check_telescoper(U,U,[0,0],r)
        self.assertEqual(r['coefficients'],['1'])

    def test_bounded_order_failure_is_not_impossibility(self):
        U=s.Matrix([[0,1],[1+Q*X,0]])
        r=search(U,U,[1,0],CoreBudget(),max_order=0)
        self.assertEqual(r['status'],'search_exhausted')
        self.assertNotIn('certificate_row',r)

    def test_invalid_shift_matrices_and_domains(self):
        with self.assertRaisesRegex(ValueError,'incompatible'):
            validate_module(s.Matrix([[Q,1],[0,1]]),s.Matrix([[1,X],[0,1]]),[1,0])
        with self.assertRaisesRegex(ValueError,'invertible'):
            validate_module(s.eye(2),s.zeros(2),[1,0])
        with self.assertRaises(UnsupportedDomain):solve_system([[s.sqrt(2)]],[[1]],X,q)
        with self.assertRaises(ValueError):solve_system([[1,0],[0,1]],[[1]],X,q)

    def test_three_tampered_certificates_are_rejected(self):
        U=s.Matrix([[0,1],[1+Q*X,0]]);h=s.Matrix([[1,0]])
        verify_relation(U,U,h,[-1,1],[1,0])
        for cs,R in [([-1,1],[2,0]),([1,1],[1,0]),([0,0],[0,0])]:
            with self.assertRaisesRegex(ValueError,'invalid_certificate'):verify_relation(U,U,h,cs,R)

    def test_source_frontend_merges_exact_dependence(self):
        nodes=[['pow',2,'n'],['mul',-1,['pow',2,'n']]]
        r=compute(req('q_holonomic',summands=nodes),CoreBudget(max_order=0))
        self.assertEqual(r['status'],'constructed');self.assertEqual(r['operator']['coefficients'],['1'])
        self.assertEqual(r['source_frontend']['group_members'],[[0,1]])
        self.assertFalse(r['domain']['input_module_equations_are_premises'])

    def test_source_frontend_rational_weights_and_unrelated_terms(self):
        nodes=[['pow',2,'n'],['mul',['pow','q','n'],['pow',2,'n']],['pow',3,'n']]
        U,V,h,front=module_from_summands(nodes,CoreBudget())
        self.assertEqual(h,s.Matrix([[Q+1,1]]));self.assertEqual(U,s.diag(2,3))
        self.assertEqual(front['group_members'],[[0,1],[2]])
        r=search(U,V,list(h),CoreBudget(),max_order=3);self.check_telescoper(U,V,list(h),r)

    def test_public_parameter_system_and_source_zero(self):
        r=solve(req('parameterized_q_system',k_matrix=[[1]],rhs_basis=[['X']]))
        self.assertEqual(r['status'],'constructed');self.assertIn('solution_basis',r['result'])
        self.assertIn('qrational_system.py',r['source_sha256']);self.assertIn('qholonomic.py',r['source_sha256'])
        self.assertFalse(r['original_identity_proved']);self.assertEqual(r['benchmark_files_read'],0)
        r=compute(req('q_holonomic',summands=[0,0]),CoreBudget())
        self.assertEqual(r['operator']['order'],0)

    def test_public_resource_and_input_classification(self):
        r=solve(req('parameterized_q_system',k_matrix=[[1]],rhs_basis=[['X']]),CoreBudget(max_unknowns=1))
        self.assertEqual(r['status'],'resource_exhausted')
        r=solve(req('q_holonomic',n_matrix=[[1]],k_matrix=[[0]],observable=[1]))
        self.assertEqual(r['status'],'unsupported_input')
        for data in [dict(n_matrix=[[1]],k_matrix=[[1]],observable=[1],certificate=[1]),
                     dict(k_matrix=[[1,0],[1]],rhs_basis=[[1]]),dict(k_matrix=[[0.5]],rhs_basis=[[1]])]:
            solver='q_holonomic' if 'n_matrix' in data else 'parameterized_q_system'
            self.assertEqual(solve(req(solver,**data))['status'],'invalid_input')


if __name__=='__main__':unittest.main()
