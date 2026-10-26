"""Untrusted finite-sum certificate printers; Lean checks all obligations."""
import sympy as s
from lean_pipeline import lean_expression

def term(node, names=None):
    names=names or {};op=node['op'];args=node.get('args',[])
    if op in ('Finset.sum','Finset.prod'):
        domain,binder=args
        operator='∑' if op=='Finset.sum' else '∏'
        return f"({operator} {binder['name']} ∈ {term(domain,names)}, {term(binder['body'],names)})"
    if op in ('Finset.range','Finset.Icc'):
        return '('+op+' '+' '.join(term(a,names) for a in args)+')'
    if op in ('Nat.cast','Int.ofNat'):
        return '(↑'+term(args[0],names)+')'
    if op=='var':return names.get(node['name'],node['name'])
    if op=='nat':return str(node['value'])
    if op=='List.nil':return '[]'
    if op=='List.cons':return '('+term(args[0],names)+' :: '+term(args[1],names)+')'
    if op=='FiniteQBenchmark.pochList':return '('+op+' '+' '.join(term(a,names) for a in args)+')'
    if op=='Neg.neg':return '(-'+term(args[0],names)+')'
    if op=='Inv.inv':return '('+term(args[0],names)+')⁻¹'
    ops={'HAdd.hAdd':'+','HSub.hSub':'-','HMul.hMul':'*','HDiv.hDiv':'/','HPow.hPow':'^','Eq':'='}
    if op in ops:return '('+term(args[0],names)+' '+ops[op]+' '+term(args[1],names)+')'
    return lean_expression(node,names)


def rational(value,mapping):
    value=s.sympify(value)
    if value.is_Integer:return '('+str(value)+')'
    if value.is_Rational:return f'({value.p} / {value.q})'
    if value.is_Symbol:return '('+mapping[str(value)]+')'
    if value.is_Add or value.is_Mul:
        return '('+(' + ' if value.is_Add else ' * ').join(rational(v,mapping) for v in value.args)+')'
    if value.is_Pow and value.exp.is_Integer:
        b=rational(value.base,mapping);e=int(value.exp)
        return f'({b} ^ {e})' if e>=0 else f'(({b} ^ {-e})⁻¹)'
    raise ValueError('proof_representation_gap: nonrational certificate '+str(value))


ALGEBRA='''    all_goals try simp only [pow_add, pow_succ, pow_zero, pow_one, Nat.cast_add,
      Nat.cast_one, Nat.cast_zero, mul_one, one_mul, add_zero, zero_add, neg_add_eq_sub,
      Finset.sum_range_succ, Finset.sum_range_zero, Finset.prod_range_succ,
      Finset.prod_range_zero, poch_succ]
    all_goals try simp only [← pow_mul, Nat.mul_comm]
    all_goals solve | ring | (field_simp [sub_ne_zero, *] <;> ring) | (simp_all <;> ring)'''


def antidifference(raw,binding,ratio,direct_g=None):
    """Use the computed G=R F; verify local relation on actual source terms."""
    if raw['op']!='Eq':raise ValueError('proof_representation_gap: equality required')
    left,right=raw['args'];reverse=left['op']!='Finset.sum'
    summation,target=(right,left) if reverse else (left,right)
    if summation['op']!='Finset.sum':raise ValueError('proof_representation_gap: whole-side sum required')
    domain,binder=summation['args']
    if domain['op']!='Finset.range':raise ValueError('proof_representation_gap: range endpoint exit required')
    names=binding['variable_mapping'];canonical={v:k for k,v in names.items()}
    if binder['name'] not in names:raise ValueError('binder not bound')
    used=set(names);j='exitIndex'
    while j in used:j+='x'
    mapping=dict(canonical,X=f"{canonical['q']}^{j}")
    if 'n' in canonical:mapping['Q']=f"{canonical['q']}^{canonical['n']}"
    f=term(binder['body'],{binder['name']:j});g=direct_g or f'({rational(ratio,mapping)}) * ({f})'
    upper=term(domain['args'][0]);target=term(target)
    script=('  symm\n' if reverse else '')+f'''  let exitF := fun ({j} : ℕ) => {f}
  let exitG := fun ({j} : ℕ) => {g}
  change (∑ {j} ∈ Finset.range {upper}, exitF {j}) = {target}
  have exitLocal : ∀ {j}, exitF {j} = exitG ({j}+1)-exitG {j} := by
    intro {j}
    dsimp only [exitF, exitG]
{ALGEBRA}
  calc
    _ = ∑ {j} ∈ Finset.range {upper}, (exitG ({j}+1)-exitG {j}) :=
      Finset.sum_congr rfl (fun {j} _ => exitLocal {j})
    _ = exitG {upper}-exitG 0 := FiniteQP1.telescope exitG {upper}
    _ = _ := by
      dsimp only [exitG]
'''+''.join('  '+line+'\n' for line in ALGEBRA.splitlines())
    return script,dict(kind='source_antidifference',ratio=str(ratio),boundary='both actual range endpoints verified in Lean')
