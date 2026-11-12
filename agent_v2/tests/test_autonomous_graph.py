"""Synthetic control fixtures; they are not Lean or model success evidence."""
from dataclasses import replace
import unittest

from agent_v2.executor import connection_type
from agent_v2.graph import Edge, Graph, Outlet
from agent_v2.models import (ContractError, Obligation, ProofLink,
                             RepresentationInstance, VerifiedCertificate)
from agent_v2.tests.test_graph_router import state_fixture


class AutonomousGraphTests(unittest.TestCase):
    def fixture(self):
        state, root = state_fixture()
        graph = Graph(state.G.sha256); graph.add_node(root)
        children = tuple(Obligation(name, 'subgoal', prop, prop, state.G.sha256)
                         for name, prop in [('a', 'True'), ('b', 'True ∧ True')])
        cert = VerifiedCertificate('split', connection_type(state.root, children),
            'by intros; trivial', state.G.sha256, (),
            {'source_sha256': state.G.sha256, 'proposition': connection_type(state.root, children)})
        state = replace(state, C=(cert,), O=children,
                        links=(ProofLink(state.root, children, cert.id),))
        return state, graph

    def test_checked_multi_child_decomposition_is_navigable(self):
        from agent_v2.graph_builder import sync_residual_graph
        state, graph = self.fixture()
        sync_residual_graph(state, graph, {}, seconds=20)
        legal, _ = graph.legal_candidates(state, llm_enabled=True)
        self.assertTrue(any(a.target == 'a' and a.T != 'identity' for a in legal))
        self.assertTrue(any(a.target == 'b' and a.T != 'identity' for a in legal))
        previous = graph.to_dict()
        sync_residual_graph(state, graph, {}, seconds=20)
        self.assertEqual(previous, graph.to_dict())

    def test_explicit_focus_moves_between_known_obligations(self):
        from agent_v2.graph_builder import sync_residual_graph
        state, graph = self.fixture()
        state = replace(state, r='a')
        sync_residual_graph(state, graph, {}, seconds=20)
        legal, _ = graph.legal_candidates(state, llm_enabled=True)
        actions = [a for a in legal if a.target == 'b']
        self.assertTrue(actions)
        self.assertTrue(all(graph.edges[a.T].mode == 'focus_obligation' for a in actions))
        self.assertTrue(all(a.source == 'a' and a.T != 'identity' for a in actions))

    def test_forged_decomposition_and_focus_are_rejected(self):
        from agent_v2.graph_builder import sync_residual_graph
        state, graph = self.fixture()
        sync_residual_graph(state, graph, {}, seconds=20)
        changed = replace(state, links=())
        self.assertFalse(any(a.target in ('a', 'b') for a in graph.legal_candidates(changed, True)[0]))
        graph.add_node(RepresentationInstance('foreign', 'closed_prop', {'proposition':'False'},
                       'Prop', (), 'False', (), state.G.sha256))
        graph.add_edge(Edge('bad-focus', 'original', 'foreign', 'focus_obligation'))
        graph.add_outlet(Outlet('bad', 'foreign', 'LLM', 'llm', {}, ('closed_prop',)))
        legal, reasons = graph.legal_candidates(state, True)
        self.assertFalse(any(a.target == 'foreign' for a in legal))
        self.assertIn('unregistered_focus_obligation', {r['code'] for r in reasons})

    def test_cas_outlet_on_child_requires_exact_local_goal(self):
        from agent_v2.graph_builder import sync_residual_graph
        state, graph = self.fixture()
        capabilities = {'telescoping': {'local_proposition': 'True', 'version': '2.0',
                                      'estimated_seconds': 1, 'local_lean': True}}
        sync_residual_graph(state, graph, capabilities, seconds=20)
        legal, _ = graph.legal_candidates(state, True)
        self.assertTrue(any(a.M == 'CAS' and a.target == 'a' for a in legal))
        self.assertFalse(any(a.M == 'CAS' and a.target == 'b' for a in legal))

    def test_decomposition_retains_every_open_child_and_root_attributes(self):
        from agent_v2.graph_builder import sync_residual_graph
        state, graph = self.fixture()
        root = replace(graph.nodes['original'], semantic_domain=None)
        graph.nodes['original'] = root
        before = state.to_dict()
        sync_residual_graph(state, graph, {}, seconds=20)
        self.assertEqual(state.to_dict(), before)
        self.assertIs(graph.nodes['original'], root)
        self.assertEqual({o.id for o in state.O}, {'a', 'b'})
        self.assertEqual(graph.nodes['a'].payload['obligation_id'], 'a')
        self.assertTrue(any(a.target == 'a' for a in graph.legal_candidates(state, True)[0]))

    def test_invalid_proof_tree_cannot_partly_mutate_graph(self):
        from agent_v2.graph_builder import sync_residual_graph
        state, graph = self.fixture()
        before = graph.to_dict()
        with self.assertRaises(ContractError):
            sync_residual_graph(replace(state, C=()), graph, {}, seconds=20)
        self.assertEqual(graph.to_dict(), before)

    def test_forged_proof_tree_is_rejected_even_before_autonomous_outlets_exist(self):
        state, graph = self.fixture()
        graph.add_outlet(Outlet('old-root', 'original', 'CAS', 'method', {}, ('closed_prop',)))
        forged = replace(state, C=())
        self.assertEqual(graph.legal_candidates(forged)[0], [])

    def test_same_lemma_suppresses_existing_and_new_cas_outlets(self):
        from agent_v2.graph_builder import sync_residual_graph
        state, graph = self.fixture()
        capability = {'telescoping': {'local_proposition': 'True', 'version': '2.0',
                                     'local_lean': True, 'estimated_seconds': 1}}
        sync_residual_graph(state, graph, capability, seconds=20)
        self.assertTrue(any(a.M == 'CAS' for a in graph.legal_candidates(state, True)[0]))
        lemma = VerifiedCertificate('independent', 'True', 'True.intro', state.G.sha256,
            (), {'source_sha256':state.G.sha256, 'proposition':'True'})
        state = replace(state, C=state.C + (lemma,))
        previous = graph.to_dict()
        sync_residual_graph(state, graph, capability, seconds=5)
        self.assertEqual(graph.to_dict(), previous)
        self.assertFalse(any(a.M == 'CAS' for a in graph.legal_candidates(state, True)[0]))
        fresh = Graph(state.G.sha256); fresh.add_node(graph.nodes['original'])
        sync_residual_graph(state, fresh, capability, seconds=5)
        self.assertFalse(any(o.M == 'CAS' for o in fresh.outlets.values()))

    def test_forged_child_payload_cannot_enable_focus_or_identity(self):
        from agent_v2.graph_builder import sync_residual_graph
        state, graph = self.fixture()
        sync_residual_graph(state, graph, {}, seconds=20)
        graph.nodes['a'] = replace(graph.nodes['a'],
            payload={'proposition':'False', 'obligation_id':'a'})
        self.assertFalse(any(a.target == 'a' for a in graph.legal_candidates(state, True)[0]))
        current = replace(state, r='a')
        self.assertEqual(graph.legal_candidates(current, True)[0], [])

    def test_focus_cannot_reopen_a_closed_proof_tree_node(self):
        from agent_v2.graph_builder import sync_residual_graph
        state, graph = self.fixture()
        sync_residual_graph(replace(state, r='b'), graph, {}, seconds=20)
        leaf = state.O[0]
        cert = VerifiedCertificate('close-a', 'True', 'True.intro', state.G.sha256,
            (), {'source_sha256':state.G.sha256, 'proposition':'True'})
        state = replace(state, r='b', C=state.C + (cert,), O=(state.O[1],),
                        links=state.links + (ProofLink(leaf, (), cert.id),))
        self.assertFalse(any(a.target == 'a' for a in graph.legal_candidates(state, True)[0]))

    def test_root_offers_multiple_bound_methods_without_old_fixed_contract(self):
        from agent_v2.graph_builder import sync_residual_graph
        state, root = state_fixture()
        graph = Graph(state.G.sha256); graph.add_node(root)
        capabilities = {name: {'version':'2.0', 'local_proposition':'True ∧ True',
                              'local_lean':True, 'estimated_seconds':1}
                        for name in ('telescoping', 'recurrence')}
        sync_residual_graph(state, graph, capabilities, seconds=20)
        actions = [a for a in graph.legal_candidates(state, True)[0] if a.M == 'CAS']
        self.assertEqual({a.theta['method'] for a in actions}, {'telescoping', 'recurrence'})
        self.assertTrue(all(a.theta['goal_id'] == 'original' and a.theta['autonomous'] is True
                            and 'method_version' not in a.theta for a in actions))
        self.assertTrue(all(graph.outlets[o].handles == ('original',) for o in graph.outlets))

    def test_decomposition_edge_cannot_claim_a_different_bridge(self):
        from agent_v2.graph_builder import sync_residual_graph
        state, graph = self.fixture()
        sync_residual_graph(state, graph, {}, seconds=20)
        graph.add_edge(Edge('forged-split', 'original', 'a', 'decomposition',
                            bridge_certificate='missing'))
        legal, reasons = graph.legal_candidates(state, True)
        self.assertFalse(any(a.T == 'forged-split' for a in legal))
        self.assertTrue(any(r['route_id'].startswith('forged-split/') for r in reasons))


if __name__ == '__main__':
    unittest.main()
