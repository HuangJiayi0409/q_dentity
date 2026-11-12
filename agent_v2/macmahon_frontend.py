"""Fully consumed complex Chebyshev Source with a finite Laurent Omega fiber.

The unused ambient Field is retained as source metadata, never generalized into
the monomorphic theorem. All three original conjuncts are parsed and matched.
"""
import re
from .formal_frontend import _Parser,_Unsupported,_closed_prefix,_node,_num,_var
from .models import Source
from .recurrence_frontend import _bounded_ast
from .storage import IntegrityError,verify_source

PROFILE='chebyshev_laurent_omega_v1'
_TOKEN=re.compile(r'\s+|:=|=>|⁻¹|[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*|[0-9]+|[(){}\[\]:,+*^=\-/]|[ℕℤℂ≠≤∑∈∧→ᶜ]')


def _tokens(text):
    if len(text)>65536:raise _Unsupported('source exceeds bounded grammar')
    clean=[];i=0;depth=0
    while i<len(text):
        pair=text[i:i+2]
        if pair=='/-':depth+=1;clean.append(' ');i+=2
        elif pair=='-/' and depth:depth-=1;clean.append(' ');i+=2
        elif not depth and pair=='--':
            end=text.find('\n',i);i=len(text) if end<0 else end;clean.append(' ')
        else:clean.append(' ' if depth else text[i]);i+=1
    if depth:raise _Unsupported('unterminated source comment')
    clean=''.join(clean);tokens=[];position=0
    for match in _TOKEN.finditer(clean):
        if match.start()!=position:raise _Unsupported('unsupported source token')
        position=match.end()
        if not match.group().isspace():tokens.append(match.group())
    if position!=len(clean) or len(tokens)>4096:raise _Unsupported('unsupported or oversized source syntax')
    return tokens


def lean(node):
    op=node['op']
    if op=='var':return node['name']
    if op=='nat':return str(node['value'])
    if op=='cast':return '('+lean(node['args'][0])+' : '+node['type']+')'
    if op=='neg':return '(-'+lean(node['args'][0])+')'
    if op=='inv':return '('+lean(node['args'][0])+')⁻¹'
    if op=='singleton':return '{'+lean(node['args'][0])+'}'
    if op=='compl':return '('+lean(node['args'][0])+')ᶜ'
    if op=='lambda':return '(fun '+node['name']+' : ℂ => '+lean(node['body'])+')'
    if op=='sum':return '(∑ '+node['index']+' ∈ Finset.range '+lean(node['range'])+', '+lean(node['body'])+')'
    if op in ('ultraspherical','regular','Filter.Tendsto','nhdsWithin','nhds'):
        name='FiniteQBenchmark.'+op if op in ('ultraspherical','regular') else op
        return '('+name+' '+' '.join(lean(a) for a in node['args'])+')'
    return '('+(' '+op+' ').join(lean(a) for a in node['args'])+')'


class MacMahonParser(_Parser):
    def __init__(self,text):self.tokens,self.pos=_tokens(text),0
    def name(self):
        name=super().name()
        if name in {'regular','ultraspherical','nhds','nhdsWithin','Filter','PowerSeries','Complex'}:
            raise _Unsupported('reserved binder name')
        return name
    def expr(self,precedence=0,depth=0):
        if depth>64:raise _Unsupported('expression nesting limit')
        left=self.primary(depth+1)
        operators={'→':0,'∧':1,'=':2,'≠':2,'≤':2,'+':3,'-':3,'*':4,'/':4,'^':5}
        while self.peek() in operators and operators[self.peek()]>=precedence:
            op=self.take();rank=operators[op]
            left=_node(op,left,self.expr(rank if op in ('^','∧','→') else rank+1,depth+1))
        return left
    def primary(self,depth):
        if depth>64:raise _Unsupported('expression nesting limit')
        token=self.peek()
        if token=='(':
            self.take();value=self.expr(depth=depth+1)
            if self.peek()==':':
                self.take();kind=self.take()
                if kind not in ('ℤ','ℂ'):raise _Unsupported('unsupported original cast')
                value={'op':'cast','type':kind,'args':[value]}
            self.take(')')
        elif token=='-':self.take();value=_node('neg',self.expr(5,depth+1))
        elif token=='{':self.take();value=_node('singleton',self.expr(depth=depth+1));self.take('}')
        elif token=='fun':
            self.take();name=self.name();self.sequence(':','ℂ','=>')
            value={'op':'lambda','name':name,'body':self.expr(depth=depth+1)}
        elif token=='∑':
            self.take();index=self.name();self.sequence('∈','Finset.range')
            bound=self.primary(depth+1);self.take(',')
            value={'op':'sum','index':index,'range':bound,'body':self.expr(depth=depth+1)}
        elif token in ('regular','FiniteQBenchmark.regular','ultraspherical','FiniteQBenchmark.ultraspherical',
                       'Filter.Tendsto','nhdsWithin','nhds'):
            name=self.take();name=name.removeprefix('FiniteQBenchmark.')
            arity={'regular':1,'ultraspherical':4,'Filter.Tendsto':3,'nhdsWithin':2,'nhds':1}[name]
            value=_node(name,*(self.primary(depth+1) for _ in range(arity)))
        elif token and token.isdecimal():
            self.take()
            if len(token)>5:raise _Unsupported('oversized natural literal')
            value=_num(int(token))
        else:value=_var(self.name())
        while self.peek() in ('⁻¹','ᶜ'):
            value=_node('inv' if self.take()=='⁻¹' else 'compl',value)
        return value
    def binder(self):
        self.take('(');names=[self.name()]
        while self.peek()!=':':names.append(self.name())
        self.take(':')
        ty=_var(self.take()) if self.peek() in ('ℂ','ℕ','True') else self.expr()
        self.take(')')
        if len(names)>8:raise _Unsupported('binder group limit')
        return [{'name':name,'type':lean(ty),'type_ast':ty,'kind':'explicit'} for name in names]
    def source(self):
        self.sequence('import','Benchmark.Batch2Proofs','open','scoped','BigOperators','open','FiniteQBenchmark',
                      'set_option','autoImplicit','false','set_option','linter.unusedVariables','false','namespace')
        namespace=self.take()
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*',namespace):raise _Unsupported('invalid namespace')
        self.sequence('variable','{');field=self.name();self.sequence(':','Type','*','}','[','Field',field,']')
        if self.peek()=='attribute':self.sequence('attribute','[','local','instance',']','Classical.propDecidable')
        self.take('theorem');theorem=self.name();binders=[]
        while self.peek()=='(':
            binders.extend(self.binder())
            if len(binders)>16:raise _Unsupported('binder count limit')
        self.take(':');body=self.expr();self.sequence(':=','by','sorry','end',namespace)
        if self.peek() is not None:raise _Unsupported('unconsumed source commands')
        return namespace+'.'+theorem,field,binders,body


def core_request():
    return {'schema_version':1,'method':'macmahon','input':{'numerator':1,
        'denominator_monomials':[['mul','C0','W0','L0'],['mul','Grade',['pow','W0',-2],['pow','L0',-1]]],
        'grading':{'C0':1,'Grade':1,'W0':0},'eliminate':[{'variable':'L0','operator':'ge'}]}}


def _expected(z,q,n,k,beta):
    text=(f'ultraspherical {q} {z} {q} {n} = (∑ {k} ∈ Finset.range ({n}+1), {z}^(({n}:ℤ)-2*{k})) ∧ '
          f'({z}-{z}⁻¹ ≠ 0 → ultraspherical {q} {z} {q} {n} = ({z}^({n}+1)-{z}^(-({n}:ℤ)-1))/({z}-{z}⁻¹)) ∧ '
          f'(1 ≤ {n} → Filter.Tendsto (fun {beta} : ℂ => (1-{q}^{n})/(2*(1-{beta}))*ultraspherical {beta} {z} {q} {n}) '
          f'(nhdsWithin 1 ({{1}}ᶜ)) (nhds (({z}^{n}+{z}^(-({n}:ℤ)))/2)))')
    parser=MacMahonParser(text);body=parser.expr()
    if parser.peek() is not None:raise RuntimeError('internal source pattern not completely consumed')
    return body


def analyze_source(source,run_root=None):
    bound=Source.from_dict(source);verify_source(bound,run_root)
    if bound.Gamma!=bound.declaration:raise IntegrityError('MacMahon original context binding mismatch')
    failure={'status':'not_applicable','profile':PROFILE,'source':bound.to_dict()}
    try:
        theorem,ambient,binders,body=MacMahonParser(bound.declaration).source();_bounded_ast(body)
        if theorem!=bound.theorem:raise IntegrityError('MacMahon theorem binding mismatch')
        names=[b['name'] for b in binders]
        if len(set(names))!=len(names) or ambient in names:raise _Unsupported('original context shadowing')
        if body['op']!='∧' or body['args'][1]['op']!='∧':raise _Unsupported('complete three-conjunct source required')
        first=body['args'][0]
        if first['op']!='=':raise _Unsupported('source coefficient equality required')
        ultra,total=first['args']
        if ultra['op']!='ultraspherical' or total['op']!='sum':raise _Unsupported('ultraspherical finite Laurent sum required')
        a,z,q,n=ultra['args']
        if any(x['op']!='var' for x in (a,z,q,n)) or a!=q:raise _Unsupported('exact ultraspherical boundary parameters required')
        z,q,n=(x['name'] for x in (z,q,n));k=total['index']
        last=body['args'][1]['args'][1]
        if last['op']!='→' or last['args'][1]['op']!='Filter.Tendsto':raise _Unsupported('complete analytic conjunct required')
        function=last['args'][1]['args'][0]
        if function['op']!='lambda':raise _Unsupported('explicit analytic lambda required')
        beta=function['name']
        if len({z,q,n,k,beta,ambient})!=6 or k in names or beta in names:raise _Unsupported('source binder roles overlap')
        if body!=_expected(z,q,n,k,beta):raise _Unsupported('source conjugate, interval, integer exponent or limit differs')
        context={};regular=[];nonzero=[]
        for binder in binders:
            ty=binder['type_ast']
            if binder['type'] in ('ℂ','ℕ','True'):context[binder['name']]=binder['type']
            elif ty==_node('regular',_var(q)) and context.get(q)=='ℂ':regular.append(binder['name'])
            elif ty==_node('≠',_var(z),_num(0)) and context.get(z)=='ℂ':nonzero.append(binder['name'])
            else:raise _Unsupported('unsupported original hypothesis or binder type')
        if any(context.get(name)!=ty for name,ty in ((z,'ℂ'),(q,'ℂ'),(n,'ℕ'))) or len(regular)!=1 or len(nonzero)!=1:
            raise _Unsupported('original complex domain and hypotheses required')
        original=_closed_prefix(binders)+', '+lean(body)
        if bound.proposition is not None and bound.proposition!=original:raise IntegrityError('MacMahon original proposition mismatch')
        return {'status':'applicable','profile':PROFILE,'source':bound.to_dict(),'binders':binders,
            'ambient_context':{'field':ambient,'type':'Type*','instance':'Field '+ambient,'used_in_theorem':False},
            'universe_parameters':[],'original_proposition':original,'body':body,'source_sum':total,
            'source_exponent':{'bound':1,'index':-2,'constant':0},
            'symbols':{'scalar':z,'base':q,'bound':n,'index':k,'regular':regular[0],'nonzero':nonzero[0]},
            'mapping':{'C0':'coefficient marker at original '+n,'W0':z,'Grade':'finite-fiber regulator for '+k,
                'L0':'nonnegative support '+n+'-'+k,'finite_fiber':'0 <= '+k+' <= '+n,
                'reindexing':{'forward':['n-k','k'],'inverse':['u+v','v']},
                'regulator_removal':'only after each fixed original n has the finite range(n+1)'},
            'core_request':core_request(),'bound_specialized':False,'adds_original_assumptions':False,
            'remaining_work':['Both ultraspherical comparison and the other original two conjuncts remain open.']}
    except (_Unsupported,RecursionError,KeyError,IndexError) as error:return dict(failure,reason=str(error))
