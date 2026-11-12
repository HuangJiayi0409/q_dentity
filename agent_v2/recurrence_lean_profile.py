"""Controlled recurrence proof reconstruction and fresh mathematical verification."""
from .storage import IntegrityError
from .recurrence_frontend import PROFILE
from .recurrence_translation import reconstruct_candidate


def reconstruct_profile_candidate(frontend, request, approved_certificates):
    """Rebuild local witnesses or the fixed closure tasks without approving them."""
    if request['id'].startswith('recurrence-local-') or request['proof_term'].startswith('/- agent_v2_recurrence_v1 '):
        if request['dependencies']:
            raise IntegrityError('local recurrence candidate has unexpected dependencies')
        return reconstruct_candidate(frontend, request['proof_term'], allow_negative=True)
    from .recurrence_closure import reconstruct_closure_candidate
    return reconstruct_closure_candidate(frontend, request, approved_certificates)


def check_recurrence_partial(checker, candidate, context, start):
    # Compatibility entry point; Source resolution and all checking are shared.
    from .math_lean_profile import check_train_partial
    return check_train_partial(checker, candidate, context, start)
