"""Independent verification of real finite-kernel affine certificates."""
import copy
import importlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from agent_v2.kernel_transform_frontend import analyze_source
from agent_v2.storage import RunStore,load_train
from agent_v2.symbolic_methods import request_digest
from agent_v2.symbolic_worker import construct


class KernelTransformCheckTests(unittest.TestCase):
    def setUp(self):
        self.module=importlib.import_module('agent_v2.kernel_transform_check')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        store=RunStore.create(Path(temp.name)/'runs')
        self.front=analyze_source(load_train('FQI-SRC-AQ-3.23',store).to_dict(),store.root)
        request=self.front['core_request']
        self.raw={'schema_version':1,'method':'kernel_transform','status':'constructed',
            'original_identity_proved':False,'request_sha256':request_digest(request),
            'construction':construct('kernel_transform',request['input'])}

    def cert(self,raw):return raw['construction']['constructions'][0]['certificate']

    def test_real_core_certificate_is_checked_without_calling_the_constructor(self):
        with patch('agent_v2.symbolic_worker.construct',side_effect=AssertionError('no solver in checker')):
            result=self.module.check(self.front,self.raw)
        self.assertEqual(result['status'],'passed')
        self.assertEqual(result['permutation'],[1,0])
        self.assertEqual(result['support_implications_checked'],8)
        self.assertEqual(result['finite_bound_witnesses_checked'],8)
        self.assertEqual(result['natural_index_guards_checked'],8)
        self.assertFalse(result['cas_proof_text_used'])
        self.assertFalse(result['bound_specialized'])

    def test_all_six_witness_families_are_independently_verified(self):
        families=['forward_implications','backward_implications','left_finite_bounds',
                  'right_finite_bounds','left_index_guards','right_index_guards']
        for family in families:
            for mode in ('zero','negative','boolean','short','oversized'):
                raw=copy.deepcopy(self.raw);witness=self.cert(raw)[family][0]
                if mode=='zero':witness[:]=[0]*len(witness)
                elif mode=='negative':witness[0]=-1
                elif mode=='boolean':witness[0]=True
                elif mode=='short':witness.pop()
                else:witness[0]=3
                with self.subTest(family=family,mode=mode),self.assertRaises(ValueError):
                    self.module.check(self.front,raw)

    def test_permutation_inverse_and_every_source_mapping_are_bound(self):
        changes={'permutation':[0,0],'inverse_permutation':[0,1],'coordinates':True,
                 'parameter':'0','type':'K','max_multiplier':True,'bound_specialized':True,
                 'permutations_tried':1,'algorithm':'unverified plan'}
        for key,value in changes.items():
            raw=copy.deepcopy(self.raw);self.cert(raw)[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.module.check(self.front,raw)
        for key in ('left_domain','right_domain','transported_left_domain'):
            raw=copy.deepcopy(self.raw);self.cert(raw)[key][0][0]=True
            with self.subTest(key=key),self.assertRaises(ValueError):self.module.check(self.front,raw)
        for key in ('left_factors','right_factors','transported_left_factors'):
            raw=copy.deepcopy(self.raw);self.cert(raw)[key][2]['index'][3]=1
            with self.subTest(key=key),self.assertRaises(ValueError):self.module.check(self.front,raw)

    def test_forward_only_proof_or_weight_reordering_with_lost_multiplicity_is_refused(self):
        raw=copy.deepcopy(self.raw);self.cert(raw).pop('backward_implications')
        with self.assertRaises(ValueError):self.module.check(self.front,raw)
        raw=copy.deepcopy(self.raw)
        factors=self.cert(raw)['transported_left_factors'];factors[-1]=copy.deepcopy(factors[0])
        with self.assertRaises(ValueError):self.module.check(self.front,raw)

    def test_source_and_raw_request_identity_are_not_trusted(self):
        for key,value in [('schema_version',True),('request_sha256','0'*64),
                          ('method','coefficient'),('status','search_exhausted'),('original_identity_proved',True)]:
            raw=copy.deepcopy(self.raw);raw[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.module.check(self.front,raw)
        front=copy.deepcopy(self.front);front['core_request']['input']['max_multiplier']=1
        with self.assertRaises(ValueError):self.module.check(front,self.raw)
        front=copy.deepcopy(self.front);front['mapping']['natural_subtraction_guard']='unconditional subtraction'
        with self.assertRaises(ValueError):self.module.check(front,self.raw)

    def test_malformed_and_multiple_constructions_are_refused(self):
        for value in (None,{},[],True):
            with self.subTest(raw=value),self.assertRaises(ValueError):self.module.check(self.front,value)
        raw=copy.deepcopy(self.raw);raw['construction']['constructions']*=2
        with self.assertRaises(ValueError):self.module.check(self.front,raw)
        raw=copy.deepcopy(self.raw);self.cert(raw)['unchecked_assumption']='r > n'
        with self.assertRaises(ValueError):self.module.check(self.front,raw)


if __name__=='__main__':unittest.main()
