"""One source-bound local transpose after independent exact certificate checking."""
from .kernel_transform_frontend import PROFILE,analyze_source
from .models import Candidate,canonical,digest
from .storage import IntegrityError


def _bound(frontend):
    if (not isinstance(frontend,dict) or frontend.get('status')!='applicable'
            or frontend.get('profile')!=PROFILE or 'source' not in frontend):
        raise IntegrityError('unsupported kernel Source frontend')
    if canonical(analyze_source(frontend['source']))!=canonical(frontend):
        raise IntegrityError('kernel frontend differs from complete frozen Source reconstruction')


def make_candidate(frontend):
    _bound(frontend);names=frontend['symbols'];proposition=frontend['local_proposition']
    used={binder['name'] for binder in frontend['binders']};instance='qv2inst'
    while instance in used:instance+='x'
    introductions=' '.join(instance if b['kind']=='instance' else b['name'] for b in frontend['binders'])
    arguments=' '.join(names[key] for key in ('bound','alpha','delta','u','v'))
    proof=f'by\n  intro {introductions}\n  exact AgentV2KernelTransform.source_transpose {arguments}'
    identity=digest({'source':frontend['source']['sha256'],'profile':PROFILE,'proposition':proposition})[:24]
    return Candidate('kernel-transform-local-'+identity,proposition,proof,
                     'AgentV2Candidate.proof',frontend['source']['sha256'])


def translate_candidate(frontend,raw):
    from .kernel_transform_check import check
    _bound(frontend)
    try:
        checked=check(frontend,raw);candidate=make_candidate(frontend)
        return {'status':'candidate_ready','candidate':candidate.to_dict(),
            'independent_symbolic_check':checked,'lean_verified':False,'original_identity_proved':False,
            'remaining_work':'Extract delta and rearrange products in the transposed sum; original theorem acceptance remains open.'}
    except IntegrityError:raise
    except (ValueError,TypeError,KeyError,AttributeError,SyntaxError,RecursionError) as error:
        return {'status':'translation_pending','lean_verified':False,'original_identity_proved':False,
                'reason':{'code':'translation_pending','message':str(error)}}
