"""Validate actual bounded interpolation certificates against their source."""
import copy
import importlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from agent_v2.interpolation_frontend import analyze_source
from agent_v2.storage import IntegrityError, RunStore, load_train
from agent_v2.symbolic_methods import request_digest
from agent_v2.symbolic_worker import construct


class InterpolationTranslationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.interpolation_translation'),
                             'source interpolation translator is absent')
        self.module = importlib.import_module('agent_v2.interpolation_translation')
        temp=tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.store=RunStore.create(Path(temp.name)/'runs')
        self.source=load_train('FQI-SRC-GR2-I-20', self.store)
        self.front=analyze_source(self.source.to_dict(), self.store.root)

    def raw(self):
        request=self.front['core_request']
        return {'schema_version':1,'method':'interpolation','status':'constructed',
                'request_sha256':request_digest(request),'original_identity_proved':False,
                'construction':construct('interpolation',request['input'])}

    def reject(self, raw):
        result=self.module.translate_candidate(self.front,raw)
        self.assertEqual(result['status'],'translation_pending',result)
        self.assertNotIn('candidate',result)

    def test_actual_core_yields_one_all_tail_index_source_bound_candidate(self):
        result=self.module.translate_candidate(self.front,self.raw())
        self.assertEqual(result['status'],'candidate_ready',result)
        candidate=self.module.make_candidate(self.front)
        self.assertEqual(result['candidate'],candidate.to_dict())
        self.assertEqual(candidate.source_sha256,self.source.sha256)
        self.assertEqual(candidate.dependencies,()); self.assertEqual(candidate.replaces,())
        self.assertIsNone(candidate.closes)
        self.assertIn('(hbase : (FiniteQBenchmark.regular q))',candidate.proposition)
        self.assertIn('(h_domain : ((FiniteQBenchmark.pochList [a] q k) ≠ 0))',candidate.proposition)
        self.assertIn('∀ qv2j : ℕ, qv2j < (n - k) →',candidate.proposition)
        self.assertIn('((k : ℤ) : ℤ)',candidate.proposition)
        self.assertIn('AgentV2Interpolation.source_factor a q k qv2j',candidate.proof_term)
        check=result['independent_symbolic_check']
        self.assertEqual(check['degree_upper_bound'],1)
        self.assertEqual(check['nodes'],['0','1'])
        self.assertFalse(result['lean_verified']); self.assertFalse(result['original_identity_proved'])

    def test_degree_variable_node_polynomial_and_domain_tampering_rejected(self):
        changes=[('degree_upper_bound',0),('degree_upper_bound',True),('variable_atom',1),
                 ('variable_atom',False),('variable_expression','u'),('kind','arbitrary'),
                 ('node_distinctness','Nat.cast_injective via CharZero'),('polynomial','0'),
                 ('nodes',[{'node':'0','exact_residual':'0'},{'node':'0','exact_residual':'0'}]),
                 ('nodes',[{'node':'0','exact_residual':'1'},{'node':'1','exact_residual':'0'}])]
        for key,value in changes:
            raw=self.raw(); raw['construction']['certificate'][key]=value
            with self.subTest(field=key,value=value): self.reject(raw)

    def test_status_request_and_method_binding_cannot_be_forged(self):
        for key,value in [('schema_version',True),('method','coefficient'),('status','search_exhausted'),
                          ('request_sha256','0'*64),('original_identity_proved',True)]:
            raw=self.raw(); raw[key]=value
            with self.subTest(key=key): self.reject(raw)
        raw=self.raw(); raw['construction']['status']='search_exhausted'; self.reject(raw)
        self.reject(None); self.reject({})

    def test_source_context_and_export_tampering_raise_integrity_errors(self):
        for key,value in [('binders',[]),('mapping',{}),('all_tail_indices',1),
                          ('original_proposition','True'),('factor_range',{})]:
            front=copy.deepcopy(self.front);front[key]=value
            with self.subTest(key=key),self.assertRaises(IntegrityError):self.module.make_candidate(front)
        front=copy.deepcopy(self.front);front['core_request']['input']['goal']['char_zero']=True
        with self.assertRaises(IntegrityError):self.module.translate_candidate(front,self.raw())

    def test_cas_proof_text_is_ignored_and_never_enters_lean_candidate(self):
        raw=self.raw();raw['construction']['certificate']['proof_script']='by sorry'
        raw['construction']['unverified_proof_script']='by exact False.elim (by sorry)'
        result=self.module.translate_candidate(self.front,raw)
        self.assertEqual(result['status'],'candidate_ready',result)
        self.assertNotIn('sorry',result['candidate']['proof_term'])
        self.assertFalse(result['independent_symbolic_check']['cas_proof_text_used'])


if __name__=='__main__': unittest.main()
