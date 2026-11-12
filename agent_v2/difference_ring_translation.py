"""A checked original-relation multiplier gives a fixed source-derived local proof."""
from .difference_ring_frontend import PROFILE,analyze_source
from .models import Candidate,canonical,digest
from .storage import IntegrityError


def _bound(frontend):
    if (not isinstance(frontend,dict) or frontend.get('status')!='applicable'
            or frontend.get('profile')!=PROFILE or 'source' not in frontend):
        raise IntegrityError('unsupported difference-ring Source frontend')
    if canonical(analyze_source(frontend['source']))!=canonical(frontend):
        raise IntegrityError('difference-ring frontend differs from frozen Source reconstruction')


def make_candidate(frontend):
    _bound(frontend)
    symbols=frontend['symbols'];binders=frontend['binders'];proposition=frontend['local_proposition']
    used={b['name'] for b in binders}
    instance=next('qv2inst'+'x'*i for i in range(32) if 'qv2inst'+'x'*i not in used)
    introductions=' '.join(instance if b['kind']=='instance' else b['name'] for b in binders)
    proof=(f'by\n  intro {introductions}\n'
           f'  simpa only [neg_mul] using AgentV2DifferenceRing.source_increment {symbols["parameter"]} {symbols["base"]} '
           f'{symbols["bound"]} {symbols["positive_bound"]}')
    identity=digest({'source':frontend['source']['sha256'],'profile':PROFILE,'proposition':proposition})[:24]
    return Candidate('difference-ring-local-'+identity,proposition,proof,
                     'AgentV2Candidate.proof',frontend['source']['sha256'])


def translate_candidate(frontend,raw):
    from .difference_ring_check import check
    _bound(frontend)
    try:
        checked=check(frontend,raw);candidate=make_candidate(frontend)
        return {'status':'candidate_ready','candidate':candidate.to_dict(),'independent_symbolic_check':checked,
            'lean_verified':False,'original_identity_proved':False,
            'remaining_work':'Initial-factor/tail parameter shift and original equality remain open.'}
    except IntegrityError:raise
    except (ValueError,TypeError,KeyError,AttributeError,RecursionError) as error:
        return {'status':'translation_pending','lean_verified':False,'original_identity_proved':False,
                'reason':{'code':'translation_pending','message':str(error)}}
