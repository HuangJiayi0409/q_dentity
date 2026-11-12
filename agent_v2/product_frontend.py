"""Complete Source export for symbolic finite-product residue reindexing."""
import re
from pathlib import Path
from .formal_frontend import _Parser,_Unsupported,_closed_prefix,_node,_num,_var
from .models import Source
from .recurrence_frontend import _bounded_ast
from .storage import IntegrityError,verify_source,sha256_file

PROFILE='pochhammer_residue_index_v1'
_TOKEN=re.compile(r'\s+|:=|[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*|[0-9]+|[(){}\[\]:,+*^=<>\-/]|[ℕ∏∈]')


def _tokens(text):
    if len(text)>65536:raise _Unsupported('source grammar size limit')
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
    if op=='poch':return '(FiniteQBenchmark.poch '+' '.join(lean(a) for a in node['args'])+')'
    if op=='prod':return '(∏ '+node['index']+' ∈ Finset.range '+lean(node['range'])+', '+lean(node['body'])+')'
    return '('+(' '+op+' ').join(lean(a) for a in node['args'])+')'


class ProductParser(_Parser):
    def __init__(self,text):self.tokens,self.pos=_tokens(text),0
    def name(self):
        value=super().name()
        if value in {'poch','Finset'}:raise _Unsupported('reserved product binder')
        return value
    def expr(self,precedence=0,depth=0):
        if depth>64:raise _Unsupported('expression nesting limit')
        left=self.primary(depth+1);operators={'=':1,'<':1,'+':2,'-':2,'*':3,'/':3,'^':4}
        while self.peek() in operators and operators[self.peek()]>=precedence:
            op=self.take();rank=operators[op]
            left=_node(op,left,self.expr(rank if op=='^' else rank+1,depth+1))
        return left
    def primary(self,depth):
        if depth>64:raise _Unsupported('expression nesting limit')
        token=self.peek()
        if token=='(':
            self.take();value=self.expr(depth=depth+1);self.take(')');return value
        if token in ('poch','FiniteQBenchmark.poch'):
            self.take();return _node('poch',*(self.primary(depth+1) for _ in range(3)))
        if token=='∏':
            self.take();index=self.name();self.sequence('∈','Finset.range')
            bound=self.primary(depth+1);self.take(',')
            return {'op':'prod','index':index,'range':bound,'body':self.expr(depth=depth+1)}
        if token and token.isdecimal():
            self.take()
            if len(token)>5:raise _Unsupported('oversized integer literal')
            return _num(int(token))
        return _var(self.name())
    def binder(self):
        self.take('(');names=[self.name()]
        while self.peek()!=':':names.append(self.name())
        self.take(':')
        ty=_var(self.take()) if self.peek() in ('ℕ','True') else self.expr()
        self.take(')')
        if len(names)>8:raise _Unsupported('binder group limit')
        return [{'name':name,'type':lean(ty),'type_ast':ty,'kind':'explicit'} for name in names]
    def source(self):
        self.sequence('import','Benchmark.Representation','open','scoped','BigOperators','open','FiniteQBenchmark',
            'set_option','autoImplicit','false','set_option','linter.unusedVariables','false','namespace')
        namespace=self.take()
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*',namespace):raise _Unsupported('unsupported namespace')
        self.sequence('variable','{');field=self.name();self.sequence(':','Type','*','}','[','Field',field,']')
        binders=[{'name':field,'type':'Type u','kind':'implicit'},{'name':None,'type':'Field '+field,'kind':'instance'}]
        if self.peek()=='attribute':self.sequence('attribute','[','local','instance',']','Classical.propDecidable')
        self.take('theorem');theorem=self.name()
        while self.peek()=='(':
            binders.extend(self.binder())
            if len(binders)>16:raise _Unsupported('binder count limit')
        self.take(':');body=self.expr();self.sequence(':=','by','sorry','end',namespace)
        if self.peek() is not None:raise _Unsupported('unconsumed source commands')
        return namespace+'.'+theorem,field,binders,body


def core_request():
    return {'schema_version':1,'method':'product','input':{
        'operation':'finite_range_index_equivalence','scalar_domain':'commutative_field',
        'parameter':'a','base':'q',
        'left':{'index':'k','bound':['mul','m','n'],'factor':['sub',1,['mul','a',['pow','q','k']]]},
        'right':{'indices':['j','i'],'bounds':['m','n'],
            'factor':['sub',1,['mul',['mul','a',['pow','q','j']],['pow',['pow','q','m'],'i']]]},
        'positive_parameters':['m'],'natural_parameters':['m','n'],'max_candidates':2}}


def product_definition():
    path=Path(__file__).resolve().parents[1]/'benchmark/lean/Benchmark/Definitions.lean'
    text=path.read_text()
    pattern=r'(?m)^def poch \{K : Type\*\} \[CommRing K\] \(a q : K\) \(n : ℕ\) : K :=\s*\n  ∏ j ∈ Finset\.range n, \(1 - a \* q \^ j\)\s*\n'
    matches=list(re.finditer(pattern,text))
    if len(matches)!=1 or 'namespace FiniteQBenchmark' not in text[:matches[0].start()]:
        raise IntegrityError('the fixed Pochhammer finite-product definition differs from the supported expansion')
    return {'path':str(path),'sha256':sha256_file(path),'declaration':matches[0].group().strip(),
            'formal_verification':'not performed; fixed definition expansion retained for symbolic provenance'}


def analyze_source(source,run_root=None):
    bound=Source.from_dict(source);verify_source(bound,run_root)
    if bound.Gamma!=bound.declaration:raise IntegrityError('product original context mismatch')
    failure={'status':'not_applicable','profile':PROFILE,'source':bound.to_dict()}
    try:
        theorem,field,binders,body=ProductParser(bound.declaration).source();_bounded_ast(body)
        if theorem!=bound.theorem:raise IntegrityError('product theorem binding mismatch')
        names=[b['name'] for b in binders if b['name']]
        if len(set(names))!=len(names):raise _Unsupported('duplicate source binder')
        if body['op']!='=':raise _Unsupported('product equality required')
        lhs,rhs=body['args'];single,multiple=(lhs,rhs) if lhs['op']=='poch' else (rhs,lhs)
        if single['op']!='poch' or multiple['op']!='prod':raise _Unsupported('one product and one finite residue product required')
        a,q,length=single['args'];m=multiple['range'];j=multiple['index']
        if any(x['op']!='var' for x in (a,q,m)) or length['op']!='*':raise _Unsupported('symbolic source dimensions required')
        left_length,n=length['args']
        if left_length!=m or n['op']!='var':raise _Unsupported('exact source rectangle cardinality required')
        if len({a['name'],q['name'],m['name'],n['name'],j,field})!=6 or j in names:
            raise _Unsupported('product roles overlap or index shadows context')
        expected=_node('poch',_node('*',a,_node('^',q,_var(j))),_node('^',q,m),n)
        if multiple['body']!=expected:raise _Unsupported('source factor, stride or finite inner bound differs')
        context={};positive=[]
        for binder in binders[2:]:
            if binder['type'] in (field,'ℕ','True'):context[binder['name']]=binder['type']
            elif binder['type_ast']==_node('<',_num(0),m) and context.get(m['name'])=='ℕ':
                positive.append(binder['name'])
            else:raise _Unsupported('unsupported original hypothesis or parameter domain')
        if any(context.get(v['name'])!=ty for v,ty in ((a,field),(q,field),(m,'ℕ'),(n,'ℕ'))) or len(positive)!=1:
            raise _Unsupported('complete original domains and positive modulus required')
        original=_closed_prefix(binders)+', '+lean(body)
        if bound.proposition is not None and bound.proposition!=original:raise IntegrityError('product original proposition binding mismatch')
        index=next('qv2i'+'x'*i for i in range(32) if 'qv2i'+'x'*i not in set(names)|{j})
        return {'status':'applicable','profile':PROFILE,'source':bound.to_dict(),'binders':binders,
            'definition_binding':product_definition(),
            'body':body,'original_proposition':original,'core_request':core_request(),
            'symbols':{'field':field,'parameter':a['name'],'base':q['name'],'modulus':m['name'],
                       'length':n['name'],'residue_index':j,'inner_index':index,'positive_modulus':positive[0]},
            'mapping':{'a':a['name'],'q':q['name'],'m':m['name'],'n':n['name'],'j':j,'i':index,
                'left_factor':'1 - '+a['name']+' * '+q['name']+'^k',
                'source_expansion':'poch b r t = product over h in range(t) of (1-b*r^h)',
                'original_positive_hypothesis':positive[0],
                'scalar_multiplication':'commutative Field; no scalar cancellation or division'},
            'orientation':'flat_equals_residues' if single is lhs else 'residues_equals_flat',
            'bound_specialized':False,'adds_original_assumptions':False,
            'formal_bridge_available':False,'remaining_work':[
                'Pochhammer definition expansion, finite product reindexing, power identities and original theorem acceptance require Lean.']}
    except (_Unsupported,KeyError,IndexError,RecursionError) as error:
        return dict(failure,reason=str(error))
