"""Incremental candidate graph; its edges are never proof evidence by themselves."""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, Literal

from .models import (ContractError, JointAction, Model, RepresentationInstance,
                     action_fingerprint, digest, thaw)


@dataclass(frozen=True)
class Edge(Model):
    id: str
    source: str
    target: str
    mode: str
    conditions: tuple[str, ...] = ()
    bridge_certificate: str | None = None
    estimated_seconds: float = 0.0
    potential_obligations: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()

    def __post_init__(self):
        super().__post_init__()
        if not all((self.id, self.source, self.target, self.mode)) or self.estimated_seconds < 0:
            raise ContractError('invalid edge identity or estimated cost')
        if self.mode == 'identity' and self.source != self.target:
            raise ContractError('identity edge cannot change representation')


@dataclass(frozen=True)
class Outlet(Model):
    id: str
    node: str
    M: Literal['CAS', 'LLM']
    backend: Literal['core', 'method', 'llm']
    parameters: dict[str, Any]
    accepted_kinds: tuple[str, ...]
    semantic_domain: str | None = None
    index_ranges: tuple[str, ...] | None = None
    estimated_seconds: float = 0.01
    handles: tuple[str, ...] = ()
    required_certificates: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()

    def __post_init__(self):
        super().__post_init__()
        if not self.id or not self.node or not self.accepted_kinds or self.estimated_seconds < 0:
            raise ContractError('invalid outlet identity, contract or cost')
        if not set(self.accepted_kinds) <= {'lean_source', 'closed_prop', 'core_request'}:
            raise ContractError('unknown representation contract')
        if (self.M == 'LLM') != (self.backend == 'llm'):
            raise ContractError('method/backend mismatch')
        if 'seconds' in self.parameters:
            value = self.parameters['seconds']
            if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
                raise ContractError('invalid action timeout')


class Graph:
    def __init__(self, source_sha256):
        if not isinstance(source_sha256, str) or not re.fullmatch('[0-9a-f]{64}', source_sha256):
            raise ContractError('invalid source hash')
        self.source_sha256 = source_sha256
        self.nodes = {}
        self.edges = {}
        self.outlets = {}
        self.history = []
        self.failures = {}

    def _add(self, collection, item, kind):
        if item.id in collection:
            if collection[item.id] != item:
                raise ContractError('stable graph ID cannot be rebound')
            return False
        collection[item.id] = item
        self.history.append({'event': 'add_' + kind, 'id': item.id})
        return True

    def add_node(self, node):
        if not isinstance(node, RepresentationInstance) or not node.id:
            raise ContractError('expected typed representation with stable ID')
        if node.source_sha256 != self.source_sha256:
            raise ContractError('representation belongs to another original theorem')
        return self._add(self.nodes, node, 'node')

    def add_edge(self, edge):
        if not isinstance(edge, Edge) or edge.source not in self.nodes or edge.target not in self.nodes:
            raise ContractError('edge endpoints must already be registered')
        return self._add(self.edges, edge, 'edge')

    def add_outlet(self, outlet):
        if not isinstance(outlet, Outlet) or outlet.node not in self.nodes:
            raise ContractError('outlet node must already be registered')
        return self._add(self.outlets, outlet, 'outlet')

    def mark_failure(self, action, code):
        action_id = action.id if isinstance(action, JointAction) else action
        if not isinstance(action_id, str) or not isinstance(code, str):
            raise ContractError('invalid failure record')
        self.failures.setdefault(action_id, []).append(code)
        self.history.append({'event': 'failure', 'id': action_id, 'code': code})

    def expand(self, state):
        # No model expansion, theorem-specific templates or speculative formula
        # synthesis are enabled in this MVP. Caller may register a new checked
        # structural proposal with add_*; a no-op never clears existing history.
        return False

    @staticmethod
    def _proposition(node, state):
        if node.kind != 'closed_prop':
            return None
        if node.id == state.root.id:
            return state.G.proposition
        value = node.payload.get('proposition')
        return value if isinstance(value, str) and value.strip() else None

    def _edge_reason(self, edge, state, certificates):
        source, target = self.nodes[edge.source], self.nodes[edge.target]
        if any(condition not in certificates for condition in edge.conditions):
            return 'condition_not_verified'
        if edge.mode == 'identity':
            return None if source == target else 'invalid_identity_edge'
        cert = certificates.get(edge.bridge_certificate)
        if cert is None:
            return 'bridge_not_verified'
        # Only already kernel-checked closed logical implications are executable
        # transformations in this MVP. Unknown symbolic domains cannot be guessed.
        if source.semantic_domain is None or target.semantic_domain is None:
            return 'unknown_transformation_domain'
        if source.semantic_domain != target.semantic_domain:
            return 'transformation_domain_mismatch'
        source_prop, target_prop = self._proposition(source, state), self._proposition(target, state)
        if source_prop is None or target_prop is None:
            return 'unsupported_transformation_anchor'
        expected = f'({target_prop}) → ({source_prop})'
        if cert.proposition != expected or cert.source_sha256 != self.source_sha256:
            return 'bridge_proposition_mismatch'
        if any(dep not in certificates for dep in cert.dependencies):
            return 'bridge_dependency_unavailable'
        return None

    def legal_candidates(self, state, llm_enabled=False):
        reasons, candidates = [], []
        def reject(route, code, **details):
            reasons.append({'route_id': route, 'code': code, **details})

        if state.G.sha256 != self.source_sha256 or state.Gamma != state.G.Gamma:
            return [], [{'route_id': '*', 'code': 'original_binding_mismatch'}]
        if state.r not in self.nodes or state.root.id not in self.nodes:
            return [], [{'route_id': '*', 'code': 'unregistered_current_or_root'}]
        root = self.nodes[state.root.id]
        if root.lean_anchor != state.G.theorem or root.payload.get('declaration') != state.G.declaration:
            return [], [{'route_id': '*', 'code': 'original_representation_mismatch'}]
        if any(n.source_sha256 != self.source_sha256 for n in self.nodes.values()):
            return [], [{'route_id': '*', 'code': 'representation_binding_mismatch'}]
        certificates = {c.id: c for c in state.C if c.source_sha256 == self.source_sha256}
        edge_reasons = {edge.id: self._edge_reason(edge, state, certificates)
                        for edge in self.edges.values()}
        reachable = {state.root.id}
        changed = True
        while changed:
            changed = False
            for edge in self.edges.values():
                if edge.source in reachable and edge_reasons[edge.id] is None and edge.target not in reachable:
                    reachable.add(edge.target); changed = True
        if state.r not in reachable:
            return [], [{'route_id': '*', 'code': 'current_representation_unverified'}]
        # Root reachability establishes the representation's provenance, not
        # permission to move the current pointer. Each candidate starts at r
        # and contains exactly one conversion plus one method outlet.
        attempts = {attempt.fingerprint: attempt for attempt in state.attempts}
        for outlet in sorted(self.outlets.values(), key=lambda item: item.id):
            target = self.nodes[outlet.node]
            if outlet.backend == 'method' and 'method_version' in outlet.parameters:
                from .method_registry import builtin_registry
                try:
                    spec = builtin_registry().get(outlet.parameters.get('method'))
                except ContractError:
                    reject(outlet.id, 'method_unregistered')
                    continue
                if spec.capability_level == 'L0':
                    reject(outlet.id, 'capability_unavailable')
                    continue
                try:
                    spec.validate_parameters(outlet.parameters)
                except ContractError:
                    reject(outlet.id, 'method_parameter_mismatch')
                    continue
                if target.kind not in spec.accepted_kinds:
                    reject(outlet.id, 'representation_kind_mismatch')
                    continue
            routes = [('identity', state.r, 0.0)] if target.id == state.r else []
            current_edges = [edge for edge in sorted(self.edges.values(), key=lambda item: item.id)
                             if edge.target == target.id and edge.source == state.r]
            for edge in current_edges:
                code = edge_reasons[edge.id]
                if code:
                    reject(edge.id + '/' + outlet.id, code)
                elif edge.mode != 'identity':
                    routes.append((edge.id, state.r, edge.estimated_seconds))
            if not routes and not current_edges:
                reject(outlet.id, 'unreachable_representation' if target.id not in reachable
                       else 'no_transition_from_current')
            for transformation, source_id, transform_cost in routes:
                route_id = 'route-' + digest({'T': transformation, 'source': source_id,
                                             'target': target.id, 'outlet': outlet.id})[:24]
                code = None
                if outlet.M == 'LLM' and not llm_enabled:
                    code = 'adapter_disabled'
                elif target.kind not in outlet.accepted_kinds:
                    code = 'representation_kind_mismatch'
                elif outlet.semantic_domain is not None and target.semantic_domain != outlet.semantic_domain:
                    code = 'semantic_domain_mismatch'
                elif outlet.index_ranges is not None and target.index_ranges != outlet.index_ranges:
                    code = 'index_ranges_mismatch'
                elif any(cert not in certificates for cert in outlet.required_certificates):
                    code = 'required_certificate_unavailable'
                elif outlet.parameters.get('produces_certificate') in certificates:
                    code = 'task_already_completed'
                elif outlet.handles and not set(outlet.handles) & {o.id for o in state.O}:
                    code = 'no_matching_open_obligation'
                elif state.b.actions <= 0 or state.b.seconds <= 0 or \
                        outlet.estimated_seconds + transform_cost > state.b.seconds:
                    code = 'budget_insufficient'
                elif outlet.backend == 'core' and target.kind != 'core_request':
                    code = 'core_input_contract_mismatch'
                if code:
                    reject(route_id, code); continue
                # Preserve theta exactly. Changing a timeout merely because the
                # wall-clock budget was charged must not unlock a duplicate.
                action = JointAction(route_id, transformation, source_id, target.id,
                                     outlet.M, outlet.backend, outlet.parameters)
                attempted = attempts.get(action_fingerprint(state, action))
                if attempted is not None:
                    # Route display IDs may differ for the same semantic action.
                    # Carry the matching attempt so stop classification cannot
                    # accidentally inherit an unrelated route's latest failure.
                    reject(route_id, 'duplicate_action', attempt_action_id=attempted.action_id,
                           attempt_code=attempted.code)
                    continue
                candidates.append(action)
        return candidates, reasons

    def to_dict(self):
        return {'schema_version': 1, 'source_sha256': self.source_sha256,
                'nodes': [node.to_dict() for node in self.nodes.values()],
                'edges': [edge.to_dict() for edge in self.edges.values()],
                'outlets': [outlet.to_dict() for outlet in self.outlets.values()],
                'history': thaw(self.history), 'failures': thaw(self.failures)}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or set(data) != {
                'schema_version', 'source_sha256', 'nodes', 'edges', 'outlets', 'history', 'failures'}:
            raise ContractError('invalid graph fields')
        if type(data['schema_version']) is not int or data['schema_version'] != 1:
            raise ContractError('unsupported graph schema')
        graph = cls(data['source_sha256'])
        for name, model, add in [('nodes', RepresentationInstance, graph.add_node),
                                 ('edges', Edge, graph.add_edge), ('outlets', Outlet, graph.add_outlet)]:
            if not isinstance(data[name], list): raise ContractError('expected graph list')
            for item in data[name]:
                if not add(model.from_dict(item)): raise ContractError('duplicate graph ID')
        if not isinstance(data['history'], list) or not isinstance(data['failures'], dict):
            raise ContractError('invalid graph history')
        for event in data['history']:
            if not isinstance(event, dict) or event.get('event') not in {'add_node', 'add_edge', 'add_outlet', 'failure'}:
                raise ContractError('invalid history event')
            keys = {'event', 'id', 'code'} if event['event'] == 'failure' else {'event', 'id'}
            if set(event) != keys or not all(isinstance(v, str) for v in event.values()):
                raise ContractError('invalid history fields')
        for key, values in data['failures'].items():
            if not isinstance(key, str) or not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                raise ContractError('invalid failure history')
        graph.history = [dict(event) for event in data['history']]
        graph.failures = {key: list(values) for key, values in data['failures'].items()}
        return graph
