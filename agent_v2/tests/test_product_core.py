"""Actual symbolic mixed-radix construction and independent verification."""
import copy
import importlib
import unittest
from unittest.mock import patch


def request():
    return {'schema_version':1,'method':'product','input':{
        'operation':'finite_range_index_equivalence','scalar_domain':'commutative_field',
        'parameter':'a','base':'q',
        'left':{'index':'k','bound':['mul','m','n'],
                'factor':['sub',1,['mul','a',['pow','q','k']]]},
        'right':{'indices':['j','i'],'bounds':['m','n'],
                 'factor':['sub',1,['mul',['mul','a',['pow','q','j']],['pow',['pow','q','m'],'i']]]},
        'positive_parameters':['m'],'natural_parameters':['m','n'],'max_candidates':2}}


class ProductCoreTests(unittest.TestCase):
    def setUp(self):
        self.core=importlib.import_module('finite_product_framework.product.index_construct')
        self.checker=importlib.import_module('agent_v2.product_check')
        self.request=request()
        self.construction=self.core.construct(self.request['input'])

    def test_real_axis_search_finds_forward_inverse_and_symbolic_factor_transport(self):
        self.assertEqual(self.construction['status'],'constructed')
        self.assertEqual(self.construction['search']['candidates_examined'],2)
        certificate=self.construction['certificate']
        self.assertEqual(certificate['forward'],['add','j',['mul','m','i']])
        self.assertEqual(certificate['inverse'],{'j':['mod','k','m'],'i':['div','k','m']})
        with patch.object(self.core,'construct',side_effect=AssertionError('checker must not search')):
            checked=self.checker.check(self.request,self.construction)
        self.assertEqual(checked['status'],'passed')
        self.assertEqual(checked['euclidean_rules_checked'],6)
        self.assertFalse(checked['lean_verified'])
        self.assertFalse(checked['bound_specialized'])

    def test_empty_and_singleton_boundaries_do_not_add_nonzero_scalar_conditions(self):
        certificate=self.construction['certificate']
        self.assertEqual(certificate['boundary_cases']['empty_inner']['both_products'],1)
        self.assertEqual(certificate['boundary_cases']['singleton_total']['unique_index'],0)
        self.assertEqual(certificate['scalar_nonzero_conditions'],[])
        self.assertFalse(certificate['cancellation_used'])
        self.assertTrue(self.checker.check(self.request,self.construction)['q_zero_supported'])

    def test_search_exhaustion_and_budget_exhaustion_are_real_distinct_results(self):
        data=copy.deepcopy(self.request['input']);data['max_candidates']=1
        result=self.core.construct(data)
        self.assertEqual(result['status'],'budget_exhausted')
        self.assertEqual(result['search']['candidates_examined'],1)
        data=copy.deepcopy(self.request['input']);data['right']['factor']=['sub',1,['mul','a',['pow','q',['add','m','j']]]]
        self.assertEqual(self.core.construct(data)['status'],'search_exhausted')
        data=copy.deepcopy(self.request['input']);data['positive_parameters']=[]
        self.assertEqual(self.core.construct(data)['status'],'search_exhausted')

    def test_inverse_support_and_rule_tampering_are_rejected(self):
        for field,value in [('forward',['add','j',['mul','n','i']]),
                            ('inverse',{'j':['mod','k','n'],'i':['div','k','m']}),
                            ('radix','n'),('scalar_nonzero_conditions',['q']),
                            ('cancellation_used',True),('commutativity_used',False)]:
            changed=copy.deepcopy(self.construction);changed['certificate'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.checker.check(self.request,changed)
        changed=copy.deepcopy(self.construction);changed['certificate']['euclidean_trace'].pop()
        with self.assertRaises(ValueError):self.checker.check(self.request,changed)
        changed=copy.deepcopy(self.construction);changed['certificate']['euclidean_trace'][0]['rule']='assume inverse'
        with self.assertRaises(ValueError):self.checker.check(self.request,changed)

    def test_false_polynomial_and_boundary_certificates_are_rejected(self):
        changed=copy.deepcopy(self.construction)
        changed['certificate']['factor_normal_forms']['left']['q'][0]['coefficient']=0
        with self.assertRaises(ValueError):self.checker.check(self.request,changed)
        changed=copy.deepcopy(self.construction)
        changed['certificate']['boundary_cases']['empty_inner']['both_products']=True
        with self.assertRaises(ValueError):self.checker.check(self.request,changed)
        changed=copy.deepcopy(self.construction);changed['certificate']['left']['bound']='m'
        with self.assertRaises(ValueError):self.checker.check(self.request,changed)

    def test_malformed_unsupported_noncommutative_and_boolean_requests_are_refused(self):
        for field,value in [('max_candidates',True),('max_candidates',0),('max_candidates',3),
                            ('scalar_domain','noncommutative_ring'),('positive_parameters',['m','m'])]:
            changed=copy.deepcopy(self.request);changed['input'][field]=value
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):self.core.validate_request(changed)
        changed=copy.deepcopy(self.request);changed['input']['left']['factor']=['div','a','q']
        with self.assertRaises(ValueError):self.core.validate_request(changed)
        changed=copy.deepcopy(self.request);changed['input']['assume_identity']=True
        with self.assertRaises(ValueError):self.core.validate_request(changed)
        changed=copy.deepcopy(self.request);changed['schema_version']=True
        with self.assertRaises(ValueError):self.core.validate_request(changed)

    def test_checker_binds_entire_request_and_construction(self):
        changed=copy.deepcopy(self.request);changed['input']['right']['bounds']=['n','m']
        with self.assertRaises(ValueError):self.checker.check(changed,self.construction)
        changed=copy.deepcopy(self.construction);changed['certificate']['extra_assumption']='q != 0'
        with self.assertRaises(ValueError):self.checker.check(self.request,changed)
        changed=copy.deepcopy(self.construction);changed['search']['candidates_examined']=True
        with self.assertRaises(ValueError):self.checker.check(self.request,changed)


if __name__=='__main__':unittest.main()
