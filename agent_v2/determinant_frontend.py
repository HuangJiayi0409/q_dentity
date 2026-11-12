"""Fully consumed Carlitz matrix Source, preserving every integer operation."""
import re
from .formal_frontend import _Unsupported,_closed_prefix,_node,_num,_var
from .models import Source
from .recurrence_frontend import RecurrenceParser,_bounded_ast
from .storage import IntegrityError,verify_source

PROFILE='carlitz_matrix_minor_v1'
_TOKEN=re.compile(r'\s+|:=|=>|\.toNat|[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*|[0-9]+|[(){}\[\]:,+*^=<>\-/]|[ℕℤ∑→]')


def _tokens(text):
    if len(text)>65536:raise _Unsupported('source exceeds bounded grammar')
    out=[];i=0;depth=0
    while i<len(text):
        pair=text[i:i+2]
        if pair=='/-':depth+=1;out.append(' ');i+=2
        elif pair=='-/' and depth:depth-=1;out.append(' ');i+=2
        elif not depth and pair=='--':
            end=text.find('\n',i);i=len(text) if end<0 else end;out.append(' ')
        else:out.append(' ' if depth else text[i]);i+=1
    if depth:raise _Unsupported('unterminated comment')
    clean=''.join(out);position=0;tokens=[]
    for match in _TOKEN.finditer(clean):
        if match.start()!=position:raise _Unsupported('unsupported source token')
        position=match.end()
        if not match.group().isspace():tokens.append(match.group())
    if position!=len(clean) or len(tokens)>4096:raise _Unsupported('unsupported or oversized syntax')
    return tokens


def lean(node):
    op=node['op']
    if op=='var':return node['name']
    if op=='nat':return str(node['value'])
    if op=='cast':return '('+lean(node['args'][0])+' : ℤ)'
    if op=='val':return lean(node['args'][0])+'.val'
    if op=='toNat':return '('+lean(node['args'][0])+').toNat'
    if op=='apply':return '('+lean(node['args'][0])+' '+lean(node['args'][1])+')'
    if op=='fin_function':return 'Fin '+lean(node['bound'])+' → ℕ'
    if op=='sum_univ':return '(∑ '+node['index']+', '+lean(node['body'])+')'
    if op=='matrix':return '(fun '+node['row']+' '+node['column']+' : Fin '+lean(node['bound'])+' => '+lean(node['body'])+')'
    if op in ('planePi','gaussianInt','Matrix.det','Antitone'):
        name='FiniteQBenchmark.'+op if op in ('planePi','gaussianInt') else op
        return '('+name+' '+' '.join(lean(a) for a in node['args'])+')'
    return '('+(' '+op+' ').join(lean(a) for a in node['args'])+')'


class DeterminantParser(RecurrenceParser):
    def __init__(self,text):self.tokens,self.pos,self.functions=_tokens(text),0,set()

    def name(self):
        value=super().name()
        if value in {'planePi','gaussianInt','Antitone','Fin'}:raise _Unsupported('reserved matrix binder')
        return value

    def binder(self):
        self.take('(');names=[self.name()]
        while self.peek()!=':':
            if len(names)>8:raise _Unsupported('binder group bound')
            names.append(self.name())
        self.take(':')
        if self.peek()=='Fin':
            self.take();bound=_var(self.name());self.sequence('→','ℕ')
            value={'op':'fin_function','bound':bound};self.functions.update(names)
        elif self.peek() in ('ℕ','ℤ','True'):value=_var(self.take())
        else:value=self.expr()
        self.take(')')
        return [{'name':name,'kind':'explicit','type':lean(value),'type_ast':value} for name in names]

    def expr(self,precedence=0,depth=0):
        if depth>64:raise _Unsupported('expression nesting bound')
        left=self.primary(depth+1);operators={'=':1,'<':1,'+':2,'-':2,'*':3,'/':3,'^':4}
        while self.peek() in operators and operators[self.peek()]>=precedence:
            op=self.take();rank=operators[op]
            left=_node(op,left,self.expr(rank if op=='^' else rank+1,depth+1))
        return left

    def primary(self,depth):
        if depth>64:raise _Unsupported('expression nesting bound')
        token=self.peek()
        if token=='(':
            self.take();value=self.expr(depth=depth+1)
            if self.peek()==':':
                self.sequence(':','ℤ');value={'op':'cast','args':[value],'type':'ℤ'}
            self.take(')')
        elif token=='fun':
            self.take();row=self.name();column=self.name();self.sequence(':','Fin')
            bound=_var(self.name());self.take('=>')
            value={'op':'matrix','row':row,'column':column,'bound':bound,'body':self.expr(depth=depth+1)}
        elif token=='∑':
            self.take();index=self.name();self.take(',')
            value={'op':'sum_univ','index':index,'body':self.expr(depth=depth+1)}
        elif token in ('planePi','FiniteQBenchmark.planePi','gaussianInt','FiniteQBenchmark.gaussianInt','Matrix.det','Antitone'):
            symbol=self.take();symbol=symbol.removeprefix('FiniteQBenchmark.')
            value=_node(symbol,*(self.primary(depth+1) for _ in range(1 if symbol in ('Matrix.det','Antitone') else 3)))
        elif token in self.functions:
            function=_var(self.take())
            if self.peek()=='(' or (self.peek() and re.fullmatch('[A-Za-z][A-Za-z0-9_]*',self.peek())):
                value=_node('apply',function,self.primary(depth+1))
            else:value=function
        elif token and token.endswith('.val') and token.count('.')==1:
            name=self.take().removesuffix('.val')
            if not re.fullmatch('[A-Za-z][A-Za-z0-9_]*',name):raise _Unsupported('invalid finite index projection')
            value=_node('val',_var(name))
        else:value=super().primary(depth)
        if self.peek()=='.toNat':self.take();value=_node('toNat',value)
        return value


def core_request():
    entries=[[{'op':'atom','key':2*i+j,'display':f'entry{i}{j}'} for j in range(2)] for i in range(2)]
    return {'schema_version':1,'method':'determinant','input':{'matrix':{'display':'source_minor','entries':entries},
            'size':2,'type':'K','reverse':False}}


def _entry(q,r,n,i,j):
    iv,jv=_node('val',i),_node('val',j)
    cast=lambda x:{'op':'cast','args':[x],'type':'ℤ'}
    d=_node('-',cast(iv),jv)
    exponent=_node('toNat',_node('/',_node('*',d,_node('-',d,_num(1))),_num(2)))
    upper=_node('-',_node('+',cast(_node('apply',n,j)),r),_num(1))
    lower=_node('-',_node('+',_node('-',cast(r),iv),jv),_num(1))
    return _node('*',_node('^',q,exponent),_node('gaussianInt',q,upper,lower))


def analyze_source(source,run_root=None):
    bound=Source.from_dict(source);verify_source(bound,run_root)
    if bound.Gamma!=bound.declaration:raise IntegrityError('determinant original context mismatch')
    failure={'status':'not_applicable','profile':PROFILE,'source':bound.to_dict()}
    try:
        theorem,field,binders,equation=DeterminantParser(bound.declaration).source();_bounded_ast(equation)
        if theorem!=bound.theorem:raise IntegrityError('determinant theorem binding mismatch')
        names=[b['name'] for b in binders if b['name']]
        if len(names)!=len(set(names)):raise _Unsupported('duplicate original binder')
        if equation['op']!='=':raise _Unsupported('original matrix equality required')
        left,right=equation['args'];target,product=(left,right) if left['op']=='planePi' else (right,left)
        if target['op']!='planePi' or product['op']!='*':raise _Unsupported('plane enumerator and weighted determinant required')
        q,r,n=target['args'];weight,det=product['args']
        if any(a['op']!='var' for a in (q,r,n)) or det['op']!='Matrix.det':raise _Unsupported('original matrix variables required')
        matrix=det['args'][0]
        if matrix['op']!='matrix' or matrix['bound']['op']!='var':raise _Unsupported('complete finite matrix lambda required')
        k=matrix['bound'];i,j=_var(matrix['row']),_var(matrix['column'])
        if len({q['name'],r['name'],n['name'],k['name']})!=4 or i['name']==j['name'] or any(x['name'] in names for x in (i,j)):
            raise _Unsupported('overlapping matrix or original binders')
        if matrix['body']!=_entry(q,r,n,i,j):raise _Unsupported('matrix entry cast, exponent or Gaussian indices differ')
        if weight['op']!='^' or weight['args'][0]!=q or weight['args'][1]['op']!='sum_univ':
            raise _Unsupported('original total weight required')
        total=weight['args'][1]
        if total['index'] in names or total['body']!=_node('apply',n,_var(total['index'])):
            raise _Unsupported('original finite-index total changed')
        required=[_node('<',_num(0),k),_node('<',_num(0),r),_node('Antitone',n)]
        expected_function={'op':'fin_function','bound':k};context={};found=[]
        for b in binders[2:]:
            ty=b['type'];ast=b['type_ast']
            if ty in (field,'ℕ','True'):context[b['name']]=ty
            elif ast==expected_function and b['name']==n['name']:
                if context.get(k['name'])!='ℕ':raise _Unsupported('finite domain binder precedes dimension')
                context[b['name']]=ast
            elif ast in required:
                if not all(context.get(v['name'])==t for v,t in ((q,field),(k,'ℕ'),(r,'ℕ'),(n,expected_function))):
                    raise _Unsupported('original hypothesis has unbound or mistyped variables')
                found.append(ast);context[b['name']]='Prop'
            else:raise _Unsupported('unsupported original domain or hypothesis')
        if any(context.get(v['name'])!=t for v,t in ((q,field),(k,'ℕ'),(r,'ℕ'),(n,expected_function))):
            raise _Unsupported('original scalar, finite-function or natural domains differ')
        if any(found.count(h)!=1 for h in required):raise _Unsupported('exact original hypotheses required')
        original=_closed_prefix(binders)+', '+lean(equation)
        if bound.proposition is not None and bound.proposition!=original:raise IntegrityError('determinant original proposition binding mismatch')
        used=set(names)|{i['name'],j['name'],total['index']};selectors=[]
        for label in ('qv2i0','qv2i1','qv2j0','qv2j1'):
            while label in used:label+='x'
            used.add(label);selectors.append(label)
        entries={f'entry{row}{col}':{'row':selectors[row],'column':selectors[2+col],
                    'expression':_entry(q,r,n,_var(selectors[row]),_var(selectors[2+col])),
                    'lean':lean(_entry(q,r,n,_var(selectors[row]),_var(selectors[2+col])))}
                 for row in range(2) for col in range(2)}
        return {'status':'applicable','profile':PROFILE,'source':bound.to_dict(),'binders':binders,
            'symbols':{'field':field,'base':q['name'],'dimension':k['name'],'height':r['name'],'sequence':n['name']},
            'original_proposition':original,'equation':equation,'matrix':matrix,'matrix_term':lean(matrix),
            'selectors':selectors,'minor_entries':entries,'core_request':core_request(),
            'orientation':'target_equals_determinant' if target is left else 'determinant_equals_target',
            'specializes_original_dimension':False,'adds_original_assumptions':False,
            'remaining_work':['Full arbitrary-size determinant and planePi identity remain open.']}
    except (_Unsupported,RecursionError,IndexError) as error:return dict(failure,reason=str(error))
