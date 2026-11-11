"""Bounded recovery classifications. None assert mathematical falsehood."""


def failure_category(sigma):
    code = sigma.get('code', '')
    if not isinstance(code, str):
        return 'contract_or_execution'
    if code in {'formal_frontend_unavailable', 'unsupported_original_translation',
                'environment_blocked', 'dependency_missing', 'lean_unavailable', 'adapter_disabled'}:
        return 'environment'
    if code in {'budget_exhausted', 'budget_insufficient', 'timeout', 'resource_exhausted'}:
        return 'budget'
    if code in {'search_exhausted', 'construction_failed', 'no_solution_in_class',
                'no_relation_in_declared_basis', 'translation_pending'}:
        return 'search'
    if 'hash' in code or code in {'integrity_error', 'original_binding_mismatch', 'invalid_evidence'}:
        return 'integrity'
    if 'lean' in code or 'proof' in code or code == 'invariant_rejected':
        return 'verification'
    return 'contract_or_execution'


def classify_stop(state, candidates, reasons):
    """Return (terminal status, explanation) from the current hard filters.

    Inapplicable or disconnected alternatives do not hide a usable route whose
    only blocker is its cost. Old failures are relevant only when a current route
    was suppressed as an already attempted action.
    """
    if state.b.seconds <= 0:
        return 'budget_exhausted', 'wall_budget_exhausted'
    if state.b.actions <= 0:
        return 'budget_exhausted', 'action_budget_exhausted'
    if candidates:
        return 'running', 'legal_route_available'
    codes = {reason.get('code') for reason in reasons}
    integrity = {'original_binding_mismatch', 'unregistered_current_or_root',
        'original_representation_mismatch', 'representation_binding_mismatch',
        'current_representation_unverified', 'invalid_identity_edge'}
    if codes & integrity:
        return 'integrity_error', 'graph_integrity_error'
    if 'budget_insufficient' in codes:
        return 'budget_exhausted', 'no_affordable_action'
    navigation = {'unreachable_representation', 'no_transition_from_current'}
    active = codes - navigation
    environmental = {code for code in active if failure_category({'code': code}) == 'environment'}
    if environmental:
        return 'environment_blocked', 'environment_unavailable'
    for reason in reasons:
        if reason.get('code') != 'duplicate_action':
            continue
        code = reason.get('attempt_code')
        if code is None:
            # Older diagnostics did not carry the fingerprint-matched attempt.
            # Match this route only; an unrelated global last failure is not its cause.
            code = next((a.code for a in reversed(state.attempts)
                         if a.action_id == reason.get('route_id')), None)
        if failure_category({'code': code}) == 'environment':
            return 'environment_blocked', 'environment_unavailable'
    if active == {'duplicate_action'}:
        return 'incomplete', 'repeated_actions_exhausted'
    contracts = {'representation_kind_mismatch', 'semantic_domain_mismatch',
        'index_ranges_mismatch', 'core_input_contract_mismatch', 'transformation_domain_mismatch',
        'unknown_transformation_domain', 'bridge_proposition_mismatch', 'no_matching_open_obligation'}
    if active and active <= contracts:
        return 'incomplete', 'input_contract_mismatch'
    capability = {'bridge_not_verified', 'condition_not_verified', 'required_certificate_unavailable',
                  'bridge_dependency_unavailable', 'unsupported_transformation_anchor'}
    if not active or active & capability:
        return 'incomplete', 'graph_capability_missing'
    return 'incomplete', 'no_legal_route'


def stop_reason(state, candidates, reasons):
    """Compatibility helper for callers needing only the status classification."""
    return classify_stop(state, candidates, reasons)[0]
