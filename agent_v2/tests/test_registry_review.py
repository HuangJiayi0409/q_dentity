"""Independent registry boundary checks; fake adapters are not proof evidence."""
from dataclasses import replace
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from agent_v2.cas_adapter import MethodAdapter, adapter_result
from agent_v2.graph import Graph, Outlet
from agent_v2.method_registry import MethodRegistry, builtin_registry
from agent_v2.models import Budget, ContractError, initial_state
from agent_v2.storage import RunStore, freeze_source


class RegistryReviewTests(unittest.TestCase):
    def setUp(self):
        self.spec = builtin_registry().get('telescoping')
        self.temp = tempfile.TemporaryDirectory(prefix='qv2-registry-review-')
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        original = root / 'Source.lean'
        original.write_text('theorem demo : True := by sorry\n')
        self.store = RunStore.create(root / 'runs')
        source = freeze_source(original, 'synthetic-registry-review', 'demo', self.store,
                               proposition='True')
        self.state, self.node = initial_state(source, Budget(100, 2))

    def graph(self, method, version):
        graph = Graph(self.state.G.sha256)
        graph.add_node(self.node)
        graph.add_outlet(Outlet('review', self.node.id, 'CAS', 'method',
            {'method': method, 'method_version': version, 'seconds': 10}, ('closed_prop',)))
        return graph

    def l0_registry(self):
        registry = MethodRegistry()
        registry.register(replace(self.spec, capability_level='L0', local_lean=False, full_original=False))
        return registry

    def test_l0_facade_never_invokes_an_adapter_even_when_its_path_exists(self):
        fake = adapter_result(time.monotonic(), 'incomplete', 'test_only', 'No mathematical evidence.')
        with patch('agent_v2.method_registry.builtin_registry', return_value=self.l0_registry()), \
                patch('agent_v2.cas_adapter.TelescopingAdapter.execute', return_value=fake) as backend:
            outcome = MethodAdapter().execute('review', 'telescoping', None,
                                               self.store.path('attempt'), 10)
        self.assertEqual(backend.call_count, 0)
        self.assertEqual(outcome['sigma']['code'], 'capability_unavailable')
        self.assertEqual(outcome['C_partial'], [])

    def test_unregistered_method_is_filtered_before_action_selection(self):
        graph = self.graph('definitely_unregistered', '1')
        legal, reasons = graph.legal_candidates(self.state)
        self.assertEqual(legal, [])
        self.assertTrue(reasons)

    def test_changed_method_version_is_filtered_before_action_selection(self):
        graph = self.graph('telescoping', 'wrong-version')
        legal, reasons = graph.legal_candidates(self.state)
        self.assertEqual(legal, [])
        self.assertTrue(reasons)

    def test_l0_registration_does_not_create_an_executable_graph_route(self):
        graph = self.graph('telescoping', self.spec.version)
        with patch('agent_v2.method_registry.builtin_registry', return_value=self.l0_registry()):
            legal, reasons = graph.legal_candidates(self.state)
        self.assertEqual(legal, [])
        self.assertTrue(reasons)

    def test_malformed_backend_result_is_rejected_by_the_strict_result_contract(self):
        malformed = adapter_result(time.monotonic(), 'incomplete', 'test_only', 'No mathematical evidence.')
        malformed['raw_result'] = []
        with patch('agent_v2.cas_adapter.TelescopingAdapter.execute', return_value=malformed):
            with self.assertRaises(ContractError):
                MethodAdapter().execute('review', 'telescoping', None, self.store.path('attempt'), 10)


if __name__ == '__main__':
    unittest.main()
