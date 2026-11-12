"""Exact independent verification of the source's two-factor Omega certificate.

Rational expressions are read with a bounded AST grammar, then compared by
integer-polynomial cross multiplication. No symbolic solver or CAS script is
used. Positive/negative expansions and the finite source fiber are checked
separately; rational equality by itself is never treated as an Omega proof.
"""
import ast
from .coefficient_translation import _add,_multiply,_integer
from .macmahon_frontend import PROFILE,analyze_source
from .models import canonical
from .symbolic_methods import request_digest

_ONE={():1}
_NAMES={'C0','W0','Grade','L0'}


def _require(value,message):
    if not value:raise ValueError(message)


def _radd(left,right,sign=1):
    a,b=left;c,d=right
    return _add(_multiply(a,d),_multiply(c,b),sign),_multiply(b,d)


def _rmul(left,right):return _multiply(left[0],right[0]),_multiply(left[1],right[1])


def _rinv(value):
    _require(bool(value[0]),'division by the zero polynomial')
    return value[1],value[0]


def _rpow(value,exponent):
    _require(type(exponent) is int and -8<=exponent<=8,'rational power exceeds bound')
    if exponent<0:value=_rinv(value);exponent=-exponent
    result=(_ONE,_ONE)
    for _ in range(exponent):result=_rmul(result,value)
    return result


def _read(text):
    _require(isinstance(text,str) and 0<len(text)<=4096,'invalid rational certificate text')
    tree=ast.parse(text,mode='eval')
    _require(sum(1 for _ in ast.walk(tree))<=256,'rational syntax exceeds bound')
    def integer(node):
        if isinstance(node,ast.Constant) and type(node.value) is int:return node.value
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):return -integer(node.operand)
        raise ValueError('rational exponent must be an integer literal')
    def visit(node,depth=0):
        _require(depth<=32,'rational syntax depth exceeds bound')
        if isinstance(node,ast.Constant):return _integer(node.value),_ONE
        if isinstance(node,ast.Name) and node.id in _NAMES:return {(node.id,):1},_ONE
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):
            result=visit(node.operand,depth+1)
            return (_add({},result[0],-1),result[1]) if isinstance(node.op,ast.USub) else result
        if isinstance(node,ast.BinOp):
            if isinstance(node.op,ast.Pow):return _rpow(visit(node.left,depth+1),integer(node.right))
            left,right=visit(node.left,depth+1),visit(node.right,depth+1)
            if isinstance(node.op,ast.Add):return _radd(left,right)
            if isinstance(node.op,ast.Sub):return _radd(left,right,-1)
            if isinstance(node.op,ast.Mult):return _rmul(left,right)
            if isinstance(node.op,ast.Div):return _rmul(left,_rinv(right))
        raise ValueError('unsupported rational syntax or symbol')
    return visit(tree.body)


def _same(left,right,message):
    _require(_multiply(left[0],right[1])==_multiply(right[0],left[1]),message)


def _substitute(value,name):
    def poly(p):
        out={}
        for monomial,c in p.items():
            remaining=tuple(x for x in monomial if x!=name)
            out[remaining]=out.get(remaining,0)+c
        return {m:c for m,c in out.items() if c}
    result=poly(value[0]),poly(value[1])
    _require(bool(result[1]),'unresolved specialization pole')
    return result


def _one_sided(factor,side):
    numerator,denominator=factor
    _require(denominator==_ONE and numerator,'polynomial block denominator required')
    terms=[(m.count('L0'),m.count('C0')+m.count('Grade')) for m in numerator]
    _require(len(terms)==2 and sorted(i for i,_ in terms)==[0,1],'linear two-term block required')
    grades=dict(terms)
    if side=='positive':_require(grades[0]==0 and grades[1]>0,'not a positive graded block')
    else:_require(grades[1]==0 and grades[0]>0,'not a negative graded block')


def _verify(frontend,raw):
    _require(isinstance(frontend,dict) and frontend.get('profile')==PROFILE
             and frontend.get('status')=='applicable','unsupported MacMahon source frontend')
    _require(canonical(frontend)==canonical(analyze_source(frontend['source'])),
             'MacMahon frontend differs from complete original Source')
    request=frontend['core_request']
    _require(isinstance(raw,dict) and type(raw.get('schema_version')) is int and raw['schema_version']==1
        and raw.get('method')=='macmahon' and raw.get('status')=='constructed'
        and raw.get('original_identity_proved') is False
        and raw.get('request_sha256')==request_digest(request),'different MacMahon request or status')
    result=raw['construction']
    _require(isinstance(result,dict) and result.get('status')=='constructed'
             and result.get('solver')=='rational_omega','missing actual Omega construction')
    expected_domain={'coefficient_field':'QQ(external indeterminates)',
        'expansion':'each 1/(1-M) expands as sum(M**j,j>=0); grade(M)>0',
        'grading':request['input']['grading'],
        'scope':'fixed finite dimension, positively graded Elliott-rational input',
        'specialization_policy':'formal generic result; parameter specialization requires a separate check',
        'negative_result_scope':'unsupported/resource status is never impossibility of an identity'}
    _require(canonical(result['domain'])==canonical(expected_domain),'different Omega expansion or grading')
    original=_read('1/((1-C0*W0*L0)*(1-Grade*W0**(-2)*L0**(-1)))')
    _same(_read(result['normalized_input']),original,'normalized Omega input differs from source encoding')
    steps=result['result']['steps']
    _require(isinstance(steps,list) and len(steps)==1,'exactly one source support projection required')
    step=steps[0]
    keys={'variable','operator','input','factors','polynomial','positive_numerator','positive_denominator',
          'negative_numerator','negative_denominator','output','rational_residual'}
    _require(isinstance(step,dict) and set(step)==keys and step['variable']=='L0' and step['operator']=='ge',
             'unsupported source projection record')
    _same(_read(step['input']),original,'Omega step input differs from source')
    p=_read(step['polynomial']);a=_read(step['positive_numerator']);dp=_read(step['positive_denominator'])
    b=_read(step['negative_numerator']);dm=_read(step['negative_denominator'])
    _require(not p[0],'nonzero polynomial block unsupported in source profile')
    _same(dp,_read('C0*L0*W0-1'),'different positive block denominator')
    _same(dm,_read('Grade-L0*W0**2'),'different negative block denominator')
    for value in (a,b):
        _require(all('L0' not in monomial for poly in value for monomial in poly),
                 'proper block numerator must be independent of auxiliary variable')
    _one_sided(dp,'positive');_one_sided(dm,'negative')
    factors=step['factors']
    _require(isinstance(factors,list) and len(factors)==2,'source two-factor decomposition required')
    sides=set()
    for factor in factors:
        _require(isinstance(factor,dict) and set(factor)=={'factor','multiplicity','side'}
            and type(factor['multiplicity']) is int and factor['multiplicity']==1
            and factor['side'] in ('positive','negative') and factor['side'] not in sides,
            'different factor multiplicity or one-sided assignment')
        side=factor['side'];sides.add(side)
        _same(_read(factor['factor']),dp if side=='positive' else dm,'factor differs from its certified block')
    positive=_rmul(a,_rinv(dp));negative=_rmul(b,_rinv(dm))
    _same(_radd(_radd(p,positive),negative),original,'independent partial-fraction residual is nonzero')
    _require(not _read(step['rational_residual'])[0],'reported residual is not zero')
    projected=_substitute(_radd(p,positive),'L0')
    _same(_read(step['output']),projected,'reported Omega output differs from nonnegative projection')
    value=_read(result['result']['value'])
    _same(value,projected,'final Omega value differs from its actual projection')
    regulated=_read('1/((1-C0*W0)*(1-C0*Grade/W0))')
    _same(value,regulated,'constructed source generating function has different factors')
    _same(_substitute(value,'Grade'),_read('1/((1-C0*W0)*(1-C0/W0))'),
          'finite-fiber regulator removal differs from source Laurent series')
    # For n,k>=0, auxiliary exponent n-k>=0 iff (u,v)=(n-k,k)>=0.
    # Inverse (n,k)=(u+v,v) preserves n; n-2k becomes u-v exactly.
    forward=((1,-1),(0,1));inverse=((1,1),(0,1))
    _require(all(sum(forward[i][k]*inverse[k][j] for k in range(2))==int(i==j)
                 for i in range(2) for j in range(2)),'invalid finite-fiber inverse')
    exponent=frontend['source_exponent']
    _require(exponent=={'bound':1,'index':-2,'constant':0},'different source Laurent weight')
    transformed=[exponent['bound']*inverse[0][j]+exponent['index']*inverse[1][j] for j in range(2)]
    _require(transformed==[1,-1],'source weight does not give the constructed denominator factors')
    return {'status':'passed','request_sha256':request_digest(request),'omega_steps':1,
        'arithmetic':'bounded exact integer rational cross multiplication; no symbolic solver',
        'partial_fraction_residual':'0','one_sided_blocks_checked':2,'strict_negative_block_omitted':True,
        'finite_fiber_checked':True,'finite_fiber':'0 <= k <= n; u=n-k,v=k; n=u+v',
        'source_integer_weight':'n-2*k becomes u-v; regulator Grade becomes Grade^v',
        'regulated_result':'1/((1-C0*W0)*(1-C0*Grade/W0))',
        'specialized_result':'1/((1-C0*W0)*(1-C0/W0))','bound_specialized':False,
        'cas_proof_text_used':False,'formal_denominator_requires_lean':True,
        'lean_required':['unit constant-term denominators','exact finite Cauchy coefficient formula',
                         'source integer-exponent bridge under original z != 0','finite-fiber regulator specialization'],
        'remaining_work':'Ultraspherical comparison and the two other original conjuncts remain open'}


def check(frontend,raw):
    try:return _verify(frontend,raw)
    except (KeyError,TypeError,IndexError,AttributeError,SyntaxError,RecursionError,OSError) as error:
        raise ValueError('malformed source-bound Omega certificate: '+str(error)) from error
