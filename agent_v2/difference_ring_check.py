"""Independent exact replay of original-relation polynomial multipliers.

The shared bounded integer-polynomial parser is verification infrastructure;
no coefficient solver, Groebner search, sympify, or CAS script is called here.
Source shift relations are premises of this algebraic check only: the fixed
Lean rule must prove them from the original Pochhammer definition.
"""
from .coefficient_translation import _add,_multiply,_integer,_read_polynomial
from .difference_ring_frontend import PROFILE,analyze_source
from .models import canonical
from .symbolic_methods import request_digest


def _require(condition,message):
    if not condition:raise ValueError(message)


def _input(node,atoms):
    op=node['op']
    if op=='integer':return _integer(node['value'])
    if op=='atom':
        key=node['key'];symbol='a'+str(key)
        _require(type(key) is int and 0<=key<32,'invalid source tower atom')
        _require(str(key) not in atoms or atoms[str(key)]==node['display'],
                 'conflicting source tower atom meanings')
        atoms[str(key)]=node['display']
        return {(symbol,):1}
    if op=='neg':return _add({},_input(node['arg'],atoms),-1)
    if op=='pow':
        exponent=node['exponent']
        _require(type(exponent) is int and 0<=exponent<=16,'unbounded tower exponent')
        result={():1};value=_input(node['arg'],atoms)
        for _ in range(exponent):result=_multiply(result,value)
        return result
    _require(op in ('HAdd.hAdd','HSub.hSub','HMul.hMul'),'unsupported source tower operation')
    left,right=(_input(value,atoms) for value in node['args'])
    return _multiply(left,right) if op=='HMul.hMul' else _add(left,right,-1 if op=='HSub.hSub' else 1)


def _verify(frontend,raw):
    _require(isinstance(frontend,dict) and frontend.get('status')=='applicable'
             and frontend.get('profile')==PROFILE,'unsupported difference-ring frontend')
    _require(canonical(frontend)==canonical(analyze_source(frontend['source'])),
             'difference-ring frontend differs from complete frozen Source')
    request=frontend['core_request'];goal=request['input']['goal']
    _require(isinstance(raw,dict) and type(raw.get('schema_version')) is int and raw['schema_version']==1
             and raw.get('method')=='difference_ring' and raw.get('status')=='constructed'
             and raw.get('original_identity_proved') is False
             and raw.get('request_sha256')==request_digest(request),'different difference-ring request or status')
    construction=raw['construction']
    _require(isinstance(construction,dict) and construction.get('status')=='constructed',
             'missing actual difference-ring construction')
    cert=construction['certificate']
    _require(isinstance(cert,dict) and set(cert)=={'algorithm','difference','relations','coefficients',
                                                 'remainder','script','atoms'},'invalid tower certificate fields')
    _require(cert['algorithm'] in ('ordered polynomial reduction',
                                  'bounded Groebner completion with original-relation multipliers'),
             'unsupported tower algorithm')
    _require(isinstance(cert['script'],str) and len(cert['script'])<=8192,'invalid diagnostic script')
    atoms={}
    target=_add(_input(goal['lhs'],atoms),_input(goal['rhs'],atoms),-1)
    names=[];relations=[]
    for hypothesis in goal['hypotheses']:
        names.append(hypothesis['name'])
        relations.append(_add(_input(hypothesis['lhs'],atoms),_input(hypothesis['rhs'],atoms),-1))
    _require(len(names)==len(set(names)),'duplicate source relation names')
    _require(canonical(cert['atoms'])==canonical(atoms),'different source tower atom map')
    symbols={'a'+key for key in atoms}
    _require(_read_polynomial(cert['difference'],symbols)==target,'reported target differs from source goal')
    reported=cert['relations']
    _require(isinstance(reported,list) and len(reported)==len(relations),'missing original tower relations')
    for actual,expected in zip(reported,relations):
        _require(_read_polynomial(actual,symbols)==expected,'reported relation differs from original source shift')
    coefficients=cert['coefficients'];active={name for name,relation in zip(names,relations) if relation}
    _require(isinstance(coefficients,dict) and set(coefficients)==active,'different original-relation multipliers')
    total={};count=0
    for name,relation in zip(names,relations):
        if not relation:continue
        multiplier=_read_polynomial(coefficients[name],symbols)
        total=_add(total,_multiply(multiplier,relation));count+=1
    residual=_add(target,total,-1)
    _require(_read_polynomial(cert['remainder'],symbols)==residual and not residual,
             'original-relation multiplier identity has nonzero residual')
    return {'status':'passed','request_sha256':request_digest(request),
        'arithmetic':'bounded exact integer polynomial dictionaries; no solver or CAS script',
        'atoms':atoms,'relations_checked':len(relations),'multipliers_checked':count,
        'original_relation_names':names,'coefficients':coefficients,
        'integer_coefficients_only':True,'independent_residual':'0','cas_proof_text_used':False,
        'source_shift_requires_lean':True,
        'remaining_work':'Lean must prove the evaluated source shift; the original first-factor connection remains open'}


def check(frontend,raw):
    try:return _verify(frontend,raw)
    except (KeyError,TypeError,IndexError,AttributeError,SyntaxError,RecursionError,OSError) as error:
        raise ValueError('malformed source-bound difference-ring certificate: '+str(error)) from error
