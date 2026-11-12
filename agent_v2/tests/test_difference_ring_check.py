"""Verify original-relation multipliers independently of the CAS search."""
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


class DifferenceRingCheckTests(unittest.TestCase):
    def setUp(self):
        self.module=importlib.import_module('agent_v2.difference_ring_check')
        from agent_v2.difference_ring_frontend import analyze_source
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        store=RunStore.create(Path(temp.name)/'runs')
        self.front=analyze_source(load_train('FQI-SRC-FINE-2.1',store).to_dict(),store.root)
        request=self.front['core_request']
        self.raw=json.loads(json.dumps({'schema_version':1,'method':'difference_ring','status':'constructed',
            'original_identity_proved':False,'request_sha256':request_digest(request),
            'construction':construct('difference_ring',request['input'])}))

    def cert(self,raw):return raw['construction']['certificate']

    def test_actual_multiplier_is_verified_without_reinvoking_a_solver(self):
        with patch('agent_v2.symbolic_worker.construct',side_effect=AssertionError('no solver in checker')):
            result=self.module.check(self.front,self.raw)
        self.assertEqual(result['status'],'passed')
        self.assertEqual(result['relations_checked'],1)
        self.assertEqual(result['multipliers_checked'],1)
        self.assertTrue(result['integer_coefficients_only'])
        self.assertFalse(result['cas_proof_text_used'])
        self.assertTrue(result['source_shift_requires_lean'])

    def test_wrong_multipliers_and_rational_or_executable_text_are_refused(self):
        for value in ('0','-1','1/2','a99','__import__("os").system("false")','True','2**100000'):
            raw=copy.deepcopy(self.raw);cert=self.cert(raw)
            cert['coefficients'][next(iter(cert['coefficients']))]=value
            with self.subTest(value=value),self.assertRaises(ValueError):self.module.check(self.front,raw)

    def test_reported_target_relations_remainder_and_atom_meanings_are_recomputed(self):
        for field,value in (('difference','0'),('relations',['0']),('remainder','1'),
                            ('atoms',{'0':'unrelated original term'}),('algorithm','unverified plan')):
            raw=copy.deepcopy(self.raw);self.cert(raw)[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.module.check(self.front,raw)
        for coefficients in ({},{'foreign_assumption':'1'}):
            raw=copy.deepcopy(self.raw);self.cert(raw)['coefficients']=coefficients
            with self.assertRaises(ValueError):self.module.check(self.front,raw)

    def test_script_is_diagnostic_only_and_never_controls_the_check(self):
        raw=copy.deepcopy(self.raw);self.cert(raw)['script']='by sorry; arbitrary untrusted text'
        checked=self.module.check(self.front,raw)
        self.assertEqual(checked['status'],'passed')
        self.assertFalse(checked['cas_proof_text_used'])

    def test_source_and_request_bindings_cannot_be_replaced(self):
        for key,value in [('schema_version',True),('request_sha256','0'*64),
                          ('method','coefficient'),('status','search_exhausted'),('original_identity_proved',True)]:
            raw=copy.deepcopy(self.raw);raw[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.module.check(self.front,raw)
        front=copy.deepcopy(self.front);front['core_request']['input']['goal']['hypotheses']=[]
        with self.assertRaises(ValueError):self.module.check(front,self.raw)

    def test_missing_and_unknown_certificate_fields_are_refused(self):
        for value in (None,{},[],True):
            with self.subTest(raw=value),self.assertRaises(ValueError):self.module.check(self.front,value)
        raw=copy.deepcopy(self.raw);self.cert(raw).pop('relations')
        with self.assertRaises(ValueError):self.module.check(self.front,raw)
        raw=copy.deepcopy(self.raw);self.cert(raw)['assume_nonzero']='q'
        with self.assertRaises(ValueError):self.module.check(self.front,raw)


if __name__=='__main__':unittest.main()
