"""Native bibasic input, certificate-to-product representation, Lean verification."""
import itertools
import sympy as s
from expressions import expression, Poch, k
from bibasic import p,q,X,Y,rationalize,shift
from lean_pipeline import HERE,find_nodes,OPS,verify_proof


def normalize(t):
    t=dict(t)
    if 'args' in t:t['args']=[normalize(a) for a in t['args']]
    if 'body' in t:t['body']=normalize(t['body'])
    if t['op'] in ('Int.ofNat','Nat.cast'):return t['args'][0]
    if t['op']=='FiniteQBenchmark.pochList':
        ls,base,length=t['args'];result={'op':'nat','value':1}
        items=[]
        while ls['op']=='List.cons':
            items.append(ls['args'][0]);ls=ls['args'][1]
        if ls['op']!='List.nil':raise ValueError('representation_gap: explicit Pochhammer list required')
        for a in reversed(items):
            result={'op':'HMul.hMul','args':[{'op':'FiniteQBenchmark.poch','args':[a,base,length]},result]}
        return result
    return t


def frontend(raw,identity):
    raw=normalize(raw)
    if raw['op']!='Eq':raise ValueError('unsupported_structure: equality required')
    left,target=raw['args'];reverse=target['op']=='Finset.sum'
    if reverse:left,target=target,left
    if left['op']!='Finset.sum':raise ValueError('unsupported_structure: one range sum required')
    domain,binder=left['args']
    if domain['op']!='Finset.range' or binder['op']!='lambda':raise ValueError('unsupported_structure: range sum required')
    upper=domain['args'][0]
    if upper['op']!='HAdd.hAdd' or upper['args'][0]['op']!='var' or upper['args'][1]!={'op':'nat','value':1}:
        raise ValueError('unsupported_structure: variable range(n+1) required')
    index=upper['args'][0]['name'];bound=binder['name'];term=binder['body']
    if any(v['name']==index for v in find_nodes(term,'var')):
        raise ValueError('unsupported_structure: first bibasic emitter needs n-independent term')
    bases=[]
    for atom in find_nodes(term,'FiniteQBenchmark.poch'):
        b=atom['args'][1]
        if b['op']!='var':raise ValueError('unsupported_structure: variable Pochhammer bases required')
        if b['name'] not in bases:bases.append(b['name'])
    if len(bases)!=2:raise ValueError('unsupported_structure: exactly two distinct base variables required')
    names={bases[0]:'p',bases[1]:'q',bound:'k',index:'n'}
    if len(names)!=4:raise ValueError('unsupported_structure: overlapping variables')
    def convert(t):
        op=t['op']
        if op=='var':
            name=t['name']
            if name not in names:names[name]='v'+str(len(names))
            return names[name]
        if op=='nat':return t['value']
        if op=='Neg.neg':return ['mul',-1,convert(t['args'][0])]
        if op=='Inv.inv':return ['div',1,convert(t['args'][0])]
        if op in OPS:return [OPS[op],*map(convert,t['args'])]
        raise ValueError('unsupported_expression: bibasic '+op)
    F=convert(term);T=convert(target)
    return {'schema_version':1,'source_id':identity,'summand':F}, {
        'names':names,'index':index,'binder':bound,'summand':F,'target':T,'reverse':reverse}


def representation(model,construction):
    F=expression(model['summand'])
    atoms=sorted(F.atoms(Poch),key=str)
    powers=F.as_powers_dict()
    if any(a.args[2]!=k or powers.get(a) not in (-1,1) for a in atoms):
        raise ValueError('representation_gap: multiplicative length-k Pochhammer atoms required')
    atomic=s.prod(a**powers[a] for a in atoms)
    weight=F/atomic
    geometric=s.prod(t for t in s.Mul.make_args(weight) if t.is_Pow and t.exp.has(k) and not t.base.has(k,p,q))
    prefactor=rationalize(s.cancel(weight/geometric))
    from expressions import shift_ratio
    U=rationalize(shift_ratio(F,k))
    symbols={str(a):a for a in F.free_symbols|{p,q,X,Y}}
    R=s.sympify(construction['certificate'],locals=symbols)
    if s.cancel(U*shift(R)-R-1)!=0:
        raise ValueError('invalid_certificate: bibasic local residual')
    Hfactor=s.cancel(U*shift(R)*prefactor)
    numerator=[a for a in atoms if powers[a]==1]
    if len(numerator)>8:raise ValueError('representation_gap: numerator representation search limit')
    # This bounded search changes only Lean representation, after Gosper finished.
    for choices in itertools.product((0,1),repeat=len(numerator)):
        ratio=s.Integer(1);replacement={}
        for a,choice in zip(numerator,choices):
            if choice:
                start,base,_=a.args
                ratio*= (1-start*base**k)/(1-start)
                replacement[a]=Poch(start*base,base,k)
        coefficient=s.cancel(Hfactor/rationalize(ratio))
        if coefficient.has(X,Y):continue
        num,den=s.fraction(coefficient)
        if den!=1 or not num.is_polynomial(*num.free_symbols):continue
        H=coefficient*geometric*atomic.xreplace(replacement)
        return H,{'inclusive_multiplier':str(s.cancel(U*shift(R))),
                  'coefficient':str(coefficient),
                  'start_shifts':[{'atom':str(a),'shift':choice} for a,choice in zip(numerator,choices)],
                  'representation':str(H),'target_used_for_representation':False}
    raise ValueError('domain_unresolved: no pole-free shifted-product representation')


def render(expr,mapping):
    if expr.is_Integer:return f'({int(expr)})'
    if expr.is_Symbol:return mapping[str(expr)]
    if expr.func==Poch:return '(poch '+' '.join(render(a,mapping) for a in expr.args)+')'
    if expr.is_Add:
        terms=s.Add.make_args(expr)
        return '('+render(terms[0],mapping)+''.join((' - '+render(-t,mapping)) if t.could_extract_minus_sign() else (' + '+render(t,mapping)) for t in terms[1:])+')'
    if expr.is_Mul:
        return '('+(' + ' if expr.is_Add else ' * ').join(render(a,mapping) for a in expr.args)+')'
    if expr.is_Pow:
        a,e=expr.args
        if e.is_Integer:
            body=render(a,mapping) if abs(int(e))==1 else f'({render(a,mapping)} ^ {abs(int(e))})'
            return body if e>=0 else f'({body})⁻¹'
        if e==k:return f'({render(a,mapping)} ^ {mapping["k"]})'
        if e==-k:return f'({render(a,mapping)} ^ {mapping["k"]})⁻¹'
    raise ValueError('representation_gap: unsupported bibasic proof expression '+str(expr))


def emit(model,construction):
    H,plan=representation(model,construction)
    F=expression(model['summand']);T=expression(model['target'])
    used=set(model['names'])
    def fresh(name):
        while name in used:name+='_' 
        used.add(name);return name
    j,ff,hh=map(fresh,('bbk','bbF','bbH'))
    names={v:a for a,v in model['names'].items()};names['k']=j
    ftext,htext=render(F,names),render(H,names)
    # Target printing substitutes the original upper index for its IR variable.
    tn=dict(names);tn['k']=model['index']
    T=T.subs(s.Symbol('n',integer=True),k)
    ttext=render(T,tn)
    index=model['index']
    shifts=[a for a in plan['start_shifts'] if a['shift']]
    atoms={str(a):a for a in F.atoms(Poch)}
    heads=[];arguments=[]
    for entry in shifts:
        a,b,_=atoms[entry['atom']].args
        heads.append(f'    rw [FiniteQP1.poch_head {render(a,names)} {render(b,names)} {j}]')
        an=fresh('bbarg')
        arguments.append((an,f'      have {an} : {render(a,names)} * {render(b,names)} = {render(a*b,names)} := by\n        first | (ring; done) | (simp only [div_eq_mul_inv, mul_inv_rev, inv_pow, pow_one] <;> ring)'))
    # Denominators are read from the two actual expressions, never from the RHS.
    den_atoms=sorted({a for e in (F,H) for a,power in e.as_powers_dict().items()
                      if a.func==Poch and power.is_Integer and power<0},key=str)
    # Constant denominators can occur inside rational prefactors and geometric weights.
    constant_den=set()
    for e in (F,H):
        for t in s.preorder_traversal(e):
            if t.is_Pow and (t.exp.is_negative or t.exp==-k) and not t.base.has(k,Poch):
                constant_den.add(t.base)
    norm='div_eq_mul_inv, mul_inv_rev, inv_inv, inv_pow, pow_one, neg_mul, mul_neg, one_mul, mul_one, mul_comm, mul_left_comm, mul_assoc'
    facts=[]; retained=[]
    for a in sorted(constant_den,key=str):
        cn=fresh('bbConstantNe');retained.append(cn)
        facts.append(f'  have {cn} : {render(a,names)} ≠ 0 := by\n    try simp only [{norm}]\n    tauto')
    localfacts=[]; factor_names=[]
    for atom_i,a in enumerate(den_atoms):
        for offset in (0,1):
            mm=dict(names,k=j if offset==0 else f'({j}+1)')
            dn=fresh(f'bbden{atom_i}_{offset}')
            if offset==0:retained.append(dn)
            localfacts.append(f'      have {dn} : {render(a,mm)} ≠ 0 := by\n        try simp only [{norm}]\n        tauto')
        fn=fresh(f'bbfactor{atom_i}')
        factor_names.append(fn);retained.append(fn)
        start,base,_=a.args
        localfacts.append(f'      have {fn} : 1 - {render(start,names)} * {render(base,names)}^{j} ≠ 0 := by rw [poch_succ] at {dn}; exact (mul_ne_zero_iff.mp {dn}).2')
    factor_line=("      field_simp at "+" ".join(factor_names)+
                 "\n      try simp only [div_ne_zero_iff, mul_ne_zero_iff] at "+" ".join(factor_names)+
                 "\n      ring_nf (ifUnchanged := .silent) at "+" ".join(factor_names)) if factor_names else ""
    proof=f'''  {'symm' if model['reverse'] else 'skip'}
  p1_bibasic_domain 0
  simp only [pochList_cons, pochList_nil, mul_one, zpow_neg, zpow_natCast] at *
  simp only [mul_ne_zero_iff, Finset.mem_range] at *
  have hzero : 0 < {index}+1 := by omega
  try have : {names['p']} ≠ 0 := (show regular {names['p']} from by assumption).1
  try have : {names['q']} ≠ 0 := (show regular {names['q']} from by assumption).1
{chr(10).join(facts)}
  let {ff} := fun ({j} : ℕ) => {ftext}
  let {hh} := fun ({j} : ℕ) => {htext}
  suffices hgoal : (∑ {j} ∈ Finset.range ({index}+1), {ff} {j}) = {ttext} by
    calc
      _ = ∑ {j} ∈ Finset.range ({index}+1), {ff} {j} := by
        apply Finset.sum_congr rfl
        intro {j} hj
        dsimp only [{ff}]
        simp only [{norm}]
        all_goals first | (ring; done) | (field_simp [*] <;> ring)
      _ = {ttext} := hgoal
      _ = _ := by simp only [{norm}] <;> ring
  have hsum : (∑ {j} ∈ Finset.range ({index}+1), {ff} {j}) = {hh} {index} := by
    apply FiniteQP1.sum_inclusive_antidifference {ff} {hh} {index}
    · simp [{ff}, {hh}, poch_zero]
      simp only [{norm}] at *
      field_simp
      <;> ring
    · intro {j} hj
      have hj0 : {j} < {index}+1 := by omega
      have hj1 : {j}+1 < {index}+1 := by omega
      p1_bibasic_domain {j}
      p1_bibasic_domain ({j}+1)
{chr(10).join(localfacts)}
{factor_line}
      dsimp only [{ff}, {hh}]
      try clear {ff} {hh}
'''
    # Indent the generated product-head rewrites inside the local proof.
    proof+='\n'.join('  '+line for line in heads)+'\n'
    proof+='\n'.join(text for _,text in arguments)+'\n'
    if arguments:proof+='      simp only ['+', '.join(name for name,_ in arguments)+']\n'
    proof+=f'''      simp only [poch_succ, pow_succ]
      simp only [div_eq_mul_inv, mul_inv_rev, inv_inv, inv_pow, pow_one,
        one_mul, mul_one]
'''
    # Abstract repeated finite products only after their exact shifts have been
    # proved. Their nonzero evidence is transported by the same generalization.
    for atom in sorted(H.atoms(Poch),key=str):
        variable=fresh('bbProduct');equation=fresh('bbProductEq')
        proof+=f'      generalize {equation} : {render(atom,names)} = {variable} at *\n'
    for base in ('p','q'):
        variable=fresh('bbPower');equation=fresh('bbPowerEq');hn=fresh('bbPowerNe')
        if {'p':p,'q':q}[base] in constant_den:
            proof+=f'      have {hn} : {names[base]}^{j} ≠ 0 := pow_ne_zero _ (by assumption)\n'
            retained.append(hn)
        proof+=f'      generalize {equation} : {names[base]}^{j} = {variable} at *\n'
    if factor_names:
        proof+='      ring_nf (ifUnchanged := .silent) at '+' '.join(factor_names)+'\n'
    if retained:proof+='      clear * - '+' '.join(retained)+'\n'
    # Normalize only the retained scalar evidence inside denominator obligations.
    ac='simp only [sub_eq_add_neg, add_comm, add_left_comm, add_assoc, mul_comm, mul_left_comm, mul_assoc, mul_ne_zero_iff] at *'
    discharger='first | field_simp_discharge | ('+ac+'; tauto)'
    proof+=f'      field_simp (disch := {discharger})\n'
    proof+=f'      all_goals first | (ring; done) | ({ac}; field_simp (disch := {discharger}) <;> ring)\n'
    proof+=f'''  rw [hsum] <;> dsimp only [{hh}] <;> simp only [{norm}] <;> ring
'''
    return proof,dict(plan,algorithm='bibasic Gosper',certificate=construction['certificate'],
                       endpoint_policy='inclusive primitive: initial term plus bounded differences')


def synthesize(source,model,construction,work,env):
    proof,plan=emit(model,construction)
    return verify_proof(source,proof,plan,work,env,[(HERE/'lean/BibasicRules.lean').read_text(),
        'set_option maxHeartbeats 4000000\n'])
