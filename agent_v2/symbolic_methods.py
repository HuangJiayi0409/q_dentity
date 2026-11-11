"""Bounded typed adapters for retained mathematical cores without a Lean bridge.

Inputs here are explicit core representations, not purported translations of a
Train theorem. A construction never adds C or replaces formal obligations.
"""
import hashlib
import json
import re
from pathlib import Path
import sys
import time

from .models import Artifact, Source
from .process import prepare_attempt, run_process, validate_seconds, write_json, guard_artifact
from .storage import verify_source, sha256_file

ROOT = Path(__file__).resolve().parents[1]
METHODS = {
    'coefficient': {'family': '系数展开与有限卷积', 'entry': 'finite_product_framework/p2/run.py:construct',
        'structure': 'exported single or branched coefficient equalities in a commutative ring',
        'domain': 'formal commutative-ring atoms, inverses remain independent atoms',
        'limits': 'no automatic Source-to-coefficient exporter; unknown sums remain atoms'},
    'product': {'family':'有限乘积与指标等价','entry':'finite_product_framework/product/pipeline.py:plans',
        'level':'L0',
        'structure':'typed equality of finite natural-range products',
        'domain':'symbolic finite-index transformations; empty ranges retained',
        'limits':'plans() only chooses structural rules, not certificates; actual construction/replay requires missing workflow.contracts/preprocessed'},
    'interpolation': {'family':'插值、零点与有理函数主部','entry':'finite_product_framework/interpolation/algebra.py:zero_certificate',
        'structure':'typed polynomial equality with explicit scalar domain and bounded degree',
        'domain':'formal polynomial ring; CharZero or finite 0/1 separation explicitly declared',
        'limits':'finite-node certificate only; original source extraction and Lean reconstruction unavailable'},
    'noncommutative': {'family':'非交换算子等式','entry':'finite_product_framework/noncommutative/pipeline.py:prove_source',
        'level':'L0','structure':'finite typed noncommutative words and explicit powers at most twelve',
        'domain':'noncommutative rings/operator actions; no commutativity assumption',
        'limits':'actual normalization is Lean operator_words; native environment depends on missing workflow.contracts/preprocessed'},
    'combinatorial': {'family':'加权双射与符号反转对合','entry':'finite_product_framework/combinatorial/pipeline.py:prove_source',
        'level':'L0','structure':'typed finite-range weighted sums and candidate maps',
        'domain':'finite combinatorial objects; map/domain/weight obligations retained',
        'limits':'plans and map descriptions are not constructed certificates; actual map/weight reconstruction requires unavailable workflow and Lean exporter'},
    'difference_ring': {'family':'嵌套和积的差分环','entry':'finite_product_framework/difference_ring/algebra.py:reduce_goal',
        'structure':'polynomial target and explicit polynomial tower relations',
        'domain':'exact QQ polynomial relation ideal with original-relation multipliers',
        'limits':'evaluated tower relation core only; original shift/evaluation bridges and Lean replay remain open'},
    'kernel_transform': {'family':'有限核变换与矩阵反演','entry':'finite_product_framework/kernel_transform/construct.py:construct',
        'dependencies':('finite_product_framework/workflow/matrix_symbolic.py','finite_product_framework/workflow/__init__.py'),
        'structure':'explicit square kernels of dimension one to four with exact scalar entries',
        'domain':'rational-function matrices; denominators require later original-domain proof',
        'limits':'computed inverse/composition certificate only; target-kernel bridge and Lean obligations remain open'},
    'spectral': {'family':'有限谱正交','entry':'finite_product_framework/spectral/construct.py:construct',
        'dependencies':('finite_product_framework/workflow/matrix_symbolic.py','finite_product_framework/workflow/__init__.py'),
        'structure':'explicit weights and two vectors of common dimension one to four',
        'domain':'rational-function weighted self-adjoint operator synthesis',
        'limits':'operator/eigenvalue separator certificate only; rational denominators and original pairing require Lean replay'},
    'determinant': {'family':'行列式结构证书','entry':'finite_product_framework/determinant/construct.py:construct',
        'dependencies':('finite_product_framework/workflow/matrix_symbolic.py','finite_product_framework/workflow/__init__.py'),
        'structure':'explicit square matrix of dimension one to four',
        'domain':'exact symbolic PLU and division-free determinant evaluation',
        'limits':'matrix-only certificate construction; target determinant value and original-domain conditions require Lean replay'},
    'macmahon': {'family':'MacMahon 有理 Ω 消元','entry':'finite_product_framework/p1/qomega.py:compute',
        'dependencies':tuple('finite_product_framework/p1/'+name for name in
            ('core.py','ore.py','expressions.py','qgosper.py','qparameterized.py','zeilberger.py')),
        'structure':'positively graded rational generating function with explicit ge/ct elimination variables',
        'domain':'exact QQ Laurent monomials; finite dimension and generic formal parameters',
        'limits':'at most 8 factors, 4 auxiliary/8 external variables, exponent magnitude 8; core degree 32/states 16/terms 256; no original-object encoding or Lean bridge'},
}


def _fields(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError('input fields do not match the typed mathematical contract')


def _integer(value, low=-1000000, high=1000000):
    if type(value) is not int or not low <= value <= high:
        raise ValueError('integer outside declared resource limits')


def _bounded(value):
    stack, count = [(value, 0)], 0
    while stack:
        node, depth = stack.pop(); count += 1
        if count > 4096 or depth > 32: raise ValueError('input structure exceeds limits')
        if isinstance(node, dict):
            if not all(isinstance(k, str) for k in node): raise ValueError('nonstring input key')
            stack.extend((v, depth+1) for v in node.values())
        elif isinstance(node, list): stack.extend((v, depth+1) for v in node)
        elif isinstance(node, str):
            if len(node) > 1024: raise ValueError('oversized input atom')
        elif node is not None and type(node) not in (int, bool): raise ValueError('nonexact input atom')


def _coefficient(data):
    def expr(node):
        if not isinstance(node, dict): raise ValueError('coefficient expression must be typed')
        op = node.get('op')
        if not isinstance(op,str):raise ValueError('expression operator must be a string')
        if op == 'atom':
            _fields(node, ('op', 'key', 'display')); _integer(node['key'], 0, 256)
            if not isinstance(node['display'], str): raise ValueError('atom display must be text')
        elif op == 'integer': _fields(node, ('op','value')); _integer(node['value'])
        elif op in ('neg','pow'):
            _fields(node, ('op','arg') if op == 'neg' else ('op','arg','exponent'))
            if op == 'pow': _integer(node['exponent'], 0, 8)
            expr(node['arg'])
        elif op in ('HAdd.hAdd','HSub.hSub','HMul.hMul'):
            _fields(node, ('op','args'))
            if not isinstance(node['args'],list) or len(node['args']) != 2: raise ValueError('binary ring operation required')
            for child in node['args']: expr(child)
        else: raise ValueError('unsupported coefficient structure')
    if isinstance(data, dict) and set(data) == {'goals'}:
        if not isinstance(data['goals'],list) or not 1 <= len(data['goals']) <= 16:
            raise ValueError('one to sixteen branches required')
        for goal in data['goals']: _coefficient(goal)
    else:
        _fields(data, ('lhs','rhs')); expr(data['lhs']); expr(data['rhs'])


VALIDATORS = {'coefficient': _coefficient}


def _lean_tree(node, allowed, depth=0):
    if not isinstance(node,dict): raise ValueError('typed expression node required')
    op=node.get('op')
    if not isinstance(op,str):raise ValueError('expression operator must be a string')
    if op=='var':
        _fields(node,('op','name'))
        if not isinstance(node['name'],str) or not re.fullmatch('[a-z][a-z0-9_]{0,31}',node['name']):
            raise ValueError('invalid symbolic variable')
    elif op=='nat': _fields(node,('op','value'));_integer(node['value'],0,10000)
    elif op=='lambda':
        _fields(node,('op','name','body'));_lean_tree({'op':'var','name':node['name']},allowed);_lean_tree(node['body'],allowed)
    elif op in allowed:
        _fields(node,('op','args'))
        if not isinstance(node['args'],list) or len(node['args']) != allowed[op]: raise ValueError('invalid mathematical arity')
        for child in node['args']: _lean_tree(child,allowed)
    else: raise ValueError('unsupported mathematical object')


def _product(data):
    _lean_tree(data,{'Eq':2,'Finset.prod':2,'Finset.range':1,'HAdd.hAdd':2,'HSub.hSub':2,'HMul.hMul':2,'HPow.hPow':2})
    if data['op'] != 'Eq' or not any(n.get('op')=='Finset.prod' for n in _dict_nodes(data)):
        raise ValueError('finite product equality required')


def _dict_nodes(data):
    stack=[data]
    while stack:
        node=stack.pop()
        if isinstance(node,dict): yield node;stack.extend(node.values())
        elif isinstance(node,list): stack.extend(node)


VALIDATORS['product']=_product


def _interpolation(data):
    _fields(data,('goal','max_degree'));_integer(data['max_degree'],0,8)
    goal=data['goal'];_fields(goal,('lhs','rhs','type','char_zero'))
    _coefficient({'lhs':goal['lhs'],'rhs':goal['rhs']})
    if goal['type'] != 'K' or type(goal['char_zero']) is not bool: raise ValueError('explicit scalar domain required')
    for node in _dict_nodes(goal):
        if node.get('op')=='atom' and not re.fullmatch('[a-z][a-z0-9_]{0,31}',node['display']):
            raise ValueError('polynomial atom display must be a scalar identifier')


VALIDATORS['interpolation']=_interpolation


def _noncommutative(data):
    _lean_tree(data,{'Eq':2,'HAdd.hAdd':2,'HSub.hSub':2,'HMul.hMul':2,'HPow.hPow':2})
    if data['op'] != 'Eq' or not any(n.get('op')=='HMul.hMul' for n in _dict_nodes(data)):
        raise ValueError('operator word equality required')
    for node in _dict_nodes(data):
        if node.get('op')=='HPow.hPow' and (node['args'][1]['op']!='nat' or node['args'][1]['value']>12):
            raise ValueError('explicit powers at most twelve required')


VALIDATORS['noncommutative']=_noncommutative


def _combinatorial(data):
    _lean_tree(data,{'Eq':2,'Finset.sum':2,'Finset.range':1,'HAdd.hAdd':2,'HMul.hMul':2,'HPow.hPow':2,'FiniteQBenchmark.gaussian':3})
    if data['op']!='Eq' or not any(n.get('op')=='Finset.sum' for n in _dict_nodes(data)):
        raise ValueError('finite weighted sum equality required')


VALIDATORS['combinatorial']=_combinatorial


def _difference_ring(data):
    _fields(data,('goal','max_degree','max_unknowns'))
    _integer(data['max_degree'],0,16);_integer(data['max_unknowns'],1,10000)
    goal=data['goal'];_fields(goal,('lhs','rhs','hypotheses'))
    _coefficient({'lhs':goal['lhs'],'rhs':goal['rhs']})
    if not isinstance(goal['hypotheses'],list) or len(goal['hypotheses'])>16: raise ValueError('bounded explicit relations required')
    names=[]
    for h in goal['hypotheses']:
        _fields(h,('name','lhs','rhs'));_coefficient({'lhs':h['lhs'],'rhs':h['rhs']})
        if not isinstance(h['name'],str) or not re.fullmatch('h[0-9]{1,3}',h['name']): raise ValueError('relation label must be h<number>')
        names.append(h['name'])
    if len(set(names))!=len(names): raise ValueError('duplicate relation labels')
    for node in _dict_nodes(goal):
        if node.get('op')=='atom' and not re.fullmatch('[a-z][a-z0-9_]{0,31}',node['display']):
            raise ValueError('tower atom display must be scalar identifier')


VALIDATORS['difference_ring']=_difference_ring


def _scalar(node):
    op=node.get('op') if isinstance(node,dict) else None
    if not isinstance(op,str):raise ValueError('scalar operator must be a string')
    if op in ('integer','atom'): _coefficient({'lhs':node,'rhs':node})
    elif op in ('neg','inv','pow'):
        _fields(node,('op','arg') if op!='pow' else ('op','arg','exponent'))
        if op=='pow':_integer(node['exponent'],0,8)
        _scalar(node['arg'])
    elif op in ('HAdd.hAdd','HSub.hSub','HMul.hMul','HDiv.hDiv'):
        _fields(node,('op','args'))
        if not isinstance(node['args'],list) or len(node['args'])!=2: raise ValueError('binary scalar operator required')
        for child in node['args']:_scalar(child)
    else:raise ValueError('unsupported matrix scalar')
    if op=='atom' and not re.fullmatch('[a-z][a-z0-9_]{0,31}',node['display']):raise ValueError('scalar display must be an identifier')


def _matrix(obj,size):
    _fields(obj,('entries','display'))
    if not isinstance(obj['display'],str) or not re.fullmatch('[a-z][a-z0-9_]{0,31}',obj['display']):raise ValueError('matrix label must be identifier')
    rows=obj['entries']
    if not isinstance(rows,list) or len(rows)!=size or any(not isinstance(row,list) or len(row)!=size for row in rows):
        raise ValueError('matrix dimensions do not match declared finite domain')
    for row in rows:
        for node in row:_scalar(node)


def _kernel(data):
    if not isinstance(data,dict) or data.get('operation') not in ('inverse','composition'):raise ValueError('kernel operation required')
    keys=('operation','matrix','proposed_inverse','vector','size','type')
    _fields(data,keys+('target_kernel',) if data['operation']=='composition' else keys)
    _integer(data['size'],1,4)
    if data['type']!='K' or data['vector']!='v':raise ValueError('explicit K scalar domain and v vector anchor required')
    for key in ('matrix','proposed_inverse')+ (('target_kernel',) if data['operation']=='composition' else ()):
        _matrix(data[key],data['size'])


VALIDATORS['kernel_transform']=_kernel


def _spectral(data):
    _fields(data,('weight','left','right','size','type'));_integer(data['size'],1,4)
    if data['type']!='K': raise ValueError('explicit scalar type K required')
    for key in ('weight','left','right'):
        obj=data[key];_fields(obj,('entries','display'))
        if not isinstance(obj['display'],str) or not re.fullmatch('[a-z][a-z0-9_]{0,31}',obj['display']):raise ValueError('vector label required')
        if not isinstance(obj['entries'],list) or len(obj['entries'])!=data['size']:raise ValueError('vector dimension mismatch')
        for node in obj['entries']:_scalar(node)


VALIDATORS['spectral']=_spectral


def _determinant(data):
    _fields(data,('matrix','size','type','reverse'));_integer(data['size'],1,4)
    if data['type']!='K' or type(data['reverse']) is not bool: raise ValueError('scalar domain and orientation required')
    _matrix(data['matrix'],data['size'])


VALIDATORS['determinant']=_determinant


def _macmahon(data):
    _fields(data,('numerator','denominator_monomials','grading','eliminate'))
    def name(value):
        if not isinstance(value,str) or not re.fullmatch('[A-Za-z][A-Za-z0-9_]{0,31}',value) or value in ('n','k'):
            raise ValueError('explicit scalar/auxiliary identifier required (raw n/k indices unsupported)')
    grading=data['grading']
    if not isinstance(grading,dict) or not 1<=len(grading)<=8:raise ValueError('one to eight graded external variables required')
    for key,value in grading.items():name(key);_integer(value,0,8)
    if not any(grading.values()):raise ValueError('positive external grading required')
    eliminate=data['eliminate']
    if not isinstance(eliminate,list) or not 1<=len(eliminate)<=4:raise ValueError('one to four auxiliary variables required')
    variables=set(grading)
    for row in eliminate:
        _fields(row,('variable','operator'));name(row['variable'])
        if row['variable'] in variables or row['operator'] not in ('ge','ct'):raise ValueError('distinct auxiliary variables and ge/ct required')
        variables.add(row['variable'])
    def rational(node):
        if type(node) is int:_integer(node);return
        if isinstance(node,str):
            name(node)
            if node not in variables:raise ValueError('undeclared Omega variable')
            return
        if not isinstance(node,list) or not node:raise ValueError('exact rational arithmetic tree required')
        op=node[0]
        if op=='pow':
            if len(node)!=3:raise ValueError('power requires base and integer exponent')
            rational(node[1]);_integer(node[2],-8,8);return
        arities={'neg':(2,2),'sub':(3,3),'div':(3,3),'add':(3,9),'mul':(3,9)}
        if not isinstance(op,str) or op not in arities or not arities[op][0]<=len(node)<=arities[op][1]:raise ValueError('unsupported rational-tree operation')
        for child in node[1:]:rational(child)
    factors=data['denominator_monomials']
    if not isinstance(factors,list) or len(factors)>8:raise ValueError('at most eight geometric denominator factors required')
    for expr in [data['numerator'],*factors]:rational(expr)


VALIDATORS['macmahon']=_macmahon


def validate_request(request):
    _fields(request, ('schema_version','method','input'))
    if type(request['schema_version']) is not int or request['schema_version'] != 1:
        raise ValueError('unsupported symbolic request version')
    method = request['method']
    if not isinstance(method,str) or method not in METHODS: raise ValueError('unregistered symbolic method')
    _bounded(request['input']); VALIDATORS[method](request['input'])
    atoms={}
    for node in _dict_nodes(request['input']):
        if node.get('op')=='atom':
            key=node['key']
            if key in atoms and atoms[key]!=node['display']:raise ValueError('inconsistent display for one shared scalar atom key')
            atoms[key]=node['display']


def request_digest(request):
    return hashlib.sha256(json.dumps(request,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def analyze_source(source, run_root=None):
    bound = Source.from_dict(source); verify_source(bound, run_root)
    return {'status':'not_applicable', 'source':bound.to_dict(),
        'reason':'This L2 interface requires an explicitly exported core_request; no verified Train exporter is registered.'}


def core_inventory(method):
    info=METHODS[method]
    paths=[info['entry'].split(':')[0],*info.get('dependencies',()),
           'agent_v2/symbolic_methods.py','agent_v2/symbolic_worker.py']
    return {path:sha256_file(ROOT/path) for path in sorted(set(paths))}


def validate_construction(method, data, value):
    """Reject empty/corrupt worker payloads, without treating shape as a proof."""
    def require(condition):
        if not condition:raise ValueError('missing or malformed '+method+' mathematical construction')
    def strings(obj, keys):
        require(isinstance(obj,dict) and all(isinstance(obj.get(k),str) and obj[k] for k in keys))
    require(isinstance(value,dict) and value.get('status')=='constructed')
    if method=='coefficient':
        if 'goals' in data:
            goals=value.get('goals')
            require(isinstance(goals,list) and len(goals)==len(data['goals']) and len(goals)>0)
            require(type(value.get('goal_count')) is int and value['goal_count']==len(goals)
                    and type(value.get('closed_goal_count')) is int and value['closed_goal_count']==len(goals))
            for source,goal in zip(data['goals'],goals):validate_construction(method,source,goal)
        else:
            strings(value,('algorithm','lhs_normal_form','rhs_normal_form','residual'))
            require(value['residual']=='0' and value.get('denominator_cancellation') is False and isinstance(value.get('atoms'),list))
    elif method=='interpolation':
        cert=value.get('certificate');strings(cert,('kind','polynomial','proof_script','node_distinctness'))
        require(cert['kind']=='finite_zero_certificate' and type(cert.get('degree_upper_bound')) is int)
        degree=cert['degree_upper_bound'];require(0<=degree<=data['max_degree'])
        nodes=cert.get('nodes');require(isinstance(nodes,list) and len(nodes)==degree+1)
        require(all(isinstance(n,dict) and isinstance(n.get('node'),str) and n.get('exact_residual')=='0' for n in nodes))
        require(value.get('unverified_proof_script')==cert['proof_script'])
    elif method=='difference_ring':
        cert=value.get('certificate');strings(cert,('algorithm','difference','remainder','script'))
        require(cert['remainder']=='0' and isinstance(cert.get('coefficients'),dict)
                and all(isinstance(k,str) and isinstance(v,str) for k,v in cert['coefficients'].items())
                and isinstance(cert.get('relations'),list) and all(isinstance(r,str) for r in cert['relations']))
    elif method in ('kernel_transform','spectral','determinant'):
        rows=value.get('constructions');require(isinstance(rows,list) and 1<=len(rows)<=2)
        plans={'kernel_transform':{'constructed_rational_inverse':('matrix','inverse'),
                                  'constructed_kernel_composition':('left','right','composition')},
               'spectral':{'constructed_weighted_separator':('operator',)},
               'determinant':{'constructed_symbolic_plu':('matrix','permutation','lower','upper'),
                              'constructed_division_free_determinant':('matrix',)}}[method]
        for row in rows:
            strings(row,('plan','proof_script'));require(row['plan'] in plans)
            cert=row.get('certificate');strings(cert,('algorithm',))
            n=data['size'];require(type(cert.get('dimension')) is int and cert['dimension']==n)
            for key in plans[row['plan']]:
                matrix=cert.get(key)
                require(isinstance(matrix,list) and len(matrix)==n and all(isinstance(r,list) and len(r)==n and all(isinstance(x,str) for x in r) for r in matrix))
            if method=='spectral':require(cert.get('eigenvalues')==['0','1'])
            if method=='determinant':strings(cert,('determinant',))
    elif method=='macmahon':
        result=value.get('result');strings(result,('value',))
        strings(value.get('domain'),('coefficient_field','expansion','scope','specialization_policy'))
        steps=result.get('steps');require(isinstance(steps,list) and len(steps)==len(data['eliminate']))
        for step,operation in zip(steps,data['eliminate']):
            strings(step,('variable','operator','input','output','rational_residual',
                          'polynomial','positive_numerator','positive_denominator','negative_numerator','negative_denominator'))
            require(step['variable']==operation['variable'] and step['operator']==operation['operator'] and step['rational_residual']=='0')
    else:raise ValueError('method has no executable mathematical payload contract')


class SymbolicAdapter:
    def __init__(self, method):
        if method not in METHODS: raise ValueError('unknown symbolic method')
        self.method = method

    def execute(self, identity, method, source, attempt_dir, seconds):
        from .cas_adapter import adapter_result
        start=time.monotonic(); validate_seconds(seconds)
        bound=Source.from_dict(source)
        if bound.identity != identity or method != self.method: raise ValueError('method/source mismatch')
        front=analyze_source(source,Path(bound.snapshot_path).parent.parent)
        attempt=prepare_attempt(attempt_dir)
        if any(attempt.iterdir()): raise ValueError('attempt must be fresh')
        write_json(attempt/'frontend.json',front,attempt)
        return adapter_result(start,'incomplete','not_applicable',front['reason'],raw_result=front,attempt=attempt)

    def execute_request(self, request, attempt_dir, seconds):
        from .cas_adapter import adapter_result
        start=time.monotonic(); attempt=None
        try:
            validate_seconds(seconds); attempt=prepare_attempt(attempt_dir)
            if any(attempt.iterdir()): raise ValueError('attempt must be fresh')
            try:
                validate_request(request)
                if request['method'] != self.method: raise ValueError('request routed to another method')
            except ValueError as error:
                write_json(attempt/'rejection.json',{'code':'not_applicable','message':str(error)},attempt)
                return adapter_result(start,'incomplete','not_applicable',str(error),attempt=attempt)
            write_json(attempt/'request.json',request,attempt)
            write_json(attempt/'input_contract.json',METHODS[self.method],attempt)
            if METHODS[self.method].get('level')=='L0':
                return adapter_result(start,'incomplete','capability_unavailable',METHODS[self.method]['limits'],
                    raw_result={'method':self.method,'capability_level':'L0'},attempt=attempt)
            before=core_inventory(self.method)
            write_json(attempt/'dependencies_before.json',before,attempt)
            command=[sys.executable,'-B','-m','agent_v2.symbolic_worker','--input',str(attempt/'request.json'),
                     '--output',str(attempt/'construction.json')]
            remaining=seconds-(time.monotonic()-start)
            if remaining<=0:
                return adapter_result(start,'budget_exhausted','timeout','Budget exhausted before starting symbolic worker.',attempt=attempt)
            process=run_process(command,ROOT,remaining,
                                attempt/'stdout.txt',attempt/'stderr.txt')
            write_json(attempt/'process.json',process,attempt)
            if process.get('cleanup_survivors'):
                return adapter_result(start,'environment_blocked','cleanup_failed','Symbolic worker process group was not cleaned.',diagnostics=[process],attempt=attempt)
            if process.get('environment_error'):
                return adapter_result(start,'environment_blocked','process_error','Symbolic worker unavailable.',diagnostics=[process],attempt=attempt)
            if process.get('timed_out'):
                return adapter_result(start,'budget_exhausted','timeout','Symbolic core exceeded wall-clock budget.',diagnostics=[process],attempt=attempt)
            output=guard_artifact(attempt/'construction.json',attempt)
            if not output.is_file():
                code='core_process_failed' if process['returncode']!=0 else 'core_output_missing'
                return adapter_result(start,'environment_blocked',code,'No mathematical result file.',diagnostics=[process],attempt=attempt)
            try: raw=json.loads(output.read_text())
            except (ValueError,UnicodeError) as error:
                return adapter_result(start,'integrity_error','malformed_core_output',str(error),attempt=attempt)
            after=core_inventory(self.method)
            write_json(attempt/'dependencies_after.json',after,attempt)
            if before != after:
                return adapter_result(start,'integrity_error','core_source_changed','Mathematical core changed during execution.',attempt=attempt)
            if (not isinstance(raw,dict) or type(raw.get('schema_version')) is not int or raw.get('schema_version')!=1
                    or set(raw)-{'schema_version','method','request_sha256','original_identity_proved','source_before','source_after','status','construction','error','python_version','sympy_version'}
                    or raw.get('source_before') != before or raw.get('source_after') != after
                    or raw.get('request_sha256') != request_digest(request)
                    or raw.get('method') != self.method or raw.get('original_identity_proved') is not False):
                return adapter_result(start,'integrity_error','core_output_mismatch','Result/request binding mismatch.',attempt=attempt)
            if process['returncode']!=0 and raw.get('status')=='constructed':
                return adapter_result(start,'integrity_error','core_exit_mismatch','Core claimed construction after an abnormal exit.',raw_result=raw,attempt=attempt)
            if process['returncode'] != 0 or raw.get('status') == 'environment_blocked':
                return adapter_result(start,'environment_blocked','core_execution_failed','Mathematical worker failed; logs retained.',raw_result=raw,attempt=attempt)
            status=raw.get('status')
            if status=='budget_exhausted':
                return adapter_result(start,'budget_exhausted','resource_exhausted',
                    'Mathematical core reached its declared resource bounds.',raw_result=raw,attempt=attempt)
            if status=='unsupported_domain':
                return adapter_result(start,'incomplete','not_applicable','Mathematical core rejected the declared domain.',raw_result=raw,attempt=attempt)
            if status not in ('constructed','search_exhausted'):
                return adapter_result(start,'integrity_error','unknown_core_status','Unexpected mathematical result status.',raw_result=raw,attempt=attempt)
            if not isinstance(raw.get('construction'),dict) or (status=='constructed' and raw['construction'].get('status')!='constructed'):
                return adapter_result(start,'integrity_error','malformed_construction','Core construction must have a matching typed status.',raw_result=raw,attempt=attempt)
            if status=='constructed':
                try:validate_construction(self.method,request['input'],raw['construction'])
                except ValueError as error:
                    return adapter_result(start,'integrity_error','malformed_construction',str(error),raw_result=raw,attempt=attempt)
            return adapter_result(start,'symbolic_constructed' if status=='constructed' else 'incomplete',
                'translation_pending' if status=='constructed' else 'search_exhausted',
                'Real symbolic construction only; no Lean bridge or formal obligation export.',
                stage='symbolic_core',backend_status=status,raw_result=raw,attempt=attempt)
        except (OSError,ValueError,TypeError) as error:
            return adapter_result(start,'integrity_error','artifact_integrity',str(error))


def adapter(method): return SymbolicAdapter(method)
def coefficient_adapter(): return adapter('coefficient')
def product_adapter(): return adapter('product')
def interpolation_adapter(): return adapter('interpolation')
def noncommutative_adapter(): return adapter('noncommutative')
def combinatorial_adapter(): return adapter('combinatorial')
def difference_ring_adapter(): return adapter('difference_ring')
def kernel_transform_adapter(): return adapter('kernel_transform')
def spectral_adapter(): return adapter('spectral')
def determinant_adapter(): return adapter('determinant')
def macmahon_adapter(): return adapter('macmahon')


def example_request(method):
    a={'op':'atom','key':0,'display':'x'}; b={'op':'atom','key':1,'display':'y'}
    var=lambda n:{'op':'var','name':n}
    prod={'op':'Finset.prod','args':[{'op':'Finset.range','args':[{'op':'HAdd.hAdd','args':[var('m'),var('n')]}]},
                                   {'op':'lambda','name':'k','body':var('x')}]}
    total={'op':'Finset.sum','args':[{'op':'Finset.range','args':[var('n')]},{'op':'lambda','name':'k','body':var('x')}]}
    matrix=lambda name,rows:{'display':name,'entries':[[{'op':'integer','value':v} for v in row] for row in rows]}
    vector=lambda name,row:{'display':name,'entries':[{'op':'integer','value':v} for v in row]}
    examples={'coefficient':{'lhs':{'op':'HAdd.hAdd','args':[a,b]},'rhs':{'op':'HAdd.hAdd','args':[b,a]}},
              'product':{'op':'Eq','args':[prod,prod]},
              'interpolation':{'goal':{'lhs':{'op':'HAdd.hAdd','args':[a,b]},
                  'rhs':{'op':'HAdd.hAdd','args':[b,a]},'type':'K','char_zero':False},'max_degree':4},
              'noncommutative':{'op':'Eq','args':[{'op':'HMul.hMul','args':[var('x'),var('y')]},
                                                  {'op':'HMul.hMul','args':[var('x'),var('y')]}]},
              'combinatorial':{'op':'Eq','args':[total,total]},
              'difference_ring':{'goal':{'lhs':{'op':'pow','arg':a,'exponent':2},
                  'rhs':{'op':'pow','arg':b,'exponent':2},'hypotheses':[{'name':'h0','lhs':a,'rhs':b}]},
                  'max_degree':8,'max_unknowns':1000},
              'kernel_transform':{'operation':'inverse','matrix':matrix('a',[[1,1],[0,1]]),
                  'proposed_inverse':matrix('b',[[1,-1],[0,1]]),'vector':'v','size':2,'type':'K'},
              'spectral':{'weight':vector('w',[1,1]),'left':vector('f',[1,0]),'right':vector('g',[0,1]),'size':2,'type':'K'},
              'determinant':{'matrix':matrix('a',[[1,2],[3,4]]),'size':2,'type':'K','reverse':False},
              'macmahon':{'numerator':1,'denominator_monomials':[['mul','x',['pow','L',2]],['mul','y',['pow','L',-3]]],
                  'grading':{'x':1,'y':1},'eliminate':[{'variable':'L','operator':'ge'}]}}
    return {'schema_version':1,'method':method,'input':examples[method]}


def _dependencies_for(method):
    return tuple(Artifact(str(ROOT/path),digest) for path,digest in core_inventory(method).items())


def coefficient_dependencies(): return _dependencies_for('coefficient')
def product_dependencies(): return _dependencies_for('product')
def interpolation_dependencies(): return _dependencies_for('interpolation')
def noncommutative_dependencies(): return _dependencies_for('noncommutative')
def combinatorial_dependencies(): return _dependencies_for('combinatorial')
def difference_ring_dependencies(): return _dependencies_for('difference_ring')
def kernel_transform_dependencies(): return _dependencies_for('kernel_transform')
def spectral_dependencies(): return _dependencies_for('spectral')
def determinant_dependencies(): return _dependencies_for('determinant')
def macmahon_dependencies(): return _dependencies_for('macmahon')
