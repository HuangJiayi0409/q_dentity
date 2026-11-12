"""Bind an actual division-free determinant to the original arbitrary minor.

The shared bounded AST integer-polynomial reader is verification infrastructure,
not a coefficient backend. Determinants are independently checked by the exact
Leibniz expansion here; no other method's solver or CAS proof script is called.
"""
import itertools
from .coefficient_translation import _add,_multiply,_read_polynomial
from .determinant_frontend import PROFILE,analyze_source
from .formal_frontend import _closed_prefix
from .models import Candidate,canonical,digest
from .storage import IntegrityError
from .symbolic_methods import request_digest


def _bound(frontend):
    if (not isinstance(frontend,dict) or frontend.get('status')!='applicable'
            or frontend.get('profile')!=PROFILE or 'source' not in frontend):
        raise IntegrityError('unsupported determinant Source frontend')
    if canonical(analyze_source(frontend['source']))!=canonical(frontend):
        raise IntegrityError('determinant frontend differs from complete frozen Source reconstruction')


def make_candidate(frontend):
    _bound(frontend);names=frontend['symbols'];selectors=' '.join(frontend['selectors'])
    entries=frontend['minor_entries'];matrix=frontend['matrix_term']
    rhs=(entries['entry00']['lean']+' * '+entries['entry11']['lean']+' - '
         +entries['entry01']['lean']+' * '+entries['entry10']['lean'])
    proposition=(_closed_prefix(frontend['binders'])+', '+f'∀ ({selectors} : Fin {names["dimension"]}), '
        f'Matrix.det (AgentV2Determinant.minorTwo {matrix} {selectors}) = '+rhs)
    used={b['name'] for b in frontend['binders']}|set(frontend['selectors']);instance='qv2inst'
    while instance in used:instance+='x'
    introductions=' '.join(instance if b['kind']=='instance' else b['name'] for b in frontend['binders'])
    proof=f'by\n  intro {introductions} {selectors}\n  exact AgentV2Determinant.minor_det {matrix} {selectors}'
    identity=digest({'source':frontend['source']['sha256'],'profile':PROFILE,'proposition':proposition})[:24]
    return Candidate('determinant-local-'+identity,proposition,proof,
                     'AgentV2Candidate.proof',frontend['source']['sha256'])


def _check(frontend,raw):
    request=frontend['core_request']
    if (not isinstance(raw,dict) or type(raw.get('schema_version')) is not int or raw['schema_version']!=1
            or raw.get('method')!='determinant' or raw.get('status')!='constructed'
            or raw.get('original_identity_proved') is not False
            or raw.get('request_sha256')!=request_digest(request)):
        raise ValueError('not an actual source-bound determinant construction')
    construction=raw['construction']
    if not isinstance(construction,dict) or construction.get('status')!='constructed':
        raise ValueError('missing constructed determinant output')
    rows=construction['constructions']
    allowed={'constructed_symbolic_plu','constructed_division_free_determinant'}
    if (not isinstance(rows,list) or not 1<=len(rows)<=2
            or any(not isinstance(row,dict) or row.get('plan') not in allowed for row in rows)):
        raise ValueError('malformed determinant construction list')
    direct=[row for row in rows if row['plan']=='constructed_division_free_determinant']
    if len(direct)!=1:raise ValueError('exactly one division-free determinant certificate required')
    certificate=direct[0]['certificate'];size=request['input']['size']
    matrix=[[f'z{node["key"]}' for node in row] for row in request['input']['matrix']['entries']]
    atoms={f'z{node["key"]}':node['display'] for row in request['input']['matrix']['entries'] for node in row}
    if (not isinstance(certificate,dict) or type(certificate.get('dimension')) is not int
            or certificate['dimension']!=size or size!=2
            or certificate.get('algorithm')!='Berkowitz determinant; Lean cofactor reconstruction'
            or certificate.get('constructor_inputs')!=['matrix']
            or certificate.get('target_value_used_in_search') is not False
            or certificate.get('matrix')!=matrix or certificate.get('atoms')!=atoms
            or certificate.get('domain_policy')!='no pivot division; any input divisions still require original-domain verification'):
        raise ValueError('division-free source matrix, atom map, dimension or domain policy mismatch')
    expected={};count=0
    for permutation in itertools.permutations(range(size)):
        inversions=sum(permutation[i]>permutation[j] for i in range(size) for j in range(i+1,size))
        term={():1}
        for i,j in enumerate(permutation):term=_multiply(term,{(matrix[i][j],):1})
        expected=_add(expected,term,-1 if inversions%2 else 1);count+=1
    actual=_read_polynomial(certificate['determinant'],set(atoms))
    if actual!=expected:raise ValueError('independent source-minor Leibniz polynomial differs from CAS result')
    return {'status':'passed','arithmetic':'bounded exact integer polynomial dictionaries',
        'request_sha256':request_digest(request),'selected_plan':'constructed_division_free_determinant',
        'leibniz_permutations':count,'matrix':matrix,'atoms':atoms,
        'expected_determinant':'entry00*entry11-entry01*entry10','cas_determinant':certificate['determinant'],
        'all_original_dimensions_preserved':True,'pivot_nonzero_assumptions':False,
        'cas_proof_text_used':False,'lean_required':'Matrix.det_fin_two for the actual source matrix minor'}


def translate_candidate(frontend,raw):
    _bound(frontend)
    try:
        check=_check(frontend,raw);candidate=make_candidate(frontend)
        return {'status':'candidate_ready','candidate':candidate.to_dict(),
                'independent_symbolic_check':check,'lean_verified':False,'original_identity_proved':False,
                'remaining_work':'Full arbitrary-size determinant and planePi identity remain open.'}
    except IntegrityError:raise
    except (ValueError,TypeError,KeyError,AttributeError,SyntaxError,RecursionError) as error:
        return {'status':'translation_pending','lean_verified':False,'original_identity_proved':False,
                'reason':{'code':'translation_pending','message':str(error)}}
