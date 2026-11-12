"""New source adapter tests; only the explicitly marked worker doubles are fake."""
from dataclasses import replace
import importlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from agent_v2.executor import normalize_result
from agent_v2.storage import RunStore,load_train


class CoefficientAdapterTests(unittest.TestCase):
    def setUp(self):
        self.module=importlib.import_module('agent_v2.coefficient_adapter')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.store=RunStore.create(Path(temp.name)/'runs')
        self.source=load_train('FQI-FINITE-Q-BINOMIAL',self.store)

    def execute(self,source=None,seconds=30,label='attempt'):
        source=source or self.source
        return normalize_result(self.module.CoefficientAdapter().execute(source.identity,
            'coefficient',source.to_dict(),self.store.path(label),seconds))

    def test_actual_core_produces_only_one_pending_source_candidate(self):
        out=self.execute()
        self.assertEqual(out.status,'symbolic_constructed',out.to_dict())
        self.assertEqual(len(out.C_partial),1)
        self.assertEqual(out.O_res,())
        self.assertFalse(out.original_identity_proved)
        self.assertIsNone(out.C_partial[0].closes)
        self.assertEqual(out.raw_result['core']['method'],'coefficient')
        self.assertEqual(out.raw_result['core']['status'],'constructed')
        self.assertEqual(out.raw_result['execution_scope'],'local_certificate_only')
        self.assertEqual(out.raw_result['translation']['independent_symbolic_check']['status'],'passed')
        self.assertEqual(out.C_partial[0].source_sha256,self.source.sha256)
        self.assertEqual(self.store.read_json('attempt/method_request.json')['version'],'2.0')
        self.assertTrue(out.artifacts)

    def test_real_mismatch_and_identity_mismatch_never_call_core(self):
        source=load_train('FQI-GAUSS-ALTERNATING',self.store)
        with patch('agent_v2.symbolic_methods.SymbolicAdapter.execute_request') as core:
            self.assertEqual(self.execute(source).sigma.code,'not_applicable')
            raw=self.module.CoefficientAdapter().execute('wrong','coefficient',source.to_dict(),
                self.store.path('wrong_identity'),30)
            self.assertEqual(raw['status'],'integrity_error')
            core.assert_not_called()

    def test_tiny_budget_and_worker_error_do_not_export_candidates(self):
        out=self.execute(seconds=0.000001)
        self.assertEqual(out.status,'budget_exhausted')
        self.assertEqual(out.C_partial,())
        from agent_v2.cas_adapter import adapter_result
        import time
        # Explicit interface fault injection, not mathematical core evidence.
        fake=adapter_result(time.monotonic(),'integrity_error','malformed_construction','worker fixture')
        with patch('agent_v2.symbolic_methods.SymbolicAdapter.execute_request',return_value=fake):
            out=self.execute(label='malformed')
        self.assertEqual(out.status,'integrity_error')
        self.assertEqual(out.sigma.code,'malformed_construction')
        self.assertEqual(out.C_partial,())

    def test_standalone_request_remains_nonformal(self):
        from agent_v2.symbolic_methods import example_request
        raw=self.module.CoefficientAdapter().execute_request(example_request('coefficient'),
            self.store.path('standalone'),30)
        out=normalize_result(raw)
        self.assertEqual(out.status,'symbolic_constructed')
        self.assertEqual(out.C_partial,())
        self.assertEqual(out.O_res,())
        self.assertFalse(out.original_identity_proved)


if __name__=='__main__':unittest.main()
