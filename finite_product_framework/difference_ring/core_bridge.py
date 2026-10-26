"""Evaluated finite-prefix towers -> strong difference field -> original Lean.

This is a restricted source bridge, not a claim that every strong-core input
has a source representation. The core sees the summand only. Initial values,
specialization, the shift identity and both endpoints are replayed in Lean.
"""
import json
from pathlib import Path
import sys
import sympy as s


class BridgeGap(ValueError):pass


def modules():
    path=str(Path(__file__).resolve().parents[1]/'p1')
    if path not in sys.path:sys.path.insert(0,path)
    from core import compute,CoreBudget
    from qdifference import rational_read
    from source_ir import exact_tree
    from general_sum_emit import source_term
    from sum_lean import rational
    return compute,CoreBudget,rational_read,exact_tree,source_term,rational


def frontend(raw):
    _,_,_,tree,render,_=modules()
    eq=raw['target']
    if eq['op']!='Eq':raise BridgeGap('core bridge requires equality')
    left,right=eq['args'];reverse=left['op']!='Finset.sum'
    total,target=(right,left) if reverse else (left,right)
    if total['op']!='Finset.sum':raise BridgeGap('core bridge requires a whole-side prefix sum')
    domain,binder=total['args']
    if domain['op']!='Finset.range' or binder['op']!='lambda':
        raise BridgeGap('core bridge requires natural range sum')
    used=set();bound_names=set()
    def names(t):
        if 'name' in t:used.add(t['name'])
        if t['op']=='lambda':bound_names.add(t['name'])
        for a in t.get('args',[]):names(a)
        if 'body' in t:names(t['body'])
    names(eq)
    index='drCoreIndex'
    while index in used:index+='x'
    extensions=[];evaluations={};parameters={};keys={}
    def extend(kind,evaluation,value):
        key=(kind,evaluation)
        if key in keys:return s.Symbol(keys[key])
        name='Tower'+str(len(extensions));keys[key]=name
        extensions.append(dict(kind=kind,name=name,**{('increment' if kind=='sum' else 'ratio'):tree(value)}))
        evaluations[name]=evaluation
        return s.Symbol(name)
    def read(t,current):
        op=t['op'];args=t.get('args',[])
        if op=='nat':return s.Integer(t['value'])
        if op=='var':
            if t['name']==current:return extend('sum',f'(↑{index})',s.Integer(1))
            if t['name'] in bound_names:raise BridgeGap('tower increment depends on an outer bound index')
            if t['name'] not in parameters:parameters[t['name']]='Parameter'+str(len(parameters))
            return s.Symbol(parameters[t['name']])
        if op in ('Nat.cast','Int.ofNat') and len(args)==1:return read(args[0],current)
        if op in ('HAdd.hAdd','HSub.hSub','HMul.hMul','HDiv.hDiv') and len(args)==2:
            if op=='HSub.hSub' and t.get('type')=='ℕ':raise BridgeGap('truncated natural subtraction needs a support bridge')
            a,b=(read(x,current) for x in args)
            if op=='HAdd.hAdd':return a+b
            if op=='HSub.hSub':return a-b
            if op=='HMul.hMul':return a*b
            if b==0:raise BridgeGap('identically zero formal denominator')
            return a/b
        if op in ('Neg.neg','Inv.inv') and len(args)==1:
            a=read(args[0],current)
            if op=='Inv.inv' and a==0:raise BridgeGap('identically zero formal denominator')
            return -a if op=='Neg.neg' else 1/a
        if op=='HPow.hPow' and len(args)==2:
            base,power=args
            if power['op']=='nat':return read(base,current)**power['value']
            if power==dict(op='var',name=current):
                value=read(base,current)
                if value.free_symbols & {s.Symbol(e['name']) for e in extensions}:
                    raise BridgeGap('geometric base must be index-independent')
                return extend('product',render(t,{current:index}),value)
            raise BridgeGap('core bridge accepts literal powers or a geometric index power')
        if op in ('Finset.sum','Finset.prod') and len(args)==2:
            rng,lam=args
            if (rng['op']!='Finset.range' or rng['args'][0]!=dict(op='var',name=current) or
                    lam['op']!='lambda' or lam['name']==current):
                raise BridgeGap('nested tower requires unshadowed prefix at the current index')
            value=read(lam['body'],lam['name'])
            return extend('sum' if op=='Finset.sum' else 'product',render(t,{current:index}),value)
        if op=='FiniteQBenchmark.poch' and len(args)==3 and args[2]==dict(op='var',name=current):
            a,base,_=args
            av,bv=read(a,current),read(base,current)
            if (av.free_symbols|bv.free_symbols)&{s.Symbol(e['name']) for e in extensions}:
                raise BridgeGap('Pochhammer parameters must be index-independent')
            geometric=dict(op='HPow.hPow',args=[base,dict(op='var',name=current)])
            ratio=1-av*read(geometric,current)
            return extend('product',render(t,{current:index}),ratio)
        raise BridgeGap('unsupported core source node: '+op)
    f=read(binder['body'],binder['name'])
    mapping={v:k for k,v in parameters.items()};mapping.update(evaluations)
    return dict(request=dict(schema_version=1,solver='difference_field',
                            input=dict(extensions=extensions,rhs_basis=[tree(f)])),
                evaluation=mapping,index=index,reverse=reverse,
                summand=render(binder['body'],{binder['name']:index}),
                bound=render(domain['args'][0]),target=render(target),
                scalar_type=total.get('type','K'),
                semantics='prefix sums start at 0; products and geometric powers start at 1; original-field replay required')


def construct(model,budget):
    compute,CoreBudget,read,_,_,printer=modules()
    result=compute(model['request'],CoreBudget(seconds=budget['symbolic_seconds'],
        max_unknowns=budget['max_unknowns'],max_order=budget['max_order']))
    if result['status']!='constructed':raise BridgeGap('strong core: '+result['status'])
    row=result['result'];cs=list(map(read,row['original_coefficients']))
    if len(cs)!=1 or cs[0]==0:raise BridgeGap('no nonzero single-summand coefficient')
    g=s.cancel(read(row['original_certificate'])/cs[0])
    if not {str(v) for v in g.free_symbols}<=set(model['evaluation']):
        raise BridgeGap('core returned an unevaluated constant or coordinate')
    # Check the returned witness again in the exact input tower before emission.
    from core import rational_input
    shift={s.Symbol(e['name']):s.Symbol(e['name'])+rational_input(e['increment']) if e['kind']=='sum'
           else s.Symbol(e['name'])*rational_input(e['ratio']) for e in model['request']['input']['extensions']}
    if s.cancel(g.xreplace(shift)-g-rational_input(model['request']['input']['rhs_basis'][0]))!=0:
        raise BridgeGap('invalid strong-core original-tower witness')
    value=printer(g,model['evaluation']);i=model['index']
    finish='''      all_goals try simp only [neg_add_eq_sub]
      all_goals first
        | (simp_all [FiniteQDifference.poch_initial, Finset.sum_range_zero, Finset.prod_range_zero]; done)
        | (ring; done)
        | (simp only [div_eq_mul_inv, mul_inv_rev, inv_pow, one_mul] <;> ring <;> done)
        | (field_simp [sub_ne_zero, *] <;> ring)'''
    script=('  classical\n'+('  symm\n' if model['reverse'] else '')+f'''  let drCoreF : ℕ → {model['scalar_type']} := fun ({i} : ℕ) => {model['summand']}
  let drCoreG : ℕ → {model['scalar_type']} := fun ({i} : ℕ) => {value}
  have drCoreLocal : ∀ {i}, drCoreF {i} = drCoreG ({i}+1)-drCoreG {i} := by
    intro {i}
    dsimp only [drCoreF, drCoreG]
    simp only [FiniteQDifference.poch_shift, Finset.sum_range_succ, Finset.prod_range_succ,
      pow_succ, Nat.cast_add, Nat.cast_one, Nat.cast_succ]
    all_goals
'''+finish+f'''
  change (∑ {i} ∈ Finset.range {model['bound']}, drCoreF {i}) = {model['target']}
  calc
    _ = ∑ {i} ∈ Finset.range {model['bound']}, (drCoreG ({i}+1)-drCoreG {i}) :=
      Finset.sum_congr rfl (fun {i} _ => drCoreLocal {i})
    _ = drCoreG {model['bound']}-drCoreG 0 := FiniteQDifference.telescope drCoreG {model['bound']}
    _ = _ := by
      dsimp only [drCoreG]
      simp only [FiniteQDifference.poch_initial, Finset.sum_range_zero, Finset.prod_range_zero,
        pow_zero, Nat.cast_zero, zero_add, add_zero, mul_one, one_mul]
'''+finish+'\n  done')
    return dict(core=result,normalized_antidifference=str(g),model=model,proof_script=script,
                original_identity_proved=False)
