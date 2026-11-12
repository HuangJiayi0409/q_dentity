"""Real triangular kernel constructor; formal acceptance belongs to common Lean."""
import importlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from agent_v2.executor import normalize_result
from agent_v2.storage import RunStore,load_train


class KernelTransformAdapterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.kernel_transform_adapter'),
                             'source kernel transform adapter is absent')
        self.module=importlib.import_module('agent_v2.kernel_transform_adapter')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.store=RunStore.create(Path(temp.name)/'runs')
        self.source=load_train('FQI-SRC-AQ-3.23',self.store)

    def execute(self,source=None,seconds=30,label='attempt'):
        source=source or self.source
        return normalize_result(self.module.KernelTransformAdapter().execute(source.identity,
            'kernel_transform',source.to_dict(),self.store.path(label),seconds))

    def test_actual_core_produces_one_source_bound_arbitrary_size_candidate(self):
        out=self.execute()
        self.assertEqual(out.status,'symbolic_constructed',out.to_dict())
        self.assertEqual(len(out.C_partial),1)
        self.assertEqual(out.O_res,());self.assertFalse(out.original_identity_proved)
        self.assertEqual(out.raw_result['core']['status'],'constructed')
        self.assertEqual(out.raw_result['core']['method'],'kernel_transform')
        self.assertEqual(out.raw_result['translation']['independent_symbolic_check']['status'],'passed')
        self.assertIs(out.raw_result['translation']['lean_verified'],False)
        self.assertEqual(out.C_partial[0].source_sha256,self.source.sha256)
        self.assertEqual(out.C_partial[0].dependencies,());self.assertIsNone(out.C_partial[0].closes)
        self.assertTrue(out.artifacts)
        front=self.store.read_json('attempt/frontend.json')
        self.assertFalse(front['specializes_bound'])
        self.assertEqual(front['symbols']['bound'],'N')
        self.assertEqual(front['source']['Gamma'],self.source.Gamma)
        mapping=self.store.read_json('attempt/mapping.json')
        self.assertEqual(mapping['mapping'],front['mapping'])
        self.assertFalse(mapping['specializes_bound'])

    def test_real_mismatch_and_identity_mismatch_do_not_call_core(self):
        source=load_train('FQI-GAUSS-ALTERNATING',self.store)
        with patch('agent_v2.symbolic_methods.SymbolicAdapter.execute_request') as core:
            self.assertEqual(self.execute(source).sigma.code,'not_applicable')
            raw=self.module.KernelTransformAdapter().execute('wrong','kernel_transform',source.to_dict(),
                self.store.path('wrong_identity'),30)
            self.assertEqual(raw['status'],'integrity_error');core.assert_not_called()

    def test_budget_and_worker_failure_export_no_candidate(self):
        out=self.execute(seconds=0.000001)
        self.assertEqual(out.status,'budget_exhausted');self.assertEqual(out.C_partial,())
        from agent_v2.cas_adapter import adapter_result
        import time
        # Explicit interface fault injection; not mathematical evidence.
        fake=adapter_result(time.monotonic(),'integrity_error','malformed_construction','worker fixture')
        with patch('agent_v2.symbolic_methods.SymbolicAdapter.execute_request',return_value=fake):
            out=self.execute(label='malformed')
        self.assertEqual(out.status,'integrity_error');self.assertEqual(out.C_partial,())

    def test_standalone_old_and_triangle_requests_remain_nonformal(self):
        from agent_v2.symbolic_methods import example_request
        from agent_v2.kernel_transform_frontend import core_request
        for label,request in [('inverse',example_request('kernel_transform')),('triangle',core_request())]:
            out=normalize_result(self.module.KernelTransformAdapter().execute_request(request,
                self.store.path('standalone_'+label),30))
            with self.subTest(label=label):
                self.assertEqual(out.status,'symbolic_constructed',out.to_dict())
                self.assertEqual(out.C_partial,());self.assertEqual(out.O_res,())
                self.assertFalse(out.original_identity_proved)

    def test_fixed_lean_and_original_definition_dependencies_are_frozen(self):
        dependencies=self.module.dependencies();names={Path(x.path).relative_to(Path(__file__).resolve().parents[2]).as_posix() for x in dependencies}
        self.assertIn('finite_product_framework/kernel_transform/lean/Rules.lean',names)
        self.assertIn('agent_v2/lean/KernelTransformRules.lean',names)
        self.assertIn('benchmark/lean/Benchmark/Definitions.lean',names)
        self.assertFalse(any('Batch4Proofs' in name for name in names))
        self.assertTrue(all(len(x.sha256)==64 for x in dependencies))


if __name__=='__main__':unittest.main()
