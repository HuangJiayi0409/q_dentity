"""Independent exact checking of ordered polynomial action certificates.

The action trace is checked step by step from polynomial definitions. A second
calculation counts ordered M-before-X pairs and checks the arbitrary-degree
monomial action independently of the trace. No constructor, CAS or sampled
polynomial degree is used. This checker creates no formal proof object.
"""
from .models import canonical


def _require(value,message):
    if not value:raise ValueError(message)


def _fields(value,keys):
    _require(type(value) is dict and set(value)==set(keys),'unexpected operator certificate fields')


def _same(actual,expected,message):
    _require(canonical(actual)==canonical(expected),message)


def _bounded(value):
    stack=[(value,0)];count=0
    while stack:
        item,depth=stack.pop();count+=1
        _require(count<=40000 and depth<=16,'operator certificate resource bound exceeded')
        if type(item) is dict:
            _require(all(type(k) is str for k in item),'nonstring operator certificate key')
            stack.extend((v,depth+1) for v in item.values())
        elif type(item) is list:stack.extend((v,depth+1) for v in item)
        elif type(item) is str:_require(len(item)<=256,'oversized operator certificate string')
        else:_require(type(item) in (bool,int) and (type(item) is bool or abs(item)<=100000),
                      'nonexact operator certificate atom')


def _request(request):
    _bounded(request);_fields(request,('schema_version','method','input'))
    _require(type(request['schema_version']) is int and request['schema_version']==1
             and request['method']=='noncommutative','wrong operator request version or method')
    data=request['input']
    _fields(data,('operation','carrier','central_scalar','operators','lhs','rhs','max_steps'))
    _require(data['operation']=='polynomial_operator_words'
             and data['carrier']=='polynomial_over_commutative_field'
             and data['central_scalar']=='q','different operator scalar domain')
    _same(data['operators'],{'X':'multiply_by_variable','M':'substitute_q_times_variable'},
          'unverified operator definitions')
    _require(type(data['max_steps']) is int and 1<=data['max_steps']<=4096,'invalid step budget')
    for side in ('lhs','rhs'):
        _require(type(data[side]) is list and len(data[side])<=16,'oversized operator sum')
        for term in data[side]:
            _fields(term,('coefficient','q_power','word'))
            _require(type(term['coefficient']) is int and abs(term['coefficient'])<=1024,
                     'nonintegral operator coefficient')
            _require(type(term['q_power']) is int and 0<=term['q_power']<=4096,
                     'non-natural scalar exponent')
            _require(type(term['word']) is list and len(term['word'])<=32
                     and all(type(op) is str and op in ('X','M') for op in term['word']),
                     'unknown or oversized operator word')
    return data


def _semantics(cert):
    # These are fixed elementary polynomial rules, never supplied assumptions
    # of the target commutation identity.
    expected={
        'composition_order':'outermost operator first; evaluate from right to left',
        'basis':{'coefficient':'c','degree':'d','degree_domain':'arbitrary natural'},
        'X':{'definition':'p(x) -> x*p(x)','monomial_action':'c*x^d -> c*x^(d+1)'},
        'M':{'definition':'p(x) -> p(q*x)','monomial_action':'c*x^d -> (c*q^d)*x^d'},
        'extension':{'domain':'arbitrary finite-support polynomial',
                     'rule':'K-linearity of multiplication by x and substitution q*x',
                     'coefficient_domain':'commutative field; integer and q coefficients are central'},
        'assumed_operator_relations':[]}
    _same(cert,expected,'changed definitional polynomial semantics or assumed target relation')


def _verify(request,construction):
    data=_request(request);_bounded(construction)
    _fields(construction,('status','certificate','search'))
    _require(construction['status']=='constructed','no constructed operator certificate')
    cert=construction['certificate']
    _fields(cert,('kind','algorithm','input','semantics','terms','normal_forms','degree_specialized',
                  'operator_commutativity_used','scalar_division_used','lean_verified','formal_certificate_exported'))
    _require(cert['kind']=='ordered_polynomial_action_v1'
             and cert['algorithm']=='exact symbolic monomial action normalization','unknown operator certificate')
    _same(cert['input'],data,'operator certificate changed input')
    for flag in ('degree_specialized','operator_commutativity_used','scalar_division_used','lean_verified','formal_certificate_exported'):
        _require(cert[flag] is False,'invalid operator mathematical or formal capability claim')
    _semantics(cert['semantics']);_fields(cert['terms'],('lhs','rhs'))
    _fields(cert['normal_forms'],('lhs','rhs'))
    normal={};steps=0;pairs_checked=0
    for side in ('lhs','rhs'):
        records=cert['terms'][side]
        _require(type(records) is list and len(records)==len(data[side]),'missing source operator terms')
        collected={}
        for original,record in zip(data[side],records):
            _fields(record,('term','trace','action'));_same(record['term'],original,'changed source term')
            word=original['word'];trace=record['trace']
            _require(type(trace) is list and len(trace)==len(word),'incomplete operator action trace')
            current={'degree_offset':0,'q_degree_coefficient':0,'q_constant':original['q_power']}
            for offset,step in enumerate(trace):
                _fields(step,('position','operator','before','after'))
                position=len(word)-1-offset;op=word[position]
                _require(type(step['position']) is int and step['position']==position and step['operator']==op,
                         'operator order differs from source composition')
                _same(step['before'],current,'operator trace has wrong predecessor')
                if op=='X':
                    following={'degree_offset':current['degree_offset']+1,
                        'q_degree_coefficient':current['q_degree_coefficient'],'q_constant':current['q_constant']}
                else:
                    following={'degree_offset':current['degree_offset'],
                        'q_degree_coefficient':current['q_degree_coefficient']+1,
                        'q_constant':current['q_constant']+current['degree_offset']}
                _same(step['after'],following,'polynomial definition action not respected')
                current=following;steps+=1
            _same(record['action'],current,'wrong final polynomial action')
            # Independently count ordered pairs in the ORIGINAL word. Every
            # M contributes d, and each X to its right contributes one extra q.
            degree=word.count('X');slope=word.count('M')
            pairs=sum(1 for i,op in enumerate(word) if op=='M' for later in word[i+1:] if later=='X')
            constant=original['q_power']+pairs;pairs_checked+=pairs
            _same(record['action'],{'degree_offset':degree,'q_degree_coefficient':slope,'q_constant':constant},
                  'trace disagrees with independently derived monomial action')
            key=(degree,slope,constant)
            collected[key]=collected.get(key,0)+original['coefficient']
        normal[side]=[{'coefficient':c,'q_power':q,'x_power':x,'m_power':m}
                      for (x,m,q),c in sorted(collected.items()) if c]
        _same(cert['normal_forms'][side],normal[side],'incorrect additive operator normal form')
    _require(normal['lhs']==normal['rhs'],'independent operator action residual is nonzero')
    _fields(construction['search'],('step_limit','steps_used'))
    _same(construction['search'],{'step_limit':data['max_steps'],'steps_used':steps},'incorrect operator action cost')
    _require(steps<=data['max_steps'],'operator certificate exceeded step budget')
    return {'status':'passed','algorithm':'definition trace replay and independent ordered-pair monomial action',
        'steps_checked':steps,'ordered_pairs_checked':pairs_checked,'normal_forms':normal,
        'arbitrary_degree':True,'degree_sampled':False,
        'finite_polynomial_extension':{
            'basis':'K-linearity of the original multiplication and substitution definitions',
            'symbolic_rule_recorded':True,'lean_verified':False},
        'operator_commutativity_used':False,'scalar_division_used':False,'q_zero_supported':True,
        'lean_verified':False,'formal_certificate_exported':False,
        'remaining_work':'Original polynomial definitions and finite linear extension still require a production Lean bridge'}


def check(request,construction):
    try:return _verify(request,construction)
    except (KeyError,TypeError,IndexError,AttributeError,RecursionError) as error:
        raise ValueError('malformed ordered polynomial action certificate: '+str(error)) from error
