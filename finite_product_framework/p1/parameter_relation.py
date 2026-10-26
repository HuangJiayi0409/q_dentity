"""Parameter specialization of a computed recurrence, with Lean uniqueness.

The universal recurrence is constructed from the actual definition, independently
of a closed-form target. Specialization is performed only after native certificate
reconstruction, so no formal rational denominator is silently specialized.
"""
import sympy as s
from expressions import q,Q
from lean_pipeline import find_nodes,extract,lean_expression,polynomial_lean
from zeilberger_pipeline import frontend as zfrontend,emit_proof as zemit


def generic_definition(raw,identity,work,env):
    used={v['name'] for v in find_nodes(raw,'var')}
    def fresh(stem):
        while stem in used:stem+='_' 
        used.add(stem);return stem
    x,b,i=[fresh(v) for v in ('fqiWeight','fqiBase','fqiN')]
    source=f'''import Benchmark.P1Atoms
open FiniteQBenchmark
open scoped BigOperators
variable {{K : Type*}} [Field K]
theorem definition_input ({x} {b} : K) ({i} : ℕ) : rogersSzego {x} {b} {i} = 0 := by
  sorry
'''
    dw=work/'object_definition';dw.mkdir(exist_ok=True)
    from workflow.preprocessed import ACTIVE
    token=ACTIVE.set(None)
    try:definition=extract(source,dw,env,prelude='  unfold rogersSzego')
    finally:ACTIVE.reset(token)
    formula,dm=zfrontend(definition,identity+'-definition')
    return formula,dm


def prepare_closed(raw,identity,work,env):
    atom=find_nodes(raw,'FiniteQBenchmark.rogersSzego')[0]
    reverse=raw['args'][1]==atom
    target=raw['args'][0 if reverse else 1]
    index=atom['args'][-1]
    if index['op']!='var':raise ValueError('defined_closed_form: unshifted natural index required')
    i=index['name']
    if any(v['name']==i for p in atom['args'][:2] for v in find_nodes(p,'var')):
        raise ValueError('defined_closed_form: parameters must be independent of sequence index')
    # Keep the native exit deliberately small. Lean checks the recurrence and
    # both initial values of the actual target, including its parameter relation.
    if target['op']!='FiniteQBenchmark.poch' or target['args'][-1]!=index:
        raise ValueError('defined_closed_form: currently a single Pochhammer target is required')
    for p in atom['args'][:2]+target['args'][:2]:
        lean_expression(p)
        if any(v['name']==i for v in find_nodes(p,'var')):
            raise ValueError('defined_closed_form: index-dependent parameters unsupported')
    formula,dm=generic_definition(raw,identity,work,env)
    return dict(formula,mode='defined_closed_form'),dict(mode='defined_closed_form',
        definition_model=dm,sequence=atom,target=target,index=i,reverse=reverse)


def universal_proof(dm,construction):
    if construction['order']!=2:raise ValueError('parameter_relation: order two required')
    symbols={v:s.Symbol(v) for v in dm['names'].values()};symbols.update(q=q,Q=Q)
    cs=[s.sympify(c,locals=symbols) for c in construction['coefficients']]
    if len(cs)!=3 or cs[-1]!=1:raise ValueError('parameter_relation: monic recurrence required')
    i,b=dm['index'],dm['base']
    x=next(v for v in dm['names'] if dm['names'][v] not in ('n','k','q'))
    mapping={c:o for o,c in dm['names'].items()};mapping['Q']=f'({b}^{i})'
    c0,c1=[polynomial_lean(c,mapping) for c in cs[:2]]
    body,plan=zemit(dm,construction,recurrence_only=True)
    proof=f'''  have fqiGeneric : ∀ ({x} {b} : K) ({i} : ℕ),
      rogersSzego {x} {b} ({i}+2) +
        ({c0} * rogersSzego {x} {b} {i} + {c1} * rogersSzego {x} {b} ({i}+1)) = 0 := by
    intro {x} {b} {i}
    unfold rogersSzego
'''+''.join('  '+line+'\n' for line in body.splitlines())
    return proof,plan


def emit_closed(model,construction):
    proof,plan=universal_proof(model['definition_model'],construction)
    atom=model['sequence'];index=model['index']
    x,b=[lean_expression(a) for a in atom['args'][:2]]
    used={v['name'] for node in [atom,model['target']] for v in find_nodes(node,'var')}
    j='fqiStep'
    while j in used:j+='_' 
    target=lean_expression(model['target'],{index:j})
    proof+=f'''  have fqiAll : ∀ {j} : ℕ, rogersSzego {x} {b} {j} = {target} := by
    intro {j}
    induction {j} using Nat.strong_induction_on with
    | h {j} ih =>
      rcases {j} with _ | {j}
      · norm_num [rogersSzego, gaussian, poch, Finset.sum_range_succ]
      rcases {j} with _ | {j}
      · norm_num [rogersSzego, gaussian, poch, Finset.sum_range_succ] <;> ring
      have hr := fqiGeneric {x} {b} {j}
      rw [ih {j} (by omega), ih ({j}+1) (by omega)] at hr
      change rogersSzego {x} {b} ({j}+2) = _
      simp only [poch_succ, pow_succ, mul_pow] at hr ⊢
      linear_combination hr
'''
    proof+=f'  '+('symm\n  ' if model['reverse'] else '')+f'exact fqiAll {index}\n'
    return proof,dict(algorithm='definition -> universal computed recurrence -> parameter substitution -> uniqueness',
        recurrence=plan,target_used_in_search=False,initial_values=2,
        parameter_substitution=[x,b],obligations='Lean initial values and specialized target recurrence')


def prepare_shift(raw,identity,work,env):
    from ore_pipeline import symbolic
    from expressions import n
    atoms=find_nodes(raw,'FiniteQBenchmark.rogersSzego')
    bases=[a['args'][1] for a in atoms]
    if any(b!=bases[0] for b in bases) or bases[0]['op']!='var':
        raise ValueError('parameter_relation: a common variable base is required')
    base=bases[0]['name']
    iv={v['name'] for a in atoms for v in find_nodes(a['args'][-1],'var')}
    if len(iv)!=1:raise ValueError('parameter_relation: one sequence index required')
    index=next(iter(iv))
    variables=sorted({v['name'] for v in find_nodes(raw,'var')}-{index,base})
    names={index:'n',base:'q',**{v:f'p{i}' for i,v in enumerate(variables)}}
    params=[]
    for a in atoms:
        p=a['args'][0]
        if any(v['name']==index for v in find_nodes(p,'var')):
            raise ValueError('parameter_relation: index-dependent parameters unsupported')
        if p not in params:params.append(p)
    if not 1<len(params)<=4:raise ValueError('parameter_relation: two to four parameter instances required')
    functions=[s.Function(f'H{i}') for i in range(len(params))]
    def translate(node):
        if node['op']=='FiniteQBenchmark.rogersSzego':
            return functions[params.index(node['args'][0])](symbolic(node['args'][-1],names))
        if not find_nodes(node,'FiniteQBenchmark.rogersSzego'):return symbolic(node,names)
        a=[translate(v) for v in node['args']]
        if node['op']=='Eq':return a[0]-a[1]
        if node['op']=='HAdd.hAdd':return a[0]+a[1]
        if node['op']=='HSub.hSub':return a[0]-a[1]
        if node['op']=='HMul.hMul':return a[0]*a[1]
        raise ValueError('parameter_relation: polynomial linear sequence relation required')
    relation=s.expand(translate(raw))
    seqs=set().union(*(relation.atoms(f) for f in functions))
    shifts=[s.expand(a.args[0]-n) for a in seqs]
    if any(not a.is_Integer for a in shifts):raise ValueError('parameter_relation: fixed shifts required')
    offset=max(0,-int(min(shifts)))
    relation=s.expand(relation.subs(n,n+offset))
    if any(a.args[0] not in (n,n+1) for f in functions for a in relation.atoms(f)):
        raise ValueError('parameter_relation: initial window must fit an order-two state')
    formula,dm=generic_definition(raw,identity,work,env)
    data=dict(names=names,index=index,base=base,parameters=params,offset=offset,
              relation=str(relation),parameter_values=[str(symbolic(p,names)) for p in params])
    return dict(formula,mode='defined_parameter_relation',relation_data=data),dict(
        mode='defined_parameter_relation',definition_model=dm,**data)


def shift_algebra(data,base_certificate):
    from expressions import n,rationalize
    from ore import companion,eliminate
    functions=[s.Function(f'H{i}') for i in range(len(data['parameters']))]
    symbols={v:s.Symbol(v) for v in data['names'].values()};symbols.update(n=n,q=q,Q=Q)
    symbols.update({f.__name__:f for f in functions})
    relation=s.sympify(data['relation'],locals=symbols)
    params=[s.sympify(p,locals=symbols) for p in data['parameter_values']]
    # The definition exporter assigns its sole geometric parameter p3.
    cs=[s.sympify(c,locals={'q':q,'Q':Q}) for c in base_certificate['coefficients']]
    other=set().union(*(c.free_symbols for c in cs))-{q,Q}
    if len(other)!=1 or len(cs)!=3 or cs[-1]!=1:
        raise ValueError('parameter_relation: one-parameter monic order-two definition required')
    parameter=next(iter(other))
    specs=[[s.expand(c.subs(parameter,p)) for c in cs] for p in params]
    atoms=[f(n+j) for f in functions for j in range(2)]
    row=s.Matrix([[rationalize(relation.coeff(a)) for a in atoms]])
    if s.expand(relation-sum(relation.coeff(a)*a for a in atoms))!=0 or any(v.has(*functions) for v in row):
        raise ValueError('parameter_relation: homogeneous linear relation required')
    matrix=s.diag(*(companion(c) for c in specs))
    operator=eliminate(matrix,row)
    coeff=[s.sympify(c,locals=symbols) for c in operator['coefficients']]
    order=len(coeff)-1
    if not 1<=order<=4:raise ValueError('parameter_relation: native closure order must be one to four')
    # Reconstruct an exact linear combination of shifted base recurrences.
    residual=s.expand(sum(c*relation.subs(n,n+j) for j,c in enumerate(coeff)))
    ratoms=set().union(*(residual.atoms(f) for f in functions))
    residual=s.expand(sum(rationalize(residual.coeff(a))*a for a in ratoms))
    witnesses=[]
    for fi,f in enumerate(functions):
        for j in reversed(range(order)):
            multiplier=s.expand(residual).coeff(f(n+j+2))
            rec=sum(c.subs(Q,Q*q**j)*f(n+j+l) for l,c in enumerate(specs[fi]))
            residual=s.expand(residual-multiplier*rec)
            if multiplier!=0:witnesses.append((fi,j,s.cancel(multiplier)))
    if s.cancel(residual)!=0:raise ValueError('parameter_relation: closure witness did not cancel')
    mapping={str(v):str(v) for v in symbols.values() if isinstance(v,s.Symbol)}
    for c in coeff+[w[2] for w in witnesses]:polynomial_lean(c,mapping)
    return relation,functions,params,coeff,witnesses,operator


def construct_shift(problem,budget):
    from zeilberger import construct as zconstruct
    result=zconstruct({k:v for k,v in problem.items() if k not in ('mode','relation_data')},budget)
    base=result['construction']
    if base['status']!='constructed':return result
    _,_,_,_,w,op=shift_algebra(problem['relation_data'],base)
    return dict(construction=dict(status='constructed',algorithm='parameter-instance Ore closure',
        base_recurrence=base,operator=op,witnesses=[[i,j,str(c)] for i,j,c in w],
        definition_target_used_in_search=False,observable_used_for_closure=True),definition_search=result)


def emit_shift(model,construction):
    from expressions import n
    from ore_pipeline import field_text,nat_text
    base=construction['base_recurrence']
    relation,functions,params,cs,witnesses,op=shift_algebra(model,base)
    if construction['operator']!=op or construction['witnesses']!=[[i,j,str(c)] for i,j,c in witnesses]:
        raise ValueError('parameter_relation: altered closure certificate')
    proof,plan=universal_proof(model['definition_model'],base)
    used=set(model['names']);j='fqiStep'
    while j in used:j+='_' 
    mapping={v:k for k,v in model['names'].items()};mapping.update(n=j,Q=f"({model['base']}^{j})")
    parameter_text=[lean_expression(p) for p in model['parameters']]
    seq=[f'rogersSzego {p} {model["base"]}' for p in parameter_text]
    def render(e):
        replace={}
        for fi,f in enumerate(functions):
            for a in e.atoms(f):
                key=s.Symbol(f'fqiAtom{len(replace)}');replace[a]=key
                mapping[str(key)]=f'({seq[fi]} {nat_text(a.args[0],mapping)})'
        return field_text(e.xreplace(replace),mapping,'UNUSED')
    expr=render(relation);order=len(cs)-1
    proof+=f'''  have fqiAll : ∀ {j} : ℕ, {expr} = 0 := by
    intro {j}
    induction {j} using Nat.strong_induction_on with
    | h {j} ih =>
'''
    for _ in range(order):
        proof+=f'''      rcases {j} with _ | {j}
      · norm_num [rogersSzego, gaussian, poch, Finset.sum_range_succ] <;> ring
'''
    terms=[]
    for i,c in enumerate(cs[:-1]):
        proof+=f'      have fqiIH{i} := ih ({j}+{i}) (by omega)\n'
        terms.append(f'({polynomial_lean(-c,mapping)}) * fqiIH{i}')
    for z,(fi,shift,c) in enumerate(witnesses):
        proof+=f'      have fqiRec{z} := fqiGeneric {parameter_text[fi]} {model["base"]} ({j}+{shift})\n'
        terms.append(f'({polynomial_lean(c,mapping)}) * fqiRec{z}')
    hypotheses=' '.join([f'fqiIH{i}' for i in range(order)]+[f'fqiRec{i}' for i in range(len(witnesses))])
    proof+=f'''      simp only [Nat.add_assoc, Nat.add_zero, pow_add, pow_succ, pow_zero, mul_one] at {hypotheses} ⊢
      linear_combination {' + '.join(terms)}
'''
    index=model['index'];offset=model['offset']
    proof+=f'''  obtain ⟨fqiAnchor, fqiIndex⟩ : ∃ j : ℕ, {index} = j + {offset} := ⟨{index}-{offset}, by omega⟩
  subst {index}
  have fqiResult := fqiAll fqiAnchor
  simp only [Nat.add_sub_cancel, Nat.add_zero, Nat.add_assoc, pow_add, pow_succ, pow_zero, mul_one] at fqiResult ⊢
  linear_combination fqiResult
'''
    return proof,dict(algorithm='definition -> parameter instances -> Ore closure -> initial values and uniqueness',
        recurrence=plan,closure=op,witnesses=construction['witnesses'],offset=offset,
        definition_target_used_in_search=False,observable_used_for_closure=True)
