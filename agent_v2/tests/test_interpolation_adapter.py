"""New interpolation adapter exercises retained core and bounded failures."""
import importlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from agent_v2.executor import normalize_result
from agent_v2.storage import RunStore,load_train


class InterpolationAdapterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.interpolation_adapter'),
                             'source interpolation adapter is absent')
        self.module=importlib.import_module('agent_v2.interpolation_adapter')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.store=RunStore.create(Path(temp.name)/'runs')
        self.source=load_train('FQI-SRC-GR2-I-20',self.store)

    def execute(self,source=None,seconds=30,label='attempt'):
        source=source or self.source
        return normalize_result(self.module.InterpolationAdapter().execute(source.identity,
            'interpolation',source.to_dict(),self.store.path(label),seconds))

    def test_actual_core_produces_one_pending_local_candidate(self):
        out=self.execute()
        self.assertEqual(out.status,'symbolic_constructed',out.to_dict())
        self.assertEqual(len(out.C_partial),1);self.assertEqual(out.O_res,())
        self.assertFalse(out.original_identity_proved);self.assertIsNone(out.C_partial[0].closes)
        self.assertEqual(out.raw_result['core']['method'],'interpolation')
        self.assertEqual(out.raw_result['core']['construction']['certificate']['degree_upper_bound'],1)
        self.assertEqual(out.raw_result['translation']['independent_symbolic_check']['status'],'passed')
        self.assertEqual(out.C_partial[0].source_sha256,self.source.sha256)
        self.assertTrue(out.artifacts)

    def test_mismatch_and_identity_mismatch_do_not_execute_core(self):
        source=load_train('FQI-FINITE-Q-BINOMIAL',self.store)
        with patch('agent_v2.symbolic_methods.SymbolicAdapter.execute_request') as core:
            self.assertEqual(self.execute(source).sigma.code,'not_applicable')
            raw=self.module.InterpolationAdapter().execute('wrong','interpolation',source.to_dict(),
                self.store.path('wrong_identity'),30)
            self.assertEqual(raw['status'],'integrity_error');core.assert_not_called()

    def test_budget_exhaustion_or_worker_failure_exports_no_candidate(self):
        out=self.execute(seconds=0.000001)
        self.assertEqual(out.status,'budget_exhausted');self.assertEqual(out.C_partial,())
        from agent_v2.cas_adapter import adapter_result
        import time
        # Explicit transport fault fixture; never counted as mathematical evidence.
        fake=adapter_result(time.monotonic(),'integrity_error','malformed_construction','worker fixture')
        with patch('agent_v2.symbolic_methods.SymbolicAdapter.execute_request',return_value=fake):
            out=self.execute(label='malformed')
        self.assertEqual(out.status,'integrity_error');self.assertEqual(out.C_partial,())

    def test_standalone_core_request_never_becomes_formal(self):
        from agent_v2.symbolic_methods import example_request
        out=normalize_result(self.module.InterpolationAdapter().execute_request(
            example_request('interpolation'),self.store.path('standalone'),30))
        self.assertEqual(out.status,'symbolic_constructed',out.to_dict())
        self.assertEqual(out.C_partial,());self.assertEqual(out.O_res,())
        self.assertFalse(out.original_identity_proved)


if __name__=='__main__':unittest.main()
