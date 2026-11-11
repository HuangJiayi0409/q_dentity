"""Method plumbing tests. Mocked symbolic outputs are never integration evidence."""
import hashlib
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from agent_v2.cas_adapter import MethodAdapter, adapter_result
from agent_v2.executor import normalize_result
from agent_v2.storage import RunStore, load_train


class TelescopingMethodTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='agent-v2-method-unit-')
        self.addCleanup(self.tmp.cleanup)
        self.store = RunStore.create(Path(self.tmp.name) / 'runs')
        self.source = load_train('FQI-SRC-AP-3.3.9', self.store)
        self.requests = []

    def fake_core(self, request, attempt, seconds):
        self.requests.append(request)
        raw = {'schema_version': 1, 'solver': 'q_gosper', 'status': 'constructed',
               'request_sha256': hashlib.sha256(json.dumps(request, sort_keys=True,
                   ensure_ascii=False).encode()).hexdigest(),
               'normalized_input': {'k_shift': 'q*(1-a*X)/(1-q*X)'},
               'result': {'status': 'constructed', 'certificate': '(X - 1)/(X*a - X)',
                          'antidifference_ratio': '(X - 1)/(X*a - X)', 'rational_residual': '0'},
               'original_identity_proved': False, 'unit_test_fixture': True}
        return adapter_result(time.monotonic(), 'symbolic_constructed', 'translation_pending',
                              'Unit test symbolic fixture only', raw_result=raw)

    def execute(self):
        return MethodAdapter().execute(self.source.identity, 'telescoping', self.source.to_dict(),
                                       self.store.root / 'rounds/1/backend', 60.0)

    def test_matching_train_invokes_core_and_emits_only_unverified_local_candidate(self):
        with patch('agent_v2.cas_adapter.CoreAdapter.execute', side_effect=self.fake_core):
            raw = self.execute()
        outcome = normalize_result(raw)
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(self.requests[0]['solver'], 'q_gosper')
        self.assertEqual(outcome.status, 'symbolic_constructed')
        self.assertEqual(len(outcome.C_partial), 1)
        self.assertIsNone(outcome.C_partial[0].closes)
        self.assertEqual(outcome.O_res, ())
        self.assertFalse(outcome.original_identity_proved)
        self.assertEqual(outcome.raw_result['execution_scope'], 'local_certificate_only')
        for name in ['frontend.json', 'mapping.json', 'cas_request.json', 'cas_return.json',
                     'translation.json', 'candidate.json']:
            self.assertTrue((self.store.root / 'rounds/1/backend' / name).is_file(), name)

    def test_constructed_untranslatable_result_has_no_C_partial(self):
        def unsupported(request, attempt, seconds):
            result = self.fake_core(request, attempt, seconds)
            result['raw_result']['result']['certificate'] = '0'
            result['raw_result']['result']['antidifference_ratio'] = '0'
            return result
        with patch('agent_v2.cas_adapter.CoreAdapter.execute', side_effect=unsupported):
            outcome = normalize_result(self.execute())
        self.assertEqual(outcome.C_partial, ())
        self.assertEqual(outcome.O_res, ())
        self.assertEqual(outcome.sigma.code, 'translation_pending')
        self.assertEqual(outcome.raw_result['core']['status'], 'constructed')

    def test_core_environment_failure_is_preserved_without_translation(self):
        failure = adapter_result(time.monotonic(), 'environment_blocked', 'core_unavailable', 'unit fixture')
        with patch('agent_v2.cas_adapter.CoreAdapter.execute', return_value=failure):
            outcome = normalize_result(self.execute())
        self.assertEqual(outcome.status, 'environment_blocked')
        self.assertEqual(outcome.sigma.code, 'core_unavailable')
        self.assertEqual(outcome.C_partial, ())

    def test_snapshot_tampering_rejected_before_core(self):
        Path(self.source.snapshot_path).write_text('tampered original')
        with patch('agent_v2.cas_adapter.CoreAdapter.execute') as core:
            outcome = normalize_result(self.execute())
        core.assert_not_called()
        self.assertEqual(outcome.status, 'integrity_error')
        self.assertEqual(outcome.C_partial, ())

    def test_method_identity_must_match_frozen_source(self):
        with patch('agent_v2.cas_adapter.CoreAdapter.execute') as core:
            result = MethodAdapter().execute('ANOTHER-IDENTITY', 'telescoping', self.source.to_dict(),
                                            self.store.root / 'wrong-identity', 60.0)
        core.assert_not_called()
        self.assertEqual(result['status'], 'integrity_error')

    def test_train_cli_freezes_mathematical_definitions_and_configuration(self):
        from dataclasses import replace
        from agent_v2 import cli
        observed = []
        def capture(state, graph, store, executor, checker):
            observed.append(state)
            return replace(state, status='incomplete')
        args = cli.parser().parse_args(['run', '--identity', self.source.identity, '--seconds', '600'])
        with patch.object(cli, '_production', return_value=(object(), object())), \
                patch('agent_v2.loop.run', side_effect=capture):
            self.assertEqual(cli.train_run(args, self.store), 'incomplete')
        dependencies = {item.path for item in observed[0].G.dependencies}
        for name in ['benchmark/lean/Benchmark/Definitions.lean',
                     'benchmark/lean/Benchmark/Auxiliary.lean',
                     'benchmark/lean/Benchmark/Gaussian.lean',
                     'finite_product_framework/p1/lean/GaussianRules.lean',
                     'project/lake-manifest.json', 'benchmark/lean/lean-toolchain']:
            self.assertIn(str(cli.REPOSITORY / name), dependencies)
        self.assertEqual(observed[0].Gamma, self.source.Gamma)
        self.assertIsNotNone(observed[0].G.proposition)


if __name__ == '__main__':
    unittest.main()
