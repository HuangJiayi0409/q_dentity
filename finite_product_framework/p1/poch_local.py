"""Generate kernel-checked, division-free product-interval normalization steps."""
import sympy as s
from expressions import n,k,q,Q,X,Poch
from poch_intervals import plan
from sum_lean import rational


def nat(value,mapping):
    p=s.Poly(s.expand(value),n,k);pos=[];neg=[]
    for powers,c in p.terms():
        if not c.is_Integer:raise ValueError('proof_representation_gap: integral length polynomial required')
        if not c:continue
        fs=[str(abs(c))] if abs(c)!=1 or not any(powers) else []
        fs += [mapping[str(v)] if e==1 else f'({mapping[str(v)]}^{e})' for v,e in zip((n,k),powers) if e]
        (pos if c>0 else neg).append('*'.join(fs))
    plus='('+' + '.join(pos or ['0'])+')'
    return plus if not neg else '('+plus+' - ('+' + '.join(neg)+'))'


def field(value,mapping):
    value=s.sympify(value)
    if value.func==Poch:
        a,b,l=value.args
        return f'(poch {field(a,mapping)} {field(b,mapping)} {nat(l,mapping)})'
    if value.is_Add or value.is_Mul:
        return '('+(' + ' if value.is_Add else ' * ').join(field(t,mapping) for t in value.args)+')'
    if value.is_Pow and value.exp.has(n,k):
        poly=s.Poly(s.expand(value.exp),n,k)
        pos=sum(c*n**i*k**j for (i,j),c in poly.terms() if c>0)
        neg=-sum(c*n**i*k**j for (i,j),c in poly.terms() if c<0)
        b=field(value.base,mapping);top=f'({b}^{nat(pos,mapping)})'
        return top if neg==0 else f'({top}/({b}^{nat(neg,mapping)}))'
    if value.is_Pow and value.exp.is_Integer:
        b=field(value.base,mapping);e=int(value.exp)
        return f'({b}^{e})' if e>=0 else f'(({b}^{-e})⁻¹)'
    return rational(value,mapping)


NORMAL='''Nat.add_zero, Nat.zero_add, Nat.mul_zero, Nat.zero_mul, Nat.one_mul, Nat.mul_one,
  Nat.sub_zero, Nat.zero_sub, Nat.sub_self,
  zero_mul, mul_zero, zero_add, add_zero,
  pow_zero, pow_one, zpow_neg, zpow_natCast, Nat.cast_add, Nat.cast_one,
  pow_add, pow_succ, mul_pow, mul_inv_rev, inv_inv, div_eq_mul_inv'''.replace('\n',' ')


def normalize(expressions,mapping,indent=4,*,rewrite_facts=True):
    """Return proof steps, preserving all length and parameter obligations."""
    data=plan(expressions);lines=[];names=[]
    shorts=set().union(*(v.atoms(Poch) for v in expressions))
    shorts={v for v in shorts if not v.args[2].has(n,k)}
    for i,row in enumerate(data['rows']):
        atom=row['atom'];core=row['core'];a,base,l=atom.args;ca,_,cl=core.args
        d,e=row['prefix'],row['suffix']
        if (d==0 and e==0) or not l.has(n,k):
            continue
        rhs=Poch(a,base,s.Integer(d))*core*Poch(ca*base**cl,base,s.Integer(e))
        shorts.update(v for v in rhs.atoms(Poch) if not v.args[2].has(n,k))
        # Constant Pochhammers are expanded only by Lean, not treated as trusted.
        name='pcNorm'+str(i);names.append(name)
        lines += [f'have {name} := FiniteQShift.interval {field(a,mapping)} {field(ca,mapping)} {field(base,mapping)} {nat(l,mapping)} {d} {nat(cl,mapping)} {e}',
          '  (by omega) (by',
          f'    try simp only [{NORMAL}]',
          '    all_goals first | (ring; done) | (field_simp [*] <;> ring))']
    # Normalize known short products at their actual arguments first. This
    # avoids inserting unnormalized rational parameters into a large target.
    for i,atom in enumerate(sorted(shorts,key=s.default_sort_key)):
        a,base,l=atom.args
        if not l.is_Integer or l<0:
            raise ValueError('proof_representation_gap: negative concrete product length')
        rhs=s.prod(1-a*base**j for j in range(int(l)))
        name='pcAtom'+str(i);names.append(name)
        lines += [f'have {name} : {field(atom,mapping)} = {field(rhs,mapping)} := by',
                  '  norm_num [poch, Finset.prod_range_succ, pow_add, pow_succ]',
                  '  all_goals first | (ring; done) | (field_simp [*] <;> ring)']
    primary_names=list(names)
    universal_names=[]
    lengths=sorted({(atom.args[1],atom.args[2]) for atom in shorts},key=s.default_sort_key)
    for i,(base,l) in enumerate(lengths):
        if not l.is_Integer or l<0:
            raise ValueError('proof_representation_gap: negative concrete product length')
        # One polynomial identity per length works for every parameter,
        # including shifted arguments introduced by an interval rewrite.
        # It also preserves composite denominator nonzero evidence as a
        # single polynomial instead of factoring away its known product.
        parameter=s.Symbol('pcParameter')
        rhs=s.expand(s.prod(1-parameter*base**j for j in range(int(l))))
        local_mapping=dict(mapping,pcParameter='pcParameter')
        name='pcShort'+str(i);names.append(name);universal_names.append(name)
        lines += [f'have {name} (pcParameter : _) : poch pcParameter {field(base,mapping)} {int(l)} = {field(rhs,local_mapping)} := by',
                  '  norm_num [poch, Finset.prod_range_succ, pow_add, pow_succ]',
                  '  all_goals ring']
    if names:
        lines += ['try simp (disch := first | assumption | omega) only [pow_sub₀] at '+' '.join(names)+' ⊢',
                  f'try simp only [{NORMAL}] at '+ ' '.join(names)+' ⊢',
                  'ring_nf (ifUnchanged := .silent) at '+' '.join(names)+' ⊢',
                  'try simp only ['+', '.join(primary_names)+']',
                  'try simp only ['+', '.join(universal_names)+']']
        if rewrite_facts:
            lines += ['all_goals poch_rewrite_facts ['+', '.join(names)+']']
    return '\n'.join(' '*indent+l for l in lines)+'\n'
