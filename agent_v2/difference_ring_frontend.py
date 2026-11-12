"""Original finite-product source mapped to a justified evaluated difference tower."""
import re
from .formal_frontend import _Unsupported,_closed_prefix,_node,_num
from .interpolation_frontend import InterpolationParser,lean as _lean
from .models import Source
from .recurrence_frontend import _bounded_ast
from .storage import IntegrityError,verify_source

PROFILE='pochhammer_evaluated_difference_v1'


def lean(node):
    if node['op']=='neg':return '(-'+lean(node['args'][0])+')'
    if node['op'] in ('var','nat','cast','list','regular','pochList'):return _lean(node)
    return '('+(' '+node['op']+' ').join(lean(a) for a in node['args'])+')'


class DifferenceRingParser(InterpolationParser):
    def source(self):
        imports=[]
        while self.peek()=='import':
            self.take();module=self.take()
            if module not in {'Benchmark.Batch4Proofs'}:raise _Unsupported('unsupported source import')
            imports.append(module)
        if len(imports)!=1:raise _Unsupported('one source import required')
        self.sequence('open','scoped','BigOperators','open','FiniteQBenchmark')
        self.sequence('set_option','autoImplicit','false')
        self.sequence('set_option','linter.unusedVariables','false')
        self.take('namespace');namespace=self.take()
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*',namespace):raise _Unsupported('unsupported namespace')
        self.sequence('variable','{');field=self.name()
        self.sequence(':','Type','*','}','[','Field',field,']')
        binders=[{'name':field,'type':'Type u','kind':'implicit'},
                 {'name':None,'type':'Field '+field,'kind':'instance'}]
        if self.peek()=='attribute':self.sequence('attribute','[','local','instance',']','Classical.propDecidable')
        self.take('theorem');theorem=self.name()
        while self.peek()=='(':
            binders.extend(self.binder())
            if len(binders)>16:raise _Unsupported('binder count limit')
        self.take(':');equation=self.expr()
        self.sequence(':=','by','sorry','end',namespace)
        if self.peek() is not None:raise _Unsupported('unconsumed source commands')
        return namespace+'.'+theorem,field,binders,equation


def core_request():
    aq,x,p,pnext=({'op':'atom','key':i,'display':name} for i,name in enumerate(('aq','x','p','pnext')))
    one={'op':'integer','value':1}
    mul=lambda a,b:{'op':'HMul.hMul','args':[a,b]}
    sub=lambda a,b:{'op':'HSub.hSub','args':[a,b]}
    return {'schema_version':1,'method':'difference_ring','input':{'max_degree':3,'max_unknowns':1000,'goal':{
        'lhs':sub(pnext,p),'rhs':{'op':'neg','arg':mul(mul(aq,x),p)},
        'hypotheses':[{'name':'h0','lhs':pnext,'rhs':mul(p,sub(one,mul(aq,x)))}]}}}


def analyze_source(source,run_root=None):
    bound=Source.from_dict(source);verify_source(bound,run_root)
    if bound.Gamma!=bound.declaration:raise IntegrityError('difference ring original context mismatch')
    failure={'status':'not_applicable','profile':PROFILE,'source':bound.to_dict()}
    try:
        theorem,field,binders,equation=DifferenceRingParser(bound.declaration).source();_bounded_ast(equation)
        if theorem!=bound.theorem:raise IntegrityError('difference ring theorem binding mismatch')
        names=[b['name'] for b in binders if b['name']]
        if len(names)!=len(set(names)):raise _Unsupported('duplicate original binder')
        if equation['op']!='=':raise _Unsupported('source equality required')
        lhs,rhs=equation['args']
        pnext,head_tail=(lhs,rhs) if lhs['op']=='pochList' else (rhs,lhs)
        if pnext['op']!='pochList' or head_tail['op']!='*':raise _Unsupported('original first-factor product relation required')
        parameters,q,n=pnext['args']
        if parameters['op']!='list' or len(parameters['args'])!=1:raise _Unsupported('one original product parameter required')
        aq=parameters['args'][0]
        if aq['op']!='*':raise _Unsupported('shifted original parameter required')
        a,q_again=aq['args']
        if q_again!=q or any(v['op']!='var' for v in (a,q,n)) or len({v['name'] for v in (a,q,n)})!=3:
            raise _Unsupported('distinct scalar parameters and natural bound required')
        lower=_node('-',n,_num(1))
        expected=_node('*',_node('-',_num(1),aq),_node('pochList',_node('list',_node('*',a,_node('^',q,_num(2)))),q,lower))
        if head_tail!=expected:raise _Unsupported('original first factor, shifted base or natural interval differs')
        positive=_node('≤',_num(1),n);context={};positive_names=[]
        for binder in binders[2:]:
            if binder['type'] in (field,'ℕ','True'):context[binder['name']]=binder['type']
            elif binder['type_ast']==positive:
                if not all(context.get(v['name'])==ty for v,ty in ((a,field),(q,field),(n,'ℕ'))):
                    raise _Unsupported('positive-bound hypothesis precedes original parameters')
                positive_names.append(binder['name']);context[binder['name']]='Prop'
            else:raise _Unsupported('unsupported original binder domain or hypothesis')
        if not all(context.get(v['name'])==ty for v,ty in ((a,field),(q,field),(n,'ℕ'))) or len(positive_names)!=1:
            raise _Unsupported('exact original scalar/natural domains and positive bound required')
        original=_closed_prefix(binders)+', '+lean(equation)
        if bound.proposition is not None and bound.proposition!=original:raise IntegrityError('difference ring original proposition mismatch')
        p=_node('pochList',parameters,q,lower);x=_node('^',q,lower)
        step=_node('=',pnext,_node('*',p,_node('-',_num(1),_node('*',aq,x))))
        delta=_node('=',_node('-',pnext,p),_node('neg',_node('*',_node('*',aq,x),p)))
        return {'status':'applicable','profile':PROFILE,'source':bound.to_dict(),'binders':binders,
            'symbols':{'field':field,'parameter':a['name'],'base':q['name'],'bound':n['name'],'positive_bound':positive_names[0]},
            'equation':equation,'orientation':'product_equals_head_tail' if pnext is lhs else 'head_tail_equals_product',
            'original_proposition':original,'core_request':core_request(),
            'mapping':{'aq':lean(aq),'x':lean(x),'p':lean(p),'pnext':lean(pnext)},
            'step_equation':step,'step_relation':_closed_prefix(binders)+', '+lean(step),
            'local_equation':delta,'local_proposition':_closed_prefix(binders)+', '+lean(delta),
            'adds_original_assumptions':False,'bound_specialized':False,
            'relation_origin':'source_step must be derived in Lean from singleton pochList, poch_succ and Nat.sub_add_cancel; it is not an original hypothesis',
            'remaining_work':['Initial-factor/tail parameter shift and the original equality remain open.']}
    except (_Unsupported,RecursionError) as error:return dict(failure,reason=str(error))
