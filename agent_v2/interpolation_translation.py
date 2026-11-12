"""Independently check source-derived finite-node certificates, then rebuild Lean.

Only exact bounded integer-polynomial arithmetic is used here. The returned CAS
proof script is never executed, parsed as code, or inserted into the candidate.
"""
from .formal_frontend import _closed_prefix
from .interpolation_frontend import PROFILE, analyze_source, lean
from .models import Candidate, canonical, digest
from .storage import IntegrityError
from .symbolic_methods import request_digest


def _bound(frontend):
    if (not isinstance(frontend,dict) or frontend.get('status')!='applicable'
            or frontend.get('profile')!=PROFILE or 'source' not in frontend):
        raise IntegrityError('unsupported interpolation Source frontend')
    if canonical(analyze_source(frontend['source'])) != canonical(frontend):
        raise IntegrityError('interpolation frontend differs from frozen source reconstruction')


def make_candidate(frontend):
    _bound(frontend)
    names=frontend['symbols'];j=frontend['factor_index']
    proposition=(_closed_prefix(frontend['binders'])+', '+f'∀ {j} : ℕ, '
                 +j+' < '+lean(frontend['factor_range'])+' → '+lean(frontend['factor_equation']))
    used={b['name'] for b in frontend['binders']}|{j}
    fresh=lambda start: next(start+'x'*i for i in range(32) if start+'x'*i not in used)
    instance=fresh('qv2inst');used.add(instance);hypothesis=fresh('qv2hj')
    introductions=' '.join(instance if b['kind']=='instance' else b['name'] for b in frontend['binders'])
    proof=(f'by\n  intro {introductions} {j} {hypothesis}\n'
           f'  exact AgentV2Interpolation.source_factor {names["parameter"]} {names["base"]} {names["offset"]} {j}')
    identity=digest({'source':frontend['source']['sha256'],'profile':PROFILE,'proposition':proposition})[:24]
    return Candidate('interpolation-local-'+identity,proposition,proof,
                     'AgentV2Candidate.proof',frontend['source']['sha256'])


def _add(left,right,sign=1):
    result=dict(left)
    for monomial,value in right.items():result[monomial]=result.get(monomial,0)+sign*value
    return {m:v for m,v in result.items() if v}


def _mul(left,right):
    result={}
    for a,x in left.items():
        for b,y in right.items():
            monomial=tuple(sorted(a+b));result[monomial]=result.get(monomial,0)+x*y
    return {m:v for m,v in result.items() if v}


def _polynomial(node):
    # This request has just been exactly reconstructed from bounded Source syntax.
    op=node['op']
    if op=='atom':return {(node['key'],):1}
    if op=='integer':return {():node['value']} if node['value'] else {}
    left,right=map(_polynomial,node['args'])
    if op=='HMul.hMul':return _mul(left,right)
    if op in ('HAdd.hAdd','HSub.hSub'):return _add(left,right,-1 if op=='HSub.hSub' else 1)
    raise IntegrityError('unsupported source-reconstructed polynomial operation')


def _degree(node,key):
    op=node['op']
    if op=='integer':return 0
    if op=='atom':return int(node['key']==key)
    values=[_degree(a,key) for a in node['args']]
    return sum(values) if op=='HMul.hMul' else max(values)


def _evaluate(poly,key,point):
    result={}
    for monomial,value in poly.items():
        power=monomial.count(key);remaining=tuple(a for a in monomial if a!=key)
        result[remaining]=result.get(remaining,0)+value*point**power
    return {m:v for m,v in result.items() if v}


def _display(node,key):
    op=node['op']
    if op=='integer':return f'({node["value"]} : Polynomial (K))'
    if op=='atom':return 'Polynomial.X' if node['key']==key else f'(Polynomial.C ({node["display"]}))'
    signs={'HAdd.hAdd':'+','HSub.hSub':'-','HMul.hMul':'*'}
    return '('+(' '+signs[op]+' ').join(_display(a,key) for a in node['args'])+')'


def _check(frontend,raw):
    request=frontend['core_request']
    if (not isinstance(raw,dict) or type(raw.get('schema_version')) is not int or raw['schema_version']!=1
            or raw.get('method')!='interpolation' or raw.get('status')!='constructed'
            or raw.get('original_identity_proved') is not False
            or raw.get('request_sha256')!=request_digest(request)):
        raise ValueError('not an actual source-bound interpolation construction')
    construction=raw['construction']
    if not isinstance(construction,dict) or construction.get('status')!='constructed':
        raise ValueError('missing successful interpolation construction')
    certificate=construction['certificate'];goal=request['input']['goal'];key=0
    degrees=[_degree(goal[side],key) for side in ('lhs','rhs')];degree=max(degrees)
    expected_poly=_display(goal['lhs'],key)+' - '+_display(goal['rhs'],key)
    if (not isinstance(certificate,dict) or certificate.get('kind')!='finite_zero_certificate'
            or type(certificate.get('variable_atom')) is not int or certificate['variable_atom']!=key
            or certificate.get('variable_expression')!='a'
            or type(certificate.get('degree_upper_bound')) is not int
            or certificate['degree_upper_bound']!=degree or degree!=1
            or degree>request['input']['max_degree'] or goal['char_zero'] is not False
            or certificate.get('polynomial')!=expected_poly
            or certificate.get('node_distinctness')!='0/1 node separation in nontrivial field'):
        raise ValueError('interpolation variable, degree, polynomial or original domain mismatch')
    expected_nodes=[{'node':'0','exact_residual':'0'},{'node':'1','exact_residual':'0'}]
    if certificate.get('nodes')!=expected_nodes:
        raise ValueError('interpolation nodes or reported residuals differ from exact 0/1 certificate')
    left,right=(_polynomial(goal[side]) for side in ('lhs','rhs'))
    for point in (0,1):
        if _evaluate(left,key,point)!=_evaluate(right,key,point):
            raise ValueError('nonzero independently evaluated node residual')
    return {'status':'passed','arithmetic':'exact integer polynomial dictionaries',
        'request_sha256':request_digest(request),'variable_atom':key,'variable_expression':'a',
        'degree_upper_bound':degree,'left_and_right_degree_bounds':degrees,'nodes':['0','1'],
        'symbolic_node_residuals':['0','0'],'node_separation':'zero_ne_one in the original Field',
        'cas_proof_text_used':False,'source_bridges_require_lean':['zpow_natCast','pow_add'],
        'lean_interpolation_required':'degree bound and two-node uniqueness, followed by evaluation at original a'}


def translate_candidate(frontend,raw):
    _bound(frontend)
    try:
        check=_check(frontend,raw);candidate=make_candidate(frontend)
        return {'status':'candidate_ready','candidate':candidate.to_dict(),
                'independent_symbolic_check':check,'lean_verified':False,'original_identity_proved':False,
                'remaining_work':'Product assembly and original quotient identity remain open.'}
    except IntegrityError:raise
    except (ValueError,TypeError,KeyError,AttributeError,RecursionError) as error:
        return {'status':'translation_pending','lean_verified':False,'original_identity_proved':False,
                'reason':{'code':'translation_pending','message':str(error)}}
