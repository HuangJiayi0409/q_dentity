"""Append executable residual work nodes; only checked proof links add structure."""
from collections.abc import Mapping
import math

from .graph import (Edge, Graph, Outlet, obligation_node_matches,
                    proof_tree_obligations)
from .models import ContractError, RepresentationInstance, digest


def _identity(kind, **values):
    return 'autonomous-' + kind + '-' + digest(values)[:24]


def sync_residual_graph(state, graph, capabilities, *, seconds):
    """Append checked decomposition/focus routes and task-bound legal outlets.

    This is a graph synchronization, not a proof update. In particular no open
    sibling is removed when a decomposition makes one of its children selectable.
    Repeated calls retain existing identities, action parameters and history.
    """
    obligations = proof_tree_obligations(state)
    if not isinstance(graph, Graph) or graph.source_sha256 != state.G.sha256:
        raise ContractError('residual graph belongs to another original theorem')
    if type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds <= 0:
        raise ContractError('invalid residual action timeout')
    if not isinstance(capabilities, Mapping):
        raise ContractError('method capabilities must be a mapping')
    if state.r not in obligations:
        raise ContractError('current work node is outside the verified proof tree')
    if state.root.id not in graph.nodes:
        raise ContractError('residual graph lacks the original representation')
    if not obligation_node_matches(graph.nodes[state.root.id], state.root, state):
        raise ContractError('residual original representation mismatch')

    methods = []
    for method, capability in sorted(capabilities.items()):
        if not isinstance(method, str) or not method or not isinstance(capability, Mapping):
            raise ContractError('invalid method capability')
        if capability.get('status', 'applicable') != 'applicable':
            continue
        version = capability.get('version')
        estimate = capability.get('estimated_seconds', 0.01)
        if (not isinstance(version, str) or not version or type(estimate) not in (int, float)
                or not math.isfinite(estimate) or estimate < 0):
            raise ContractError('invalid method capability version or cost')
        methods.append((method, capability, version, estimate))

    pending_nodes = []
    for name, obligation in obligations.items():
        if name == state.root.id:
            continue
        if not isinstance(obligation.proposition, str) or not obligation.proposition.strip():
            raise ContractError('residual work node requires a closed proposition')
        node = RepresentationInstance(name, 'closed_prop',
            {'proposition': obligation.proposition, 'obligation_id': name}, 'Prop', (),
            obligation.lean_anchor, ('verified_proof_tree',), state.G.sha256)
        if name in graph.nodes and graph.nodes[name] != node:
            raise ContractError('residual obligation representation cannot be rebound')
        pending_nodes.append(node)
    for node in pending_nodes:
        graph.add_node(node)

    direct = set()
    for link in state.links:
        for child in link.children:
            direct.add((link.parent.id, child.id))
            graph.add_edge(Edge(_identity('decomposition', source=link.parent.id,
                target=child.id, certificate=link.certificate_id), link.parent.id, child.id,
                'decomposition', bridge_certificate=link.certificate_id,
                potential_obligations=tuple(o.id for o in link.children),
                provenance=('verified_proof_tree',)))
    for obligation in state.O:
        if obligation.id != state.r and (state.r, obligation.id) not in direct:
            graph.add_edge(Edge(_identity('focus', source=state.r, target=obligation.id),
                state.r, obligation.id, 'focus_obligation', provenance=('open_proof_leaf',)))

    known_propositions = {certificate.proposition for certificate in state.C}
    for obligation in state.O:
        node = graph.nodes[obligation.id]
        llm_id = _identity('llm', goal=obligation.id, source=state.G.sha256)
        if llm_id not in graph.outlets:
            graph.add_outlet(Outlet(llm_id, node.id, 'LLM', 'llm',
                {'autonomous': True, 'goal_id': obligation.id, 'seconds': seconds},
                (node.kind,), handles=(obligation.id,), provenance=('autonomous_local_task',)))
        for method, capability, version, estimate in methods:
            local = capability.get('local_proposition')
            if obligation.id != state.root.id and not (
                    capability.get('local_lean') is True and local == obligation.proposition):
                continue
            if isinstance(local, str) and local in known_propositions:
                continue
            cas_id = _identity('cas', goal=obligation.id, source=state.G.sha256,
                               method=method, version=version)
            if cas_id in graph.outlets:
                continue
            parameters = {'autonomous': True, 'goal_id': obligation.id, 'method': method,
                          'version': version, 'seconds': seconds}
            if isinstance(local, str) and local.strip():
                parameters['produces_proposition'] = local
            graph.add_outlet(Outlet(cas_id, node.id, 'CAS', 'method', parameters,
                (node.kind,), estimated_seconds=estimate, handles=(obligation.id,),
                provenance=('source_bound_local_capability',)))
    return graph
