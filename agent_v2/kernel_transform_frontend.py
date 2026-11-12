"""Complete finite Bailey transpose grammar and source-derived affine support.

Ambient namespace variables remain frozen in Source/Gamma. Lean does not
generalize unused namespace K/Field into the theorem-local R/CommRing statement.
"""
import re
from .formal_frontend import _Parser,_Unsupported,_closed_prefix,_node,_num,_var,_NAME,_RESERVED
from .recurrence_frontend import _bounded_ast
from .models import Source
from .storage import IntegrityError,verify_source

PROFILE='bailey_triangular_kernel_v1'
_TOKEN=re.compile(r'\s+|:=|[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*|[0-9]+|[(){}\[\]:,+*^=\-/]|[ℕ∑∈→]')


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
    clean=''.join(clean);position=0;tokens=[]
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
    if op=='apply':return '('+lean(node['args'][0])+' '+lean(node['args'][1])+')'
    if op in ('Finset.range','Finset.Icc'):
        return '('+op+' '+' '.join(lean(a) for a in node['args'])+')'
    if op=='sum':
        return '(∑ '+node['index']+' ∈ '+lean(node['range'])+', '+lean(node['body'])+')'
    return '('+(' '+op+' ').join(lean(a) for a in node['args'])+')'


def total(index,domain,body):return {'op':'sum','index':index,'range':domain,'body':body}
def app(function,index):return _node('apply',function,index)


class KernelParser(_Parser):
    def __init__(self,text):self.tokens,self.pos,self.functions=_tokens(text),0,set()

    def name(self):
        name=self.take()
        # A universe-level name and a term-level sequence named u coexist in
        # Lean. Only this bounded grammar admits u as an ordinary term name.
        if (len(name)>64 or not _NAME.fullmatch(name)
                or name in (_RESERVED-{'u'})|{'CommRing','Finset'}):
            raise _Unsupported('reserved or unsupported kernel binder')
        return name

    def primary(self,depth):
        if depth>64:raise _Unsupported('expression nesting bound')
        if self.peek()=='∑':
            self.take();index=self.name();self.take('∈');kind=self.take()
            if kind not in ('Finset.range','Finset.Icc'):raise _Unsupported('finite kernel range required')
            domain=_node(kind,*(self.primary(depth+1) for _ in range(1 if kind=='Finset.range' else 2)))
            self.take(',');return total(index,domain,self.expr(depth=depth+1))
        if self.peek() in self.functions:
            function=_var(self.take());return app(function,self.primary(depth+1))
        return super().primary(depth)

    def source(self):
        self.sequence('import','Benchmark.Batch4Proofs','open','scoped','BigOperators','open','FiniteQBenchmark')
        self.sequence('set_option','autoImplicit','false','set_option','linter.unusedVariables','false')
        self.take('namespace');namespace=self.take()
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*',namespace):
            raise _Unsupported('unsupported source namespace')
        self.sequence('variable','{');ambient=self.name()
        self.sequence(':','Type','*','}','[','Field',ambient,']')
        self.sequence('attribute','[','local','instance',']','Classical.propDecidable')
        self.take('theorem');name=self.name();self.take('{');ring=self.name()
        if ring==ambient:raise _Unsupported('theorem ring shadows ambient universe parameter')
        self.sequence(':','Type','*','}','[','CommRing',ring,']')
        binders=[{'name':ring,'kind':'implicit','type':'Type u'},
                 {'name':None,'kind':'instance','type':'CommRing '+ring}]
        while self.peek()=='(':
            self.take();names=[self.name()]
            while self.peek()!=':':
                if len(names)>8:raise _Unsupported('binder group bound')
                names.append(self.name())
            self.take(':');kind=self.take()
            if kind not in ('ℕ','True',ring):raise _Unsupported('unsupported kernel parameter type')
            if self.peek()=='→':
                self.sequence('→',ring)
                if kind!='ℕ':raise _Unsupported('natural sequence domain required')
                kind='ℕ → '+ring;self.functions.update(names)
            self.take(')');binders.extend({'name':x,'kind':'explicit','type':kind} for x in names)
            if len(binders)>16:raise _Unsupported('original binder count bound')
        self.take(':');equation=self.expr();self.sequence(':=','by','sorry','end',namespace)
        if self.peek() is not None:raise _Unsupported('unconsumed source command')
        return namespace+'.'+name,ring,binders,equation,[
            {'name':ambient,'kind':'implicit','type':'Type*'},
            {'name':None,'kind':'instance','type':'Field '+ambient}]


def _typed(node,wanted,context,ring):
    op=node['op'];args=node.get('args',[])
    if op=='var':return context.get(node['name'])==wanted
    if op=='nat':return wanted in ('ℕ',ring)
    if op=='apply':return (wanted==ring and args[0]['op']=='var'
        and context.get(args[0]['name'])=='ℕ → '+ring and _typed(args[1],'ℕ',context,ring))
    if op=='sum':
        return (wanted==ring and node['index'] not in context
            and all(_typed(a,'ℕ',context,ring) for a in node['range']['args'])
            and _typed(node['body'],ring,{**context,node['index']:'ℕ'},ring))
    if op in ('+','-','*'):return wanted in ('ℕ',ring) and all(_typed(a,wanted,context,ring) for a in args)
    if op=='=':return wanted=='Prop' and all(_typed(a,ring,context,ring) for a in args)
    return False


def core_request():
    factor=lambda name,index:{'sequence':name,'index':index}
    return {'schema_version':1,'method':'kernel_transform','input':{
        'operation':'triangular_transpose','coordinates':2,'parameter':'N','type':'R',
        'left_domain':[[1,0,0,0],[-1,0,1,0],[-1,1,0,0],[0,-1,1,0]],
        'right_domain':[[1,0,0,0],[-1,0,1,0],[0,1,0,0],[1,-1,0,0]],
        'left_factors':[factor('alpha',[1,0,0,0]),factor('delta',[0,1,0,0]),
                        factor('u',[-1,1,0,0]),factor('v',[1,1,0,0])],
        'right_factors':[factor('delta',[1,0,0,0]),factor('alpha',[0,1,0,0]),
                         factor('u',[1,-1,0,0]),factor('v',[1,1,0,0])],
        'max_multiplier':2}}


def analyze_source(source,run_root=None):
    bound=Source.from_dict(source);verify_source(bound,run_root)
    if bound.Gamma!=bound.declaration:raise IntegrityError('kernel original context mismatch')
    failure={'status':'not_applicable','profile':PROFILE,'source':bound.to_dict()}
    try:
        theorem,ring,binders,equation,ambient=KernelParser(bound.declaration).source();_bounded_ast(equation)
        if theorem!=bound.theorem:raise IntegrityError('kernel theorem binding mismatch')
        names=[b['name'] for b in binders if b['name']]
        if len(names)!=len(set(names)) or ambient[0]['name'] in names:raise _Unsupported('duplicate original binder')
        context={b['name']:b['type'] for b in binders[2:]}
        if equation['op']!='=' or not _typed(equation,'Prop',context,ring):
            raise _Unsupported('typed finite kernel equality required')
        lhs,rhs=equation['args']
        if lhs['op']!='sum' or rhs['op']!='sum':raise _Unsupported('two outer finite sums required')
        ns,rs=lhs['index'],rhs['index'];n=_var(ns);r=_var(rs)
        if lhs['range']['op']!='Finset.range' or rhs['range']!=lhs['range']:
            raise _Unsupported('same original finite outer bound required')
        limit=lhs['range']['args'][0]
        if limit['op']!='+' or limit['args'][0]['op']!='var' or limit['args'][1]!=_num(1):
            raise _Unsupported('arbitrary natural prefix N+1 required')
        N=limit['args'][0]
        if lhs['body']['op']!='*' or rhs['body']['op']!='*':raise _Unsupported('source scalar/kernel actions required')
        alpha_term,inner=lhs['body']['args'];delta_term,other=rhs['body']['args']
        if alpha_term['op']!='apply' or delta_term['op']!='apply' or inner['op']!='sum' or other['op']!='sum':
            raise _Unsupported('original sequence factors and inner finite sums required')
        alpha,delta=alpha_term['args'][0],delta_term['args'][0]
        # Both source scopes are retained; inner names may differ from the other outer names.
        lr=_var(inner['index']);rn=_var(other['index'])
        body=inner['body']
        if body['op']!='*' or body['args'][0]['op']!='*':raise _Unsupported('three inner kernel factors required')
        du,vt=body['args'];dt,ut=du['args']
        if ut['op']!='apply' or vt['op']!='apply':raise _Unsupported('two sequence kernel factors required')
        u,v=ut['args'][0],vt['args'][0]
        symbols=[N,alpha,delta,u,v]
        if any(x['op']!='var' for x in symbols) or len({x['name'] for x in symbols})!=5:
            raise _Unsupported('distinct original bound and sequence binders required')
        weighted=lambda a,d,x,y:_node('*',_node('*',app(a,x),app(u,_node('-',y,x))),app(v,_node('+',y,x)))
        expected_l=total(ns,_node('Finset.range',_node('+',N,_num(1))),
            _node('*',app(alpha,n),total(inner['index'],_node('Finset.Icc',n,N),
                _node('*',_node('*',app(delta,lr),app(u,_node('-',lr,n))),app(v,_node('+',lr,n))))))
        expected_r=total(rs,_node('Finset.range',_node('+',N,_num(1))),
            _node('*',app(delta,r),total(other['index'],_node('Finset.range',_node('+',r,_num(1))),
                weighted(alpha,delta,rn,r))))
        if lhs!=expected_l or rhs!=expected_r:raise _Unsupported('source support, kernel direction or weight differs')
        if context.get(N['name'])!='ℕ' or any(context.get(x['name'])!='ℕ → '+ring for x in (alpha,delta,u,v)):
            raise _Unsupported('source scalar/sequence domains differ')
        original=_closed_prefix(binders)+', '+lean(equation)
        if bound.proposition is not None and bound.proposition!=original:raise IntegrityError('kernel original proposition mismatch')
        term=_node('*',app(alpha,rn),_node('*',_node('*',app(delta,r),app(u,_node('-',r,rn))),app(v,_node('+',r,rn))))
        transposed=total(rs,rhs['range'],total(other['index'],other['range'],term))
        local=_closed_prefix(binders)+', '+lean(_node('=',lhs,transposed))
        return {'status':'applicable','profile':PROFILE,'source':bound.to_dict(),'binders':binders,
            'ambient_context':ambient,'ambient_variables_generalized':False,'original_proposition':original,
            'local_proposition':local,'equation':equation,'transposed':transposed,
            'symbols':{'ring':ring,'bound':N['name'],'alpha':alpha['name'],'delta':delta['name'],'u':u['name'],'v':v['name']},
            'core_request':core_request(),'mapping':{'left_coordinates':[ns,inner['index']],
                'right_coordinates':[rs,other['index']],'symbolic_parameter':N['name'],
                'sequence_atoms':{role:value['name'] for role,value in zip(('alpha','delta','u','v'),(alpha,delta,u,v))},
                'inequality_convention':'a*x0+b*x1+c*N+d >= 0; all index arithmetic stays natural in Lean',
                'natural_subtraction_guard':'inner lower index <= outer upper index'},
            'specializes_bound':False,'adds_original_assumptions':False,
            'remaining_work':['Extracting delta from the transposed sum and original theorem acceptance remain open.']}
    except (_Unsupported,RecursionError,IndexError,KeyError) as error:return dict(failure,reason=str(error))
