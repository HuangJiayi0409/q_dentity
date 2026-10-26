"""Use catalogue definitions directly in the existing finite-sum source IR.

No field cancellation, sum evaluation, assumed sequence law, or method selection.
Natural arithmetic stays in the source tree. Arbitrary functions stay opaque.
"""
import copy

from .registry import Library, LibraryError, names


def literal_list(tree):
    items=[]
    while tree.get('op')=='List.cons':
        if len(tree.get('args',[]))!=2:raise LibraryError('malformed_list')
        first,tree=tree['args'];items.append(first)
        if len(items)>4096:raise LibraryError('list_length_limit')
    if tree.get('op')!='List.nil':raise LibraryError('literal_parameter_list_required')
    return items


def apply_definition(lib,key,bindings,trace,avoid=()):
    result=lib.instantiate(key,bindings,avoid=avoid)
    if result['unresolved']:raise LibraryError('definition_requires_unresolved_condition')
    trace.append(dict(rule=key,lean=result['lean'],catalog_sha256=result['catalog_sha256'],
                      proof_status=result['proof_status']))
    return result['rhs']


def expand_terms(tree,*,library=None):
    """Bounded definition expansion, using literal lists only for phi weights."""
    lib=library or Library();trace=[];count=0
    def visit(t,depth=0):
        nonlocal count
        count+=1
        if depth>128 or count>20000:raise LibraryError('representation_budget')
        t=copy.deepcopy(t);op=t['op'];args=t.get('args',[])
        if op=='FiniteQBenchmark.phiTerm':
            if len(args)!=5:raise LibraryError('invalid_phiTerm_arity')
            literal_list(args[0]);literal_list(args[1])
            t=apply_definition(lib,'phiTerm_definition',dict(zip(('as','bs','q','z','k'),args)),trace)
            return visit(t,depth+1)
        if op=='FiniteQBenchmark.pochList':
            if len(args)!=3:raise LibraryError('invalid_pochList_arity')
            items=literal_list(args[0])
            key='pochList_cons' if items else 'pochList_nil'
            binding=dict(q=args[1],n=args[2])
            if items:binding.update(a=args[0]['args'][0],**{'as':args[0]['args'][1]})
            t=apply_definition(lib,key,binding,trace)
            return visit(t,depth+1)
        if 'args' in t:t['args']=[visit(v,depth+1) for v in args]
        if 'body' in t:t['body']=visit(t['body'],depth+1)
        return t
    return visit(tree),trace


def finite_sum_view(tree,*,avoid=(),library=None):
    lib=library or Library()
    matches=lib.lookup(tree['op'],'finite_sum')['rules']
    if not matches:return None
    if len(matches)!=1:raise LibraryError('ambiguous_finite_sum_view')
    rule=matches[0];params=[p['name'] for p in rule['parameters']]
    if len(tree.get('args',[]))!=len(params):raise LibraryError('invalid_source_object_arity')
    # These names are mathematical arguments, not theorem identifiers.
    bindings=dict(zip(params,tree['args']))
    trace=[]
    expression=apply_definition(lib,rule['id'],bindings,trace,set(avoid)|names(tree))
    expression,steps=expand_terms(expression,library=lib);trace+=steps
    domain,binder=expression['args']
    return dict(expression=expression,body=binder['body'],binder=binder['name'],domain=domain,
                definition=rule['lean']['name'],library_trace=trace,
                method_applicability='not_established',proof_status='requires_Lean_replay')
