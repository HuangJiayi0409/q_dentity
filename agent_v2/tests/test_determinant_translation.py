"""Actual division-free source minor certificates, independently Leibniz checked."""
import copy
import importlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from agent_v2.determinant_frontend import analyze_source
from agent_v2.storage import IntegrityError,RunStore,load_train
from agent_v2.symbolic_methods import request_digest
from agent_v2.symbolic_worker import construct


class DeterminantTranslationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.determinant_translation'),
                             'source determinant translation is absent')
        self.module=importlib.import_module('agent_v2.determinant_translation')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.store=RunStore.create(Path(temp.name)/'runs');self.source=load_train('FQI-SRC-AP-11.2.4',self.store)
        self.front=analyze_source(self.source.to_dict(),self.store.root)

    def raw(self):
        request=self.front['core_request']
        return {'schema_version':1,'method':'determinant','status':'constructed',
                'request_sha256':request_digest(request),'original_identity_proved':False,
                'construction':construct('determinant',request['input'])}

    def certificate(self,raw):return raw['construction']['constructions'][1]['certificate']

    def reject(self,raw):
        result=self.module.translate_candidate(self.front,raw)
        self.assertEqual(result['status'],'translation_pending',result);self.assertNotIn('candidate',result)

    def test_actual_division_free_core_gives_arbitrary_source_minor(self):
        result=self.module.translate_candidate(self.front,self.raw())
        self.assertEqual(result['status'],'candidate_ready',result)
        candidate=self.module.make_candidate(self.front)
        self.assertEqual(candidate.to_dict(),result['candidate'])
        self.assertIn('(n : Fin k → ℕ)',candidate.proposition)
        self.assertIn('∀ (qv2i0 qv2i1 qv2j0 qv2j1 : Fin k)',candidate.proposition)
        self.assertIn('FiniteQBenchmark.gaussianInt',candidate.proposition)
        self.assertNotIn('planePi',candidate.proposition)
        self.assertEqual(candidate.dependencies,());self.assertEqual(candidate.replaces,());self.assertIsNone(candidate.closes)
        self.assertEqual(result['independent_symbolic_check']['leibniz_permutations'],2)
        self.assertFalse(result['independent_symbolic_check']['pivot_nonzero_assumptions'])
        self.assertFalse(result['lean_verified']);self.assertFalse(result['original_identity_proved'])

    def test_false_sign_zero_result_matrix_map_dimension_or_pivot_policy_rejected(self):
        for key,value in [('determinant','z0*z3+z1*z2'),('determinant','0'),
                          ('matrix',[['z0','z2'],['z1','z3']]),('atoms',{'z0':'entry11'}),
                          ('dimension',True),('dimension',3),('constructor_inputs',['matrix','target']),
                          ('target_value_used_in_search',True),('domain_policy','assume z0 nonzero')]:
            raw=self.raw();self.certificate(raw)[key]=value
            with self.subTest(key=key):self.reject(raw)

    def test_plu_only_or_duplicate_direct_constructions_are_not_accepted(self):
        raw=self.raw();raw['construction']['constructions'].pop();self.reject(raw)
        raw=self.raw();raw['construction']['constructions']=[raw['construction']['constructions'][1]]*2;self.reject(raw)

    def test_untrusted_arithmetic_and_raw_bindings_are_rejected(self):
        for expression in ['z0/z0','__import__("os")','z0**1000000000','z9','True','1.0']:
            raw=self.raw();self.certificate(raw)['determinant']=expression
            with self.subTest(expression=expression):self.reject(raw)
        for key,value in [('schema_version',True),('method','spectral'),('status','search_exhausted'),
                          ('request_sha256','0'*64),('original_identity_proved',True)]:
            raw=self.raw();raw[key]=value
            with self.subTest(key=key):self.reject(raw)
        self.reject(None)

    def test_proof_text_is_never_used_and_equivalent_polynomial_is_checked(self):
        raw=self.raw();raw['construction']['constructions'][1]['proof_script']='by sorry'
        self.certificate(raw)['determinant']='z3*z0 - z2*z1 + 0'
        result=self.module.translate_candidate(self.front,raw)
        self.assertEqual(result['status'],'candidate_ready',result)
        self.assertNotIn('sorry',result['candidate']['proof_term'])
        self.assertFalse(result['independent_symbolic_check']['cas_proof_text_used'])

    def test_source_entry_mapping_frontend_and_original_binding_are_reconstructed(self):
        for key,value in [('minor_entries',{}),('matrix_term','fun i j => 0'),('selectors',[]),
                          ('specializes_original_dimension',0),('original_proposition','True')]:
            front=copy.deepcopy(self.front);front[key]=value
            with self.subTest(key=key),self.assertRaises(IntegrityError):self.module.make_candidate(front)


if __name__=='__main__':unittest.main()
