"""Single-action execution and constructive, transactional residual updates."""
from dataclasses import replace
from pathlib import Path
import time

from .models import (Artifact, Candidate, ContractError, Cost, ExecutionResult,
                     FailureSignature, Obligation, ProofLink, VerifiedCertificate,
                     canonical, thaw)
from .storage import IntegrityError, guard_path, sha256_file, verify_source


def connection_type(parent, children):
    if parent.proposition is None or any(child.proposition is None for child in children):
        raise ContractError('formal closed proposition unavailable')
    if not children:
        return parent.proposition
    return ' → '.join(f'({o.proposition})' for o in (*children, parent))


def validate_invariant(state):
    """Reconstruct a proof tree of (open leaves -> unchanged original G).

    The initial tree is the identity G -> G. Every internal node must carry
    a checked theorem children -> parent. Its leaves must be exactly O.
    Certificates not used in this tree remain independent progress in C.
    """
    if state.Gamma != state.G.Gamma:
        raise ContractError('context changed')
    expected_root = Obligation('original', 'original', state.G.proposition,
                               state.G.theorem, state.G.sha256)
    if state.root != expected_root:
        raise ContractError('root is not the original theorem')
    certificates = {}
    for cert in state.C:
        if cert.id in certificates or cert.source_sha256 != state.G.sha256:
            raise ContractError('duplicate or foreign certificate')
        if any(dep not in certificates for dep in cert.dependencies):
            raise ContractError('missing or cyclic certificate dependency')
        if cert.evidence.get('source_sha256') != state.G.sha256 or cert.evidence.get('proposition') != cert.proposition:
            raise ContractError('certificate evidence binding mismatch')
        certificates[cert.id] = cert
    links = {link.parent.id: link for link in state.links}
    if len(links) != len(state.links):
        raise ContractError('duplicate derivation parent')
    leaves, visited, active = {}, set(), set()
    nodes = {}

    def visit(node):
        if node.source_sha256 != state.G.sha256 or node.id in active:
            raise ContractError('foreign obligation or cyclic derivation')
        if node.id in nodes and nodes[node.id] != node:
            raise ContractError('obligation ID has inconsistent semantics')
        nodes[node.id] = node
        if node.id in visited:
            return
        active.add(node.id)
        link = links.get(node.id)
        if link is None:
            leaves[node.id] = node
        else:
            cert = certificates.get(link.certificate_id)
            if link.parent != node or cert is None or cert.proposition != connection_type(node, link.children):
                raise ContractError('unjustified conditional proof link')
            if len({o.id for o in link.children}) != len(link.children):
                raise ContractError('duplicate child obligation')
            for child in link.children:
                visit(child)
        active.remove(node.id); visited.add(node.id)

    visit(state.root)
    if set(links) - visited:
        raise ContractError('unreachable proof link')
    if len({o.id for o in state.O}) != len(state.O) or leaves != {o.id: o for o in state.O}:
        raise ContractError('open obligations differ from reachable proof leaves')


def assemble_term(state):
    validate_invariant(state)
    if state.O:
        raise ContractError('cannot assemble with open obligations')
    links = {link.parent.id: link for link in state.links}
    certificates = {c.id: c for c in state.C}

    def build(node):
        link = links[node.id]
        term = f'({certificates[link.certificate_id].proof_term})'
        return ' '.join([term, *(f'({build(child)})' for child in link.children)])

    return build(state.root)


def _candidate_request(candidate):
    return {key: thaw(getattr(candidate, key)) for key in
            ('id', 'proposition', 'proof_term', 'theorem', 'source_sha256', 'dependencies')}


def validate_action_origin(state, action):
    """Even a stale/forged route must not relocate r through an identity."""
    if action.source != state.r:
        raise ContractError('action source is not the current representation')
    if action.T == 'identity' and action.target != state.r:
        raise ContractError('identity action cannot change the current representation')


def verify_and_update(state, action, result, checker, context):
    validate_action_origin(state, action)
    verify_source(state.G, context['run_dir'])
    validate_invariant(state)
    certificates = {cert.id: cert for cert in state.C}
    accepted, diagnostics, closure_candidates = [], [], []
    deadline = time.monotonic() + min(context['seconds'], state.b.seconds)
    for candidate in result.C_partial:
        if candidate.source_sha256 != state.G.sha256 or candidate.id in certificates or any(
                dep not in certificates for dep in candidate.dependencies):
            diagnostics.append({'code': 'candidate_binding_rejected', 'id': candidate.id})
            continue
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            diagnostics.append({'code': 'verification_budget_exhausted'})
            break
        check_context = dict(context, seconds=remaining,
            attempt_dir=str(Path(context['attempt_dir']) / 'lean' / ('candidate-' + str(len(diagnostics)))),
            approved_certificates={key: value.to_dict() for key, value in certificates.items()})
        try:
            checked = checker.check_partial(_candidate_request(candidate), check_context)
            if not isinstance(checked, dict):
                raise ContractError('checker result must be an object')
        except Exception as error:
            diagnostics.append({'id': candidate.id, 'code': 'partial_checker_exception',
                                'message': str(error), 'type': type(error).__name__})
            continue
        diagnostics.append({'id': candidate.id, 'check': checked})
        if checked.get('accepted') is not True or checked.get('status') != 'partial_lean_verified':
            continue
        evidence = checked.get('evidence', {})
        if evidence.get('source_sha256') != state.G.sha256 or evidence.get('proposition') != candidate.proposition:
            diagnostics.append({'code': 'checker_binding_rejected', 'id': candidate.id})
            continue
        cert = VerifiedCertificate(candidate.id, candidate.proposition, candidate.proof_term,
                                   candidate.source_sha256, candidate.dependencies, evidence)
        certificates[cert.id] = cert; accepted.append(cert)
        if candidate.closes is not None:
            closure_candidates.append(candidate)

    # Even when a proposed graph update is invalid, these independent theorems
    # retain their actual kernel evidence. No obligation is removed by this step.
    safe = replace(state, C=state.C + tuple(accepted))
    validate_invariant(safe)
    try:
        obligations = {o.id: o for o in state.O}
        links = list(state.links)
        introduced = {}
        for candidate in closure_candidates:
            parent = obligations.get(candidate.closes)
            if parent is None or candidate.proposition != connection_type(parent, candidate.replaces):
                raise ContractError('candidate does not prove requested connection')
            for child in candidate.replaces:
                if child.id in obligations or child.id in introduced or child.id == state.root.id:
                    raise ContractError('obligation identity collision')
                introduced[child.id] = child
            del obligations[parent.id]
            obligations.update({child.id: child for child in candidate.replaces})
            links.append(ProofLink(parent, candidate.replaces, candidate.id))
        if introduced != {o.id: o for o in result.O_res} or len(introduced) != len(result.O_res):
            raise ContractError('remaining obligations lack a verified connection')
        updated = replace(safe, r=action.target, O=tuple(obligations.values()), links=tuple(links))
        validate_invariant(updated)
    except ContractError as error:
        diagnostics.append({'code': 'invariant_update_rejected', 'message': str(error)})
        updated = safe
    verify_source(state.G, context['run_dir'])
    return updated, diagnostics


def normalize_result(raw):
    """Boundary objects are strict, including unknown fields and enum values."""
    if not isinstance(raw, dict):
        raise ContractError('adapter result must be an object')
    data = dict(raw)
    def nested(cls, value):
        if isinstance(value, cls): return value
        return cls.from_dict(value if 'schema_version' in value else {'schema_version': 1, **value})
    for key, cls in [('sigma', FailureSignature), ('cost', Cost)]:
        if key in data: data[key] = nested(cls, data[key])
    for key, cls in [('C_partial', Candidate), ('O_res', Obligation), ('artifacts', Artifact)]:
        if key in data: data[key] = tuple(nested(cls, value) for value in data[key])
    return ExecutionResult.from_dict(data)


class Executor:
    def __init__(self, adapters):
        self.adapters = dict(adapters)

    def execute(self, state, action, graph, attempt_dir):
        validate_action_origin(state, action)
        legal, _ = graph.legal_candidates(state, llm_enabled=False)
        if action not in legal:
            raise ContractError('executor received unfiltered or changed action')
        if action.backend not in self.adapters:
            raise ContractError('unregistered executable backend')
        attempt_dir = guard_path(attempt_dir)
        seconds = min(state.b.seconds, action.theta.get('seconds', state.b.seconds))
        if seconds <= 0:
            raise ContractError('no executable budget')
        adapter = self.adapters[action.backend]
        backend_dir = guard_path(attempt_dir / 'backend', attempt_dir)
        if action.backend == 'core':
            node = graph.nodes[action.target]
            if node.kind != 'core_request':
                raise ContractError('core requires an explicitly bound core_request representation')
            raw = adapter.execute(thaw(node.payload), backend_dir, seconds)
        elif action.backend == 'method':
            raw = adapter.execute(state.G.identity, action.theta.get('method'), state.G.to_dict(),
                                  backend_dir, seconds)
        elif action.backend == 'llm':
            raise ContractError('LLM execution is disabled')
        else:
            raise ContractError('unsupported execution backend')
        result = normalize_result(raw)
        for artifact in result.artifacts:
            path = guard_path(artifact.path, attempt_dir)
            if sha256_file(path) != artifact.sha256:
                raise IntegrityError('backend artifact hash mismatch')
        if result.cost.actions != 1:
            raise ContractError('one execution must charge one action')
        return result
