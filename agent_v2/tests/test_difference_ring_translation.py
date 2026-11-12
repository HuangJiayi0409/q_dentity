"""Only independently checked original-relation witnesses become local candidates."""
import copy
import importlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from agent_v2.difference_ring_frontend import analyze_source
from agent_v2.storage import IntegrityError,RunStore,load_train
from agent_v2.symbolic_methods import request_digest
from agent_v2.symbolic_worker import construct

class DifferenceRingTranslationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.difference_ring_translation'))
        self.module=importlib.import_module('agent_v2.difference_ring_translation')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.store=RunStore.create(Path(temp.name)/'runs');self.source=load_train('FQI-SRC-FINE-2.1',self.store)
        self.front=analyze_source(self.source.to_dict(),self.store.root)
    def raw(self):
        request=self.front['core_request']
        return {'schema_version':1,'method':'difference_ring','status':'constructed',
                'request_sha256':request_digest(request),'original_identity_proved':False,
                'construction':construct('difference_ring',request['input'])}
    def test_actual_witness_becomes_source_bound_candidate_and_leaves_original_open(self):
        result=self.module.translate_candidate(self.front,self.raw());self.assertEqual(result['status'],'candidate_ready',result)
        candidate=self.module.make_candidate(self.front);self.assertEqual(candidate.to_dict(),result['candidate'])
        self.assertEqual(candidate.proposition,self.front['local_proposition'])
        self.assertIn('source_increment a q n hn',candidate.proof_term)
        self.assertIn('(hn : (1 ≤ n))',candidate.proposition);self.assertIn('(h_domain : True)',candidate.proposition)
        self.assertEqual(candidate.dependencies,());self.assertIsNone(candidate.closes);self.assertEqual(candidate.replaces,())
        self.assertFalse(result['lean_verified']);self.assertFalse(result['original_identity_proved'])
    def test_bad_bindings_never_produce_candidate(self):
        for key,value in [('method','coefficient'),('schema_version',True),('request_sha256','0'*64),('original_identity_proved',True)]:
            raw=self.raw();raw[key]=value
            with self.subTest(key=key):self.assertEqual(self.module.translate_candidate(self.front,raw)['status'],'translation_pending')
    def test_corrupt_multiplier_never_produces_candidate(self):
        raw=self.raw();raw['construction']['certificate']['coefficients']['h0']='-1'
        result=self.module.translate_candidate(self.front,raw)
        self.assertEqual(result['status'],'translation_pending');self.assertNotIn('candidate',result)
    def test_cas_script_is_diagnostic_only(self):
        raw=self.raw();raw['construction']['certificate']['script']='by sorry; run_arbitrary_code'
        result=self.module.translate_candidate(self.front,raw);self.assertEqual(result['status'],'candidate_ready',result)
        self.assertEqual(result['candidate'],self.module.make_candidate(self.front).to_dict())
        self.assertNotIn('sorry',result['candidate']['proof_term'])
    def test_frontend_and_mapping_tamper_is_integrity_error(self):
        for key,value in [('local_proposition','True'),('step_relation','True'),('mapping',{}),('bound_specialized',True)]:
            front=copy.deepcopy(self.front);front[key]=value
            with self.subTest(key=key),self.assertRaises(IntegrityError):self.module.make_candidate(front)
if __name__=='__main__':unittest.main()
