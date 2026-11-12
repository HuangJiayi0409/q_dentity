"""Independent structural checking of finite ranked choice certificates.

This checks generic Boolean membership, rank rule instances and exact scalar
weights. It does not invoke a search algorithm, enumerate n, verify a Gaussian
representation theorem or export a formal certificate.
"""
from .models import canonical


def _require(value,message):
    if not value:raise ValueError(message)


def _same(actual,expected,message):
    _require(canonical(actual)==canonical(expected),message)


def _fields(value,names):
    _require(type(value) is dict and set(value)==set(names),'unexpected finite choice fields')


def _bounded(value):
    pending=[(value,0)];seen=0
    while pending:
        item,depth=pending.pop();seen+=1
        _require(seen<=12000 and depth<=32,'finite choice certificate resource bound exceeded')
        if type(item) is dict:
            _require(all(type(key) is str for key in item),'nonstring certificate key')
            pending.extend((v,depth+1) for v in item.values())
        elif type(item) is list:pending.extend((v,depth+1) for v in item)
        elif type(item) is str:_require(len(item)<=512,'oversized certificate string')
        else:_require(type(item) in (bool,int) and (type(item) is bool or abs(item)<=10000),
                      'nonexact certificate scalar')


def _small_integer(value,low,high):
    _require(type(value) is int and low<=value<=high,'invalid exact finite choice integer')


def _request(request):
    _bounded(request);_fields(request,('schema_version','method','input'))
    _require(type(request['schema_version']) is int and request['schema_version']==1
             and request['method']=='combinatorial','wrong finite choice request version or method')
    data=request['input']
    _fields(data,('operation','scalar_domain','domain','rank_upper_offset','selected_weight',
                  'factor','rank_weight','max_candidates'))
    _require(data['operation']=='ranked_boolean_choices' and data['scalar_domain']=='commutative_field',
             'different operation or noncommutative scalar domain')
    _same(data['domain'],{'kind':'range','bound':'n'},'ground set is not symbolic range n')
    _small_integer(data['rank_upper_offset'],0,4);_small_integer(data['max_candidates'],1,2)
    _fields(data['factor'],('constant','selected'));_small_integer(data['factor']['constant'],-8,8)
    for weight in (data['selected_weight'],data['factor']['selected']):
        _fields(weight,('coefficient','z_power','q_index_multiplier'))
        _small_integer(weight['coefficient'],-8,8)
        _small_integer(weight['z_power'],0,8);_small_integer(weight['q_index_multiplier'],0,8)
    _fields(data['rank_weight'],('sign_base','z_rank_multiplier','q_index_multiplier'))
    _small_integer(data['rank_weight']['sign_base'],-8,8)
    _small_integer(data['rank_weight']['z_rank_multiplier'],0,8)
    _small_integer(data['rank_weight']['q_index_multiplier'],0,8)
    return data


def _monomial(coefficient,z_degree=0,q_degree=0):
    return {'coefficient':coefficient,'z_power':z_degree if coefficient else 0,
            'q_index_multiplier':q_degree if coefficient else 0}


def _evaluate(expr,member,depth=0):
    _require(depth<=8,'Boolean expression depth exceeded')
    if expr=='b':return member
    _require(type(expr) is list and len(expr)==2 and expr[0]=='not','unknown membership expression')
    return not _evaluate(expr[1],member,depth+1)


def _check_trial(trial,data,name):
    _fields(trial,('candidate','forward','inverse','rows','inverse_checked','weight_preserving',
                   'rank_preserving','rank_range_exact','rank_weights_match','status'))
    _require(trial['candidate']==name,'candidate search order changed')
    expression=['not','b'] if name=='complement' else 'b'
    _same(trial['forward'],expression,'wrong forward membership map')
    _same(trial['inverse'],expression,'wrong inverse membership map')
    _require(type(trial['rows']) is list and len(trial['rows'])==2,'missing universal Boolean cases')
    inverse_ok=True;weights_ok=True;rank_ok=True
    selected=data['selected_weight'];factor=data['factor'];rank=data['rank_weight']
    for bit,row in zip((False,True),trial['rows']):
        _fields(row,('member','forward','inverse_forward','forward_inverse','source_weight','target_weight'))
        forward=_evaluate(trial['forward'],bit)
        backward=_evaluate(trial['inverse'],bit)
        inverse_forward=_evaluate(trial['inverse'],forward)
        forward_inverse=_evaluate(trial['forward'],backward)
        source=_monomial(selected['coefficient'],selected['z_power'],selected['q_index_multiplier']) if bit else _monomial(1)
        chosen=factor['selected']
        target=_monomial(chosen['coefficient'],chosen['z_power'],chosen['q_index_multiplier']) if forward else _monomial(factor['constant'])
        expected={'member':bit,'forward':forward,'inverse_forward':inverse_forward,
                  'forward_inverse':forward_inverse,'source_weight':source,'target_weight':target}
        _same(row,expected,'membership inverse or pointwise scalar weight differs')
        inverse_ok=inverse_ok and inverse_forward==bit and forward_inverse==bit
        weights_ok=weights_ok and source==target;rank_ok=rank_ok and forward==bit
    rank_weight_ok=(rank['sign_base'],rank['z_rank_multiplier'],rank['q_index_multiplier'])==(
        selected['coefficient'],selected['z_power'],selected['q_index_multiplier'])
    verdict={'inverse_checked':inverse_ok,'weight_preserving':weights_ok,'rank_preserving':rank_ok,
             'rank_range_exact':data['rank_upper_offset']==1,'rank_weights_match':rank_weight_ok}
    for key,value in verdict.items():_same(trial[key],value,'false finite choice verdict: '+key)
    _require(trial['status']==('matched' if all(verdict.values()) else 'rejected'),'incorrect candidate classification')
    return all(verdict.values())


def _rank_map(value):
    ground=['range','n'];subset=['subset','s',ground];card=['card','s']
    rules=[
        ('finite_subset_card_nonnegative',[subset],['le',0,card]),
        ('finite_subset_card_le_range',[subset],['le',card,'n']),
        ('nat_lt_successor_of_le',[['le',card,'n']],['lt',card,['add','n',1]]),
        ('rank_tag_cardinality',[subset],['eq',['card',['second',['pair',card,'s']]],card]),
        ('forget_after_rank_tag',[subset],['eq',['second',['pair',card,'s']],'s']),
        ('rank_tag_after_forget',[subset,['eq',card,'k']],['eq',['pair',card,'s'],['pair','k','s']])]
    _same(value,{'forward':['second',['pair','k','s']],'inverse':['pair',card,'s'],
        'rules':[{'rule':name,'requires':premises,'conclusion':conclusion} for name,premises,conclusion in rules]},
        'rank/cardinality rule or inverse pair is incorrect')


def _expansion(value,data):
    _fields(value,('scope','empty_weight','successor','rule_status'))
    _require(value['scope']=='finite distributivity with generic last coordinate, not a Gaussian bridge'
             and type(value['empty_weight']) is int and value['empty_weight']==1
             and value['rule_status']=='symbolic finite-set and distributivity rules; no Lean proof',
             'incorrect finite expansion scope or base')
    step=value['successor']
    _fields(step,('free_atoms','choice_split','rank_increments','sum_normal_form','product_normal_form'))
    _same(step['free_atoms'],['aggregate','z','q^n'],'wrong generic successor scalar atoms')
    _same(step['choice_split'],{
        'domain':['function',['range',['add','n',1]],'Bool'],
        'forward':['pair',['restrict','choice',['range','n']],['at','choice','n']],
        'inverse':['append_last','old_choice','last_bit'],
        'old_coordinate_guard':['lt','i','n'],'new_coordinate':'n',
        'new_coordinate_guard':['lt','n',['add','n',1]],
        'old_coordinate_replay':'old_choice(i)','new_coordinate_replay':'last_bit'},
        'last-coordinate split does not preserve the finite function domain')
    _same(step['rank_increments'],[{'last_bit':False,'increment':0},{'last_bit':True,'increment':1}],
          'wrong cardinality of an appended Boolean choice')
    weight=data['factor']['selected'];constant=data['factor']['constant']
    # Independently derive the two branches A*c and A*w. Their only variables
    # are A, z, q^n; merging equal monomials also covers constant/zero weights.
    polynomial={}
    for key,coefficient in [((1,0,0),constant),
            ((1,weight['z_power'],weight['q_index_multiplier']),weight['coefficient'])]:
        polynomial[key]=polynomial.get(key,0)+coefficient
    expected=[{'powers':list(key),'coefficient':coefficient}
              for key,coefficient in sorted(polynomial.items()) if coefficient]
    _same(step['sum_normal_form'],expected,'incorrect finite choice successor sum')
    _same(step['product_normal_form'],expected,'incorrect distributive product normal form')


def _verify(request,construction):
    data=_request(request);_bounded(construction)
    _fields(construction,('status','certificate','search'))
    _require(construction['status']=='constructed','no constructed finite choice certificate')
    cert=construction['certificate']
    _fields(cert,('kind','algorithm','input','domains','bijection','membership_meaning','rank_map','weights',
                  'finite_expansion','boundaries','construction_kind','gaussian_subset_bridge',
                  'bound_specialized','scalar_cancellation_used','lean_verified','formal_certificate_exported'))
    _require(cert['kind']=='ranked_finite_choice_bijection_v1'
        and cert['algorithm']=='bounded Boolean map synthesis with exact weight and rank normalization',
        'unknown finite choice certificate')
    _same(cert['input'],data,'finite choice certificate changed source request')
    for flag in ('bound_specialized','scalar_cancellation_used','lean_verified','formal_certificate_exported'):
        _require(cert[flag] is False,'unsupported finite choice formal or mathematical claim')
    _require(cert['construction_kind']=='weight_preserving_bijection'
        and cert['gaussian_subset_bridge']=='pending','unverified Gaussian bridge or involution claim')
    _same(cert['domains'],{'ground':['range','n'],'subsets':['powerset',['range','n']],
        'ranked_subsets':['sigma','k',['range',['add','n',1]],['powersetCard',['range','n'],'k']],
        'choices':['function',['range','n'],'Bool'],'bound_type':'arbitrary natural'},'changed finite domains')
    search=construction['search'];_fields(search,('candidate_limit','candidates_examined','trials'))
    _require(type(search['candidate_limit']) is int and search['candidate_limit']==data['max_candidates'],
             'changed choice search budget')
    trials=search['trials']
    _require(type(trials) is list and 1<=len(trials)<=data['max_candidates']
        and type(search['candidates_examined']) is int and search['candidates_examined']==len(trials),
        'incorrect number of actual choice trials')
    verdicts=[_check_trial(trial,data,name) for trial,name in zip(trials,('complement','membership'))]
    _require(verdicts[-1] and not any(verdicts[:-1]),'search did not stop at first valid bijection')
    _same(cert['bijection'],trials[-1],'selected bijection differs from actual search result')
    _same(cert['membership_meaning'],{'b':'i belongs to s','guard':['lt','i','n'],
        'forward':'characteristic Boolean function on range n',
        'inverse':['filter',['range','n'],['eq',['at','choice','i'],True]],
        'pointwise_check':'complete Boolean domain, not a sampled finite bound'},'membership domain or inverse changed')
    _rank_map(cert['rank_map']);weight=data['selected_weight']
    _same(cert['weights'],{'rank_product':{'coefficient_base':weight['coefficient'],'cardinality':'k',
        'z_card_multiplier':weight['z_power'],'q_sum_multiplier':weight['q_index_multiplier'],
        'sum_index':['sum','i','s','i']},'requested_rank_weight':data['rank_weight'],
        'rule':'finite product of central scalar natural-power monomials',
        'rank_relation':['eq','k',['card','s']],
        'sign_reversal_used':False,'fixed_point_cancellation':'not_used'},'ranked weight loses a sign, exponent or domain')
    _expansion(cert['finite_expansion'],data)
    _same(cert['boundaries'],{'empty':{'condition':['eq','n',0],'only_subset':[],'only_choice':[],
        'only_rank':0,'weight':1},'singleton':{'condition':['eq','n',1],
        'subset_choices':[[],[0]],'boolean_choices':[[False],[True]],'ranks':[0,1],
        'selected_weight':{'coefficient':weight['coefficient'],'z_power':weight['z_power'],
                           'q_index_multiplier':0},'unselected_weight':1,'uses_natural_power_zero':True}},
        'empty or singleton range/weight boundary changed')
    return {'status':'passed','algorithm':'independent Boolean inverse, rank rule and integer monomial checking',
        'arbitrary_bound':True,'bound_sampled':False,'generic_boolean_cases_checked':2*len(trials),
        'rank_rule_instances_checked':6,'finite_distributivity_step_checked':True,
        'empty_domain_checked':True,'singleton_domain_checked':True,
        'q_zero_supported':True,'z_zero_supported':True,'scalar_division_used':False,
        'construction_kind':'weight_preserving_bijection','sign_reversal_used':False,
        'fixed_point_cancellation':'not_used','gaussian_subset_bridge':'pending',
        'gaussian_bridge_used_as_assumption':False,'lean_verified':False,
        'formal_certificate_exported':False,
        'remaining_work':'Gaussian fixed-rank subset representation and all finite-set/weight steps require a production Lean bridge'}


def check(request,construction):
    try:return _verify(request,construction)
    except (KeyError,TypeError,IndexError,AttributeError,RecursionError) as error:
        raise ValueError('malformed finite choice certificate: '+str(error)) from error
