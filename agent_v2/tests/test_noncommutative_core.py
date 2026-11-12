"""Exact symbolic arbitrary-degree operator semantics, never Lean evidence."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]


def request(lhs=None,rhs=None,steps=128):
    return {'schema_version':1,'method':'noncommutative','input':{
        'operation':'polynomial_operator_words','carrier':'polynomial_over_commutative_field',
        'central_scalar':'q','operators':{'X':'multiply_by_variable','M':'substitute_q_times_variable'},
        'lhs':lhs if lhs is not None else [term('MX')],
        'rhs':rhs if rhs is not None else [term('XM',q=1)],'max_steps':steps}}


def term(word='',coefficient=1,q=0):return {'coefficient':coefficient,'q_power':q,'word':list(word)}


class NoncommutativeCoreTests(unittest.TestCase):
    def setUp(self):
        path=ROOT/'finite_product_framework/noncommutative/operator_construct.py'
        self.assertTrue(path.is_file(),'bounded operator constructor missing')
        spec=importlib.util.spec_from_file_location('operator_core_under_test',path)
        self.core=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.core)
        from agent_v2.noncommutative_check import check
        self.check=check
    def construct(self,data):
        self.core.validate_request(data)
        return self.core.construct(data['input'])
    def test_actual_commutation_from_definitional_actions_for_arbitrary_degree(self):
        data=request();out=self.construct(data)
        self.assertEqual(out['status'],'constructed')
        checked=self.check(data,out)
        self.assertEqual(checked['status'],'passed')
        self.assertTrue(checked['arbitrary_degree']);self.assertFalse(checked['degree_sampled'])
        self.assertFalse(checked['lean_verified']);self.assertFalse(checked['formal_certificate_exported'])
        self.assertEqual(out['certificate']['normal_forms']['lhs'],[
            {'coefficient':1,'q_power':1,'x_power':1,'m_power':1}])
        self.assertEqual(out['certificate']['terms']['lhs'][0]['trace'][0]['operator'],'X')
    def test_order_and_scalar_errors_are_real_search_failures(self):
        for data in (request(rhs=[term('XM')]),request(rhs=[term('XM',q=2)]),
                     request(lhs=[term('XM')],rhs=[term('MX',q=1)])):
            self.assertEqual(self.construct(data)['status'],'search_exhausted')
    def test_long_words_use_shift_exponents_not_commutative_operator_sorting(self):
        data=request(lhs=[term('MMXXXMXX')],rhs=[term('XXXXXMMM',q=12)])
        out=self.construct(data);self.assertEqual(out['status'],'constructed')
        self.assertEqual(self.check(data,out)['status'],'passed')
        # Two initial M operators see all five X, the inner M sees two X.
        self.assertEqual(out['certificate']['normal_forms']['lhs'][0]['q_power'],12)
    def test_additive_distribution_and_zero_cancellation(self):
        data=request(lhs=[term('MX',2),term('XM',-1,1),term('',0)],rhs=[term('XM',1,1)])
        out=self.construct(data);self.assertEqual(out['status'],'constructed');self.check(data,out)
        zero=request(lhs=[term('MX'),term('XM',-1,1)],rhs=[])
        out=self.construct(zero);self.assertEqual(out['certificate']['normal_forms']['lhs'],[]);self.check(zero,out)
    def test_empty_word_and_empty_sum_are_exact_boundary_cases(self):
        for data in (request(lhs=[term()],rhs=[term()]),request(lhs=[],rhs=[])):
            self.assertEqual(self.check(data,self.construct(data))['status'],'passed')
    def test_step_budget_is_consumed_by_actual_semantic_actions(self):
        data=request(steps=1);out=self.construct(data)
        self.assertEqual(out['status'],'budget_exhausted')
        self.assertEqual(out['search']['steps_used'],1)
        self.assertTrue(out['search']['partial_terms'])
    def test_request_schema_rejects_assumed_target_unknown_operator_and_nonexact_values(self):
        samples=[]
        data=request();data['input']['relations']=['MX=qXM'];samples.append(data)
        data=request();data['input']['lhs'][0]['word']=['D'];samples.append(data)
        data=request();data['input']['lhs'][0]['q_power']=True;samples.append(data)
        data=request();data['input']['lhs'][0]['coefficient']=1.0;samples.append(data)
        data=request();data['input']['operators']['M']='multiply_by_q';samples.append(data)
        data=request();data['input']['lhs'][0]['word']=['M']*33;samples.append(data)
        for data in samples:
            with self.assertRaises(ValueError):self.core.validate_request(data)
    def test_certificate_checker_rejects_changed_order_exponent_trace_and_capability(self):
        data=request();out=self.construct(data)
        changes=[lambda c:c['certificate']['terms']['lhs'][0]['trace'][0].update(operator='M'),
                 lambda c:c['certificate']['normal_forms']['lhs'][0].update(q_power=0),
                 lambda c:c['certificate']['terms']['lhs'][0]['trace'][0]['after'].update(degree_offset=7),
                 lambda c:c['certificate'].update(lean_verified=True),
                 lambda c:c['certificate']['input']['lhs'][0]['word'].reverse(),
                 lambda c:c['search'].update(steps_used=0)]
        for change in changes:
            bad=copy.deepcopy(out);change(bad)
            with self.assertRaises(ValueError):self.check(data,bad)
    def test_independent_checker_never_uses_constructor(self):
        data=request();out=self.construct(data)
        self.core.construct=lambda _:(_ for _ in ()).throw(AssertionError('constructor replay'))
        self.assertEqual(self.check(data,out)['status'],'passed')
        text=(ROOT/'agent_v2/noncommutative_check.py').read_text()
        self.assertNotIn('operator_construct',text)


if __name__=='__main__':unittest.main()
