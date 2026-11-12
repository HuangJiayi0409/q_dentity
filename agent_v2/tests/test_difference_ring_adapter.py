"""Real difference-ring subprocess and source-preserving pending certificate boundary."""
import importlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from agent_v2.executor import normalize_result
from agent_v2.storage import RunStore,load_train

class DifferenceRingAdapterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.difference_ring_adapter'))
        self.module=importlib.import_module('agent_v2.difference_ring_adapter')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.store=RunStore.create(Path(temp.name)/'runs');self.source=load_train('FQI-SRC-FINE-2.1',self.store)
    def execute(self,source=None,seconds=30,label='attempt'):
        source=source or self.source
        return normalize_result(self.module.DifferenceRingAdapter().execute(source.identity,'difference_ring',
            source.to_dict(),self.store.path(label),seconds))
    def test_real_core_constructs_one_candidate_with_provenance(self):
        out=self.execute();self.assertEqual(out.status,'symbolic_constructed',out.to_dict())
        self.assertEqual(len(out.C_partial),1);self.assertEqual(out.O_res,());self.assertFalse(out.original_identity_proved)
        self.assertEqual(out.raw_result['translation']['independent_symbolic_check']['status'],'passed')
        self.assertIs(out.raw_result['translation']['lean_verified'],False)
        self.assertEqual(out.C_partial[0].source_sha256,self.source.sha256);self.assertEqual(out.C_partial[0].dependencies,())
        self.assertIsNone(out.C_partial[0].closes);self.assertTrue(out.artifacts)
        front=self.store.read_json('attempt/frontend.json');self.assertEqual(front['source']['Gamma'],self.source.Gamma)
        self.assertEqual(front['core_request']['input']['goal']['hypotheses'][0]['name'],'h0')
    def test_mismatch_and_wrong_identity_do_not_call_core(self):
        other=load_train('FQI-GAUSS-ALTERNATING',self.store)
        with patch('agent_v2.symbolic_methods.SymbolicAdapter.execute_request') as core:
            self.assertEqual(self.execute(other).sigma.code,'not_applicable')
            out=self.module.DifferenceRingAdapter().execute('wrong','difference_ring',self.source.to_dict(),self.store.path('wrong'),30)
            self.assertEqual(out['status'],'integrity_error');core.assert_not_called()
    def test_tiny_budget_and_malformed_backend_do_not_export_candidate(self):
        out=self.execute(seconds=0.000001);self.assertEqual(out.status,'budget_exhausted');self.assertEqual(out.C_partial,())
        from agent_v2.cas_adapter import adapter_result
        import time
        # Explicit interface failure injection; not mathematical success evidence.
        fixture=adapter_result(time.monotonic(),'integrity_error','malformed_construction','worker fixture')
        with patch('agent_v2.symbolic_methods.SymbolicAdapter.execute_request',return_value=fixture):out=self.execute(label='bad_worker')
        self.assertEqual(out.status,'integrity_error');self.assertEqual(out.C_partial,())
    def test_standalone_requests_remain_nonformal(self):
        from agent_v2.difference_ring_frontend import core_request
        from agent_v2.symbolic_methods import example_request
        for label,request in [('source_core',core_request()),('legacy',example_request('difference_ring'))]:
            out=normalize_result(self.module.DifferenceRingAdapter().execute_request(request,self.store.path(label),30))
            with self.subTest(label=label):
                self.assertEqual(out.status,'symbolic_constructed',out.to_dict());self.assertEqual(out.C_partial,())
                self.assertEqual(out.O_res,());self.assertFalse(out.original_identity_proved)
    def test_fixed_dependencies_include_source_definitions_and_rules(self):
        deps=self.module.dependencies();names={Path(x.path).name for x in deps}
        self.assertTrue({'Definitions.lean','Auxiliary.lean','DifferenceRingRules.lean','algebra.py'}<=names)
        self.assertFalse(any('Proofs' in name for name in names));self.assertTrue(all(len(x.sha256)==64 for x in deps))
if __name__=='__main__':unittest.main()
