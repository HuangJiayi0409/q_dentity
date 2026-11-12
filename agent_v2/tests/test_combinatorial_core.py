"""Symbolic arbitrary-size finite choice bijections, never Lean evidence."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]


def request():
    selected={'coefficient':-1,'z_power':1,'q_index_multiplier':1}
    return {'schema_version':1,'method':'combinatorial','input':{
        'operation':'ranked_boolean_choices','scalar_domain':'commutative_field',
        'domain':{'kind':'range','bound':'n'},'rank_upper_offset':1,
        'selected_weight':selected,'factor':{'constant':1,'selected':dict(selected)},
        'rank_weight':{'sign_base':-1,'z_rank_multiplier':1,'q_index_multiplier':1},
        'max_candidates':2}}


class CombinatorialCoreTests(unittest.TestCase):
    def setUp(self):
        path=ROOT/'finite_product_framework/combinatorial/choice_construct.py'
        self.assertTrue(path.is_file(),'finite choice constructor missing')
        spec=importlib.util.spec_from_file_location('finite_choice_core_under_test',path)
        self.core=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.core)
        from agent_v2.combinatorial_check import check
        self.check=check
    def construct(self,data):
        self.core.validate_request(data)
        return self.core.construct(data['input'])
    def test_real_search_checks_generic_boolean_membership_and_signed_weights(self):
        data=request();out=self.construct(data)
        self.assertEqual(out['status'],'constructed');checked=self.check(data,out)
        self.assertEqual(checked['status'],'passed')
        self.assertEqual(out['search']['candidates_examined'],2)
        self.assertEqual(out['search']['trials'][0]['candidate'],'complement')
        self.assertFalse(out['search']['trials'][0]['weight_preserving'])
        self.assertEqual(out['certificate']['bijection']['candidate'],'membership')
        self.assertTrue(checked['arbitrary_bound']);self.assertFalse(checked['bound_sampled'])
        self.assertFalse(checked['lean_verified']);self.assertFalse(checked['formal_certificate_exported'])
        self.assertEqual(out['certificate']['gaussian_subset_bridge'],'pending')
    def test_rank_range_sign_weight_and_factor_errors_are_real_search_failures(self):
        variants=[]
        for offset in (0,2):
            d=request();d['input']['rank_upper_offset']=offset;variants.append(d)
        d=request();d['input']['rank_weight']['sign_base']=1;variants.append(d)
        d=request();d['input']['rank_weight']['q_index_multiplier']=2;variants.append(d)
        d=request();d['input']['factor']['selected']['coefficient']=1;variants.append(d)
        d=request();d['input']['factor']['constant']=2;variants.append(d)
        for data in variants:
            with self.subTest(input=data['input']):self.assertEqual(self.construct(data)['status'],'search_exhausted')
    def test_search_budget_stops_after_the_actually_rejected_first_candidate(self):
        data=request();data['input']['max_candidates']=1;out=self.construct(data)
        self.assertEqual(out['status'],'budget_exhausted')
        self.assertEqual(out['search']['candidates_examined'],1)
        self.assertEqual(out['search']['trials'][0]['candidate'],'complement')
    def test_empty_and_singleton_boundaries_preserve_zero_and_natural_zero_power(self):
        data=request();out=self.construct(data);bounds=out['certificate']['boundaries']
        self.assertEqual(bounds['empty']['only_rank'],0)
        self.assertEqual(bounds['empty']['weight'],1)
        self.assertEqual(bounds['singleton']['selected_weight'],{'coefficient':-1,'z_power':1,'q_index_multiplier':0})
        self.assertTrue(self.check(data,out)['q_zero_supported'])
        self.assertTrue(self.check(data,out)['z_zero_supported'])
    def test_universal_weight_variation_is_calculated_not_a_fixed_success(self):
        data=request();inp=data['input']
        inp['selected_weight']={'coefficient':2,'z_power':3,'q_index_multiplier':2}
        inp['factor']['selected']=dict(inp['selected_weight'])
        inp['rank_weight']={'sign_base':2,'z_rank_multiplier':3,'q_index_multiplier':2}
        out=self.construct(data);self.assertEqual(out['status'],'constructed');self.check(data,out)
        self.assertEqual(out['certificate']['weights']['rank_product']['coefficient_base'],2)
        self.assertEqual(out['certificate']['weights']['rank_product']['z_card_multiplier'],3)
    def test_zero_and_constant_selected_weights_keep_empty_product_and_rank_semantics(self):
        for coefficient,z_power,q_power in ((0,3,2),(1,0,0)):
            data=request();inp=data['input']
            inp['selected_weight']={'coefficient':coefficient,'z_power':z_power,'q_index_multiplier':q_power}
            inp['factor']['selected']=dict(inp['selected_weight'])
            inp['rank_weight']={'sign_base':coefficient,'z_rank_multiplier':z_power,'q_index_multiplier':q_power}
            out=self.construct(data);self.assertEqual(out['status'],'constructed');self.check(data,out)
            self.assertEqual(out['certificate']['boundaries']['empty']['weight'],1)
            self.assertEqual(out['certificate']['bijection']['candidate'],'membership')
            self.assertFalse(out['search']['trials'][0]['rank_preserving'])
    def test_schema_refuses_extra_assumptions_unknown_domain_and_nonexact_values(self):
        variants=[]
        d=request();d['input']['q_nonzero']=True;variants.append(d)
        d=request();d['input']['domain']['bound']=7;variants.append(d)
        d=request();d['input']['rank_upper_offset']=True;variants.append(d)
        d=request();d['input']['selected_weight']['coefficient']=-1.0;variants.append(d)
        d=request();d['input']['max_candidates']=0;variants.append(d)
        for data in variants:
            with self.assertRaises(ValueError):self.core.validate_request(data)
    def test_checker_rejects_changed_inverse_rank_weight_boundaries_and_formal_claims(self):
        data=request();out=self.construct(data)
        mutations=[lambda c:c['certificate']['bijection'].update(inverse=['not','b']),
            lambda c:c['certificate']['bijection']['rows'][0].update(inverse_forward=True),
            lambda c:c['certificate']['rank_map'].update(inverse=['pair',0,'s']),
            lambda c:c['certificate']['weights']['rank_product'].update(coefficient_base=1),
            lambda c:c['certificate']['boundaries']['empty'].update(weight=0),
            lambda c:c['certificate'].update(gaussian_subset_bridge='verified'),
            lambda c:c['certificate'].update(lean_verified=True),
            lambda c:c['search'].update(candidates_examined=0)]
        for mutate in mutations:
            bad=copy.deepcopy(out);mutate(bad)
            with self.assertRaises(ValueError):self.check(data,bad)
    def test_finite_expansion_is_actual_exact_distributivity_normalization(self):
        data=request();out=self.construct(data);step=out['certificate']['finite_expansion']['successor']
        self.assertEqual(step['sum_normal_form'],step['product_normal_form'])
        bad=copy.deepcopy(out);bad['certificate']['finite_expansion']['successor']['sum_normal_form'][0]['coefficient']+=1
        with self.assertRaises(ValueError):self.check(data,bad)
    def test_independent_checker_does_not_invoke_constructor(self):
        data=request();out=self.construct(data)
        self.core.construct=lambda _:(_ for _ in ()).throw(AssertionError('constructor replay'))
        self.assertEqual(self.check(data,out)['status'],'passed')
        self.assertNotIn('choice_construct',(ROOT/'agent_v2/combinatorial_check.py').read_text())


if __name__=='__main__':unittest.main()
