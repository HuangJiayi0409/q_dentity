"""Independently replay actual Omega blocks and their finite source fiber."""
import copy
import importlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from agent_v2.storage import RunStore,load_train
from agent_v2.symbolic_methods import request_digest
from agent_v2.symbolic_worker import construct


class MacMahonCheckTests(unittest.TestCase):
    def setUp(self):
        self.module=importlib.import_module('agent_v2.macmahon_check')
        from agent_v2.macmahon_frontend import analyze_source
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        store=RunStore.create(Path(temp.name)/'runs')
        self.front=analyze_source(load_train('FQI-SRC-GR2-7.Ex14',store).to_dict(),store.root)
        request=self.front['core_request']
        self.raw=json.loads(json.dumps({'schema_version':1,'method':'macmahon','status':'constructed',
            'original_identity_proved':False,'request_sha256':request_digest(request),
            'construction':construct('macmahon',request['input'])}))
    def step(self,raw):return raw['construction']['result']['steps'][0]
    def test_actual_omega_blocks_are_rechecked_without_a_symbolic_solver(self):
        with patch('agent_v2.symbolic_worker.construct',side_effect=AssertionError('no solver in check')):
            checked=self.module.check(self.front,self.raw)
        self.assertEqual(checked['status'],'passed');self.assertEqual(checked['omega_steps'],1)
        self.assertTrue(checked['finite_fiber_checked']);self.assertFalse(checked['bound_specialized'])
        self.assertTrue(checked['formal_denominator_requires_lean']);self.assertFalse(checked['cas_proof_text_used'])
    def test_each_reconstruction_field_and_projection_is_bound(self):
        for key in ('input','positive_numerator','positive_denominator','negative_numerator','negative_denominator','output'):
            raw=copy.deepcopy(self.raw);self.step(raw)[key]='1'
            with self.subTest(key=key),self.assertRaises(ValueError):self.module.check(self.front,raw)
        for key in ('polynomial','rational_residual'):
            raw=copy.deepcopy(self.raw);self.step(raw)[key]='1'
            with self.assertRaises(ValueError):self.module.check(self.front,raw)
        raw=copy.deepcopy(self.raw);raw['construction']['result']['value']='1/(1-C0*W0)'
        with self.assertRaises(ValueError):self.module.check(self.front,raw)
    def test_false_one_sidedness_grading_or_unsupported_elimination_is_refused(self):
        raw=copy.deepcopy(self.raw);self.step(raw)['factors'][0]['side']='positive'
        with self.assertRaises(ValueError):self.module.check(self.front,raw)
        raw=copy.deepcopy(self.raw);self.step(raw)['operator']='ct'
        with self.assertRaises(ValueError):self.module.check(self.front,raw)
        raw=copy.deepcopy(self.raw);raw['construction']['domain']['grading']['Grade']=0
        with self.assertRaises(ValueError):self.module.check(self.front,raw)
        raw=copy.deepcopy(self.raw);self.step(raw)['positive_numerator']='L0*W0/(C0*Grade-W0)'
        with self.assertRaises(ValueError):self.module.check(self.front,raw)
    def test_arbitrary_evaluation_or_nonexact_expression_is_never_executed(self):
        for value in ('__import__("os").system("false")','0.5','True','W0**100000','1/0','sqrt(W0)'):
            raw=copy.deepcopy(self.raw);raw['construction']['result']['value']=value
            with self.subTest(value=value),self.assertRaises(ValueError):self.module.check(self.front,raw)
    def test_request_source_and_mathematical_mapping_cannot_drift(self):
        for key,value in [('schema_version',True),('method','coefficient'),('request_sha256','0'*64),
                          ('status','unsupported_domain'),('original_identity_proved',True)]:
            raw=copy.deepcopy(self.raw);raw[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.module.check(self.front,raw)
        front=copy.deepcopy(self.front);front['source_exponent']['index']=-1
        with self.assertRaises(ValueError):self.module.check(front,self.raw)
        front=copy.deepcopy(self.front);front['mapping']['finite_fiber']='unbounded'
        with self.assertRaises(ValueError):self.module.check(front,self.raw)
    def test_malformed_or_missing_omega_steps_are_refused(self):
        for value in (None,{},[],True):
            with self.assertRaises(ValueError):self.module.check(self.front,value)
        raw=copy.deepcopy(self.raw);raw['construction']['result']['steps']*=2
        with self.assertRaises(ValueError):self.module.check(self.front,raw)
        raw=copy.deepcopy(self.raw);self.step(raw).pop('negative_numerator')
        with self.assertRaises(ValueError):self.module.check(self.front,raw)

if __name__=='__main__':unittest.main()
