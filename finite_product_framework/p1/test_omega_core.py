"""Synthetic algorithm tests only: no benchmark files, no Lean."""
import copy
import random
import unittest
import sympy as s
from core import CoreBudget, compute, solve
from qgosper import UnsupportedDomain
from ore import OreResourceLimit
from qdifference import rational_read
from check_omega_core import replay

x,y,w,q,L,M = s.symbols('x y w q L M')


def tree(v):
    v = s.sympify(v)
    if v.is_Integer:return int(v)
    if v.is_Rational:return ['div',int(v.p),int(v.q)]
    if v.is_Symbol:return str(v)
    if v.is_Add:return ['add', *map(tree,v.args)]
    if v.is_Mul:return ['mul', *map(tree,v.args)]
    if v.is_Pow and v.exp.is_Integer:return ['pow',tree(v.base),int(v.exp)]
    raise ValueError(v)


def request(numerator, factors, operations=((L,'ge'),), grading=None):
    if grading is None:
        symbols = set().union(*(s.sympify(v).free_symbols for v in [numerator,*factors]))
        grading = {str(v):1 for v in symbols-{z for z,_ in operations}}
        if not grading:grading={'x':1}
    return dict(schema_version=1,solver='rational_omega',input=dict(
        numerator=tree(numerator),denominator_monomials=list(map(tree,factors)),
        grading=grading,eliminate=[dict(variable=str(z),operator=op) for z,op in operations]))


def projected_coefficients(numerator, factors, operations, degree):
    """Independent finite geometric enumeration after x=y=w=t, q=2.

    Used only in tests; degree is NOT passed to the symbolic solver.
    """
    auxiliaries = [z for z,_ in operations]
    def entry(term):
        powers=term.as_powers_dict()
        g=sum(int(powers.get(v,0)) for v in (x,y,w))
        es=tuple(int(powers.get(v,0)) for v in auxiliaries)
        c=term.subs({x:1,y:1,w:1,q:2,**{z:1 for z in auxiliaries}})
        return g,es,c
    states={}
    for term in s.Add.make_args(s.expand(numerator)):
        g,es,c=entry(term);states[g,es]=states.get((g,es),0)+c
    for factor in factors:
        g,es,c=entry(factor)
        assert g>0
        following={}
        for (oldg,oldes),oldc in states.items():
            for j in range((degree-oldg)//g+1):
                key=oldg+j*g,tuple(a+j*b for a,b in zip(oldes,es))
                following[key]=following.get(key,0)+oldc*c**j
        states=following
    out=[s.S.Zero]*(degree+1)
    for (g,es),c in states.items():
        if all(e>=0 if op=='ge' else e==0 for e,(_,op) in zip(es,operations)):
            out[g]+=c
    return out


def rational_coefficients(value, degree):
    t=s.Symbol('t')
    v=s.cancel(value.subs({x:t,y:t,w:t,q:2}))
    num,den=map(lambda f:s.Poly(f,t),s.fraction(v))
    assert den.nth(0)!=0
    out=[]
    for j in range(degree+1):
        out.append(s.cancel((num.nth(j)-sum(den.nth(i)*out[j-i]
            for i in range(1,j+1)))/den.nth(0)))
    return out


class OmegaTests(unittest.TestCase):
    def run_case(self, numerator, factors, expected=None, operations=((L,'ge'),), grading=None):
        req=request(numerator,factors,operations,grading)
        result=compute(req,CoreBudget())
        self.assertEqual(result['status'],'constructed')
        self.assertEqual(replay(req,result),len(operations))
        value=rational_read(result['result']['value'])
        if expected is not None:self.assertEqual(s.cancel(value-expected),0)
        return value

    def test_coprime_inequality(self):
        self.run_case(1,[x*L**2,y/L**3],(1+x**2*y)/((1-x)*(1-x**3*y**2)))

    def test_constant_term(self):
        self.run_case(1,[x*L**2,y/L**3],1/(1-x**3*y**2),((L,'ct'),))

    def test_non_coprime_exponents(self):
        self.run_case(1,[x*L**4,y/L**6],1/(1-x**3*y**2),((L,'ct'),))

    def test_inconsistent_congruence(self):
        self.run_case(L,[x*L**2,y/L**2],0,((L,'ct'),))

    def test_repeated_factors(self):
        self.run_case(1,[x*L,x*L,y/L],1/(1-x*y)**2,((L,'ct'),))

    def test_non_coprime_factors(self):
        self.run_case(1,[x*L,x**2*L**2,y/L],1/((1-x*y)*(1-x**2*y**2)),((L,'ct'),))

    def test_cyclotomic_factors(self):
        self.run_case(1,[x**3*L**3,y/L],1/(1-x**3*y**3),((L,'ct'),))

    def test_only_positive(self):
        self.run_case(1,[x*L,y*L**2],1/((1-x)*(1-y)))

    def test_only_negative(self):
        self.run_case(1,[x/L,y/L**2],1)

    def test_negative_numerator_tail(self):
        self.run_case(L**-4,[x*L],x**4/(1-x))

    def test_positive_numerator_cutoff(self):
        self.run_case(L**4,[x/L],sum(x**i for i in range(5)))

    def test_laurent_polynomial(self):
        self.run_case(x/L+2+L*y+L**3,[],3+y)

    def test_polynomial_constant(self):
        self.run_case(x/L+2+L*y+L**3,[],2,((L,'ct'),))

    def test_zero(self):self.run_case(0,[x*L,y/L],0)

    def test_inactive_variable(self):self.run_case(1,[x],1/(1-x))

    def test_rational_coefficient_and_sign(self):
        self.run_case(s.Rational(2,3),[-x*L,y/(2*L)],s.Rational(2,3)/(1+x*y/2),((L,'ct'),))

    def test_weight_zero_q_parameter(self):
        self.run_case(1,[x*q**3*L,x*q**-2/L],1/(1-x**2*q),((L,'ct'),),{'x':1,'q':0})

    def test_laurent_external_monomials(self):
        self.run_case(1,[x**2/y*L,y**2/x/L],1/(1-x*y),((L,'ct'),),{'x':1,'y':1})

    def test_two_inequalities_chain(self):
        self.run_case(1,[x*L,y*M/L,w/M],1/((1-x)*(1-x*y)*(1-x*y*w)),((L,'ge'),(M,'ge')))

    def test_equalities(self):
        self.run_case(1,[x*L,y*M/L,w/M],1/(1-x*y*w),((L,'ct'),(M,'ct')))

    def test_redundant_third_equality(self):
        N=s.Symbol('N')
        self.run_case(1,[x*L/M,y*M/N,w*N/L],1/(1-x*y*w),((L,'ct'),(M,'ct'),(N,'ct')))

    def test_two_coupled_equalities_four_factors(self):
        v=s.Symbol('v')
        self.run_case(1,[x*L*M,y*L/M,w*M/L,v/(L*M)],
            1/((1-x*v)*(1-y*w)),((L,'ct'),(M,'ct')))

    def test_mixed_constraints(self):
        self.run_case(1,[x*L,y*M/L,w/M],1/((1-x*y)*(1-x*y*w)),((L,'ct'),(M,'ge')))

    def test_elimination_order(self):
        factors=[x*L**2*M,y*M/L,w/M**2]
        a=self.run_case(1,factors,operations=((L,'ge'),(M,'ct')))
        self.run_case(1,factors,a,((M,'ct'),(L,'ge')))

    def test_shifted_finite_interval(self):
        self.run_case(M**4,[x*L/M],sum(x**i for i in range(5)),((L,'ge'),(M,'ge')))

    def test_numerator_cancellation(self):
        self.run_case(1-x*L,[x*L,y/L],1)

    def test_q_and_parameter_specialization(self):
        a=self.run_case(1,[x*q*L,y/L],1/(1-x*y*q),((L,'ct'),),{'x':1,'y':1,'q':0})
        self.assertEqual(a.subs(q,0),1)
        self.assertEqual(s.cancel(a.subs(q,1)-1/(1-x*y)),0)

    def test_different_external_weights(self):
        self.run_case(1,[x*L,y/L],1/(1-x*y),((L,'ct'),),{'x':1,'y':3})

    def test_independent_enumeration(self):
        rng=random.Random(74021)
        for case in range(18):
            operations=((L,'ge' if case%2 else 'ct'),(M,'ge' if case%3 else 'ct'))
            factors=[v*L**rng.randint(-2,2)*M**rng.randint(-2,2) for v in (x,y,w)]
            numerator=L**rng.randint(-2,2)*M**rng.randint(-2,2)
            with self.subTest(case=case,factors=factors):
                value=self.run_case(numerator,factors,operations=operations)
                self.assertEqual(rational_coefficients(value,9),projected_coefficients(numerator,factors,operations,9))

    def test_invalid_shape(self):
        req=request(1,[x*L]);req['input']['certificate']=1
        with self.assertRaises(ValueError):compute(req,CoreBudget())

    def test_undeclared_symbol(self):
        req=request(y,[x*L],grading={'x':1})
        with self.assertRaises(ValueError):compute(req,CoreBudget())

    def test_ungraded_factor(self):
        for v in [L,1,x/L]:
            grading={'x':0,'y':1}
            with self.subTest(v=v),self.assertRaises(UnsupportedDomain):
                compute(request(1,[v],grading=grading),CoreBudget())

    def test_zero_and_negative_grade(self):
        for v in [0,x**-1*L]:
            with self.subTest(v=v),self.assertRaises((ValueError,UnsupportedDomain)):
                compute(request(1,[v],grading={'x':1}),CoreBudget())

    def test_non_monomial_factor(self):
        with self.assertRaises(UnsupportedDomain):compute(request(1,[(x+y)*L]),CoreBudget())

    def test_non_laurent_numerator(self):
        with self.assertRaises(UnsupportedDomain):compute(request(1/(1+L),[x*L]),CoreBudget())

    def test_invalid_variable_and_operator(self):
        for op in ['pt',None,1]:
            with self.subTest(op=op),self.assertRaises(ValueError):
                compute(request(1,[x*L],((L,op),)),CoreBudget())

    def test_duplicate_and_overlapping_variables(self):
        for ops,grading in [(((L,'ge'),(L,'ct')),{'x':1}),(((L,'ge'),),{'L':0,'x':1})]:
            with self.assertRaises(ValueError):compute(request(1,[x*L],ops,grading),CoreBudget())

    def test_degree_budget(self):
        with self.assertRaises(OreResourceLimit):compute(request(1,[x*L**20]),CoreBudget(max_normal_form_degree=5))

    def test_state_budget(self):
        with self.assertRaises(OreResourceLimit):compute(request(1,[x*L,y/L]),CoreBudget(max_states=2))

    def test_term_budget(self):
        with self.assertRaises(OreResourceLimit):compute(request(1+L+L**2,[]),CoreBudget(max_unknowns=2))

    def test_certificate_tampering(self):
        req=request(1,[x*L,y/L]);result=compute(req,CoreBudget())
        variants=[]
        bad=copy.deepcopy(result);bad['result']['value']='0';variants.append(bad)
        bad=copy.deepcopy(result);bad['result']['steps'][0]['positive_numerator']='0';variants.append(bad)
        bad=copy.deepcopy(result);bad['result']['steps'][0]['factors'][0]['side']='positive';variants.append(bad)
        bad=copy.deepcopy(result);bad['result']['steps']=[];variants.append(bad)
        bad=copy.deepcopy(result);bad['result']['steps'][0]['operator']='ct';variants.append(bad)
        bad=copy.deepcopy(result);step=bad['result']['steps'][0]
        step['polynomial']=str(rational_read(step['polynomial'])+1)
        step['negative_numerator']=str(rational_read(step['negative_numerator'])-rational_read(step['negative_denominator']))
        variants.append(bad)  # same rational function, invalid negative support
        for bad in variants:
            with self.assertRaises(AssertionError):replay(req,bad)

    def test_public_process_and_provenance(self):
        req=request(1,[x*L,y/L]);out=solve(req,CoreBudget(seconds=20))
        self.assertEqual(out['status'],'constructed',out)
        self.assertFalse(out['original_identity_proved'])
        self.assertEqual(out['benchmark_files_read'],0)
        self.assertIn('qomega.py',out['source_sha256'])
        replay(req,out)

    def test_public_failure_labels(self):
        for req,status in [(request(1,[L],grading={'x':1}),'unsupported_domain'),
                           (dict(request(1,[x*L]),target='0'),'invalid_input')]:
            self.assertEqual(solve(req,CoreBudget(seconds=10))['status'],status)

    def test_hard_timeout(self):
        result=solve(request(1,[x*L]),CoreBudget(seconds=0.00001))
        self.assertEqual(result['status'],'resource_exhausted')


if __name__=='__main__':unittest.main()
