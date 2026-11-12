"""Bounded exact normalization of ordered polynomial operator actions.

X multiplies a polynomial by its variable and M substitutes q times the
variable. Each word is evaluated on an arbitrary monomial c*x^d, with d a
symbolic natural number. The relation M X = q X M is NOT an input relation.
No operator symbols commute: the evaluated exponent remembers their order.
The result is an untrusted symbolic certificate, never a Lean proof.
"""
import copy


def _require(value,message):
    if not value:raise ValueError(message)


def _fields(value,keys):
    _require(type(value) is dict and set(value)==set(keys),'unsupported operator fields')


def _validate(data):
    _fields(data,('operation','carrier','central_scalar','operators','lhs','rhs','max_steps'))
    _require(data['operation']=='polynomial_operator_words'
             and data['carrier']=='polynomial_over_commutative_field'
             and data['central_scalar']=='q','unsupported operator domain')
    _fields(data['operators'],('X','M'))
    _require(data['operators']=={'X':'multiply_by_variable','M':'substitute_q_times_variable'},
             'unknown polynomial operator definition')
    _require(type(data['max_steps']) is int and 1<=data['max_steps']<=4096,'invalid operator step budget')
    for side in ('lhs','rhs'):
        terms=data[side]
        _require(type(terms) is list and len(terms)<=16,'operator sum resource bound exceeded')
        for term in terms:
            _fields(term,('coefficient','q_power','word'))
            _require(type(term['coefficient']) is int and abs(term['coefficient'])<=1024,
                     'operator coefficient must be a bounded integer')
            _require(type(term['q_power']) is int and 0<=term['q_power']<=4096,
                     'scalar q exponent must be a bounded natural')
            word=term['word']
            _require(type(word) is list and len(word)<=32 and all(type(x) is str and x in ('M','X') for x in word),
                     'unsupported ordered operator word')


def validate_request(request):
    _fields(request,('schema_version','method','input'))
    _require(type(request['schema_version']) is int and request['schema_version']==1
             and request['method']=='noncommutative','unsupported operator request')
    _validate(request['input'])


def _normal(records):
    coefficients={}
    for term in records:
        state=term['action'];key=(state['degree_offset'],state['q_degree_coefficient'],state['q_constant'])
        coefficients[key]=coefficients.get(key,0)+term['term']['coefficient']
    return [{'coefficient':coefficient,'q_power':q,'x_power':x,'m_power':m}
            for (x,m,q),coefficient in sorted(coefficients.items()) if coefficient]


def _semantics():
    return {
        'composition_order':'outermost operator first; evaluate from right to left',
        'basis':{'coefficient':'c','degree':'d','degree_domain':'arbitrary natural'},
        'X':{'definition':'p(x) -> x*p(x)',
             'monomial_action':'c*x^d -> c*x^(d+1)'},
        'M':{'definition':'p(x) -> p(q*x)',
             'monomial_action':'c*x^d -> (c*q^d)*x^d'},
        'extension':{'domain':'arbitrary finite-support polynomial',
                     'rule':'K-linearity of multiplication by x and substitution q*x',
                     'coefficient_domain':'commutative field; integer and q coefficients are central'},
        'assumed_operator_relations':[]}


def construct(data):
    _validate(data);data=copy.deepcopy(data)
    used=0;records={'lhs':[],'rhs':[]}
    for side in ('lhs','rhs'):
        for term_index,term in enumerate(data[side]):
            state={'degree_offset':0,'q_degree_coefficient':0,'q_constant':term['q_power']}
            trace=[]
            record={'term':term,'trace':trace,'action':state}
            records[side].append(record)
            for position in range(len(term['word'])-1,-1,-1):
                if used>=data['max_steps']:
                    return {'status':'budget_exhausted','reason':'ordered monomial action step budget exhausted',
                        'search':{'step_limit':data['max_steps'],'steps_used':used,
                                  'partial_terms':copy.deepcopy(records),
                                  'next_action':{'side':side,'term_index':term_index,'position':position}}}
                operator=term['word'][position];before=dict(state)
                if operator=='X':state['degree_offset']+=1
                else:
                    state['q_degree_coefficient']+=1
                    state['q_constant']+=state['degree_offset']
                trace.append({'position':position,'operator':operator,'before':before,'after':dict(state)})
                used+=1
    normal={side:_normal(records[side]) for side in ('lhs','rhs')}
    search={'step_limit':data['max_steps'],'steps_used':used}
    certificate={'kind':'ordered_polynomial_action_v1','algorithm':'exact symbolic monomial action normalization',
        'input':data,'semantics':_semantics(),'terms':records,'normal_forms':normal,
        'degree_specialized':False,'operator_commutativity_used':False,'scalar_division_used':False,
        'lean_verified':False,'formal_certificate_exported':False}
    if normal['lhs']!=normal['rhs']:
        return {'status':'search_exhausted','reason':'ordered polynomial action normal forms differ',
                'certificate':certificate,'search':search}
    return {'status':'constructed','certificate':certificate,'search':search}
