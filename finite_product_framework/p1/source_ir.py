"""Source expression adapters shared by the finite-sum proof methods.

Formal conversion retains domain/support obligations for Lean reconstruction.
This module does not select methods or run benchmark experiments.
"""
import sympy as s
import sys
from pathlib import Path

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parent.parent))
from math_library.source_views import finite_sum_view
from math_library.registry import Library, LibraryError

OPS={'HAdd.hAdd':'add','HSub.hSub':'sub','HMul.hMul':'mul',
     'HDiv.hDiv':'div','HPow.hPow':'pow'}


ATOMS={'FiniteQBenchmark.gaussian':'gaussian','FiniteQBenchmark.poch':'poch',
       'FiniteQBenchmark.kacPowerNat':'fall'}


class InputGap(ValueError):pass


def nodes(node,path=()):
    yield path,node
    for i,a in enumerate(node.get('args',[])):
        yield from nodes(a,path+('args',i))
    if 'body' in node:yield from nodes(node['body'],path+('body',))


def list_items(node):
    out=[]
    while node['op']=='List.cons':
        if len(node.get('args',[]))!=2:raise InputGap('malformed list')
        first,node=node['args'];out.append(first)
    if node['op']!='List.nil':raise InputGap('nonliteral parameter list')
    return out


def var(name):return dict(op='var',name=name)


def nat(i):return dict(op='nat',value=i)


def node(op,*args):return dict(op=op,args=list(args))


def phi_body(term,binder):
    """Compatibility helper; the mathematical formula lives in the library."""
    try:view=finite_sum_view(term)
    except LibraryError as exc:raise InputGap(str(exc)) from exc
    if view is None:raise InputGap('missing phi library view')
    occupied={a['name'] for _,a in nodes(term) if a['op']=='var'}
    if binder in occupied:raise InputGap('requested sum binder would capture a source variable')
    body=view['body']
    for _,a in nodes(body):
        if a.get('op')=='var' and a['name']==view['binder']:a['name']=binder
    return body,view['domain']


def candidates(raw):
    if raw['op']!='Eq':raise InputGap('non-equality target')
    library=Library()
    used={a['name'] for _,a in nodes(raw) if a['op']=='var'}
    fresh='coreindex'
    while fresh in used:fresh+='x'
    out=[]
    for path,a in nodes(raw):
        if a['op']=='Finset.sum':
            domain,binder=a['args']
            if binder['op']!='lambda':continue
            if domain['op'] not in ('Finset.range','Finset.Icc'):continue
            out.append(dict(path=list(path),body=binder['body'],binder=binder['name'],
                            domain=domain,definition=None))
        else:
            try:view=finite_sum_view(a,avoid=used,library=library)
            except LibraryError as exc:raise InputGap(str(exc)) from exc
            if view is not None:
                out.append(dict(path=list(path),**{k:view[k] for k in
                    ('body','binder','domain','definition','library_trace')}))
    return out


class Converter:
    def __init__(self,trees,index,binder=None):
        variables=sorted({a['name'] for tree in trees for _,a in nodes(tree) if a['op']=='var'})
        bases=[]
        geometric=[]
        def base_root(a):
            # Integer powers of the same parameter share a base. Do not infer
            # mathematical dependence between two distinct source parameters.
            if a['op']=='var':return a['name']
            args=a.get('args',[])
            if (a['op']=='HPow.hPow' and len(args)==2 and
                    args[1]['op']=='nat' and args[1]['value']>0):
                return base_root(args[0])
            raise InputGap('base must be a parameter or its positive integer power')
        for tree in trees:
            for _,a in nodes(tree):
                args=a.get('args',[]);op=a['op']
                base=args[0] if op=='FiniteQBenchmark.gaussian' and len(args)==3 else (
                    args[1] if op in ('FiniteQBenchmark.poch','FiniteQBenchmark.pochList') and len(args)==3 else (
                    args[2] if op=='FiniteQBenchmark.kacPowerNat' and len(args)==4 else None))
                if base is not None:bases.append(base_root(base))
                if op=='HPow.hPow' and len(args)==2:
                    exponents={v['name'] for _,v in nodes(args[1]) if v['op']=='var'}
                    if exponents.intersection(v for v in (index,binder) if v is not None):
                        if args[0]['op']=='var':geometric.append(args[0]['name'])
        choices=set(bases or geometric)
        if not choices:raise InputGap('no structural q base exposed')
        if len(choices)!=1:
            raise InputGap('multiple independent bases require a multibase backend: '+', '.join(sorted(choices)))
        base=choices.pop()
        if base in (index,binder) or (binder is not None and index==binder):
            raise InputGap('overlapping index/base roles')
        self.names={base:'q'}
        if index is not None:self.names[index]='n'
        if binder is not None:self.names[binder]='k'
        for name in variables:
            if name not in self.names:self.names[name]='p'+str(len(self.names))
        self.obligations=set(['generic parameter specialization','source-to-formal-expression bridge'])

    def read(self,a):
        op=a['op'];args=a.get('args',[])
        if op=='nat':return a['value']
        if op=='var':return self.names[a['name']]
        if op in ('Nat.cast','Int.ofNat') and len(args)==1:return self.read(args[0])
        if op=='Int.toNat':raise InputGap('integer-to-natural truncation requires a support bridge')
        if op in OPS and len(args)==2:
            if op in ('HSub.hSub','HDiv.hDiv'):
                self.obligations.add('natural subtraction/division versus formal field arithmetic')
            return [OPS[op],*map(self.read,args)]
        if op=='Neg.neg' and len(args)==1:return ['mul',-1,self.read(args[0])]
        if op in ATOMS:
            arity=4 if ATOMS[op]=='fall' else 3
            if len(args)!=arity:raise InputGap('opaque atom arguments: '+op)
            self.obligations.add('finite-product lengths and support')
            if ATOMS[op]=='gaussian':self.obligations.add('Gaussian quotient and zero/singular support')
            return [ATOMS[op],*map(self.read,args)]
        if op=='FiniteQBenchmark.pochList' and len(args)==3:
            values=list_items(args[0]);base,length=map(self.read,args[1:])
            return ['mul',1,*[['poch',self.read(a),base,length] for a in values]]
        raise InputGap('unsupported exported node: '+op)


def outer_index(domain,binder=None):
    names=sorted({a['name'] for _,a in nodes(domain) if a['op']=='var' and a['name']!=binder})
    return 'n' if 'n' in names else names[0] if names else None


def exact_tree(v):
    v=s.sympify(v)
    if v.is_Integer:return int(v)
    if v.is_Rational:return ['div',int(v.p),int(v.q)]
    if v.is_Symbol:return str(v)
    if v.is_Add:return ['add',*map(exact_tree,v.args)]
    if v.is_Mul:return ['mul',*map(exact_tree,v.args)]
    if v.is_Pow and v.exp.is_Integer:return ['pow',exact_tree(v.base),int(v.exp)]
    raise InputGap('shift is not in exact rational-tree grammar: '+str(v))
