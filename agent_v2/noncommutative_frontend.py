"""Complete Source export of polynomial multiplication and q-substitution actions."""
import re
from pathlib import Path
from .formal_frontend import _Parser,_Unsupported,_closed_prefix,_node,_num,_var
from .models import Source
from .recurrence_frontend import _bounded_ast
from .storage import IntegrityError,verify_source,sha256_file

PROFILE='polynomial_q_shift_words_v1'
_TOKEN=re.compile(r'\s+|:=|[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*|[0-9]+|[(){}\[\]:,+*^=<>\-/]|[ℕ≠•]')


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
    if op in ('kacM','kacX'):return '(FiniteQBenchmark.'+op+' '+' '.join(lean(a) for a in node['args'])+')'
    if op=='Polynomial':return '(Polynomial '+lean(node['args'][0])+')'
    return '('+(' '+op+' ').join(lean(a) for a in node['args'])+')'


class NoncommutativeParser(_Parser):
    def __init__(self,text):self.tokens,self.pos=_tokens(text),0
    def name(self):
        value=super().name()
        if value in {'kacM','kacX','Polynomial'}:raise _Unsupported('reserved operator binder')
        return value
    def expr(self,precedence=0,depth=0):
        if depth>64:raise _Unsupported('expression nesting limit')
        left=self.primary(depth+1);operators={'=':1,'≠':1,'•':2,'+':2,'-':2,'*':3,'^':4}
        while self.peek() in operators and operators[self.peek()]>=precedence:
            op=self.take();rank=operators[op]
            left=_node(op,left,self.expr(rank if op=='^' else rank+1,depth+1))
        return left
    def primary(self,depth):
        if depth>64:raise _Unsupported('expression nesting limit')
        token=self.peek()
        if token=='(':
            self.take();value=self.expr(depth=depth+1);self.take(')');return value
        for name,arity in [('kacM',2),('kacX',1),('Polynomial',1)]:
            if token in (name,'FiniteQBenchmark.'+name):
                self.take();return _node(name,*(self.primary(depth+1) for _ in range(arity)))
        if token and token.isdecimal():
            self.take()
            if len(token)>5:raise _Unsupported('oversized integer literal')
            return _num(int(token))
        return _var(self.name())
    def binder(self):
        self.take('(');names=[self.name()]
        while self.peek()!=':':
            names.append(self.name())
            if len(names)>8:raise _Unsupported('binder group limit')
        self.take(':')
        ty=_var(self.take()) if self.peek()=='True' else self.expr()
        self.take(')')
        return [{'name':name,'type':lean(ty),'type_ast':ty,'kind':'explicit'} for name in names]
    def source(self):
        self.sequence('import','Benchmark.Batch5Proofs','open','scoped','BigOperators','open','FiniteQBenchmark',
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


def core_request(reverse=False):
    left={'coefficient':1,'q_power':0,'word':['M','X']}
    right={'coefficient':1,'q_power':1,'word':['X','M']}
    return {'schema_version':1,'method':'noncommutative','input':{
        'operation':'polynomial_operator_words','carrier':'polynomial_over_commutative_field',
        'central_scalar':'q','operators':{'X':'multiply_by_variable','M':'substitute_q_times_variable'},
        'lhs':[right if reverse else left],'rhs':[left if reverse else right],'max_steps':128}}


def operator_definitions():
    path=Path(__file__).resolve().parents[1]/'benchmark/lean/Benchmark/Batch5Definitions.lean'
    text=path.read_text();declarations={}
    patterns={
        'kacX':r'(?m)^def kacX \(f : Polynomial K\) : Polynomial K := Polynomial\.X\*f\s*\n',
        'kacM':r'(?m)^def kacM \(q : K\) \(f : Polynomial K\) : Polynomial K := f\.comp \(Polynomial\.C q\*Polynomial\.X\)\s*\n'}
    for name,pattern in patterns.items():
        matches=list(re.finditer(pattern,text))
        if (len(matches)!=1 or 'namespace FiniteQBenchmark' not in text[:matches[0].start()]
                or 'variable {K : Type*} [Field K]' not in text[:matches[0].start()]):
            raise IntegrityError('fixed polynomial operator definition differs: '+name)
        declarations[name]=matches[0].group().strip()
    return {'path':str(path),'sha256':sha256_file(path),'declarations':declarations,
            'formal_verification':'not performed; definition-derived symbolic action semantics only'}


def analyze_source(source,run_root=None):
    bound=Source.from_dict(source);verify_source(bound,run_root)
    if bound.Gamma!=bound.declaration:raise IntegrityError('noncommutative original context mismatch')
    failure={'status':'not_applicable','profile':PROFILE,'source':bound.to_dict()}
    try:
        theorem,field,binders,body=NoncommutativeParser(bound.declaration).source();_bounded_ast(body)
        if theorem!=bound.theorem:raise IntegrityError('noncommutative theorem binding mismatch')
        names=[b['name'] for b in binders if b['name']]
        if len(set(names))!=len(names):raise _Unsupported('duplicate source binder')
        if body['op']!='=':raise _Unsupported('operator equality required')
        lhs,rhs=body['args'];direct,scaled=(lhs,rhs) if lhs['op']=='kacM' else (rhs,lhs)
        if direct['op']!='kacM' or scaled['op']!='•':raise _Unsupported('q-shift and scalar action pattern required')
        q,inner=direct['args']
        if q['op']!='var' or inner['op']!='kacX':raise _Unsupported('outer q-shift must act after multiplication')
        f=inner['args'][0]
        if f['op']!='var' or len({q['name'],f['name'],field})!=3:raise _Unsupported('distinct symbolic polynomial roles required')
        if scaled!=_node('•',q,_node('kacX',_node('kacM',q,f))):raise _Unsupported('scalar, q-shift base or operator order differs')
        context={};hypotheses={0:[],1:[]}
        for binder in binders[2:]:
            ty=binder['type_ast']
            if ty in (_var(field),_node('Polynomial',_var(field)),_var('True')):
                context[binder['name']]=ty
            elif (ty['op']=='≠' and ty['args'][0]==q and ty['args'][1] in (_num(0),_num(1))
                    and context.get(q['name'])==_var(field)):
                hypotheses[ty['args'][1]['value']].append(binder['name'])
            else:raise _Unsupported('unsupported original hypothesis or carrier')
        if (context.get(q['name'])!=_var(field) or context.get(f['name'])!=_node('Polynomial',_var(field))
                or any(len(values)!=1 for values in hypotheses.values())):
            raise _Unsupported('complete polynomial carrier and original q hypotheses required')
        original=_closed_prefix(binders)+', '+lean(body)
        if bound.proposition is not None and bound.proposition!=original:raise IntegrityError('noncommutative original proposition mismatch')
        reverse=direct is rhs
        return {'status':'applicable','profile':PROFILE,'source':bound.to_dict(),'binders':binders,
            'definition_binding':operator_definitions(),'body':body,'original_proposition':original,
            'core_request':core_request(reverse),'symbols':{'field':field,'base':q['name'],'polynomial':f['name'],
                'q_nonzero':hypotheses[0][0],'q_not_one':hypotheses[1][0]},
            'mapping':{'q':q['name'],'f':f['name'],'arbitrary_polynomial':True,
                'composition_order':'outermost operator first; evaluate word from right to left',
                'X':'multiply polynomial by Polynomial.X','M':'substitute Polynomial.C q * Polynomial.X',
                'scalar_domain':'central coefficients in the original commutative Field',
                'degree':'arbitrary natural d; each finite polynomial extends by coefficient linearity',
                'hypotheses_preserved':[hypotheses[0][0],hypotheses[1][0]],
                'assumed_operator_relations':[]},
            'orientation':'scalar_XM_equals_MX' if reverse else 'MX_equals_scalar_XM',
            'degree_specialized':False,'adds_original_assumptions':False,'formal_bridge_available':False,
            'remaining_work':['Lean formalization of definition expansion, linear extension of monomial action and original theorem acceptance.']}
    except (_Unsupported,KeyError,IndexError,RecursionError) as error:
        return dict(failure,reason=str(error))
