"""Bounded recovery classifications. None assert mathematical falsehood."""


def failure_category(sigma):
    code = sigma.get('code', '')
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


def stop_reason(state, candidates, reasons):
    if state.b.actions <= 0 or state.b.seconds <= 0:
        return 'budget_exhausted'
    if candidates:
        return 'running'
    codes = {reason.get('code') for reason in reasons}
    if codes and codes <= {'budget_insufficient', 'duplicate_action'} and 'budget_insufficient' in codes:
        return 'budget_exhausted'
    if state.attempts and failure_category({'code': state.attempts[-1].code}) == 'environment':
        return 'environment_blocked'
    return 'incomplete'
