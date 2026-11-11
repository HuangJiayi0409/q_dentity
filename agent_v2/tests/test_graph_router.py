"""Controller behavior fixtures; no benchmark data and no model API."""
import dataclasses
import unittest

from agent_v2.models import (
    Attempt, Budget, ContractError, RepresentationInstance, Source,
    VerifiedCertificate, action_fingerprint, initial_state,
)


def state_fixture():
    source = Source('synthetic', '/unused/source.lean', '/unused/snapshot.lean',
                    'a' * 64, 'Demo.statement', 'theorem source', 'theorem source', 'True')
    state, node = initial_state(source, Budget(30.0, 4))
    return state, dataclasses.replace(node, semantic_domain='Prop')


class GraphRouterTests(unittest.TestCase):
    def graph(self):
        from agent_v2.graph import Graph, Outlet
        state, node = state_fixture()
        graph = Graph(state.G.sha256)
        graph.add_node(node)
        graph.add_outlet(Outlet('cas', node.id, 'CAS', 'method', {'seconds': 20.0},
                                ('closed_prop',), estimated_seconds=1.0))
        return state, graph

    def certified_chain(self):
        """Test-only accepted bridges: original -> child -> grandchild."""
        from agent_v2.graph import Edge, Outlet
        state, graph = self.graph()
        for name, proposition in [('child', 'True ∧ True'), ('grandchild', 'True')]:
            graph.add_node(RepresentationInstance(name, 'closed_prop', {'proposition': proposition},
                'Prop', (), proposition, ('test-fixture',), state.G.sha256))
            graph.add_outlet(Outlet(name + '-cas', name, 'CAS', 'method', {}, ('closed_prop',)))
        first = VerifiedCertificate('first', '(True ∧ True) → (True)', 'fun h => And.left h',
            state.G.sha256, (), {'test_only': True})
        second = VerifiedCertificate('second', '(True) → (True ∧ True)', 'fun h => And.intro h h',
            state.G.sha256, (), {'test_only': True})
        graph.add_edge(Edge('to-child', 'original', 'child', 'split', bridge_certificate='first'))
        graph.add_edge(Edge('to-grandchild', 'child', 'grandchild', 'simplify', bridge_certificate='second'))
        return dataclasses.replace(state, C=(first, second)), graph

    def test_identity_only_exists_at_current_representation(self):
        state, graph = self.certified_chain()
        legal, _ = graph.legal_candidates(state)
        identities = [(a.source, a.target) for a in legal if a.T == 'identity']
        self.assertEqual(identities, [('original', 'original')])

    def test_one_action_cannot_skip_intermediate_transformation(self):
        state, graph = self.certified_chain()
        legal, reasons = graph.legal_candidates(state)
        self.assertEqual([(a.T, a.source, a.target) for a in legal if a.T != 'identity'],
                         [('to-child', 'original', 'child')])
        self.assertFalse(any(a.target == 'grandchild' for a in legal))
        self.assertIn({'route_id': 'grandchild-cas', 'code': 'no_transition_from_current'}, reasons)

    def test_changed_current_node_needs_a_real_back_edge(self):
        from agent_v2.graph import Edge
        state, graph = self.certified_chain()
        state = dataclasses.replace(state, r='child')
        legal, reasons = graph.legal_candidates(state)
        self.assertEqual([(a.source, a.target) for a in legal if a.T == 'identity'], [('child', 'child')])
        self.assertFalse(any(a.target == 'original' for a in legal))
        self.assertIn({'route_id': 'cas', 'code': 'no_transition_from_current'}, reasons)
        self.assertTrue(any(a.T == 'to-grandchild' and a.source == 'child' for a in legal))
        graph.add_edge(Edge('back-to-original', 'child', 'original', 'rebuild', bridge_certificate='second'))
        returned, _ = graph.legal_candidates(state)
        self.assertEqual([(a.T, a.source, a.target) for a in returned if a.target == 'original'],
                         [('back-to-original', 'child', 'original')])

    def test_graph_preserves_history_and_only_appends_new_structure(self):
        from agent_v2.graph import Graph, Outlet
        state, graph = self.graph()
        original = graph.nodes['original']
        previous = graph.to_dict()
        self.assertFalse(graph.expand(state))
        self.assertFalse(graph.add_node(original))
        self.assertEqual(graph.to_dict(), previous)
        graph.add_outlet(Outlet('llm', original.id, 'LLM', 'llm', {}, ('closed_prop',)))
        self.assertIs(graph.nodes['original'], original)
        self.assertEqual(len(graph.history), len(previous['history']) + 1)
        self.assertEqual(Graph.from_dict(graph.to_dict()).to_dict(), graph.to_dict())
        bad = graph.to_dict(); bad['made_up'] = True
        with self.assertRaises(ContractError): Graph.from_dict(bad)
        with self.assertRaises(ContractError):
            graph.add_node(dataclasses.replace(original, payload={'different': True}))

    def test_filters_before_routing_and_budget_does_not_unlock_repeat(self):
        from agent_v2.graph import Outlet
        state, graph = self.graph()
        graph.add_outlet(Outlet('llm', 'original', 'LLM', 'llm', {}, ('closed_prop',)))
        graph.add_outlet(Outlet('wrong-domain', 'original', 'CAS', 'method', {},
                                ('closed_prop',), semantic_domain='Field'))
        graph.add_outlet(Outlet('wrong-kind', 'original', 'CAS', 'core', {}, ('core_request',)))
        legal, reasons = graph.legal_candidates(state)
        self.assertEqual(len(legal), 1)
        self.assertEqual(legal[0].backend, 'method')
        self.assertEqual({r['code'] for r in reasons},
                         {'adapter_disabled', 'semantic_domain_mismatch', 'representation_kind_mismatch'})
        attempted = Attempt(action_fingerprint(state, legal[0]), legal[0].id, 'search_exhausted', 1)
        charged = dataclasses.replace(state, attempts=(attempted,), b=Budget(15.0, 3))
        candidates, reasons = graph.legal_candidates(charged)
        self.assertEqual(candidates, [])
        self.assertIn('duplicate_action', {r['code'] for r in reasons})
        exhausted = dataclasses.replace(state, b=Budget(30.0, 0))
        self.assertEqual(graph.legal_candidates(exhausted)[0], [])

    def test_duplicate_diagnostic_uses_the_matching_attempt_not_global_latest(self):
        state, graph = self.graph()
        action = graph.legal_candidates(state)[0][0]
        fingerprint = action_fingerprint(state, action)
        for history, expected_id, expected_code in [
            ((Attempt(fingerprint, 'renamed-route', 'search_exhausted', 1),
              Attempt('unrelated-state', 'unrelated-route', 'formal_frontend_unavailable', 2)),
             'renamed-route', 'search_exhausted'),
            ((Attempt(fingerprint, 'old-route', 'search_exhausted', 1),
              Attempt(fingerprint, 'newer-alias', 'formal_frontend_unavailable', 2),
              Attempt('unrelated-state', 'unrelated-route', 'search_exhausted', 3)),
             'newer-alias', 'formal_frontend_unavailable'),
        ]:
            with self.subTest(expected_code=expected_code):
                legal, reasons = graph.legal_candidates(dataclasses.replace(state, attempts=history))
                self.assertEqual(legal, [])
                duplicate = next(reason for reason in reasons if reason['code'] == 'duplicate_action')
                self.assertEqual(duplicate['route_id'], action.id)
                self.assertEqual(duplicate.get('attempt_action_id'), expected_id)
                self.assertEqual(duplicate.get('attempt_code'), expected_code)

    def test_unverified_or_wrong_bridge_cannot_enable_transformation(self):
        from agent_v2.graph import Edge, Outlet
        state, graph = self.graph()
        node = RepresentationInstance('child', 'closed_prop', {'proposition': 'True ∧ True'},
                                      'Prop', (), 'True ∧ True', ('transform',), state.G.sha256)
        graph.add_node(node)
        graph.add_edge(Edge('split', 'original', 'child', 'split', bridge_certificate='bridge'))
        graph.add_outlet(Outlet('child-cas', 'child', 'CAS', 'method', {}, ('closed_prop',)))
        legal, reasons = graph.legal_candidates(state)
        self.assertEqual(len(legal), 1)
        self.assertIn('bridge_not_verified', {r['code'] for r in reasons})
        wrong = VerifiedCertificate('bridge', 'False → True', 'fun h => False.elim h',
                                    state.G.sha256, (), {'test_only': True})
        state = dataclasses.replace(state, C=(wrong,))
        self.assertEqual(len(graph.legal_candidates(state)[0]), 1)
        bridge = dataclasses.replace(wrong, proposition='(True ∧ True) → (True)')
        state = dataclasses.replace(state, C=(bridge,))
        legal, _ = graph.legal_candidates(state)
        self.assertTrue(any(action.T == 'split' and action.target == 'child' for action in legal))
        state = dataclasses.replace(state, C=())
        self.assertFalse(any(action.target == 'child' for action in graph.legal_candidates(state)[0]))

    def test_disconnected_nodes_and_index_contracts_are_filtered(self):
        from agent_v2.graph import Outlet
        state, graph = self.graph()
        disconnected = RepresentationInstance('unrelated', 'closed_prop', {'proposition': 'False'},
                                              None, (), 'False', ('candidate',), state.G.sha256)
        graph.add_node(disconnected)
        graph.add_outlet(Outlet('unrelated-out', 'unrelated', 'CAS', 'method', {}, ('closed_prop',)))
        graph.add_outlet(Outlet('needs-range', 'original', 'CAS', 'method', {}, ('closed_prop',),
                                index_ranges=('0..n',)))
        legal, reasons = graph.legal_candidates(state)
        self.assertEqual(len(legal), 1)
        self.assertIn('index_ranges_mismatch', {r['code'] for r in reasons})
        self.assertIn('unreachable_representation', {r['code'] for r in reasons})

    def test_current_pointer_cannot_select_an_unverified_representation(self):
        state, graph = self.graph()
        graph.add_node(RepresentationInstance('unrelated', 'closed_prop', {'proposition': 'False'},
                                              'Prop', (), 'False', ('candidate',), state.G.sha256))
        changed = dataclasses.replace(state, r='unrelated')
        legal, reasons = graph.legal_candidates(changed)
        self.assertEqual(legal, [])
        self.assertIn('current_representation_unverified', {r['code'] for r in reasons})

    def test_identity_conditions_are_not_silently_ignored(self):
        from agent_v2.graph import Edge
        state, graph = self.graph()
        graph.add_edge(Edge('conditional-noop', 'original', 'original', 'identity',
                            conditions=('missing-domain-proof',)))
        legal, reasons = graph.legal_candidates(state)
        self.assertEqual(len(legal), 1)
        self.assertIn('condition_not_verified', {r['code'] for r in reasons})

    def test_invalid_jev_response_never_creates_an_action(self):
        from agent_v2.router import JevRouter, RuleBasedRouter
        state, graph = self.graph()
        legal, _ = graph.legal_candidates(state)
        for response in [
            {'route_id': 'invented', 'confidence': 1.0, 'rationale': 'do it'},
            {'route_id': legal[0].id, 'confidence': 0.1, 'rationale': 'unsure'},
            {'route_id': legal[0].id, 'confidence': True, 'rationale': 'invalid'},
        ]:
            router = JevRouter(lambda s, candidates: response)
            self.assertEqual(router.choose(state, legal), legal[0])
            self.assertIsNotNone(router.last_diagnostic)
        def broken(s, candidates): raise RuntimeError('offline')
        router = JevRouter(broken)
        self.assertEqual(router.choose(state, legal), legal[0])
        self.assertIsNone(router.choose(state, []))
        self.assertEqual(RuleBasedRouter().choose(state, legal), legal[0])

    def test_recovery_distinguishes_budget_environment_and_unknown_math(self):
        from agent_v2.recovery import failure_category, stop_reason
        state, graph = self.graph()
        self.assertEqual(failure_category({'code': 'formal_frontend_unavailable'}), 'environment')
        self.assertEqual(failure_category({'code': 'search_exhausted'}), 'search')
        self.assertEqual(stop_reason(dataclasses.replace(state, b=Budget(0, 3)), [], []),
                         'budget_exhausted')
        self.assertEqual(stop_reason(state, [], [{'code': 'semantic_domain_mismatch'}]), 'incomplete')


if __name__ == '__main__': unittest.main()
