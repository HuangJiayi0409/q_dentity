"""Algorithm-only regression: no Train/Test files and no Lean compilation."""
import json
import multiprocessing as mp
from pathlib import Path
import time
import unittest
import sympy as s

from core import CoreBudget, compute, solve, rational_input
from expressions import q, Q, X
from qgosper import Budget, antidifference
from qparameterized import solve as parameterized, primitive_relation
from zeilberger import search


def request(solver, **inputs):
    return dict(schema_version=1, solver=solver, input=inputs)


class CoreSolverTests(unittest.TestCase):
    def assert_relation(self, U, V, result):
        symbols = {str(t):t for t in U.free_symbols | V.free_symbols | {q,Q,X}}
        parse = lambda text: s.sympify(text, locals=symbols)
        vs = [s.Integer(1)]
        for j in range(result['order']):
            vs.append(s.cancel(vs[-1]*U.subs(Q,q**j*Q)))
        for relation in (result, result['primitive_relation']):
            R = parse(relation['certificate'])
            coefficients = list(map(parse, relation['coefficients']))
            self.assertTrue(any(c != 0 for c in coefficients))
            self.assertEqual(s.cancel(V*R.subs(X,q*X)-R-sum(c*v for c,v in zip(coefficients,vs))),0)
        for c in result['primitive_relation']['coefficients']:
            self.assertEqual(s.fraction(parse(c))[1],1)

    def test_order_zero_is_computed(self):
        result = search(X,Q,max_order=0,min_order=0)
        self.assertEqual(result['order'],0)
        self.assert_relation(X,Q,result)

    def test_general_parameter_q_binomial_relation(self):
        z=s.Symbol('z')
        U=X*(1-q*Q)/(X-q*Q)
        V=z*(X-Q)/(1-q*X)
        result=search(U,V,max_order=1,min_order=0)
        self.assertEqual(result['order'],1)
        self.assertEqual(s.sympify(result['coefficients'][0],locals={'Q':Q,'q':q,'z':z}),-1-Q*z)
        self.assert_relation(U,V,result)

    def test_order_three_and_budget_distinction(self):
        U=X*(1-q*Q)/(X-q*Q)
        V=X**2*(X-Q)/(1-q*X)
        result=search(U,V,max_order=3,min_order=0)
        self.assertEqual(result['order'],3)
        self.assert_relation(U,V,result)
        limited=search(U,V,max_order=1,min_order=0)
        self.assertEqual(limited['status'],'search_exhausted')
        self.assertNotIn('certificate',limited)

    def test_legacy_order_two_contract(self):
        U=X*(1-q*Q)/(X-q*Q)
        V=-(1-Q/X)/(1-q*X)
        result=search(U,V,max_order=2)
        self.assertEqual(result['order'],2)
        self.assertEqual(result['coefficients'],['Q*q - 1','0','1'])
        self.assert_relation(U,V,result)

    def test_order_five_without_fixed_order_four_limit(self):
        a=s.Symbol('a')
        U,V=X,Q*(1-a*X**5)
        result=search(U,V,max_order=None,min_order=0)
        self.assertEqual(result['order'],5)
        self.assertEqual(result['primitive_relation']['coefficients'],
                         ['1 - Q','0','0','0','0','Q*a'])
        self.assert_relation(U,V,result)

    def test_incompatible_shifts_are_rejected(self):
        with self.assertRaisesRegex(ValueError,'incompatible'):
            search(Q,Q,max_order=1)

    def test_zero_shift_not_a_valid_summand(self):
        with self.assertRaisesRegex(ValueError,'nonzero'):
            search(s.Integer(0),q)

    def test_parameterized_system_constructs_a_combination(self):
        # Delta(X)=(q-1)X; 1 and 1+X only become summable after cancellation.
        result=parameterized(s.Integer(1),[s.Integer(1),1+X],X,q)
        self.assertEqual(result['status'],'constructed')
        c=list(map(s.sympify,result['coefficients']));R=s.sympify(result['certificate'],locals={'q':q,'X':X})
        self.assertEqual(s.cancel(R.subs(X,q*X)-R-c[0]-c[1]*(1+X)),0)
        self.assertEqual(s.cancel(c[0]+c[1]),0)
        self.assertNotEqual(c[1],0)

    def test_parameterized_rational_denominator(self):
        a=s.Symbol('a');primitive=1/(1-a*X)
        rhs=s.cancel(primitive.subs(X,q*X)-primitive)
        result=parameterized(s.Integer(1),[rhs],X,q)
        self.assertEqual(result['status'],'constructed')
        R=s.sympify(result['certificate'],locals={'q':q,'X':X,'a':a})
        self.assertEqual(s.cancel(R.subs(X,q*X)-R-rhs),0)

    def test_parameterized_zero_rhs_and_pure_homogeneous_solution(self):
        result=parameterized(s.Integer(1),[s.Integer(0)],X,q)
        self.assertEqual(result['coefficients'],['1'])
        self.assertEqual(result['certificate'],'0')
        result=parameterized(s.Integer(1),[s.Integer(1)],X,q)
        self.assertEqual(result['status'],'no_relation_in_joint_system')

    def test_primitive_normalization_preserves_singular_leading_factor(self):
        result=primitive_relation([1/(Q-1),s.Integer(1)],1/(X-1),[q,Q])
        self.assertEqual(result['coefficients'],['1','Q - 1'])
        self.assertEqual(result['leading_coefficient'],'Q - 1')
        R=s.sympify(result['certificate'],locals={'Q':Q,'X':X})
        self.assertEqual(s.cancel(R-(Q-1)/(X-1)),0)

    def test_large_derived_normal_form_stops_before_expansion(self):
        a=s.Symbol('a')
        result=antidifference((1-a*q**1000*X)/(1-a*X),X,q,
                             Budget(max_normal_form_degree=10))
        self.assertEqual(result['status'],'resource_exhausted')
        self.assertIn('normal-form degree',result['reason'])

    def test_laurent_primitive_and_generic_no_solution(self):
        for primitive in [X**(-9),X**11,1/(1-X)**2]:
            term=s.cancel(primitive.subs(X,q*X)-primitive)
            result=antidifference(s.cancel(term/term.subs(X,X/q)),X,q)
            self.assertEqual(result['status'],'constructed')
            G=result['antidifference_ratio']*term
            self.assertEqual(s.cancel(G.subs(X,q*X)-G-term),0)
        result=compute(request('q_gosper',k_shift=1),CoreBudget())
        self.assertEqual(result['status'],'no_solution_in_class')
        self.assertIn('specified rational shift field',result['domain']['negative_result_scope'])

    def test_source_ir_without_target_or_membership(self):
        result=solve(request('q_gosper',summand=['mul',['pow','q','k'],
             ['div',['poch','a','q','k'],['poch','q','q','k']]]),CoreBudget(seconds=20))
        self.assertEqual(result['status'],'constructed',result)
        self.assertFalse(result['original_identity_proved'])
        self.assertEqual(result['benchmark_files_read'],0)
        self.assertIn('qparameterized.py',result['source_sha256'])

    def test_zero_summand(self):
        result=compute(request('q_gosper',summand=0),CoreBudget())
        self.assertEqual(result['result']['kind'],'zero_summand')

    def test_ratio_parser_rejects_code_float_and_zero_division(self):
        for value in ['__import__("os")',1.5,['div',1,0],['pow',0,-1],['sin','X']]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                rational_input(value)

    def test_no_injected_certificate_fields(self):
        for field in ['target','certificate','denominator','degree','recurrence']:
            r=request('q_gosper',k_shift='q');r[field]='preset'
            with self.assertRaisesRegex(ValueError,'no targets or proof hints'):
                compute(r,CoreBudget())

    def test_domain_rejects_algebraic_shift_and_raw_lattice_index(self):
        for V in [s.sqrt(q)+X,s.Float(1.2)*X,s.zoo]:
            with self.assertRaises(ValueError):
                antidifference(V,X,q)
        with self.assertRaises(ValueError):
            rational_input('k')

    def test_actual_process_timeout_leaves_no_worker(self):
        before={p.pid for p in mp.active_children()}
        result=solve(request('q_gosper',k_shift='q'),CoreBudget(seconds=.00001))
        self.assertEqual(result['status'],'resource_exhausted')
        self.assertIn('wall-clock',result['reason'])
        self.assertEqual({p.pid for p in mp.active_children()},before)

    def test_unknown_limit_is_not_no_solution(self):
        result=parameterized(q,[1,X],X,q,Budget(max_unknowns=1))
        self.assertEqual(result['status'],'resource_exhausted')


if __name__=='__main__':
    started=time.monotonic()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(CoreSolverTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    folder=Path(__file__).parents[1]/'generated/core_solver_20261014'
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'tests.json').write_text(json.dumps(dict(status='passed' if result.wasSuccessful() else 'failed',
        tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        elapsed_seconds=time.monotonic()-started,train_proofs_counted=0,test_files_read=0),indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
