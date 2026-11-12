"""Independent symbolic verification of finite product index certificates.

No constructor or solver is imported. Euclidean rule instances must reproduce
both maps and all domain inequalities. Exact polynomial arithmetic separately
checks natural exponent transport; no field division or cancellation is used.
These are symbolic checks only and never certify a Lean theorem.
"""
from .coefficient_translation import _add,_multiply,_integer
from .models import canonical


def _require(value,message):
    if not value:raise ValueError(message)


def _same(actual,expected,message):
    _require(canonical(actual)==canonical(expected),message)


def _fields(value,keys):
    _require(isinstance(value,dict) and set(value)==set(keys),'unexpected product certificate fields')


def _bounded(value):
    stack=[(value,0)];count=0
    while stack:
        item,depth=stack.pop();count+=1
        _require(count<=4096 and depth<=32,'product certificate resource bound exceeded')
        if isinstance(item,dict):
            _require(all(isinstance(k,str) for k in item),'nonstring product certificate key')
            stack.extend((v,depth+1) for v in item.values())
        elif isinstance(item,list):stack.extend((v,depth+1) for v in item)
        elif isinstance(item,str):_require(len(item)<=256,'oversized product certificate atom')
        else:_require(type(item) in (int,bool) and (type(item) is bool or 0<=item<=100),
                      'nonexact product certificate atom')


def _poly(node,substitution=None):
    substitution=substitution or {}
    if type(node) is int:
        _require(0<=node<=16,'unnatural exponent coefficient')
        return _integer(node)
    if isinstance(node,str):
        _require(node in {'m','n','j','i','k'},'foreign natural exponent variable')
        return substitution.get(node,{(node,):1})
    _require(isinstance(node,list) and len(node)==3 and node[0] in ('add','mul'),
             'unverified natural exponent operation')
    a,b=(_poly(item,substitution) for item in node[1:])
    return _add(a,b) if node[0]=='add' else _multiply(a,b)


def _powers(node,substitution=None):
    if node=='a':return {'a':{():1},'q':{}}
    if node=='q':return {'a':{},'q':{():1}}
    if type(node) is int and node==1:return {'a':{},'q':{}}
    _require(isinstance(node,list) and len(node)==3 and node[0] in ('mul','pow'),
             'unverified product factor operation')
    a=_powers(node[1],substitution)
    if node[0]=='mul':
        b=_powers(node[2],substitution)
        return {key:_add(a[key],b[key]) for key in ('a','q')}
    power=_poly(node[2],substitution)
    return {key:_multiply(a[key],power) for key in ('a','q')}


def _factor(node,substitution=None):
    _require(isinstance(node,list) and len(node)==3 and node[0]=='sub'
             and type(node[1]) is int and node[1]==1,'unverified one-minus-monomial source factor')
    return _powers(node[2],substitution)


def _request(request):
    _bounded(request);_fields(request,('schema_version','method','input'))
    _require(type(request['schema_version']) is int and request['schema_version']==1
             and request['method']=='product','different method request')
    data=request['input']
    _fields(data,('operation','scalar_domain','parameter','base','left','right',
                  'positive_parameters','natural_parameters','max_candidates'))
    _require(data['operation']=='finite_range_index_equivalence' and data['scalar_domain']=='commutative_field'
             and data['parameter']=='a' and data['base']=='q','unsupported source product domain')
    _same(data['natural_parameters'],['m','n'],'changed symbolic natural parameters')
    positive=data['positive_parameters']
    _require(isinstance(positive,list) and all(isinstance(x,str) and x in ('m','n') for x in positive)
             and len(set(positive))==len(positive),'invalid original positive assumptions')
    _require(type(data['max_candidates']) is int and 1<=data['max_candidates']<=2,'invalid original candidate budget')
    left,right=data['left'],data['right']
    _fields(left,('index','bound','factor'));_fields(right,('indices','bounds','factor'))
    _require(left['index']=='k' and right['indices']==['j','i'],'changed source index roles')
    _require(isinstance(right['bounds'],list) and all(isinstance(x,str) for x in right['bounds'])
             and sorted(right['bounds'])==['m','n'],'changed symbolic rectangle bounds')
    names=lambda p:{x for monomial in p for x in monomial}
    _require(names(_poly(left['bound']))<={'m','n'},'index-dependent source range')
    _require(all(names(p)<={'m','n','k'} for p in _factor(left['factor']).values()),'foreign left index')
    _require(all(names(p)<={'m','n','j','i'} for p in _factor(right['factor']).values()),'foreign right index')
    return data


def _record(poly):
    return [{'variables':list(m),'coefficient':c} for m,c in sorted(poly.items())]


def _verify(request,construction):
    data=_request(request);_bounded(construction)
    _fields(construction,('status','certificate','search'))
    _require(construction['status']=='constructed','no constructed product certificate')
    cert=construction['certificate']
    _fields(cert,('kind','algorithm','scalar_domain','natural_parameters','positive_parameters','left','right',
                  'order','radix','outer_bound','forward','inverse','euclidean_trace','factor_normal_forms',
                  'boundary_cases','commutativity_used','cancellation_used','scalar_nonzero_conditions',
                  'bound_specialized','lean_verified'))
    _require(cert['kind']=='euclidean_rectangle_bijection_v1'
             and cert['algorithm']=='bounded mixed-radix axis-order search','unsupported index certificate')
    for key in ('scalar_domain','natural_parameters','positive_parameters','left','right'):
        _same(cert[key],data[key],'certificate changed source '+key)
    _require(cert['commutativity_used'] is True and cert['cancellation_used'] is False
             and cert['scalar_nonzero_conditions']==[] and cert['bound_specialized'] is False
             and cert['lean_verified'] is False,'invalid mathematical or formal capability claim')
    order=cert['order']
    _require(isinstance(order,list) and all(isinstance(x,str) for x in order) and sorted(order)==['i','j'],
             'index map must use both original coordinates exactly once')
    first,second=order;bounds=dict(zip(data['right']['indices'],data['right']['bounds']))
    radix,outer=bounds[first],bounds[second]
    _require(radix in data['positive_parameters'],'Euclidean inverse has no original positive radix hypothesis')
    _require(cert['radix']==radix and cert['outer_bound']==outer,'different radix or quotient range')
    _require(_poly(data['left']['bound'])==_poly(['mul',radix,outer]),'rectangle and source cardinalities differ')
    forward=['add',first,['mul',radix,second]]
    remainder=['mod','k',radix];quotient=['div','k',radix]
    _same(cert['forward'],forward,'changed forward mixed-radix map')
    _same(cert['inverse'],{first:remainder,second:quotient},'changed inverse quotient or remainder')

    # Each entry is an instance of one explicitly bounded elementary Nat rule.
    # Both inverse equations plus image membership establish bijectivity; no
    # finite parameter samples or CAS success flag are used as evidence.
    positive=['lt',0,radix];rbound=['lt',first,radix];qbound=['lt',second,outer]
    expected=[
        {'rule':'nat_remainder_lt','requires':[positive],'conclusion':['lt',remainder,radix]},
        {'rule':'nat_quotient_lt_of_lt_mul','requires':[positive,['lt','k',['mul',radix,outer]]],
         'conclusion':['lt',quotient,outer]},
        {'rule':'nat_remainder_add_radix_quotient','requires':[positive],
         'conclusion':['eq',['add',remainder,['mul',radix,quotient]],'k']},
        {'rule':'nat_mixed_radix_remainder','requires':[positive,rbound],
         'conclusion':['eq',['mod',forward,radix],first]},
        {'rule':'nat_mixed_radix_quotient','requires':[positive,rbound],
         'conclusion':['eq',['div',forward,radix],second]},
        {'rule':'nat_mixed_radix_range','requires':[positive,rbound,qbound],
         'conclusion':['lt',forward,['mul',radix,outer]]}]
    _same(cert['euclidean_trace'],expected,'incomplete or invalid Euclidean proof rule instance')
    left=_factor(data['left']['factor'],{'k':_poly(forward)})
    right=_factor(data['right']['factor'])
    _require(left==right,'independent source factor exponents do not agree under the map')
    normal={'left':{key:_record(p) for key,p in left.items()},
            'right':{key:_record(p) for key,p in right.items()}}
    _same(cert['factor_normal_forms'],normal,'reported factor normal forms differ from independent arithmetic')
    singleton=_factor(data['left']['factor'],{'m':{():1},'n':{():1},'k':{}})
    boundary={
        'empty_inner':{'condition':['eq',outer,0],'left_cardinality':0,'right_cardinality':0,'both_products':1},
        'singleton_outer':{'condition':['eq',radix,1],'first_coordinate':0,
                           'forward_after':['add',0,second],'inverse_first':0,'inverse_second':'k'},
        'singleton_total':{'conditions':[['eq',radix,1],['eq',outer,1]],
                           'unique_index':0,'factor_normal_form':{key:_record(p) for key,p in singleton.items()}}}
    _same(cert['boundary_cases'],boundary,'invalid empty or singleton product boundary')
    search=construction['search'];_fields(search,('candidate_limit','candidates_examined','trials'))
    _require(type(search['candidate_limit']) is int and search['candidate_limit']==data['max_candidates']
             and type(search['candidates_examined']) is int and 1<=search['candidates_examined']<=search['candidate_limit'],
             'invalid bounded search record')
    trials=search['trials']
    _require(isinstance(trials,list) and len(trials)==search['candidates_examined'],'missing actual search trials')
    for position,trial in enumerate(trials):
        _fields(trial,('order','radix','status'))
        trial_order=[['i','j'],['j','i']][position];a,b=trial_order;r,s=bounds[a],bounds[b]
        _same(trial['order'],trial_order,'search used a different coordinate order')
        _require(trial['radix']==r,'search used a different trial radix')
        status=('missing_positive_radix' if r not in data['positive_parameters'] else
                'different_cardinality' if _poly(data['left']['bound'])!=_poly(['mul',r,s]) else
                'different_factors' if _factor(data['left']['factor'],{'k':_poly(['add',a,['mul',r,b]])})
                    !=_factor(data['right']['factor']) else 'matched')
        _require(trial['status']==status and (status=='matched')==(position==len(trials)-1),
                 'search status does not follow from the actual source contract')
    _same(trials[-1]['order'],order,'certificate differs from the selected search candidate')
    return {'status':'passed','algorithm':'independent Euclidean rule instances and exact exponent-polynomial arithmetic',
        'euclidean_rules_checked':6,'forward':forward,'inverse':cert['inverse'],
        'factor_normal_forms':normal,'empty_product_checked':True,'singleton_product_checked':True,
        'natural_exponents_only':True,'q_zero_supported':True,'field_cancellation_used':False,
        'bound_specialized':False,'lean_verified':False,'formal_certificate_exported':False,
        'remaining_work':'Source expansion, Euclidean bijection and factor transport still require a production Lean bridge'}


def check(request,construction):
    try:return _verify(request,construction)
    except (KeyError,TypeError,IndexError,AttributeError,RecursionError) as error:
        raise ValueError('malformed finite product certificate: '+str(error)) from error
