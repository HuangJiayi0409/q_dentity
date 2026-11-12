"""Only a bound actual Omega certificate can produce the fixed local candidate."""
import copy
import importlib
from pathlib import Path
import tempfile
import unittest
from agent_v2.storage import RunStore,load_train,IntegrityError
from agent_v2.symbolic_worker import construct
from agent_v2.symbolic_methods import request_digest
from agent_v2.macmahon_frontend import analyze_source


class MacMahonTranslationTests(unittest.TestCase):
    def setUp(self):
        self.module=importlib.import_module('agent_v2.macmahon_translation')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        store=RunStore.create(Path(temp.name)/'runs')
        self.front=analyze_source(load_train('FQI-SRC-GR2-7.Ex14',store).to_dict(),store.root)
        request=self.front['core_request']
        self.raw={'schema_version':1,'method':'macmahon','status':'constructed','original_identity_proved':False,
                  'request_sha256':request_digest(request),'construction':construct('macmahon',request['input'])}
    def test_actual_omega_result_produces_denominator_and_coefficient_conjunction(self):
        out=self.module.translate_candidate(self.front,self.raw)
        self.assertEqual(out['status'],'candidate_ready',out)
        c=out['candidate'];self.assertIn('PowerSeries.C',c['proposition']);self.assertIn('PowerSeries.coeff',c['proposition'])
        self.assertIn('(z : ℂ)',c['proposition']);self.assertIn('(hq : (FiniteQBenchmark.regular q))',c['proposition'])
        self.assertNotIn('Type u',c['proposition']);self.assertIn('source_realization z n hz',c['proof_term'])
        self.assertEqual(c['dependencies'],[]);self.assertIsNone(c['closes']);self.assertEqual(c['replaces'],[])
        self.assertFalse(out['lean_verified']);self.assertFalse(out['original_identity_proved'])
    def test_incorrect_rational_result_never_produces_a_candidate(self):
        raw=copy.deepcopy(self.raw);raw['construction']['result']['value']='0'
        out=self.module.translate_candidate(self.front,raw)
        self.assertEqual(out['status'],'translation_pending');self.assertNotIn('candidate',out)
    def test_request_and_method_mismatch_are_translation_pending(self):
        for key,value in [('request_sha256','0'*64),('method','interpolation'),('original_identity_proved',True)]:
            raw=copy.deepcopy(self.raw);raw[key]=value
            with self.subTest(key=key):self.assertEqual(self.module.translate_candidate(self.front,raw)['status'],'translation_pending')
    def test_frontend_and_original_target_mutation_are_integrity_errors(self):
        for key,value in [('original_proposition','True'),('universe_parameters',['u'])]:
            front=copy.deepcopy(self.front);front[key]=value
            with self.assertRaises(IntegrityError):self.module.translate_candidate(front,self.raw)
    def test_untrusted_proof_text_cannot_override_the_template(self):
        raw=copy.deepcopy(self.raw);raw['proof_script']='by sorry'
        out=self.module.translate_candidate(self.front,raw)
        self.assertEqual(out['status'],'candidate_ready',out);self.assertNotIn('sorry',out['candidate']['proof_term'])

if __name__=='__main__':unittest.main()
