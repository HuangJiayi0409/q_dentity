"""Native q-Zeilberger frontend and certificate-driven, restricted Lean emitter.

Symbolic search supports general bounded order. The new native verifier initially
handles monic order two with a geometric Gaussian weight and polynomial flux
on row n+1; unsupported witnesses remain explicit domain/representation gaps.
"""
import sympy as s
from expressions import expression, shift_ratio, rationalize, n, k, q, Q, X
from lean_pipeline import (frontend as first_frontend, lean_expression, polynomial_lean,
                           find_nodes, verify_proof)


def frontend(raw, identity):
    if raw['op'] != 'Eq':
        raise ValueError('unsupported_structure: Zeilberger requires an equality')
    lhs, rhs = raw['args']
    reversed_equality = rhs['op'] == 'Finset.sum'
    if reversed_equality:
        lhs, rhs = rhs, lhs
    # The target is retained verbatim, never passed to the search backend.
    formula, model = first_frontend({'op': 'Eq', 'args': [lhs, {'op':'nat','value':1}]}, identity)
    del formula['target']
    model.update(target=rhs, reversed_equality=reversed_equality,
                 summand_formula=formula['summand'])
    lean_expression(rhs)  # Fail explicitly if target printing is unsupported.
    return formula, model


def emit_proof(model, construction, recurrence_only=False):
    order = construction['order']
    if order == 1:
        from lean_pipeline import emit_proof as first_emit
        F = expression(model['summand_formula'])
        symbols = {str(t):t for t in F.free_symbols | {q,Q,X}}
        c = [s.sympify(t,locals=symbols) for t in construction['coefficients']]
        if len(c) != 2 or c[-1] != 1:
            raise ValueError('domain_unresolved: monic recurrence required')
        shifts = {'n_shift':rationalize(shift_ratio(F,n)),
                  'k_shift':rationalize(shift_ratio(F,k)), 'target_coefficient':-c[0]}
        proof,plan = first_emit(model,shifts,construction)
        plan.update(order=1, coefficients=list(map(str,c)), target_used_in_search=False)
        return proof,plan
    if order != 2:
        raise ValueError('representation_gap: native Zeilberger verifier currently supports orders one/two')
    weight = expression(model['weight_formula'])
    if weight.has(n):
        raise ValueError('representation_gap: order-two verifier requires n-independent weight')
    z = rationalize(shift_ratio(weight, k))
    if z.has(X, Q):
        raise ValueError('representation_gap: order-two verifier requires geometric weight')
    symbols = {str(t):t for t in weight.free_symbols | {q,Q,X}}
    coeff = [s.sympify(t, locals=symbols) for t in construction['coefficients']]
    if coeff[-1] != 1 or len(coeff) != 3:
        raise ValueError('domain_unresolved: monic order-two recurrence required')
    R = s.sympify(construction['certificate'], locals=symbols)
    Fsym = expression(['mul', model['weight_formula'], ['gaussian','q','n','k']])
    if s.cancel(expression(model['summand_formula'])-Fsym) != 0:
        raise ValueError('representation_gap: order-two verifier requires one Gaussian factor')
    U = rationalize(shift_ratio(Fsym,k))
    V = rationalize(shift_ratio(Fsym,n))
    gap = s.Symbol('Gap')
    flux = s.cancel((R.subs(X,q*X)*U/V).subs(Q,gap*X/q))
    # flux(X,Gap) times F(n+1,k), Gap=q^(n+1-k), is G(n,k+1).
    # Check polynomiality before any Lean generation, preserving q=0.
    mapping_probe = {str(a):str(a) for a in flux.free_symbols | set().union(*(c.free_symbols for c in coeff))}
    polynomial_lean(flux,mapping_probe)
    for c in coeff:
        polynomial_lean(c,mapping_probe)
    # Compute a polynomial multiplier of the generic Gaussian adjacent identity.
    A,B,C = s.symbols('AtomA AtomB AtomC')
    v0,v1 = [c.subs(Q,gap*X) for c in coeff[:2]]
    h0 = flux.subs(gap,q*gap)
    h1 = flux.subs(X,q*X)
    residual = s.expand(z*((1+v1-h1)*(q*X*A+B)+v0*A)+(z*q*gap+h0)*C)
    adj = (1-q*X)*A-(1-gap)*B
    witness = s.cancel(residual.coeff(B)/(-(1-gap)))
    if s.cancel(residual-witness*adj) != 0:
        raise ValueError('representation_gap: local relation requires a wider Gaussian verifier')
    names = model['names']
    used = set(names)
    def fresh(stem):
        while stem in used: stem += '_'
        used.add(stem)
        return stem
    i,j,F,G,T,Cn = [fresh(a) for a in ('zln','zlk','zlF','zlG','zlT','zlC')]
    base,index,binder = model['base'],model['index'],model['binder']
    mapping = {canonical:original for original,canonical in names.items()
               if canonical not in ('n','k','q')}
    mapping.update(q=base,Q=f'({base}^{i})',X=f'({base}^{j})',Gap=f'({base}^({i}+1-{j}))')
    ctexts = [polynomial_lean(c,mapping) for c in coeff[:2]]
    htext = polynomial_lean(flux,mapping)
    witness_map = dict(mapping, Gap=f'({base}^({i}-{j}))')
    wtext = lean_expression(model['weight_expression'],{binder:j})
    witness_text = polynomial_lean(witness,witness_map)
    ftext = lean_expression(model['summand'],{index:i,binder:j})
    ttext = lean_expression(model['target'],{index:i})
    orientation = '  symm\n' if model['reversed_equality'] else ''
    proof = orientation + f'''  let {F} := fun ({i} {j} : ℕ) => {ftext}
  let {T} := fun ({i} : ℕ) => {ttext}
  let {Cn} := fun ({i} j : ℕ) => if j = 0 then {ctexts[0]} else {ctexts[1]}
  let {G} := fun ({i} {j} : ℕ) => match {j} with
    | 0 => 0
    | {j}+1 => {htext} * {F} ({i}+1) {j}
  change (∑ {j} ∈ Finset.range ({index}+1), {F} {index} {j}) = {T} {index}
  have hsupport : ∀ n k, n < k → {F} n k = 0 := by
    intro n k hk
    simp [{F}, gaussian_above {base} hk]
  have hlocal : ∀ {i} {j}, {j} ∈ Finset.range ({i}+2+1) →
      {F} ({i}+2) {j} + (∑ a ∈ Finset.range 2, {Cn} {i} a * {F} ({i}+a) {j}) =
        {G} {i} ({j}+1) - {G} {i} {j} := by
    intro {i} {j} hmem
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, {Cn}, if_pos rfl,
      show ¬(1 : ℕ) = 0 by omega, if_false, Nat.add_zero, zero_add, ite_true, ite_false]
    cases {j} with
    | zero =>
      simp [{F}, {G}, gaussian_zero_right, pow_succ] <;> ring
    | succ {j} =>
      by_cases hle : {j} ≤ {i}
      · dsimp only [{F}, {G}]
        rw [FiniteQP1.gaussian_pascal {base} ({i}+1) {j} (by omega)]
        rw [show gaussian {base} ({i}+1) ({j}+1) =
          {base}^({j}+1)*gaussian {base} {i} ({j}+1) + gaussian {base} {i} {j} by rw [gaussian]; ring]
        have hp : {base}^{i} = {base}^{j} * {base}^({i}-{j}) := by
          rw [← pow_add, Nat.add_sub_of_le hle]
        have hadj := FiniteQP1.gaussian_adjacent {base} {i} {j} hle
        simp only [show {i}+1-({j}+1) = {i}-{j} by omega,
          show {i}+1-{j} = ({i}-{j})+1 by omega, pow_succ, hp] at hadj ⊢
        linear_combination ({witness_text} * {wtext}) * hadj
      · have he : {j} = {i}+1 := by simp only [Finset.mem_range] at hmem; omega
        subst {j}
        simp [{F}, {G}, gaussian_self, gaussian_above {base} (by omega : {i} < {i}+1+1),
          gaussian_above {base} (by omega : {i}+1 < {i}+1+1), pow_succ] <;> ring
  apply FiniteQP1.higher_order_unique 2 (by omega)
    (fun n => ∑ k ∈ Finset.range (n+1), {F} n k) {T} {Cn} (fun _ => 0)
    ?_ ?_ ?_ {index}
  · intro j hj
    have hc : j = 0 ∨ j = 1 := by omega
    rcases hc with rfl | rfl <;> norm_num [{F}, {T}, gaussian, poch, Finset.sum_range_succ]
  · intro {i}
    have h := FiniteQP1.telescoper_sum {F} {G} 2 {Cn} hsupport {i} (hlocal {i})
    have hb : {G} {i} ({i}+2+1) - {G} {i} 0 = 0 := by
      simp [{G}, {F}, gaussian_above {base} (by omega : {i}+1 < {i}+2)]
    simpa only [hb] using h
  · intro {i}
    dsimp only [{T}, {Cn}]
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add, Nat.add_zero,
      if_pos rfl, show ¬(1 : ℕ) = 0 by omega, if_false]
    have hm : {i} % 2 < 2 := Nat.mod_lt _ (by omega)
    have hcases : {i}%2 = 0 ∨ {i}%2 = 1 := by omega
    rcases hcases with he | he
    all_goals
      have hd : ({i}+2)/2 = {i}/2+1 := by omega
      have hp : {base}^{i} = ({base}^2)^({i}/2) * {base}^({i}%2) := by
        rw [← pow_mul, ← pow_add, Nat.div_add_mod]
      have hm0 : ({i}+2)%2 = {i}%2 := by omega
      have hm1 : ({i}+1)%2 = 1-{i}%2 := by omega
      have hd1 : ({i}+1)/2 = {i}/2+{i}%2 := by omega
      simp only [hm0, hm1, hd, hd1, he, Nat.reduceSub, Nat.reduceEqDiff,
        ite_true, ite_false, Nat.add_zero, poch_succ, pow_succ, hp]
      norm_num <;> ring
'''
    if recurrence_only:
        proof=proof.split('  apply FiniteQP1.higher_order_unique',1)[0]
        proof=proof.replace(f'  change (∑ {j} ∈ Finset.range ({index}+1), {F} {index} {j}) = {T} {index}\n','')
        proof+=f'''  have h := FiniteQP1.telescoper_sum {F} {G} 2 {Cn} hsupport {index} (hlocal {index})
  have hb : {G} {index} ({index}+2+1) - {G} {index} 0 = 0 := by
    simp [{G}, {F}, gaussian_above {base} (by omega : {index}+1 < {index}+2)]
  simp only [hb, {F}, {Cn}, Finset.sum_range_succ, Finset.sum_range_zero,
    Nat.add_zero, zero_add, add_zero, if_pos rfl, show ¬(1 : ℕ) = 0 by omega, if_false, ite_true, ite_false] at h ⊢
  linear_combination h
'''
    return proof, {'order':order, 'coefficients':list(map(str,coeff)),
                   'certificate':str(R), 'flux_multiplier':str(flux),
                   'flux_n_shift':1, 'flux_k_shift':-1,
                   'adjacent_witness':str(witness),
                   'boundary':'zero checked on largest support; no quotient evaluation',
                   'target_used_in_search':False}


def synthesize(source, model, construction, work, env):
    if model.get('mode')=='general_recurrence':
        from general_summation import synthesize as general_synthesize
        return general_synthesize(source,model,construction,work,env)
    proof,plan = emit_proof(model,construction)
    return verify_proof(source,proof,plan,work,env)
