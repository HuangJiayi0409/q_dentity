"""Source-preserving local transpose candidates from actual affine certificates."""
import copy
import importlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from agent_v2.kernel_transform_frontend import analyze_source
from agent_v2.storage import IntegrityError,RunStore,load_train
from agent_v2.symbolic_methods import request_digest
from agent_v2.symbolic_worker import construct


class KernelTransformTranslationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.kernel_transform_translation'),
                             'source kernel transpose translation is absent')
        self.module=importlib.import_module('agent_v2.kernel_transform_translation')
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        self.store=RunStore.create(Path(temporary.name)/'runs')
        self.source=load_train('FQI-SRC-AQ-3.23',self.store)
        self.front=analyze_source(self.source.to_dict(),self.store.root)

    def raw(self):
        request=self.front['core_request']
        return {'schema_version':1,'method':'kernel_transform','status':'constructed',
            'request_sha256':request_digest(request),'original_identity_proved':False,
            'construction':construct('kernel_transform',request['input'])}

    def test_real_transpose_candidate_keeps_all_parameters_and_original_open(self):
        result=self.module.translate_candidate(self.front,self.raw())
        self.assertEqual(result['status'],'candidate_ready',result)
        candidate=self.module.make_candidate(self.front)
        self.assertEqual(candidate.to_dict(),result['candidate'])
        self.assertEqual(candidate.proposition,self.front['local_proposition'])
        for term in ['(N : ℕ)','(alpha : ℕ → R)','(delta : ℕ → R)',
                     '(u : ℕ → R)','(v : ℕ → R)','CommRing R','Finset.Icc']:
            self.assertIn(term,candidate.proposition)
        self.assertNotIn('Field',candidate.proposition)
        self.assertIn('source_transpose N alpha delta u v',candidate.proof_term)
        self.assertEqual(candidate.dependencies,());self.assertEqual(candidate.replaces,());self.assertIsNone(candidate.closes)
        self.assertFalse(result['lean_verified']);self.assertFalse(result['original_identity_proved'])

    def test_bad_raw_bindings_never_produce_candidate(self):
        for key,value in [('schema_version',True),('method','determinant'),('status','search_exhausted'),
                          ('request_sha256','0'*64),('original_identity_proved',True)]:
            raw=self.raw();raw[key]=value;result=self.module.translate_candidate(self.front,raw)
            with self.subTest(key=key):
                self.assertEqual(result['status'],'translation_pending');self.assertNotIn('candidate',result)

    def test_missing_natural_subtraction_guard_never_produces_candidate(self):
        raw=self.raw();raw['construction']['constructions'][0]['certificate']['left_index_guards'][2]=[0,0,0,0]
        result=self.module.translate_candidate(self.front,raw)
        self.assertEqual(result['status'],'translation_pending');self.assertNotIn('candidate',result)

    def test_unexpected_cas_proof_text_is_rejected_by_certificate_schema(self):
        raw=self.raw();raw['construction']['constructions'][0]['proof_script']='by sorry'
        result=self.module.translate_candidate(self.front,raw)
        self.assertEqual(result['status'],'translation_pending',result)
        self.assertNotIn('candidate',result)

    def test_complete_source_reconstruction_rejects_frontend_or_target_tampering(self):
        for key,value in [('local_proposition','True'),('original_proposition','True'),
                          ('specializes_bound',True),('symbols',{}),('mapping',{})]:
            front=copy.deepcopy(self.front);front[key]=value
            with self.subTest(key=key),self.assertRaises(IntegrityError):self.module.make_candidate(front)


if __name__=='__main__':unittest.main()
