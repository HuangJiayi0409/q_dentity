"""Independent exact verification of finite triangular-kernel certificates.

This module never searches for a map or multipliers. It checks a supplied
bijection and each nonnegative linear-combination witness over integer affine
rows. In particular the natural subtraction indices must be nonnegative on
the certified support; they are not silently treated as integer subtraction.
"""
from collections import Counter

from .kernel_transform_frontend import PROFILE,analyze_source
from .models import canonical
from .symbolic_methods import request_digest


def _require(value,message):
    if not value:raise ValueError(message)


def _same(actual,expected,message):
    # JSON structural equality distinguishes booleans from integers.
    _require(canonical(actual)==canonical(expected),message)


def _combination(rows,target,coefficients,bound):
    _require(isinstance(coefficients,list) and len(coefficients)==len(rows),
             'affine witness has the wrong coefficient count')
    _require(all(type(c) is int and 0<=c<=bound for c in coefficients),
             'affine witness must use bounded nonnegative integer coefficients')
    accumulated=[0,0,0,0]
    for coefficient,row in zip(coefficients,rows):
        for column,value in enumerate(row):accumulated[column]+=coefficient*value
    _require(accumulated==target,'affine witness does not reproduce its target inequality')


def _family(rows,targets,witnesses,bound):
    _require(isinstance(witnesses,list) and len(witnesses)==len(targets),'missing affine witness family')
    for target,coefficients in zip(targets,witnesses):_combination(rows,target,coefficients,bound)
    return len(targets)


def _verify(frontend,raw):
    _require(isinstance(frontend,dict) and frontend.get('profile')==PROFILE
             and frontend.get('status')=='applicable','unsupported kernel Source frontend')
    _same(frontend,analyze_source(frontend['source']),'kernel frontend differs from frozen Source')
    request=frontend['core_request'];data=request['input']
    _require(isinstance(raw,dict) and type(raw.get('schema_version')) is int and raw['schema_version']==1
        and raw.get('method')=='kernel_transform' and raw.get('status')=='constructed'
        and raw.get('original_identity_proved') is False
        and raw.get('request_sha256')==request_digest(request),'kernel raw result has a different request or status')
    construction=raw['construction']
    _require(isinstance(construction,dict) and construction.get('status')=='constructed',
             'missing actual kernel construction')
    proposals=construction['constructions']
    _require(isinstance(proposals,list) and len(proposals)==1,'one triangular certificate required')
    proposal=proposals[0]
    _require(isinstance(proposal,dict) and set(proposal)=={'plan','certificate'}
        and proposal['plan']=='constructed_triangular_transpose','unsupported kernel construction plan')
    cert=proposal['certificate']
    keys={'algorithm','parameter','type','coordinates','permutation','inverse_permutation',
          'left_domain','right_domain','transported_left_domain','left_factors','right_factors',
          'transported_left_factors','forward_implications','backward_implications',
          'left_finite_bounds','right_finite_bounds','left_index_guards','right_index_guards',
          'max_multiplier','permutations_tried','bound_specialized','index_arithmetic'}
    _require(isinstance(cert,dict) and set(cert)==keys,'missing or unexpected kernel certificate fields')
    _require(cert['algorithm']=='coordinate permutation with exact nonnegative affine witnesses'
        and cert['index_arithmetic']=='natural with certified nonnegative affine indices'
        and cert['bound_specialized'] is False,'wrong kernel algorithm or specialized bound')
    for key in ('parameter','type','coordinates','max_multiplier','left_domain','right_domain',
                'left_factors','right_factors'):
        _same(cert[key],data[key],'certificate differs from source-derived '+key)
    permutation=cert['permutation'];inverse=cert['inverse_permutation']
    for value in (permutation,inverse):
        _require(isinstance(value,list) and len(value)==2
                 and all(type(i) is int for i in value) and sorted(value)==[0,1],
                 'kernel map must be a bijection on both original coordinates')
    _require(all(permutation[inverse[i]]==i and inverse[permutation[i]]==i for i in range(2)),
             'kernel map and supplied inverse disagree')
    _require(type(cert['permutations_tried']) is int
        and cert['permutations_tried']==(1 if permutation==[0,1] else 2),
        'bounded coordinate-search record does not match the map')

    # Re-express a source affine form in target coordinates using the inverse.
    # The symbolic parameter N and constant coefficient are held fixed.
    def transport(row):
        result=[0,0,row[2],row[3]]
        for source_coordinate in range(2):result[inverse[source_coordinate]]=row[source_coordinate]
        return result
    left=data['left_domain'];right=data['right_domain'];bound=data['max_multiplier']
    mapped=[transport(row) for row in left]
    _same(cert['transported_left_domain'],mapped,'transported support rows were altered')
    support=_family(mapped,right,cert['forward_implications'],bound)
    support+=_family(right,mapped,cert['backward_implications'],bound)
    finite=[]
    for coordinate in range(2):
        lower=[0,0,0,0];lower[coordinate]=1
        upper=[0,0,1,0];upper[coordinate]=-1
        finite.extend([lower,upper])
    finiteness=_family(left,finite,cert['left_finite_bounds'],bound)
    finiteness+=_family(right,finite,cert['right_finite_bounds'],bound)
    indices=_family(left,[x['index'] for x in data['left_factors']],cert['left_index_guards'],bound)
    indices+=_family(right,[x['index'] for x in data['right_factors']],cert['right_index_guards'],bound)
    mapped_factors=[{'sequence':x['sequence'],'index':transport(x['index'])} for x in data['left_factors']]
    _same(cert['transported_left_factors'],mapped_factors,'transported sequence indices were altered')
    as_multiset=lambda factors:Counter((x['sequence'],tuple(x['index'])) for x in factors)
    _require(as_multiset(mapped_factors)==as_multiset(data['right_factors']),
             'sequence weight or factor multiplicity changes under the map')
    return {'status':'passed','request_sha256':request_digest(request),
        'arithmetic':'independent exact integer affine combinations; no search or symbolic solver',
        'permutation':permutation,'inverse_permutation':inverse,
        'support_implications_checked':support,'finite_bound_witnesses_checked':finiteness,
        'natural_index_guards_checked':indices,'bound_specialized':False,'cas_proof_text_used':False,
        'natural_subtraction':'nonnegative affine index witnesses checked on both supports',
        'weight_check':'exact sequence-index multiset including factor multiplicities',
        'remaining_work':'Lean must check the source LHS transposition; extracting and reassociating delta for the original RHS remains open'}


def check(frontend,raw):
    try:return _verify(frontend,raw)
    except (KeyError,TypeError,IndexError,AttributeError,RecursionError,OSError) as error:
        raise ValueError('malformed source-bound kernel certificate: '+str(error)) from error
