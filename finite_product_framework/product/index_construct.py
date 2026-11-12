"""Bounded symbolic construction of a finite mixed-radix index equivalence.

Only natural-index arithmetic and commutative monomial factors are supported.
The search never instantiates either symbolic length and never divides a field
element. Its result is an untrusted symbolic certificate, not a Lean proof.
"""
import copy
import itertools


def _require(value,message):
    if not value:raise ValueError(message)


def _fields(value,keys):
    _require(isinstance(value,dict) and set(value)==set(keys),'unsupported typed product fields')


def _bound(value):
    stack=[(value,0)];count=0
    while stack:
        item,depth=stack.pop();count+=1
        _require(count<=512 and depth<=16,'product input resource bound exceeded')
        if isinstance(item,dict):
            _require(all(isinstance(k,str) for k in item),'nonstring product input key')
            stack.extend((v,depth+1) for v in item.values())
        elif isinstance(item,list):stack.extend((v,depth+1) for v in item)
        elif isinstance(item,str):_require(len(item)<=64,'oversized product atom')
        else:_require(type(item) is int and 0<=item<=16,'non-natural product input atom')


def _add(a,b):
    out=dict(a)
    for key,value in b.items():out[key]=out.get(key,0)+value
    return {k:v for k,v in out.items() if v}


def _mul(a,b):
    out={}
    for x,a0 in a.items():
        for y,b0 in b.items():
            key=tuple(sorted(x+y));out[key]=out.get(key,0)+a0*b0
    _require(len(out)<=64 and all(len(k)<=8 for k in out),'product polynomial resource bound exceeded')
    return out


def _poly(node,substitution=None):
    substitution=substitution or {}
    if type(node) is int:return {():node} if node else {}
    if isinstance(node,str):
        _require(node in {'m','n','j','i','k'},'unknown natural product variable')
        return substitution.get(node,{(node,):1})
    _require(isinstance(node,list) and len(node)==3 and node[0] in ('add','mul'),
             'natural exponents require bounded addition and multiplication')
    a,b=(_poly(x,substitution) for x in node[1:])
    return _add(a,b) if node[0]=='add' else _mul(a,b)


def _monomial(node,substitution=None):
    if node=='a':return {'a':{():1},'q':{}}
    if node=='q':return {'a':{},'q':{():1}}
    if type(node) is int and node==1:return {'a':{},'q':{}}
    _require(isinstance(node,list) and len(node)==3 and node[0] in ('mul','pow'),
             'factor is not a supported commutative natural-power monomial')
    if node[0]=='mul':
        a,b=(_monomial(x,substitution) for x in node[1:])
        return {key:_add(a[key],b[key]) for key in ('a','q')}
    value=_monomial(node[1],substitution);power=_poly(node[2],substitution)
    return {key:_mul(value[key],power) for key in ('a','q')}


def _factor(node,substitution=None):
    _require(isinstance(node,list) and len(node)==3 and node[0]=='sub'
             and type(node[1]) is int and node[1]==1,'factor must be one minus a monomial')
    return _monomial(node[2],substitution)


def _validate(data):
    _bound(data)
    _fields(data,('operation','scalar_domain','parameter','base','left','right',
                  'positive_parameters','natural_parameters','max_candidates'))
    _require(data['operation']=='finite_range_index_equivalence'
             and data['scalar_domain']=='commutative_field' and data['parameter']=='a' and data['base']=='q',
             'unsupported product operation or scalar domain')
    _require(data['natural_parameters']==['m','n'],'exact symbolic natural parameters required')
    positive=data['positive_parameters']
    _require(isinstance(positive,list) and all(isinstance(x,str) and x in ('m','n') for x in positive)
             and len(set(positive))==len(positive),'invalid positive radix assumptions')
    _require(type(data['max_candidates']) is int and 1<=data['max_candidates']<=2,'candidate budget must be one or two')
    left,right=data['left'],data['right']
    _fields(left,('index','bound','factor'));_fields(right,('indices','bounds','factor'))
    _require(left['index']=='k' and right['indices']==['j','i'],'fixed distinct index roles required')
    _require(isinstance(right['bounds'],list) and all(isinstance(x,str) for x in right['bounds'])
             and sorted(right['bounds'])==['m','n'],
             'rectangle bounds must be the two symbolic natural parameters')
    _poly(left['bound']);_factor(left['factor']);_factor(right['factor'])
    def names(poly):return {x for monomial in poly for x in monomial}
    _require(names(_poly(left['bound']))<={'m','n'},'source range depends on an index')
    _require(all(names(p)<={'m','n','k'} for p in _factor(left['factor']).values()),'left factor has foreign indices')
    _require(all(names(p)<={'m','n','j','i'} for p in _factor(right['factor']).values()),'right factor has foreign indices')


def validate_request(request):
    _fields(request,('schema_version','method','input'))
    _require(type(request['schema_version']) is int and request['schema_version']==1
             and request['method']=='product','unsupported product request version or method')
    _validate(request['input'])


def _record(poly):
    return [{'variables':list(m),'coefficient':c} for m,c in sorted(poly.items())]


def _trace(first,second,radix,outer,forward):
    k='k';mod=['mod',k,radix];div=['div',k,radix];positive=['lt',0,radix]
    rbound=['lt',first,radix];qbound=['lt',second,outer];kbound=['lt',k,['mul',radix,outer]]
    return [
        {'rule':'nat_remainder_lt','requires':[positive], 'conclusion':['lt',mod,radix]},
        {'rule':'nat_quotient_lt_of_lt_mul','requires':[positive,kbound], 'conclusion':['lt',div,outer]},
        {'rule':'nat_remainder_add_radix_quotient','requires':[positive],
         'conclusion':['eq',['add',mod,['mul',radix,div]],k]},
        {'rule':'nat_mixed_radix_remainder','requires':[positive,rbound],
         'conclusion':['eq',['mod',forward,radix],first]},
        {'rule':'nat_mixed_radix_quotient','requires':[positive,rbound],
         'conclusion':['eq',['div',forward,radix],second]},
        {'rule':'nat_mixed_radix_range','requires':[positive,rbound,qbound],
         'conclusion':['lt',forward,['mul',radix,outer]]}]


def construct(data):
    _validate(data)
    indices=data['right']['indices'];bounds=dict(zip(indices,data['right']['bounds']))
    orders=list(reversed(list(itertools.permutations(indices))))
    trials=[];limit=data['max_candidates']
    search={'candidate_limit':limit,'candidates_examined':0,'trials':trials}
    for order in orders:
        if len(trials)>=limit:
            return {'status':'budget_exhausted','reason':'mixed-radix candidate budget exhausted','search':search}
        first,second=order;radix,outer=bounds[first],bounds[second]
        forward=['add',first,['mul',radix,second]]
        trial={'order':list(order),'radix':radix}
        trials.append(trial);search['candidates_examined']=len(trials)
        if radix not in data['positive_parameters']:
            trial['status']='missing_positive_radix';continue
        if _poly(data['left']['bound'])!=_poly(['mul',radix,outer]):
            trial['status']='different_cardinality';continue
        left=_factor(data['left']['factor'],{'k':_poly(forward)})
        right=_factor(data['right']['factor'])
        if left!=right:
            trial['status']='different_factors';continue
        trial['status']='matched'
        singleton=_factor(data['left']['factor'],{'m':{():1},'n':{():1},'k':{}})
        certificate={'kind':'euclidean_rectangle_bijection_v1','algorithm':'bounded mixed-radix axis-order search',
            'scalar_domain':data['scalar_domain'],'natural_parameters':data['natural_parameters'],
            'positive_parameters':data['positive_parameters'],'left':data['left'],'right':data['right'],
            'order':list(order),'radix':radix,'outer_bound':outer,'forward':forward,
            'inverse':{first:['mod','k',radix],second:['div','k',radix]},
            'euclidean_trace':_trace(first,second,radix,outer,forward),
            'factor_normal_forms':{'left':{key:_record(p) for key,p in left.items()},
                                   'right':{key:_record(p) for key,p in right.items()}},
            'boundary_cases':{
                'empty_inner':{'condition':['eq',outer,0],'left_cardinality':0,'right_cardinality':0,'both_products':1},
                'singleton_outer':{'condition':['eq',radix,1],'first_coordinate':0,
                                   'forward_after':['add',0,second],'inverse_first':0,'inverse_second':'k'},
                'singleton_total':{'conditions':[['eq',radix,1],['eq',outer,1]],
                                   'unique_index':0,'factor_normal_form':{key:_record(p) for key,p in singleton.items()}}},
            'commutativity_used':True,'cancellation_used':False,'scalar_nonzero_conditions':[],
            'bound_specialized':False,'lean_verified':False}
        return {'status':'constructed','certificate':copy.deepcopy(certificate),'search':copy.deepcopy(search)}
    return {'status':'search_exhausted','reason':'no supported mixed-radix map preserves source factors and ranges',
            'search':copy.deepcopy(search)}
