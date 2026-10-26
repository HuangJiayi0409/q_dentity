"""Prove linear recurrence statements from a defined finite-sum sequence.

The target is used only after q-Zeilberger independently constructs a recurrence
for the exported definition. Native reconstruction closes local and boundary
obligations; reindexing guards Nat subtraction through an explicit Lean proof.
"""
import sympy as s
from expressions import n,k,q,Q,rationalize
from lean_pipeline import find_nodes,extract,lean_expression,polynomial_lean
from zeilberger_pipeline import frontend as zfrontend,emit_proof as zemit
from ore_pipeline import symbolic,H


def prepare(raw,identity,work,env):
    if raw['op']!='Eq' or find_nodes(raw,'Finset.sum'):
        raise ValueError('defined_relation: a sequence equality without an explicit outer sum is required')
    atoms=find_nodes(raw,'FiniteQBenchmark.rogersSzego')
    if not atoms:raise ValueError('defined_relation: no supported defined sequence')
    if len(atoms)==1 and any(side==atoms[0] for side in raw['args']):
        from parameter_relation import prepare_closed
        return prepare_closed(raw,identity,work,env)
    params=atoms[0]['args'][:2]
    if any(a['op']!='var' for a in params) or any(a['args'][:2]!=params for a in atoms):
        from parameter_relation import prepare_shift
        return prepare_shift(raw,identity,work,env)
    x,base=[a['name'] for a in params]
    indices={v['name'] for a in atoms for v in find_nodes(a['args'][-1],'var')}-{x,base}
    if len(indices)!=1:raise ValueError('defined_relation: one sequence index required')
    index=next(iter(indices))
    source=f'''import Benchmark.P1Atoms
open FiniteQBenchmark
open scoped BigOperators
variable {{K : Type*}} [Field K]
theorem definition_input ({x} {base} : K) ({index} : ℕ) : rogersSzego {x} {base} {index} = 0 := by
  sorry
'''
    dw=work/'object_definition';dw.mkdir(exist_ok=True)
    # This auxiliary extraction is not the original target and carries no proof.
    from workflow.preprocessed import ACTIVE
    token=ACTIVE.set(None)
    try:definition=extract(source,dw,env,prelude='  unfold rogersSzego')
    finally:ACTIVE.reset(token)
    formula,dm=zfrontend(definition,identity+'-definition')
    names=dm['names']
    left,right=raw['args'];relation=symbolic(left,names)-symbolic(right,names)
    shifts=[s.expand(a.args[0]-n) for a in relation.atoms(H)]
    if not shifts or any(not a.is_Integer for a in shifts):
        raise ValueError('defined_relation: fixed integer shifts required')
    offset=max(0,-int(min(shifts)))
    return dict(formula,mode='defined_linear_relation'),dict(mode='defined_linear_relation',
        names=names,index=index,base=base,parameter=x,definition_model=dm,
        relation_raw=raw,offset=offset)


def construct(problem,budget):
    if problem.get("mode")=="defined_parameter_relation":
        from parameter_relation import construct_shift
        return construct_shift(problem,budget)
    from zeilberger import construct as zconstruct
    formula={key:value for key,value in problem.items() if key!='mode'}
    result=zconstruct(formula,budget)
    if result['construction']['status']=='constructed':
        result['construction']['defined_relation_target_used_in_search']=False
    return result


def emit(model,construction):
    if model.get("mode")=="defined_parameter_relation":
        from parameter_relation import emit_shift
        return emit_shift(model,construction)
    if model.get('mode')=='defined_closed_form':
        from parameter_relation import emit_closed
        return emit_closed(model,construction)
    if construction['order']!=2:
        raise ValueError('defined_relation: current recurrence-only reconstruction requires order two')
    names=model['names'];raw=model['relation_raw'];offset=model['offset']
    relation=symbolic(raw['args'][0],names)-symbolic(raw['args'][1],names)
    shifted=s.expand(relation.subs(n,n+offset))
    atoms=[H(n+j) for j in range(3)]
    if shifted.atoms(H)-set(atoms):raise ValueError('defined_relation: relation outside constructed recurrence window')
    coefficients=[rationalize(s.expand(shifted).coeff(a)) for a in atoms]
    residual=s.expand(shifted-sum(s.expand(shifted).coeff(a)*a for a in atoms))
    if residual!=0 or any(c.has(H,n,k) for c in coefficients):
        raise ValueError('defined_relation: homogeneous linear recurrence required')
    symbols={str(t):t for t in set().union(*(c.free_symbols for c in coefficients)) | {q,Q}}
    computed=[s.sympify(c,locals=symbols) for c in construction['coefficients']]
    if len(computed)!=3 or computed[-1]!=1:raise ValueError('defined_relation: monic order two required')
    factor=coefficients[-1]
    if factor==0 or any(s.cancel(a-factor*b)!=0 for a,b in zip(coefficients,computed)):
        raise ValueError('defined_relation: target is not a multiple of the independently constructed recurrence')
    index,base,x=model['index'],model['base'],model['parameter']
    used=set(names);anchor='fqiAnchor'
    while anchor in used:anchor+='_' 
    mapping={value:key for key,value in names.items()};mapping['Q']=f'({base}^{index})'
    c0,c1=[polynomial_lean(c,mapping) for c in computed[:2]]
    seq=f'rogersSzego {x} {base}'
    body,plan=zemit(model['definition_model'],construction,recurrence_only=True)
    proof=f'''  have fqiComputed : ∀ {index} : ℕ,
      {seq} ({index}+2) + ({c0} * {seq} {index} + {c1} * {seq} ({index}+1)) = 0 := by
    intro {index}
    unfold rogersSzego
'''+''.join('  '+line+'\n' for line in body.splitlines())
    proof+=f'''  obtain ⟨{anchor}, fqiIndex⟩ : ∃ j : ℕ, {index} = j + {offset} := ⟨{index}-{offset}, by omega⟩
  subst {index}
  have fqiRec := fqiComputed {anchor}
  simp only [Nat.add_sub_cancel, Nat.add_zero, Nat.add_assoc] at *
'''
    mm=dict(mapping,Q=f'({base}^{anchor})')
    proof+=f'  linear_combination ({polynomial_lean(factor,mm)}) * fqiRec\n'
    return proof,dict(algorithm='definition -> computed q-Zeilberger recurrence -> scalar relation',
                      recurrence=plan,offset=offset,relation_multiplier=str(factor),
                      target_used_in_search=False,source_index_obligations='Lean omega, no new assumptions')
