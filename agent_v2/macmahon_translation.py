"""Reconstruct the original complex finite-fiber generating-function certificate."""
from .formal_frontend import _closed_prefix
from .macmahon_frontend import PROFILE,analyze_source,lean
from .models import Candidate,canonical,digest
from .storage import IntegrityError


def _bound(frontend):
    if (not isinstance(frontend,dict) or frontend.get('status')!='applicable'
            or frontend.get('profile')!=PROFILE or 'source' not in frontend):
        raise IntegrityError('unsupported MacMahon Source frontend')
    if canonical(analyze_source(frontend['source']))!=canonical(frontend):
        raise IntegrityError('MacMahon frontend differs from complete frozen Source')


def make_candidate(frontend):
    _bound(frontend);names=frontend['symbols'];z,n=names['scalar'],names['bound']
    series=f'(AgentV2MacMahon.geometric {z} * AgentV2MacMahon.geometric ({z}⁻¹))'
    denominator=f'((1 - PowerSeries.C {z} * PowerSeries.X) * (1 - PowerSeries.C ({z}⁻¹) * PowerSeries.X))'
    proposition=(_closed_prefix(frontend['binders'])+', '+series+' * '+denominator+' = 1 ∧ '
                 f'PowerSeries.coeff {n} '+series+' = '+lean(frontend['source_sum']))
    proof=('by\n  intro '+' '.join(b['name'] for b in frontend['binders'])+'\n'
           f'  exact AgentV2MacMahon.source_realization {z} {n} {names["nonzero"]}')
    identity=digest({'source':frontend['source']['sha256'],'profile':PROFILE,'proposition':proposition})[:24]
    return Candidate('macmahon-local-'+identity,proposition,proof,
                     'AgentV2Candidate.proof',frontend['source']['sha256'])


def translate_candidate(frontend,raw):
    from .macmahon_check import check
    _bound(frontend)
    try:
        checked=check(frontend,raw);candidate=make_candidate(frontend)
        return {'status':'candidate_ready','candidate':candidate.to_dict(),'independent_symbolic_check':checked,
                'lean_verified':False,'original_identity_proved':False,
                'remaining_work':'Ultraspherical comparison and the two other original conjuncts remain open.'}
    except IntegrityError:raise
    except (ValueError,TypeError,KeyError,AttributeError,RecursionError) as error:
        return {'status':'translation_pending','lean_verified':False,'original_identity_proved':False,
                'reason':{'code':'translation_pending','message':str(error)}}
