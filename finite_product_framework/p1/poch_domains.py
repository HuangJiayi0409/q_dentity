"""Construct bounded nonzero obligations from actual original product hypotheses."""
import sympy as s
from expressions import n,k,q,Q,X,Poch,expression,rationalize
from source_ir import nodes,list_items,Converter
from poch_intervals import plan,compact
from poch_local import field,nat,NORMAL


def sources(model):
    from poch_recurrence_emit import typed_source
    from general_sum_emit import source_term
    conv=Converter.__new__(Converter);conv.names=model['names'];conv.obligations=set()
    base=next(a for a,b in model['names'].items() if b=='q');N=model['index'];rows=[]
    for _,node in nodes(model['raw']):
        if node['op']=='FiniteQBenchmark.phi':
            bs=node['args'][1];params=[dict(op='var',name=base),*list_items(bs)]
            product_base=q;product_base_lean=base
            premise=f'(show phiDefined {source_term(typed_source(bs))} {base} {N} from by assumption) {N} (by omega)'
        elif node['op'] in ('FiniteQBenchmark.pochList','FiniteQBenchmark.poch') and node['args'][2]==dict(op='var',name=N):
            params=(list_items(node['args'][0]) if node['op'].endswith('pochList') else [node['args'][0]])
            premise=f'(show {source_term(typed_source(node))} ≠ 0 from by first | assumption | tauto)'
            product_base=expression(conv.read(node['args'][1]))
            product_base_lean=source_term(typed_source(node['args'][1]))
        else:continue
        for p in params:
            A=expression(conv.read(p));ap=source_term(typed_source(p))
            rows.append(dict(expression=A,lean=ap,premise=premise,
                             base=product_base,base_lean=product_base_lean))
    return rows


def transport(row,cur,length,mapping,N,name,full):
    """Nonpositive geometric parameter motion; all inequalities are Lean goals."""
    A=row['expression'];ar=s.factor(rationalize(A));cr=s.factor(rationalize(cur))
    product_base=row.get('base',q)
    stride=product_base.as_powers_dict().get(q,s.S.Zero)
    if not stride.is_Integer or stride<=0 or product_base!=q**stride:return []
    power=ar.as_powers_dict().get(Q,s.S.Zero)
    if not power.is_Integer or power>0:return []
    unit=s.cancel(ar/Q**power)
    if unit.has(Q,X):return []
    ratio=s.factor(cr/ar);offset=ratio.as_powers_dict().get(q,s.S.Zero)
    if not offset.is_Integer or s.cancel(ratio/q**offset)!=1:return []
    if power % stride or offset % stride:return []
    offset=int(offset/stride);t=-int(power/stride);base=row.get('base_lean',mapping['q']);ap=row['lean']
    if t==0:
        if offset<0:return []
        d=str(offset);prefix=[]
    else:
        reserve=max(0,(-offset+t-1)//t)
        rest=t*reserve+offset
        d=f'({t}*({N}-(gsN+{reserve}))+{rest})'
        prefix=[f'    have pdIndex : {N} = gsN+{reserve}+({N}-(gsN+{reserve})) := by omega',
                '    conv_lhs => lhs; rw [pdIndex]']
    zpow=(f'zpow_sub₀ (by assumption : {mapping["q"]} ≠ 0), zpow_add₀ (by assumption : {mapping["q"]} ≠ 0), ' if t else '')
    return ['try',f'  have {name} : {field(Poch(cur,product_base,length),mapping)} ≠ 0 := by',
      f'    have pdArg : {ap}*({base})^{d} = {field(cur,mapping)} := by',
      *['  '+l for l in prefix],
      f'      try simp only [Nat.cast_add, Nat.cast_one, Nat.cast_ofNat, {zpow}{NORMAL}, Nat.mul_add, Nat.add_mul]',
      '      all_goals first | (ring; done) | (field_simp [*] <;> ring)',
      f'    simpa only [pdArg] using (FiniteQShift.shifted_ne {ap} ({base}) {d} {nat(length,mapping)} {N} (by omega) {full})']


def emit(expressions,model,mapping,indent):
    src=sources(model)
    if not src:return ''
    N=model['index'];base=mapping['q'];data=plan(expressions)
    atoms=set(data['cores'].values())|set().union(*(v.atoms(Poch) for v in expressions))
    required=[]
    for v in [*expressions,*data['normalized']]:
        den=s.denom(compact(v,s.factor))
        for f in s.Mul.make_args(den):
            if f.is_Pow:f=f.base
            if f.has(Poch) or any(str(x).startswith('pc') for x in f.free_symbols):continue
            if f.is_Add and f not in required:required.append(f)
    lines=[];number=0
    for si,row in enumerate(src):
        group_start=len(lines)
        full=f'ptFull{si}';ap=row['lean'];A=row['expression']
        product_base=row['base'];pb=row['base_lean']
        lines+=['try',f'  have {full} : poch {ap} ({pb}) {N} ≠ 0 := by',
                f'    have hd := {row["premise"]}',
                '    try simp only [pochList_cons, pochList_nil, mul_one, mul_ne_zero_iff] at hd',
                '    tauto']
        for atom in sorted(atoms,key=s.default_sort_key):
            if atom.args[1]!=product_base:continue
            number+=1;lines+=transport(row,atom.args[0],atom.args[2],mapping,N,f'ptAtom{number}',full)
        for f in required:
            # Read the shift from the actual binomial factor, rather than
            # limiting the proof language to an arbitrary window of shifts.
            terms=s.Add.make_args(s.expand(rationalize(f)))
            # A requested linear factor can divide a quadratic-base factor
            # (1-z²), without equalling it. Check that divisibility exactly.
            shifts={(0,idx) for idx in (s.S.Zero,n,k)} if product_base!=q else set()
            if len(terms)==2:
                for top,bottom in (terms,terms[::-1]):
                    for idx in (s.S.Zero,n,k):
                        ratio=s.factor(-top/bottom/rationalize(A*product_base**idx))
                        delta=ratio.as_powers_dict().get(q,s.S.Zero)
                        if delta.is_Integer and s.cancel(ratio/q**delta)==1:
                            shifts.add((int(delta),idx))
            for delta,idx in sorted(shifts,key=lambda v:(v[0],str(v[1]))):
                    cur=A*q**delta;h=1-cur*product_base**idx
                    try:
                        quotient=s.cancel(rationalize(h)/rationalize(f))
                        if s.gcd(s.denom(quotient),s.numer(rationalize(f)))!=1:continue
                    except (ValueError,s.PolynomialError):continue
                    number+=1;hn=f'ptForFactor{number}';prefix=transport(row,cur,idx+1,mapping,N,hn,full)
                    if not prefix:continue
                    lines+=prefix
                    ratio=quotient.subs({Q:q**n,X:q**k})
                    lines+=['try',f'  have ptScalar{number} : {field(f,mapping)} ≠ 0 := by',
                       '    intro hz',
                       f'    have hh := FiniteQShift.factor_ne {field(cur,mapping)} ({pb}) {nat(idx,mapping)} {nat(idx+1,mapping)} (by omega) {hn}',
                       '    apply hh',
                       f'    calc 1-{field(cur,mapping)}*({pb})^{nat(idx,mapping)} = {field(ratio,mapping)} * {field(f,mapping)} := by',
                       f'           try simp only [{NORMAL}, inv_pow]',
                       '           poch_orient_powers',
                       '           all_goals first | (ring; done) | (field_simp [*] <;> ring)',
                       '         _ = 0 := by rw [hz]; ring']
        lines[group_start+5:]=['  '+line for line in lines[group_start+5:]]
    denominators=set()
    for v in [*expressions,*[x.subs(data['cores']) for x in data['normalized']]]:
        den=s.denom(compact(v))
        denominators.add(den)
        denominators.update(s.Mul.make_args(den))
        denominators.update(p.base for p in v.atoms(s.Pow)
                            if p.exp.is_Integer and p.exp<0)
    for i,den in enumerate(sorted(denominators,key=s.default_sort_key)):
        if den==1 or not den.is_Add:continue
        factored=compact(den,s.factor)
        def nz(v):
            if v.is_Mul:
                first,*rest=v.args
                return '(mul_ne_zero '+nz(first)+' '+nz(s.Mul(*rest))+')'
            if v.is_Pow:
                if v.exp.is_Integer and v.exp<0:
                    return '(inv_ne_zero (pow_ne_zero _ '+nz(v.base)+'))'
                return '(pow_ne_zero _ '+nz(v.base)+')'
            return '(by first | assumption | (poch_normalize_facts; assumption) | (norm_num; done))'
        lines+=['try',f'  have ptComposite{i} : {field(den,mapping)} ≠ 0 := by',
          f'    have hh : {field(factored,mapping)} ≠ 0 := by',
          '      exact '+nz(factored),
          f'    convert hh using 1 <;> simp only [{NORMAL}, inv_pow, pow_mul]',
          '    all_goals poch_orient_powers',
          '    all_goals ring', '    all_goals done']
    return '\n'.join(' '*indent+(l[:-3]+'poch_try' if l.strip()=='try' else l) for l in lines)+'\n'
