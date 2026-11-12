"""Bounded symbolic synthesis of rank-preserving finite choice bijections.

The bound n is never instantiated. Boolean rows cover every possible generic
membership value at an arbitrary i < n. Polynomial arithmetic checks weights
and the successor distributive step. All output remains untrusted symbolic
evidence, including the explicit finite-set rule instances; no Lean is called.
"""
import copy


def _require(value,message):
    if not value:raise ValueError(message)


def _fields(value,names):
    _require(type(value) is dict and set(value)==set(names),'unsupported finite choice fields')


def _integer(value,low,high):
    _require(type(value) is int and low<=value<=high,'nonexact or oversized finite choice integer')


def _weight(value):
    _fields(value,('coefficient','z_power','q_index_multiplier'))
    _integer(value['coefficient'],-8,8)
    _integer(value['z_power'],0,8);_integer(value['q_index_multiplier'],0,8)


def _validate(data):
    _fields(data,('operation','scalar_domain','domain','rank_upper_offset','selected_weight',
                  'factor','rank_weight','max_candidates'))
    _require(data['operation']=='ranked_boolean_choices'
             and data['scalar_domain']=='commutative_field','unsupported finite choice operation or scalar domain')
    _fields(data['domain'],('kind','bound'))
    _require(data['domain']=={'kind':'range','bound':'n'},'arbitrary symbolic natural ground bound required')
    _integer(data['rank_upper_offset'],0,4);_integer(data['max_candidates'],1,2)
    _weight(data['selected_weight']);_fields(data['factor'],('constant','selected'))
    _integer(data['factor']['constant'],-8,8);_weight(data['factor']['selected'])
    _fields(data['rank_weight'],('sign_base','z_rank_multiplier','q_index_multiplier'))
    _integer(data['rank_weight']['sign_base'],-8,8)
    _integer(data['rank_weight']['z_rank_multiplier'],0,8)
    _integer(data['rank_weight']['q_index_multiplier'],0,8)


def validate_request(request):
    _fields(request,('schema_version','method','input'))
    _require(type(request['schema_version']) is int and request['schema_version']==1
             and request['method']=='combinatorial','unsupported finite choice request')
    _validate(request['input'])


def _bool(expr,value):
    if expr=='b':return value
    _require(expr==['not','b'],'unknown Boolean candidate')
    return not value


def _normal_weight(weight):
    if not weight['coefficient']:
        return {'coefficient':0,'z_power':0,'q_index_multiplier':0}
    return dict(weight)


def _trial(data,name):
    expr=['not','b'] if name=='complement' else 'b'
    rows=[]
    for member in (False,True):
        encoded=_bool(expr,member)
        source=_normal_weight(data['selected_weight'] if member else
            {'coefficient':1,'z_power':0,'q_index_multiplier':0})
        target=_normal_weight(data['factor']['selected'] if encoded else
            {'coefficient':data['factor']['constant'],'z_power':0,'q_index_multiplier':0})
        rows.append({'member':member,'forward':encoded,'inverse_forward':_bool(expr,encoded),
                     'forward_inverse':_bool(expr,_bool(expr,member)),
                     'source_weight':source,'target_weight':target})
    selected=data['selected_weight'];rank=data['rank_weight']
    rank_weights=(rank['sign_base']==selected['coefficient']
        and rank['z_rank_multiplier']==selected['z_power']
        and rank['q_index_multiplier']==selected['q_index_multiplier'])
    verdict={'inverse_checked':all(r['inverse_forward']==r['forward_inverse']==r['member'] for r in rows),
        'weight_preserving':all(r['source_weight']==r['target_weight'] for r in rows),
        'rank_preserving':all(r['forward']==r['member'] for r in rows),
        'rank_range_exact':data['rank_upper_offset']==1,'rank_weights_match':rank_weights}
    return {'candidate':name,'forward':expr,'inverse':copy.deepcopy(expr),'rows':rows,**verdict,
            'status':'matched' if all(verdict.values()) else 'rejected'}


def _add(a,b):
    result=dict(a)
    for key,value in b.items():result[key]=result.get(key,0)+value
    return {key:value for key,value in result.items() if value}


def _multiply(a,b):
    result={}
    for x,c in a.items():
        for y,d in b.items():
            key=tuple(i+j for i,j in zip(x,y));result[key]=result.get(key,0)+c*d
    return {key:value for key,value in result.items() if value}


def _record(poly):
    return [{'powers':list(key),'coefficient':value} for key,value in sorted(poly.items())]


def _rank_rules():
    subset=['subset','s',['range','n']];card=['card','s']
    return [
        {'rule':'finite_subset_card_nonnegative','requires':[subset],'conclusion':['le',0,card]},
        {'rule':'finite_subset_card_le_range','requires':[subset],'conclusion':['le',card,'n']},
        {'rule':'nat_lt_successor_of_le','requires':[['le',card,'n']],
         'conclusion':['lt',card,['add','n',1]]},
        {'rule':'rank_tag_cardinality','requires':[subset],
         'conclusion':['eq',['card',['second',['pair',card,'s']]],card]},
        {'rule':'forget_after_rank_tag','requires':[subset],
         'conclusion':['eq',['second',['pair',card,'s']],'s']},
        {'rule':'rank_tag_after_forget','requires':[subset,['eq',card,'k']],
         'conclusion':['eq',['pair',card,'s'],['pair','k','s']]}]


def _expansion(data):
    factor=data['factor'];weight=factor['selected']
    aggregate={(1,0,0):1};constant={(0,0,0):factor['constant']}
    selected={(0,weight['z_power'],weight['q_index_multiplier']):weight['coefficient']}
    sum_form=_add(_multiply(constant,aggregate),_multiply(selected,aggregate))
    product_form=_multiply(aggregate,_add(constant,selected))
    return {'scope':'finite distributivity with generic last coordinate, not a Gaussian bridge',
        'empty_weight':1,
        'successor':{'free_atoms':['aggregate','z','q^n'],
            'choice_split':{'domain':['function',['range',['add','n',1]],'Bool'],
                'forward':['pair',['restrict','choice',['range','n']],['at','choice','n']],
                'inverse':['append_last','old_choice','last_bit'],
                'old_coordinate_guard':['lt','i','n'],'new_coordinate':'n',
                'new_coordinate_guard':['lt','n',['add','n',1]],
                'old_coordinate_replay':'old_choice(i)','new_coordinate_replay':'last_bit'},
            'rank_increments':[{'last_bit':False,'increment':0},{'last_bit':True,'increment':1}],
            'sum_normal_form':_record(sum_form),'product_normal_form':_record(product_form)},
        'rule_status':'symbolic finite-set and distributivity rules; no Lean proof'}


def _certificate(data,matched):
    w=data['selected_weight'];rank=data['rank_weight']
    return {'kind':'ranked_finite_choice_bijection_v1',
        'algorithm':'bounded Boolean map synthesis with exact weight and rank normalization',
        'input':copy.deepcopy(data),
        'domains':{'ground':['range','n'],'subsets':['powerset',['range','n']],
            'ranked_subsets':['sigma','k',['range',['add','n',1]],['powersetCard',['range','n'],'k']],
            'choices':['function',['range','n'],'Bool'],'bound_type':'arbitrary natural'},
        'bijection':copy.deepcopy(matched),
        'membership_meaning':{'b':'i belongs to s','guard':['lt','i','n'],
            'forward':'characteristic Boolean function on range n',
            'inverse':['filter',['range','n'],['eq',['at','choice','i'],True]],
            'pointwise_check':'complete Boolean domain, not a sampled finite bound'},
        'rank_map':{'forward':['second',['pair','k','s']],
            'inverse':['pair',['card','s'],'s'],'rules':_rank_rules()},
        'weights':{'rank_product':{'coefficient_base':w['coefficient'],'cardinality':'k',
                'z_card_multiplier':w['z_power'],'q_sum_multiplier':w['q_index_multiplier'],
                'sum_index':['sum','i','s','i']},
            'requested_rank_weight':copy.deepcopy(rank),
            'rule':'finite product of central scalar natural-power monomials',
            'rank_relation':['eq','k',['card','s']],
            'sign_reversal_used':False,'fixed_point_cancellation':'not_used'},
        'finite_expansion':_expansion(data),
        'boundaries':{'empty':{'condition':['eq','n',0],'only_subset':[],'only_choice':[],
                'only_rank':0,'weight':1},
            'singleton':{'condition':['eq','n',1],'subset_choices':[[],[0]],
                'boolean_choices':[[False],[True]],'ranks':[0,1],
                'selected_weight':{'coefficient':w['coefficient'],'z_power':w['z_power'],
                                   'q_index_multiplier':0},
                'unselected_weight':1,'uses_natural_power_zero':True}},
        'construction_kind':'weight_preserving_bijection','gaussian_subset_bridge':'pending',
        'bound_specialized':False,'scalar_cancellation_used':False,
        'lean_verified':False,'formal_certificate_exported':False}


def construct(data):
    _validate(data);data=copy.deepcopy(data);trials=[]
    search={'candidate_limit':data['max_candidates'],'candidates_examined':0,'trials':trials}
    for name in ('complement','membership'):
        if len(trials)>=data['max_candidates']:
            return {'status':'budget_exhausted','reason':'finite choice candidate budget exhausted',
                    'search':copy.deepcopy(search)}
        trial=_trial(data,name);trials.append(trial);search['candidates_examined']=len(trials)
        if trial['status']=='matched':
            return {'status':'constructed','certificate':_certificate(data,trial),
                    'search':copy.deepcopy(search)}
    return {'status':'search_exhausted','reason':'no bounded Boolean map preserves rank, factor and signed weight',
            'search':copy.deepcopy(search)}
