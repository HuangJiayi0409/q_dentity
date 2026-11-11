"""Method capability declarations do not stand in for proof evidence."""
from dataclasses import replace
import importlib.util
import unittest


class MethodRegistryTests(unittest.TestCase):
    def registry(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.method_registry'))
        from agent_v2.method_registry import MethodRegistry, builtin_registry
        return MethodRegistry, builtin_registry()

    def test_unique_ids_and_real_implementations(self):
        cls, registry = self.registry()
        spec = registry.get('telescoping')
        self.assertEqual(spec.capability_level, 'L3')
        self.assertTrue(callable(spec.factory()))
        empty = cls()
        empty.register(spec)
        with self.assertRaises(ValueError): empty.register(spec)
        with self.assertRaises(ValueError): registry.get('unknown')

    def test_missing_adapter_and_false_capability_are_rejected(self):
        cls, registry = self.registry()
        spec = registry.get('telescoping')
        with self.assertRaises(ValueError):
            cls().register(replace(spec, adapter='agent_v2.no_such_module:Adapter'))
        with self.assertRaises(ValueError):
            replace(spec, local_lean=False)

    def test_strict_parameters_and_versions(self):
        _, registry = self.registry()
        spec = registry.get('telescoping')
        spec.validate_parameters({'method': 'telescoping', 'method_version': spec.version,
                                  'seconds': 120, 'scope': 'full', 'task': 'bridge'})
        for values in ({'seconds': -1}, {'seconds': float('inf')}, {'seconds': True},
                       {'method': 'unknown'}, {'method_version': 'wrong'}, {'scope': 'all'},
                       {'task': 'run_everything'}, {'unregistered_parameter': 1}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                spec.validate_parameters(values)

    def test_cli_method_choices_and_inventory_come_from_registry(self):
        import contextlib, io, json
        from agent_v2 import cli
        _, registry = self.registry()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(['methods']), 0)
        entries = json.loads(output.getvalue())['methods']
        self.assertEqual({entry['id'] for entry in entries}, set(registry.ids()))
        for identity in registry.ids():
            args = cli.parser().parse_args(['run', '--identity', 'Train', '--method', identity])
            self.assertEqual(args.method, identity)

    def test_method_facade_returns_strict_normalized_capability_metadata(self):
        from pathlib import Path
        import tempfile
        from agent_v2.cas_adapter import MethodAdapter
        from agent_v2.executor import normalize_result
        _, registry = self.registry()
        with tempfile.TemporaryDirectory() as directory:
            result = normalize_result(MethodAdapter().execute('synthetic', 'telescoping', None,
                                                              Path(directory) / 'attempt', 10))
        self.assertEqual(result.raw_result['method_id'], 'telescoping')
        self.assertEqual(result.raw_result['method_version'], registry.get('telescoping').version)
        self.assertEqual(result.C_partial, ())
        self.assertEqual(result.O_res, ())
        self.assertFalse(result.original_identity_proved)

    def test_mismatched_train_has_no_registered_executable_outlet(self):
        from pathlib import Path
        import tempfile
        from agent_v2 import cli
        from agent_v2.storage import RunStore
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore.create(Path(directory))
            args = cli.parser().parse_args(['run', '--identity', 'FQI-GAUSS-ALTERNATING',
                                            '--method', 'telescoping', '--seconds', '30'])
            self.assertEqual(cli.train_run(args, store), 'incomplete')
            self.assertEqual(store.read_json('run.json')['stop_reason'], 'not_applicable')
            self.assertEqual(store.read_json('graph.json')['outlets'], [])
            self.assertEqual(store.load_checkpoint()['state']['b']['actions'], 1)

    def test_l2_cannot_claim_formal_candidates_even_if_wire_shape_is_valid(self):
        from agent_v2.cas_adapter import MethodAdapter
        from agent_v2.models import Candidate
        from agent_v2.tests.test_executor import result
        _, registry = self.registry()
        candidate = Candidate('untrusted', 'True', 'by exact True.intro',
                              'AgentV2Candidate.proof', '0' * 64)
        with self.assertRaises(ValueError):
            MethodAdapter._annotate(result([candidate]).to_dict(), registry.get('coefficient'))

    def test_explicit_core_representation_runs_actual_registered_core_without_proofs(self):
        from pathlib import Path
        import tempfile
        from agent_v2.cas_adapter import MethodAdapter
        from agent_v2.executor import Executor, verify_and_update
        from agent_v2.graph import Graph, Outlet
        from agent_v2.models import Budget, initial_state
        from agent_v2.storage import RunStore, freeze_source
        from agent_v2.symbolic_methods import example_request
        from agent_v2.tests.test_executor import RecordingChecker
        _, registry = self.registry()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'Source.lean'; path.write_text('theorem demo : True := by sorry\n')
            store = RunStore.create(root / 'runs')
            source = freeze_source(path, 'synthetic-core-exploration', 'demo', store, proposition='True')
            state, node = initial_state(source, Budget(30, 1))
            node = replace(node, kind='core_request', payload={'declaration': source.declaration,
                            'request': example_request('coefficient')})
            graph = Graph(source.sha256); graph.add_node(node)
            graph.add_outlet(Outlet('coefficient', node.id, 'CAS', 'method',
                {'method': 'coefficient', 'method_version': registry.get('coefficient').version},
                ('core_request',)))
            action = graph.legal_candidates(state)[0][0]
            result = Executor({'method': MethodAdapter()}).execute(state, action, graph, store.path('attempt'))
            self.assertEqual(result.status, 'symbolic_constructed')
            checker = RecordingChecker()
            after, _ = verify_and_update(state, action, result, checker, {
                'run_dir': str(store.root), 'attempt_dir': str(store.path('check')), 'seconds': 10})
            self.assertEqual(after.O, state.O)
            self.assertEqual(after.C, ())
            self.assertEqual(checker.seen, [])


if __name__ == '__main__':
    unittest.main()
