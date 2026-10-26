"""Exact algorithm tests, with no benchmark access or Lean invocation."""
import unittest
import sympy as s
from core import CoreBudget,compute,solve
from expressions import q,Q
from ore import (multiply,add,subtract,divide,greatest_common_right_divisor,
                 common_left_multiple,companion,polynomial_closure,observable_row,
                 eliminate,OreResourceLimit,clean)


def parse(value):
    return s.sympify(value,locals={name:s.Symbol(name) for name in
        ('q','Q','a','b','l0','r0','u0')})


def request(operation,**data):
    return dict(schema_version=1,solver='q_ore',input=dict(operation=operation,**data))


def action(operator,f):
    # Independent realization of an operator on rational functions of Q.
    return s.cancel(sum(c*f.subs(Q,q**j*Q) for j,c in enumerate(operator)))


class OreCoreTests(unittest.TestCase):
    def check_witness(self,result):
        raw=result['result'];T=s.Matrix([[parse(v) for v in r] for r in raw['transition']])
        row=s.Matrix([[parse(v) for v in raw['observable_row']]])
        cs=list(map(parse,result['operator']['coefficients']))
        rows=[row]
        for _ in range(len(cs)-1):
            rows.append((rows[-1].subs(Q,q*Q)*T).applyfunc(s.cancel))
        residual=sum((c*r for c,r in zip(cs,rows)),s.zeros(1,T.rows))
        self.assertEqual(residual.applyfunc(s.cancel),s.zeros(1,T.rows))
        self.assertEqual(raw['shifted_rows'],[[str(v) for v in r] for r in rows])
        M=s.Matrix([[parse(v) for v in r] for r in raw['input_transition']])
        variables=s.symbols(f'v0:{M.rows}');next_values=M*s.Matrix(variables)
        monoms=raw['monomial_exponents']
        state=s.Matrix([s.prod(v**e for v,e in zip(variables,m)) for m in monoms])
        expected=s.Matrix([s.prod(v**e for v,e in zip(next_values,m)) for m in monoms])
        self.assertEqual((T*state-expected).applyfunc(s.expand),s.zeros(T.rows,1))

    def test_skew_multiplication_by_independent_action(self):
        a=[Q,1,Q+1];b=[1/(Q+1),Q]
        for f in (Q,Q**3,1/(1+Q)):
            self.assertEqual(action(multiply(a,b),f),action(a,action(b,f)))

    def test_both_divisions_and_distinct_sides(self):
        self.assertEqual(divide([0,q*Q],[Q],'right'),([0,1],[0]))
        self.assertEqual(divide([0,q*Q],[Q],'left'),([0,q],[0]))
        for side in ('right','left'):
            a=[Q,1,Q+1,2];b=[1,Q]
            u,r=divide(a,b,side)
            self.assertLess(len(r),len(b))
            for f in (Q,Q**2,1/(Q+1)):
                product=action(u,action(b,f)) if side=='right' else action(b,action(u,f))
                self.assertEqual(s.cancel(action(a,f)-product-action(r,f)),0)

    def test_division_zero_scalar_and_trailing_zeros(self):
        self.assertEqual(divide([0],[2,1]),([0],[0]))
        self.assertEqual(divide([1],[1,1]),([0],[1]))
        self.assertEqual(divide([2,0,0],[Q]),([2/Q],[0]))
        with self.assertRaisesRegex(ValueError,'zero'):divide([1],[0,0])

    def test_gcrd_known_factor_and_bezout(self):
        factor=[-Q,1]
        a=multiply([1,Q],factor);b=multiply([2,1],factor)
        result=greatest_common_right_divisor(a,b)
        G=list(map(parse,result['operator']))
        self.assertEqual(G,factor)
        U=list(map(parse,result['bezout_a']));V=list(map(parse,result['bezout_b']))
        self.assertEqual(add(multiply(U,a),multiply(V,b)),G)
        for name,operand in (('a',a),('b',b)):
            self.assertEqual(multiply(list(map(parse,result[name+'_left_quotient'])),G),operand)

    def test_gcrd_zero_and_scalar_cases(self):
        for a,b,expected in [([0],[0],[0]),([0],[Q,Q],[1,1]),
                             ([Q,Q],[0],[1,1]),([Q],[1,1],[1])]:
            r=greatest_common_right_divisor(a,b)
            self.assertEqual(list(map(parse,r['operator'])),expected)

    def test_lclm_minimal_order_and_multipliers(self):
        factor=[-Q,1];a=multiply([1,1],factor);b=multiply([2,1],factor)
        r=common_left_multiple(a,b);L=list(map(parse,r['operator']))
        self.assertEqual(len(L)-1,3)
        self.assertEqual(multiply(list(map(parse,r['left_multiplier'])),a),L)
        self.assertEqual(multiply(list(map(parse,r['right_multiplier'])),b),L)
        self.assertEqual(common_left_multiple([0],[1])['operator'],['0'])
        self.assertEqual(common_left_multiple([Q],[1,Q])['operator'],['1/Q','1'])

    def test_coefficient_names_do_not_capture_unknowns(self):
        l0,r0,u0=s.symbols('l0 r0 u0')
        a,b=[l0,1],[r0,1]
        r=common_left_multiple(a,b)
        self.assertEqual(multiply(list(map(parse,r['left_multiplier'])),a),
                         multiply(list(map(parse,r['right_multiplier'])),b))
        M=companion([-u0,1]);T,_,_=polynomial_closure(M,2)
        self.assertEqual(T,s.Matrix([[u0**2]]))

    def test_primitive_normalization_records_singularities(self):
        r=compute(request('normalize',a=[['div',1,['sub','Q',1]],1]),CoreBudget())
        self.assertEqual(list(map(parse,r['operator']['coefficients'])),[1,Q-1])
        self.assertIn('Q - 1',r['domain']['encountered_denominators'])
        self.assertIn('Q - 1',r['domain']['leading_coefficients'])
        self.assertEqual(compute(request('normalize',a=[0]),CoreBudget())['operator']['order'],None)

    def test_general_mixed_degree_two_sequence_closure(self):
        r=compute(request('closure',sequences={'f':[-2,1],'g':[-3,1]},
            observable=['add',1,['seq','f',0],['pow',['seq','g',0],2]]),CoreBudget())
        self.check_witness(r)
        self.assertEqual(list(map(parse,r['operator']['coefficients'])),[-18,29,-12,1])
        self.assertTrue(r['result']['input_recurrences_are_assumptions'])

    def test_sum_product_and_shifts_different_orders(self):
        for obs in (['add',['seq','f',0],['seq','g',0]],
                    ['mul',['seq','f',0],['seq','g',0]],
                    ['add',1,['mul',['seq','f',0],['seq','g',0]],['seq','f',2]]):
            r=compute(request('closure',sequences={'f':[1,-2,1],'g':[-2,1]},observable=obs),CoreBudget())
            self.check_witness(r)
            cs=list(map(parse,r['operator']['coefficients']))
            # Independent sequence values f_n=n and g_n=2^n.
            value=(lambda n:n+2**n) if obs[0]=='add' and len(obs)==3 else (
                (lambda n:n*2**n) if obs[0]=='mul' else lambda n:1+n*2**n+n+2)
            for n in range(5):self.assertEqual(sum(c*value(n+j) for j,c in enumerate(cs)),0)

    def test_q_dependent_observable_coefficients(self):
        r=compute(request('closure',sequences={'f':[['neg','Q'],1]},
            observable=['mul','Q',['seq','f',0]]),CoreBudget())
        self.check_witness(r)
        self.assertEqual(list(map(parse,r['operator']['coefficients'])),[-q*Q,1])

    def test_backward_shift_is_constructed(self):
        r=compute(request('closure',sequences={'f':[['neg','Q'],1]},
            observable=['seq','f',-1]),CoreBudget())
        self.check_witness(r)
        self.assertEqual(s.cancel(parse(r['result']['observable_row'][0])-q/Q),0)
        cs=list(map(parse,r['operator']['coefficients']))
        self.assertEqual(s.cancel(cs[0]/cs[1]+Q/q),0)
        self.assertIn('Q',r['domain']['encountered_denominators'])

    def test_constants_and_zero_observables(self):
        for observable,expected in [(0,[1]),(1,[-1,1]),('Q',[-q,1])]:
            r=compute(request('closure',sequences={'f':[-2,1]},observable=observable),CoreBudget())
            self.check_witness(r)
            self.assertEqual(list(map(parse,r['operator']['coefficients'])),expected)

    def test_existing_homogeneous_api(self):
        M=companion([1,-2,1])
        for degree in (2,3):
            T,powers,u=polynomial_closure(M,degree)
            row=observable_row(u[0]**degree+u[1]**degree,u,powers)
            r=eliminate(T,row)
            self.assertEqual(len(r['coefficients'])-1,degree+1)

    def test_limits_are_resource_results(self):
        r=solve(request('closure',sequences={'f':[1,2,1]},
            observable=['pow',['seq','f',0],8]),CoreBudget(max_states=4))
        self.assertEqual(r['status'],'resource_exhausted')
        r=solve(request('lclm',a=[1,1],b=[2,1]),CoreBudget(max_unknowns=2))
        self.assertEqual(r['status'],'resource_exhausted')
        r=solve(request('closure',sequences={'f':[-2,1]},observable=['seq','f',100]),
                CoreBudget(max_unknowns=10))
        self.assertEqual(r['status'],'resource_exhausted')

    def test_unsupported_observable_is_not_impossibility(self):
        for sequences,observable in [({'f':[-2,1]},['div',1,['seq','f',0]]),
                                    ({'f':[0,1]},['seq','f',-1]),({'f':[1]},['seq','f',0])]:
            r=solve(request('closure',sequences=sequences,observable=observable))
            self.assertEqual(r['status'],'unsupported_input',r)

    def test_exact_domain_and_invalid_input(self):
        for value in (s.Float('0.5'),s.sqrt(2),s.I,s.oo,s.zoo,s.nan):
            with self.assertRaises(ValueError):clean([value,1])
        for req in (request('right_division',a=[1],b=[0]),
                    request('normalize',a=[0.5,1]),request('normalize',a=['__import__']),
                    request('normalize',a=[1],certificate=[1])):
            self.assertEqual(solve(req)['status'],'invalid_input')
        self.assertEqual(solve(request('normalize',a=['X',1]))['status'],'unsupported_domain')

    def test_public_contract_and_source_tracking(self):
        r=solve(request('gcrd',a=[-1,0,1],b=[-1,1]))
        self.assertEqual(r['status'],'constructed')
        self.assertFalse(r['original_identity_proved'])
        self.assertEqual(r['benchmark_files_read'],0)
        self.assertIn('ore_core.py',r['source_sha256'])
        self.assertIn('ore.py',r['source_sha256'])


if __name__=='__main__':unittest.main()
