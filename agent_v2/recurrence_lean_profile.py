"""Controlled recurrence proof reconstruction and fresh mathematical verification."""
from .models import Source
from .storage import IntegrityError
from .recurrence_frontend import PROFILE, analyze_source
from .recurrence_translation import reconstruct_candidate


def check_recurrence_partial(checker, candidate, context, start):
    from .lean_checker import _result
    from .math_lean_profile import _verify_train
    source = Source.from_dict(context['source'])
    frontend = analyze_source(source.to_dict(), context['run_dir'])
    if frontend['status'] != 'applicable': return None
    if candidate['source_sha256'] != source.sha256 or context['source_sha256'] != source.sha256:
        raise IntegrityError('recurrence source binding mismatch')
    if candidate['dependencies']:
        raise IntegrityError('local recurrence candidate has unexpected dependencies')
    try:
        rebuilt = reconstruct_candidate(frontend, candidate['proof_term'], allow_negative=True)
    except ValueError as error:
        return _result(start, False, 'incomplete', 'partial', 'unsupported_term_syntax', str(error))
    if candidate['proposition'] != rebuilt.proposition or candidate['id'] != rebuilt.id:
        raise IntegrityError('recurrence proposition or witness identity mismatch')
    return _verify_train(checker, candidate, context, start, source, frontend, rebuilt.proposition,
        additional_rules=(checker.repository / 'finite_product_framework/p1/lean/Shared.lean',),
        profile=PROFILE)
