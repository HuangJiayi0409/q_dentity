"""Computed recurrence reconstruction through common product intervals.

No identity names or closed-form summation theorems are used. All generated
normalizations, domain transports, endpoints and initial values are obligations.
"""
import sympy as s
from expressions import n,k,q,Q,X,Poch,expression
from general_summation import parse,pieces,validate_local
from general_sum_emit import source_term,choice,SIMP
from poch_intervals import backward_certificate,compact
from poch_local import field,nat,normalize,NORMAL
from source_ir import list_items


def typed_source(node,names=None,exponent=False):
    names=names or {}
    if exponent and node['op']=='Nat.cast':
        return dict(op='var',name='(('+source_term(node['args'][0],names)+' : ℕ) : ℤ)')
    out=dict(node)
    out['args']=[typed_source(a,names,exponent or (node['op']=='HPow.hPow' and i==1))
                 for i,a in enumerate(node.get('args',[]))]
    if 'body' in node:out['body']=typed_source(node['body'],names,exponent)
    return out


def specialize(v,**values):
    return v.subs({{'n':n,'k':k}[key]:value for key,value in values.items()},simultaneous=True)


def finite_constants(v):
    return v.replace(lambda t:t.func==Poch and t.args[2].is_Integer and t.args[2]>=0,
                     lambda t:s.prod(1-t.args[0]*t.args[1]**i for i in range(int(t.args[2]))))


def facts(model,mapping,indent,extra_indices=()):
    """Instantiate actual original-domain hypotheses, never assume genericity."""
    lines=[];base=mapping['q'];N=model['index']
    for side in model['raw']['args']:
        if side['op']!='FiniteQBenchmark.phi':continue
        bs=side['args'][1];items=[dict(op='var',name=base),*list_items(bs)]
        lower=source_term(typed_source(bs))
        for i,a in enumerate(items):
            ap=source_term(typed_source(a))
            lines += ['try',f'  have pdFull{i} : poch {ap} {base} {N} ≠ 0 := by',
              f'    have hd := (show phiDefined {lower} {base} {N} from by assumption) {N} (by omega)',
              '    simp only [pochList_cons, pochList_nil, mul_one, mul_ne_zero_iff] at hd',
              '    tauto']
            for j,idx in enumerate(['0','gsN','gsN+1','gsK','gsK+1','gsK+2',*extra_indices]):
                lines += ['try',f'  have pdPrefix{i}_{j} : poch {ap} {base} ({idx}) ≠ 0 :=',
                  f'    FiniteQShift.prefix_ne {ap} {base} ({idx}) {N} (by omega) pdFull{i}',
                  'try',f'  have pdFactor{i}_{j} : 1-{ap}*{base}^({idx}) ≠ 0 :=',
                  f'    FiniteQShift.factor_ne {ap} {base} ({idx}) {N} (by omega) pdFull{i}',
                  'try',f'  have pdFactorRev{i}_{j} : -1+{ap}*{base}^({idx}) ≠ 0 := by',
                  f'    intro hz; apply pdFactor{i}_{j}; linear_combination -hz']
    return '\n'.join(' '*indent+(l[:-3]+'poch_try' if l.strip()=='try' else l) for l in lines)+'\n'


def finish(exprs,model,mapping,indent,extra_indices=()):
    # Kernel-check each rational identity once in a separate theorem. Keeping
    # the full normalization proof inline duplicates it in later rewrites.
    from poch_intervals import plan as interval_plan
    rows=interval_plan(exprs)['rows']
    spans=[int(row[key]) for row in rows for key in ('prefix','suffix')]
    spans += [int(atom.args[2]) for v in exprs for atom in v.atoms(Poch)
              if atom.args[2].is_Integer]
    if max(spans,default=0)<=1:
        return finish_body(exprs,model,mapping,indent,extra_indices)
    return (' '*indent+'as_aux_lemma =>\n'+
            finish_body(exprs,model,mapping,indent+2,extra_indices))


def finish_body(exprs,model,mapping,indent,extra_indices=()):
    from poch_domains import emit as domain_emit
    # Derive endpoint evidence from the actual products. A lifted recurrence
    # may require factors beyond the fixed first-order n+1 prefix.
    endpoints=set(extra_indices)
    supplied={s.S.Zero,n,n+1,k,k+1,k+2}
    for value in exprs:
        for atom in value.atoms(Poch):
            length=atom.args[2]
            if length.has(n,k) or (length.is_Integer and length>0):
                for index in (length,s.expand(length-1)):
                    if s.expand(index) not in supplied:
                        endpoints.add(nat(index,mapping))
    lines=' '*indent+'poch_clear_context\n'
    explicit=any(side['op']=='Finset.sum' for side in model['raw']['args'])
    if explicit:
        for idx in ('0',model['index'],'gsN','gsN+1','gsK','gsK+1',*extra_indices):
            lines+=' '*indent+f'poch_domain_at ({idx})\n'
    lines+=facts(model,mapping,indent,sorted(endpoints))
    lines+=domain_emit(exprs,model,mapping,indent)
    pad=' '*indent
    lines+=pad+f'try simp only [{NORMAL}, pochList_cons, pochList_nil, mul_one]\n'
    lines+=pad+'poch_normalize_arguments\n'
    if explicit:lines+=pad+'all_goals poch_prefix_facts\n'
    lines+=pad+'all_goals\n'
    indent+=2;pad=' '*indent
    lines+=normalize(exprs,mapping,indent,rewrite_facts=False)
    lines+=pad+'all_goals\n'
    indent+=2;pad=' '*indent
    lines+=pad+f'try simp only [{NORMAL}, poch_zero]\n'
    lines+=pad+'poch_normalize_powers\n'
    lines+=pad+'poch_orient_powers\n'
    for index,label in [('gsN','Outer'),('gsK','Inner')]:
        lines+=pad+f'try have pt{label}Pow : {mapping["q"]}^{index} ≠ 0 := pow_ne_zero _ (by assumption)\n'
        lines+=pad+f'try generalize ps{label}Eq : {mapping["q"]}^{index} = ps{label}Power at *\n'
    close='all_goals (poch_clear_denominators <;> (try simp only [inv_pow, pow_mul]) <;> (try poch_clear_denominators) <;> ring)'
    from poch_intervals import plan as interval_plan
    rows=interval_plan(exprs)['rows']
    spans=[int(row[key]) for row in rows for key in ('prefix','suffix')]
    spans += [int(atom.args[2]) for v in exprs for atom in v.atoms(Poch)
              if atom.args[2].is_Integer]
    if max(spans,default=0)<=1:
        # Binomial endpoints usually already have direct nonzero witnesses.
        # Keep their small context first; replay the full product ledger only
        # if the complete kernel proof cannot close with those witnesses.
        fast=('all_goals (field_simp (disch := first | field_simp_discharge | tauto) <;> (try simp only [inv_pow, pow_mul]) <;> ring)' if explicit else close)
        lines+=pad+'first\n'+pad+'| ('+fast+'; done)\n'
        lines+=pad+'| (poch_rewrite_all_facts; all_goals poch_prepare_facts; '+close+'; done)\n'
    else:
        lines+=pad+'poch_rewrite_all_facts\n'+pad+'all_goals poch_prepare_facts\n'+pad+close+'\n'
    return lines


def finish_outer(exprs,model,mapping,indent):
    """Separate the finite outer-index prefix where intervals do not overlap."""
    from poch_intervals import plan as interval_plan
    cores=interval_plan(exprs)['cores'].values()
    cutoff=max([0]+[-int(s.expand(t.args[2]).subs({n:0,k:0}))
                    for t in cores if t.args[2].has(n)
                    and s.expand(t.args[2]).subs({n:0,k:0}).is_Integer])
    def branches(depth,padsize):
        pad=' '*padsize
        if depth==cutoff:
            return finish([specialize(v,n=n+depth) for v in exprs],model,mapping,padsize)
        result=pad+'cases gsN with\n'+pad+'| zero =>\n'
        result+=pad+f'  let gsN : ℕ := {depth}\n'
        result+=finish([specialize(v,n=depth) for v in exprs],model,mapping,padsize+2)
        result+=pad+'| succ gsN =>\n'+branches(depth+1,padsize+2)
        return result
    return branches(0,indent)


def emit(model,construction):
    if construction.get('status') != 'constructed':
        raise ValueError('invalid_certificate: not constructed')
    if len(model['sides']) != 2 or len(construction.get('sides',[])) != 2:
        raise ValueError('invalid_certificate: exactly two source sides required')
    cs=list(map(parse,construction['coefficients']));r=len(cs)-1
    if r<1 or r!=construction['order']:raise ValueError('invalid_certificate: recurrence order')
    canonical={v:key for key,v in model['names'].items()}
    mapping=dict(canonical,n='gsN',k='gsK',Q=f"({canonical['q']}^gsN)",X=f"({canonical['q']}^gsK)")
    printedcs=[s.factor(c) for c in cs]
    actualcs=[c.subs({Q:q**n,X:q**k}) for c in printedcs]
    index=model['index'];script='';boundaries=[];defined=[]
    explicit=any(side['op']=='Finset.sum' for side in model['raw']['args'])
    flux_normalize=(lambda v:compact(v,s.factor)) if explicit else (lambda v:s.factor(s.cancel(v)))
    # A nonzero constant initial residual cannot be discharged by this
    # recurrence proof. Reject it before generating large local proofs; this
    # is only a rejection filter. Accepted initial values remain Lean goals.
    initial_values=[]
    for row in model['sides']:
        f=expression(row['expression'])
        value=(sum(specialize(f,n=0,k=t) for t in range(row['offset']))
               if row['kind']=='sum' else specialize(f,n=0))
        initial_values.append(finite_constants(value))
    initial_residual=s.cancel(initial_values[0]-initial_values[1])
    if initial_residual.is_number and initial_residual.is_zero is False:
        raise ValueError('initial_value_mismatch: nonzero constant residual at index zero')
    for i,raw in enumerate(model['raw']['args']):
        printed=source_term(typed_source(raw,{index:'gsN'}),{index:'gsN'})
        if model['sides'][i]['kind']=='scalar':printed=f'({printed}) + 0*{canonical["q"]}'
        script+=f'  let psS{i} := fun (gsN : ℕ) => {printed}\n'
    script+=f'  let psC := fun (gsN gsJ : ℕ) => ({choice(printedcs,mapping)}) + 0*{canonical["q"]}\n'
    for i,(row,witness) in enumerate(zip(model['sides'],construction['sides'])):
        if list(map(parse,witness['coefficients']))!=cs:raise ValueError('invalid_certificate: side coefficients')
        F=expression(row['expression'])
        if row['kind']=='scalar':
            boundaries.append(sum(c*specialize(F,n=n+j) for j,c in enumerate(actualcs)))
            continue
        components=pieces(F);Rs=list(map(parse,witness['certificates']))
        validate_local(components,cs,Rs)
        seeds=list(map(parse,witness.get('seed_certificates',witness['certificates'])))
        seedcs=list(map(parse,witness.get('seed_coefficients',witness['coefficients'])))
        multipliers=list(map(parse,witness.get('multiplier',['1'])
                             if 'seed_certificates' in witness else ['1']))
        from ore import multiply
        product=multiply(multipliers,seedcs)
        if len(product)!=len(cs) or any(s.cancel(a-b)!=0 for a,b in zip(product,cs)):
            raise ValueError('invalid_certificate: Ore seed does not produce the common relation')
        validate_local(components,seedcs,seeds)
        # Lift the flux itself. Dividing shifted summands by the unshifted
        # summand introduces removable poles at zeros of numerator products.
        baseflux=sum(flux_normalize(backward_certificate(f,R).subs({Q:q**n,X:q**k})*f)
                     for f,R in zip(components,seeds))
        baseinitial=finite_constants(sum(R.subs({X:1,Q:q**n})*specialize(f,k=0)
                                        for R,f in zip(seeds,components)))
        flux=sum(a.subs(Q,q**n)*specialize(baseflux,n=n+j) for j,a in enumerate(multipliers))
        if explicit:flux=flux_normalize(flux)
        initial=sum(a.subs(Q,q**n)*specialize(baseinitial,n=n+j) for j,a in enumerate(multipliers))
        initial=flux_normalize(initial) if explicit else s.cancel(initial)
        if initial.has(s.nan,s.zoo,s.oo):initial=s.S.Zero
        a,b=row['slope'],row['offset'];m=a*n+b
        if b<1:raise ValueError('proof_representation_gap: zero moving prefix requires separate endpoint branch')
        bound=nat(m,mapping)
        ftext=field(F,mapping);btext=field(flux,mapping)
        if F.is_number:ftext+=f' + 0*{canonical["q"]}'
        if flux.is_number:btext+=f' + 0*{canonical["q"]}'
        script+=f'  let psF{i} := fun (gsN gsK : ℕ) => {ftext}\n'
        script+=f'  let psB{i} := fun (gsN gsK : ℕ) => {btext}\n'
        script+=f'  let psG{i} := fun (gsN gsK : ℕ) => if gsK=0 then {field(initial,mapping)} else psB{i} gsN (gsK-1)\n'
        defined += [f'psF{i}',f'psB{i}',f'psG{i}']
        script+=f'''  have psSource{i} : ∀ gsN, psS{i} gsN =
      ∑ gsK ∈ Finset.range {bound}, psF{i} gsN gsK := by
    intro gsN
    try simp only [psS{i}, psF{i}, zpow_sub₀ (by assumption : {canonical['q']} ≠ 0),
      zpow_neg, zpow_natCast, zpow_one]
    simp only [psS{i}, psF{i}, phi, phiTerm, pochList_cons, pochList_nil,
      List.length_cons, List.length_nil, Int.reduceAdd, Int.reduceSub, zpow_zero,
      {NORMAL}, one_mul, mul_one, zero_mul, mul_zero, add_zero, zero_add,
      Nat.add_assoc, Nat.add_comm, Nat.add_left_comm, mul_assoc, mul_comm, mul_left_comm]
    all_goals try ring
    all_goals try simp only [pow_zero, zpow_zero, mul_one, one_mul]
    all_goals try ring
    all_goals
      apply Finset.sum_congr rfl
      intro gsK gsRange
      simp only [Finset.mem_range] at gsRange
      simp only [mul_ne_zero_iff] at *
      simp (disch := first | assumption | omega | tauto) only [pow_sub₀, inv_inv, inv_pow]
      all_goals try simp only [inv_inv, inv_pow]
      all_goals ring
'''
        boundary=specialize(flux,k=m-1)-initial+sum(c*sum(specialize(F,n=n+j,k=m+t) for t in range(a*j)) for j,c in enumerate(actualcs))
        boundaries.append(boundary)
        script+=f'''  have psH{i} : ∀ gsN, gsN+{r} ≤ {index} →
      (∑ gsJ ∈ Finset.range {r+1}, psC gsN gsJ * psS{i} (gsN+gsJ)) = {field(boundary,mapping)} := by
    intro gsN gsBound
    have psTelescoping := FiniteQGeneralSum.telescoper_range
      (fun gsJ gsK => psF{i} (gsN+gsJ) gsK) (psG{i} gsN)
      (psC gsN) {r} {bound} (fun gsJ => {a}*gsJ) (by
        intro gsK gsRange
'''
        # Common product intervals may start only after several summation
        # indices. Check every earlier index explicitly, then the stable tail.
        from poch_intervals import plan as interval_plan
        generic_left=sum(c*specialize(F,n=n+j) for j,c in enumerate(actualcs))
        generic_right=flux-specialize(flux,k=k-1)
        cores=interval_plan([generic_left,generic_right])['cores'].values()
        cutoff=max([1,r]+[-int(s.expand(t.args[2]).subs({n:0,k:0}))
                          for t in cores if s.expand(t.args[2]).subs({n:0,k:0}).is_Integer])
        def local_steps(idx,indent):
            pad=' '*indent
            steps=pad+f'dsimp only [psF{i}, psG{i}, psB{i}, psC]\n'
            steps+=pad+'try '+SIMP.replace(chr(10),' ')+'\n'
            steps+=pad+('try simp only [Nat.reduceSub, Nat.reduceEqDiff, Nat.succ_ne_zero, '
                'Nat.succ_sub_one, Nat.succ_eq_add_one, Nat.add_sub_cancel, '
                'Nat.add_eq_zero_iff, Nat.one_ne_zero, and_false, ite_true, ite_false]\n')
            left=sum(c*specialize(F,n=n+j,k=idx) for j,c in enumerate(actualcs))
            right=specialize(flux,k=idx)-(initial if idx==0 else specialize(flux,k=idx-1))
            return steps+finish([left,right],model,mapping,indent)
        def local_cases(depth,indent):
            pad=' '*indent
            if depth==cutoff:return local_steps(k+depth,indent)
            return (pad+'cases gsK with\n'+pad+'| zero =>\n'+local_steps(s.Integer(depth),indent+2)
                    +pad+'| succ gsK =>\n'+local_cases(depth+1,indent+2))
        script+=local_cases(0,8)+')\n'
        script+=f'''    simp_rw [psSource{i}]
    convert psTelescoping using 1 <;> (try simp only [psF{i}, psG{i}, psB{i}, psC,
      phi, phiTerm, pochList_cons, pochList_nil, List.length_cons, List.length_nil,
      Int.reduceAdd, Int.reduceSub, zpow_zero,
      Nat.mul_add, Nat.add_sub_cancel_left, Nat.add_sub_cancel, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm,
      {NORMAL}, one_mul, mul_one, zero_mul, mul_zero, add_zero, zero_add,
      Nat.reduceEqDiff, Nat.reduceAdd, Nat.reduceSub, Finset.sum_range_succ, Finset.sum_range_zero,
      ite_true, ite_false])
    all_goals try omega
    all_goals
'''
        from poch_domains import emit as domain_emit
        script+='      poch_clear_context\n'
        script+=facts(model,mapping,6)
        script+=domain_emit([boundary],model,mapping,6)
        script+='      poch_normalize_arguments\n'
        script+='      all_goals\n'
        script+='        poch_normalize_powers\n'
        script+='        poch_orient_powers\n'
        script+='        poch_clear_denominators <;> (try simp only [inv_pow, pow_mul]) <;> (try poch_orient_powers) <;> ring\n'
    defs=', '.join(['psS0','psS1','psC',*defined])
    script+=f'''  suffices psTarget : psS0 {index} = psS1 {index} by
    simpa only [psS0, psS1, zero_mul, add_zero] using psTarget
  apply FiniteQGeneralSum.recurrence_unique psS0 psS1 psC {r} {index} (by omega)
  · intro gsJ gsSmall gsBound
    interval_cases gsJ
'''
    for j in range(r):
        script+=f'''    · let gsN : ℕ := {j}
      change psS0 gsN = psS1 gsN
      norm_num only [{defs}, gsN, phi, phiTerm, pochList, poch,
        Finset.sum_range_succ, Finset.sum_range_zero, Finset.prod_range_succ, Finset.prod_range_zero, List.map_cons, List.map_nil,
        List.prod_cons, List.prod_nil, List.length_cons, List.length_nil,
        Int.reduceAdd, Int.reduceSub, Int.reduceNeg, Nat.reduceAdd,
        Nat.cast_ofNat, pow_zero, pow_one, zpow_zero, zpow_one,
        mul_one, one_mul, zero_add, add_zero, mul_zero, zero_mul]
      all_goals
'''
        initials=[]
        for row in model['sides']:
            f=expression(row['expression'])
            initials.append(sum(specialize(f,k=t) for t in range(row['slope']*j+row['offset']))
                            if row['kind']=='sum' else f)
        script+=finish(initials,model,mapping,8,tuple(map(str,range(j))))
    script+='  · intro gsN gsBound\n'
    for i,row in enumerate(model['sides']):
        if row['kind']=='sum':script+=f'    rw [psH{i} gsN gsBound]\n'
    script+=f'    try dsimp only [{defs}]\n    try {SIMP.replace(chr(10)," ")}\n'
    from poch_intervals import plan as interval_plan
    if all(interval_plan([b])['normalized'][0] == 0 for b in boundaries):
        # Homogeneous forcing is checked independently on each side. Combining
        # their unrelated product denominators needlessly enlarges the proof.
        script+='    trans 0\n    ·\n'
        script+=finish_outer([boundaries[0]],model,mapping,6)
        script+='    · symm\n'
        script+=finish_outer([boundaries[1]],model,mapping,6)
    else:
        script+=finish_outer(boundaries,model,mapping,4)
    from singular_emit import singular_branch
    script+=singular_branch('ps',r,actualcs[-1],lambda c:field(c,mapping),defs)
    return script,dict(kind='product_interval_recurrence',order=r,backward_flux=True,
          target_used_for_local_search=False,
          coefficients=list(map(str,cs)),
          obligations=['unchanged source expression bridge',
                       'computed local telescoping certificate',
                       'product interval lengths and parameter shifts',
                       'denominators from original assumptions',
                       'both flux endpoints and every moving tail',
                       'common recurrence and all initial values',
                       'leading coefficient or explicit singular obligation',
                       'original theorem kernel and dependency audit'])
