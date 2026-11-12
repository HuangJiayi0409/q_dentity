"""Instantiate a declared finite task chain after its real witness is approved.

This is dependency binding for recurrence full scope. It creates no expressions,
representation nodes, transformations, searches, proofs or state updates.
"""
from .graph import Outlet
from .models import ContractError
from .recurrence_frontend import PROFILE, analyze_source
from .recurrence_translation import reconstruct_candidate
from .storage import IntegrityError

TASKS = ('local', 'uniqueness_bridge', 'rhs_recurrence', 'initial_zero', 'initial_one')
PROVENANCE = ('recurrence_full_contract_v1',)


def full_scope_contract(frontend):
    from .recurrence_closure import closure_blueprint
    plan = closure_blueprint(frontend)
    return {'schema_version': 1, 'method': 'recurrence', 'profile': PROFILE,
        'source_sha256': frontend['source']['sha256'], 'tasks': list(TASKS),
        'local_dependency': 'unique_current_source_reconstructed_local_witness',
        'local_certificate_id': None, 'obligations': plan['obligations'],
        'bridge_proposition': plan['bridge_proposition'],
        'automatic_graph_expansion': False}


def initial_full_outlet(frontend, seconds, version, estimated_seconds):
    full_scope_contract(frontend)
    return Outlet('recurrence-local', 'original', 'CAS', 'method',
        {'method': 'recurrence', 'method_version': version, 'seconds': seconds,
         'scope': 'full', 'task': 'local'}, ('closed_prop',),
        estimated_seconds=estimated_seconds, handles=('original',), provenance=PROVENANCE)


def _approved_local(frontend, certificates):
    """Do not accept a renamed, foreign or uncontrolled local witness as a slot."""
    approved = {}
    for cert in certificates:
        if cert.source_sha256 != frontend['source']['sha256']:
            raise IntegrityError('full scope contains a foreign certificate')
        if cert.id.startswith('recurrence-local-') or cert.proof_term.startswith('/- agent_v2_recurrence_v1 '):
            try:
                canonical = reconstruct_candidate(frontend, cert.proof_term)
            except (ValueError, KeyError, TypeError) as error:
                raise IntegrityError('uncontrolled local witness in full scope') from error
            if (cert.id != canonical.id or cert.proposition != canonical.proposition
                    or cert.dependencies != canonical.dependencies):
                raise IntegrityError('local witness identity or semantics changed')
            approved[cert.id] = cert.to_dict()
    if len(approved) > 1:
        raise IntegrityError('multiple local witnesses cannot bind one full task chain')
    return approved


def _full(outlet):
    return (outlet.backend == 'method' and outlet.parameters.get('method') == 'recurrence'
            and outlet.parameters.get('scope') == 'full')


def fixed_task_completed(state, outlet):
    if not _full(outlet) or outlet.parameters.get('task') != 'local':
        return False
    frontend = analyze_source(state.G.to_dict())
    if frontend['status'] != 'applicable':
        raise IntegrityError('full recurrence task no longer matches frozen source')
    return bool(_approved_local(frontend, state.C))


def bind_full_scope_outlets(state, graph):
    """Return missing fixed outlets; validate already-bound outlets without edits."""
    from .recurrence_closure import closure_blueprint
    existing = [outlet for outlet in graph.outlets.values() if _full(outlet)]
    if not existing:
        return ()
    local = graph.outlets.get('recurrence-local')
    if local is None or not _full(local):
        raise IntegrityError('recurrence full scope lacks its declared local entry')
    frontend = analyze_source(state.G.to_dict())
    if frontend['status'] != 'applicable' or graph.source_sha256 != state.G.sha256:
        raise IntegrityError('full task contract/source mismatch')
    try:
        expected_local = initial_full_outlet(frontend, local.parameters['seconds'],
            local.parameters['method_version'], local.estimated_seconds)
    except (KeyError, TypeError, ValueError, ContractError) as error:
        raise IntegrityError('malformed declared full scope entry') from error
    if local != expected_local:
        raise IntegrityError('declared full scope local entry changed')
    approved = _approved_local(frontend, state.C)
    expected = {expected_local.id: expected_local}
    if approved:
        plan = closure_blueprint(frontend, approved)
        for task in TASKS[1:]:
            bridge = task == 'uniqueness_bridge'
            outlet = Outlet('recurrence-' + task, 'original', 'CAS', 'method',
                dict(local.parameters, task=task, produces_certificate=plan['certificate_ids'][task]),
                ('closed_prop',), estimated_seconds=local.estimated_seconds,
                handles=('original',) if bridge else (plan['obligation_ids'][task],),
                required_certificates=(plan['local_id'],) if bridge else (),
                provenance=PROVENANCE)
            expected[outlet.id] = outlet
    for outlet in existing:
        if expected.get(outlet.id) != outlet:
            raise IntegrityError('full scope outlet differs from its fixed source-bound task contract')
    return tuple(outlet for name, outlet in expected.items() if name not in graph.outlets)
