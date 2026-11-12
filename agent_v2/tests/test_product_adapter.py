"""Real bounded Source worker, without a formal certificate or obligation."""
import importlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from agent_v2.executor import normalize_result
from agent_v2.storage import RunStore,load_train,sha256_file


class ProductAdapterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.product_adapter'))
        self.module=importlib.import_module('agent_v2.product_adapter')
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        self.store=RunStore.create(Path(temporary.name)/'runs');self.source=load_train('FQI-POCHHAMMER-RESIDUES',self.store)
    def execute(self,source=None,seconds=30,label='attempt'):
        source=source or self.source
        return normalize_result(self.module.ProductAdapter().execute(source.identity,'product',source.to_dict(),self.store.path(label),seconds))
    def test_actual_source_worker_constructs_checked_map_but_no_formal_state(self):
        result=self.execute();self.assertEqual(result.status,'symbolic_constructed',result.to_dict())
        self.assertEqual(result.sigma.code,'translation_pending')
        self.assertEqual(result.C_partial,());self.assertEqual(result.O_res,());self.assertFalse(result.original_identity_proved)
        self.assertEqual(result.raw_result['execution_scope'],'source_symbolic_only')
        self.assertEqual(result.raw_result['independent_symbolic_check']['status'],'passed')
        self.assertEqual(self.store.read_json('attempt/frontend.json')['source'],self.source.to_dict())
        process=self.store.read_json('attempt/core/process.json')
        self.assertEqual(process['returncode'],0);self.assertFalse(process['timed_out']);self.assertEqual(process['cleanup_survivors'],[])
        self.assertGreater(result.cost.wall_seconds,0)
        for artifact in result.artifacts:self.assertEqual(sha256_file(artifact.path),artifact.sha256)
        self.assertFalse(hasattr(self.module.ProductAdapter(),'execute_request'))
    def test_real_mismatch_and_wrong_identity_do_not_spawn_core(self):
        other=load_train('FQI-GAUSS-ALTERNATING',self.store)
        with patch('agent_v2.product_adapter.run_process') as process:
            self.assertEqual(self.execute(other).sigma.code,'not_applicable')
            result=self.module.ProductAdapter().execute('wrong','product',self.source.to_dict(),self.store.path('wrong'),30)
            self.assertEqual(result['status'],'integrity_error');process.assert_not_called()
    def test_actual_tiny_budget_never_exports_formal_objects(self):
        result=self.execute(seconds=0.000001)
        self.assertEqual(result.status,'budget_exhausted');self.assertEqual(result.C_partial,());self.assertEqual(result.O_res,())
    def test_malformed_worker_output_is_an_integrity_failure(self):
        real_run=self.module.run_process
        def damage(*args,**kwargs):
            process=real_run(*args,**kwargs)
            output=Path(args[0][-1]);raw=json.loads(output.read_text());raw['request_sha256']='0'*64
            output.write_text(json.dumps(raw));return process
        with patch('agent_v2.product_adapter.run_process',side_effect=damage):result=self.execute()
        self.assertEqual(result.status,'integrity_error');self.assertEqual(result.C_partial,())
    def test_dependencies_bind_actual_pure_core_and_definition(self):
        paths={Path(a.path).name for a in self.module.dependencies()}
        self.assertTrue({'index_construct.py','Definitions.lean','product_worker.py','product_check.py'}<=paths)
        self.assertFalse(any('Proofs' in name for name in paths))


if __name__=='__main__':unittest.main()
