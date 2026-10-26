"""P1 defined-sequence closure: actual definition export, Ore witnesses, Lean exit."""
import sympy as s
from expressions import n,k,q,Q,Poch
from bibasic_pipeline import normalize
from lean_pipeline import HERE,find_nodes,extract,verify_proof
from zeilberger_pipeline import frontend as zfrontend,emit_proof as zemit
from ore import companion,polynomial_closure,observable_row,iterate_row,eliminate,forced_relation

H=s.Function('Sequence')
SUM=s.Symbol('SumAtom')


def symbolic(t,names):
    op=t['op']
    if op=='var':return {'n':n,'k':k,'q':q}.get(names[t['name']],s.Symbol(names[t['name']]))
    if op=='nat':return s.Integer(t['value'])
    if op=='Finset.sum':return SUM
    a=[symbolic(v,names) for v in t.get('args',[])]
    if op=='FiniteQBenchmark.rogersSzego':return H(a[-1])
    if op=='FiniteQBenchmark.poch':return Poch(*a)
    if op=='HAdd.hAdd':return a[0]+a[1]
    if op=='HSub.hSub':return a[0]-a[1]
    if op=='HMul.hMul':return a[0]*a[1]
    if op=='HDiv.hDiv':return a[0]/a[1]
    if op=='HPow.hPow':return a[0]**a[1]
    if op=='Neg.neg':return -a[0]
    raise ValueError('unsupported_expression: Ore '+op)



def observable_ir(e):
    if e.is_Integer:return int(e)
    if e.is_Symbol:return str(e)
    if e.func==H:return ['sequence',observable_ir(e.args[0])]
    op={s.Add:'add',s.Mul:'mul',s.Pow:'pow'}.get(e.func)
    if op:return [op,*map(observable_ir,e.args)]
    raise ValueError('unsupported_structure: arithmetic sequence observable required')


def observable_expression(node):
    from expressions import expression
    if not isinstance(node,list):return expression(node)
    op,*children=node
    if op=='sequence' and len(children)==1:return H(expression(children[0]))
    args=list(map(observable_expression,children))
    if op=='add' and args:return s.Add(*args)
    if op=='mul' and args:return s.Mul(*args)
    if op=='pow' and len(args)==2:return args[0]**args[1]
    raise ValueError('unsupported_expression: malformed observable IR')

def prepare(raw,identity,work,env):
    raw=normalize(raw)
    if raw['op']!='Eq':raise ValueError('unsupported_structure: Ore equality required')
    if not find_nodes(raw,'Finset.sum'):
        from defined_relation import prepare as prepare_relation
        return prepare_relation(raw,identity,work,env)
    left,right=raw['args']
    atoms=find_nodes(raw,'FiniteQBenchmark.rogersSzego')
    sums=find_nodes(right,'Finset.sum')
    if not atoms or len(sums)!=1 or find_nodes(left,'Finset.sum'):
        raise ValueError('unsupported_structure: one defined-sequence observable and one finite sum required')
    params=atoms[0]['args'][:2]
    if any(a['op']!='var' for a in params) or any(a['args'][:2]!=params for a in atoms):
        raise ValueError('unsupported_structure: common variable sequence parameters required')
    domain,binder=sums[0]['args']
    if domain['op']!='Finset.Icc' or domain['args'][0]!={'op':'nat','value':1} or domain['args'][1]['op']!='var':
        raise ValueError('unsupported_structure: first Ore exit needs Icc 1 n')
    index=domain['args'][1]['name'];x,base=[a['name'] for a in params]
    definition_source=f'''import Benchmark.P1Atoms
open FiniteQBenchmark
open scoped BigOperators
variable {{K : Type*}} [Field K]
theorem definition_input ({x} {base} : K) ({index} : ℕ) : rogersSzego {x} {base} {index} = 0 := by
  sorry
'''
    dw=work/'object_definition';dw.mkdir(exist_ok=True)
    from workflow.preprocessed import ACTIVE
    token=ACTIVE.set(None)
    try:definition=extract(definition_source,dw,env,prelude='  unfold rogersSzego')
    finally:ACTIVE.reset(token)
    formula,dm=zfrontend(definition,identity+'-definition')
    names=dict(dm['names']);names[binder['name']]='k'
    obs=symbolic(left,names)
    shifts=[s.expand(a.args[0]-n) for a in obs.atoms(H)]
    if not shifts or any(not a.is_Integer for a in shifts) or min(shifts)!=-1:
        raise ValueError('representation_gap: observable must start at n-1')
    term=symbolic(binder['body'],names)
    seq=list(term.atoms(H))
    if seq!=[H(n-k)]:raise ValueError('representation_gap: triangular sequence index required')
    degree=term.as_powers_dict().get(seq[0])
    if degree!=2:raise ValueError('representation_gap: current native closure exit is quadratic')
    weight=term/seq[0]**degree
    pref=symbolic(right,names)/SUM
    if pref.has(SUM,H,k):raise ValueError('unsupported_structure: scalar outer prefactor required')
    model={'names':names,'index':index,'parameter':x,'base':base,'definition_model':dm,
           'observable':str(obs.subs(n,n+1)),
           'prefactor':str(pref.subs(n,n+1)),
           'kernel':str(weight.subs({n:n+1,k:n+1-k},simultaneous=True))}
    problem=dict(formula,observable=observable_ir(obs.subs(n,n+1)),degree=int(degree))
    return problem,model


def construct(problem,budget):
    if problem.get('mode') in ('defined_linear_relation','defined_closed_form','defined_parameter_relation'):
        from defined_relation import construct as construct_relation
        return construct_relation(problem,budget)
    from zeilberger import construct as zconstruct
    if set(problem)!={'schema_version','source_id','summand','observable','degree'}:
        raise ValueError('invalid_problem: expected exported definition and observable')
    zr=zconstruct({k:problem[k] for k in ('schema_version','source_id','summand')},budget)
    z=zr['construction']
    if z['status']!='constructed':return {'construction':z,'definition_search':zr}
    cs=[s.sympify(v,locals={'q':q,'Q':Q}) for v in z['coefficients']]
    M=companion(cs);T,powers,u=polynomial_closure(M,problem['degree'],budget.max_unknowns)
    obs=observable_expression(problem['observable'])
    replace={}
    for atom in obs.atoms(H):
        j=s.expand(atom.args[0]-n)
        if not j.is_Integer or j<0:raise ValueError('unsupported_structure: nonnegative observable shifts required')
        row=iterate_row(s.eye(M.rows)[0,:],M,int(j))
        replace[atom]=(row*s.Matrix(u))[0]
    row=observable_row(obs.xreplace(replace),u,powers)
    if row.has(n,k,Poch) or any(v.has(s.Float) or not v.is_rational_function() for v in row):
        raise ValueError('unsupported_structure: closure coefficients must be rational in Q and parameters')
    forcing=observable_row(((M*s.Matrix(u))[0])**problem['degree'],u,powers)
    rel=forced_relation(T,row,forcing,max_order=getattr(budget,'max_order',4))
    if rel.get('status')=='search_exhausted':return {'construction':rel,'definition_search':zr}
    return {'construction':{'status':'constructed','algorithm':'q-Ore polynomial closure and elimination',
        'base_recurrence':z,'companion':[[str(v) for v in M.row(i)] for i in range(M.rows)],
        'transition':[[str(v) for v in T.row(i)] for i in range(T.rows)],
        'state_powers':powers,'observable_row':list(map(str,row)),
        'observable_operator':eliminate(T,row),'forcing_operator':eliminate(T,forcing),
        'forced_relation':rel,'definition_target_used_in_search':False,
        'observable_used_for_closure':True,'rhs_weight_used_in_search':False},'definition_search':zr}


def parse_model(model):
    symbols={v:s.Symbol(v) for v in model['names'].values()}
    symbols.update(n=n,k=k,q=q,Q=Q,Poch=Poch,Sequence=H)
    return {a:s.sympify(model[a],locals=symbols) for a in ('observable','prefactor','kernel')}


def nat_text(e,mapping):
    e=s.expand(e);positive=[];negative=[]
    for t in sorted(s.Add.make_args(e),key=lambda v:(not v.has(n,k),str(v))):
        neg=t.could_extract_minus_sign();v=-t if neg else t
        if v.is_Integer:text=str(v)
        elif v.is_Symbol:text=mapping[str(v)]
        else:raise ValueError('representation_gap: unsupported natural index '+str(e))
        (negative if neg else positive).append(text)
    return '('+(' + '.join(positive) or '0')+''.join(' - '+a for a in negative)+')'


def field_text(e,mapping,sequence):
    if e.is_Integer:return f'({e})'
    if e.is_Symbol:return mapping[str(e)]
    if e.func==H:return f'({sequence} {nat_text(e.args[0],mapping)})'
    if e.func==Poch:
        return f'(poch {field_text(e.args[0],mapping,sequence)} {field_text(e.args[1],mapping,sequence)} {nat_text(e.args[2],mapping)})'
    if e.is_Add or e.is_Mul:
        return '('+(' + ' if e.is_Add else ' * ').join(field_text(a,mapping,sequence) for a in e.args)+')'
    if e.is_Pow:
        a,b=e.args;at=field_text(a,mapping,sequence)
        if b.is_Integer:return f'({at}^{b})' if b>=0 else f'({at}^{-b})⁻¹'
        return f'({at}^{nat_text(b,mapping)})'
    raise ValueError('representation_gap: cannot print '+str(e))


def emit(model,construction):
    if model.get('mode') in ('defined_linear_relation','defined_closed_form','defined_parameter_relation'):
        from defined_relation import emit as emit_relation
        return emit_relation(model,construction)
    from expressions import expression,shift_ratio,rationalize,X
    z=construction['base_recurrence'];rel=construction['forced_relation']
    if z['order']!=2 or rel['order']!=1:raise ValueError('representation_gap: current native Ore exit needs second-order object and first-order forced relation')
    # Recompute all closure witnesses instead of trusting a stored recurrence.
    F=expression(model['definition_model']['summand_formula'])
    symbols={str(v):v for v in F.free_symbols|{q,Q,X}}
    R=s.sympify(z['certificate'],locals=symbols)
    cc=[s.sympify(c,locals=symbols) for c in z['coefficients']]
    U=rationalize(shift_ratio(F,k));V=rationalize(shift_ratio(F,n))
    if s.cancel(U*R.subs(X,q*X)-R-cc[0]-cc[1]*V-cc[2]*V*V.subs(Q,q*Q))!=0:
        raise ValueError('invalid_certificate: base object recurrence')
    M=companion([s.sympify(c,locals={'q':q,'Q':Q}) for c in z['coefficients']])
    T,powers,u=polynomial_closure(M,2)
    obs=parse_model(model)['observable']
    mapping={v:a for a,v in model['names'].items()}
    base,index=model['base'],model['index'];seq=f'rogersSzego {model["parameter"]} {base}'
    def text(e,i='om',j='oj'):
        mm=dict(mapping,n=i,k=j,Q=f'({base}^{i})')
        return field_text(s.sympify(e,locals={'n':n,'k':k,'q':q,'Q':Q,'Sequence':H,'Poch':Poch}),mm,seq)
    repl={a:(iterate_row(s.eye(2)[0,:],M,int(s.expand(a.args[0]-n)))*s.Matrix(u))[0] for a in obs.atoms(H)}
    drow=observable_row(obs.xreplace(repl),u,powers);forcing=observable_row(u[1]**2,u,powers)
    if s.Matrix([[s.sympify(v,locals={'q':q,'Q':Q}) for v in row] for row in construction['companion']])!=M or s.Matrix([[s.sympify(v,locals={'q':q,'Q':Q}) for v in row] for row in construction['transition']])!=T:
        raise ValueError('invalid_certificate: state transition')
    for name,row in [('observable_operator',drow),('forcing_operator',forcing)]:
        op=construction[name]
        rows=[iterate_row(row,T,j) for j in range(len(op['coefficients']))]
        cs_op=[s.sympify(c,locals={'q':q,'Q':Q}) for c in op['coefficients']]
        if not cs_op or cs_op[-1]==0 or sum((a*v for a,v in zip(cs_op,rows)),s.zeros(1,T.rows)).applyfunc(s.cancel)!=s.zeros(1,T.rows):
            raise ValueError('invalid_certificate: '+name)

    cs=[s.sympify(c,locals={'q':q,'Q':Q}) for c in rel['coefficients']];b=s.sympify(rel['forcing_coefficient'],locals={'q':q,'Q':Q})
    if cs[-1]!=1 or (iterate_row(drow,T,1)+cs[0]*drow-b*forcing).applyfunc(s.cancel)!=s.zeros(1,T.rows):
        raise ValueError('invalid_certificate: Ore closure relation')
    # zemit independently checks the base certificate and produces its local proof.
    zproof,zplan=zemit(model['definition_model'],z,recurrence_only=True)
    c0,c1=[text(c,index) for c in z['coefficients'][:2]]
    data=parse_model(model)
    alpha=text(-cs[0]);beta=text(b)
    rec=f'''  have orec : ∀ {index} : ℕ,
      {seq} ({index}+2) + ({c0} * {seq} {index} + {c1} * {seq} ({index}+1)) = 0 := by
    intro {index}
    unfold rogersSzego
'''+''.join('  '+line+'\n' for line in zproof.splitlines())
    rec+=f'''  have ostep : ∀ {index} : ℕ, {seq} ({index}+2) =
      -{c0} * {seq} {index} - {c1} * {seq} ({index}+1) := by
    intro {index}
    linear_combination orec {index}
  let OD := fun om : ℕ => {text(data['observable'])}
  let OP := fun om : ℕ => {text(data['prefactor'])}
  let OW := fun om oj : ℕ => {text(data['kernel'])}
  let OA := fun om : ℕ => {alpha}
  let OB := fun om : ℕ => {beta}
  let OS := fun om : ℕ => OP om * (∑ oj ∈ Finset.range (om+1), OW om oj * ({seq} oj)^2)
  have hd : ∀ om, OD (om+1) = OA om*OD om + OB om*({seq} (om+1))^2 := by
    intro om
    dsimp only [OD, OA, OB]
    simp only [Nat.add_assoc]
    rw [ostep (om+1), ostep om]
    simp only [pow_succ]
    ring
  have ohq : regular {base} := by assumption
  have onz : ∀ j, poch {base} {base} j ≠ 0 := FiniteQP1.regular_poch_ne {base} ohq
  have hs : ∀ om, OS (om+1) = OA om*OS om + OB om*({seq} (om+1))^2 := by
    intro om
    apply FiniteQP1.triangular_recurrence (fun j => ({seq} j)^2) OP OW OA OB
    · intro om oj hj
      dsimp only [OP, OW, OA]
      have he : om+1+1-oj = (om+1-oj)+1 := by omega
      simp only [he, poch_succ, pow_succ]
      ring
    · intro om
      dsimp only [OP, OW, OB]
      have hp := onz (om+1)
      simp only [Nat.add_sub_cancel_left, Nat.add_sub_cancel, pow_zero, pow_one]
      field_simp
      <;> simp only [pow_succ]
      <;> ring
  have oe : ∀ om, OD om = OS om := by
    intro om
    induction om with
    | zero =>
      norm_num [OD, OS, OP, OW, rogersSzego, gaussian, poch, Finset.sum_range_succ]
      <;> ring
    | succ om ih => rw [hd, hs, ih]
  have ohn : 1 ≤ {index} := by assumption
  obtain ⟨om, he⟩ : ∃ om, {index} = om+1 := ⟨{index}-1, by omega⟩
  subst {index}
  simp only [pochList_cons, pochList_nil, mul_one, Nat.add_sub_cancel] at *
  rw [show {seq} (om+1+1) = {seq} (om+2) by congr 1]
  calc
    _ = OD om := by dsimp [OD]; ring
    _ = OS om := oe om
    _ = _ := by
      dsimp only [OS, OP, OW]
      rw [← FiniteQP1.sum_Icc_reverse (fun oj => {text(data['kernel'])} * ({seq} oj)^2) om]
      apply congrArg₂ (fun a b => a*b)
      · ring
      · apply Finset.sum_congr rfl
        intro oj hj
        simp only [Finset.mem_Icc] at hj
        have he : om+1-(om+1-oj) = oj := by omega
        have hez : ((om+1 : ℕ) : ℤ)-(oj : ℤ) = ((om+1-oj : ℕ) : ℤ) := by omega
        simp only [he, hez, zpow_natCast]
        ring
'''
    return rec,{'base_recurrence_verification':zplan,'forced_relation':rel,
                'boundary':'actual triangular kernel and finite Icc reindexing',
                'closure_witness_verified':True}


def synthesize(source,model,construction,work,env):
    proof,plan=emit(model,construction)
    return verify_proof(source,proof,plan,work,env,[(HERE/'lean/OreRules.lean').read_text()])
