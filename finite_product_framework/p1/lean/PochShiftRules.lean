import Benchmark.P1Atoms
import Mathlib.Tactic

namespace FiniteQShift
open FiniteQBenchmark
open scoped BigOperators
variable {K : Type*} [Field K]

/-- Division-free splitting; valid even when a factor vanishes. -/
theorem split (a q : K) (m n : ℕ) :
    poch a q (m+n) = poch a q m * poch (a*q^m) q n := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Nat.add_succ, poch_succ, ih, poch_succ, pow_add]
    ring

/-- Parameter shifts retain the prefix multiplier, including at singular points. -/
theorem shift_cross (a q : K) (d k : ℕ) :
    poch (a*q^d) q k * poch a q d =
      poch a q k * poch (a*q^k) q d := by
  rw [mul_comm, ← split, Nat.add_comm, split]

theorem shift (a q : K) (d k : ℕ) (hd : poch a q d ≠ 0) :
    poch (a*q^d) q k = poch a q k * poch (a*q^k) q d / poch a q d := by
  exact (eq_div_iff hd).2 (shift_cross a q d k)

/-- Normalize overlapping intervals without dividing by any product factor. -/
theorem interval (a b q : K) (l d m e : ℕ)
    (hlen : l = d+m+e) (harg : a*q^d = b) :
    poch a q l = poch a q d * poch b q m * poch (b*q^m) q e := by
  rw [hlen, split a q (d+m) e, split a q d m, pow_add]
  rw [← mul_assoc a, harg]

theorem factor_ne (a q : K) (i n : ℕ) (hi : i < n)
    (h : poch a q n ≠ 0) : 1-a*q^i ≠ 0 := by
  exact (Finset.prod_ne_zero_iff.mp h) i (Finset.mem_range.mpr hi)

theorem prefix_ne (a q : K) (m n : ℕ) (hm : m ≤ n)
    (h : poch a q n ≠ 0) : poch a q m ≠ 0 := by
  rw [show n = m+(n-m) by omega, split] at h
  exact (mul_ne_zero_iff.mp h).1

theorem shifted_ne (a q : K) (d k N : ℕ) (hdk : d+k ≤ N)
    (h : poch a q N ≠ 0) : poch (a*q^d) q k ≠ 0 := by
  have hp := prefix_ne a q (d+k) N hdk h
  rw [split] at hp
  exact (mul_ne_zero_iff.mp hp).2

/-- Every denominator in a literal phi list is available at every valid prefix. -/
theorem phi_den (bs : List K) (q : K) (N k : ℕ)
    (h : phiDefined bs q N) (hk : k ≤ N) :
    poch q q k ≠ 0 ∧ pochList bs q k ≠ 0 := by
  exact mul_ne_zero_iff.mp (h k hk)

theorem phi_den_mono (bs : List K) (q : K) (N m : ℕ)
    (h : phiDefined bs q N) (hm : m ≤ N) : phiDefined bs q m := by
  intro k hk
  exact h k (by omega)

/-- The shifted-flux convention evaluates only actual in-support terms. -/
def backwardFlux (B : ℕ → K) (F : ℕ → K) : ℕ → K
  | 0 => 0
  | k+1 => B k * F k

@[simp] theorem backwardFlux_zero (B F : ℕ → K) : backwardFlux B F 0 = 0 := rfl
@[simp] theorem backwardFlux_succ (B F : ℕ → K) (k : ℕ) :
    backwardFlux B F (k+1) = B k * F k := rfl

end FiniteQShift

open Lean Elab Tactic

/-- Optional evidence must fail transactionally, including term elaboration;
an unresolved premise must never enter the context as a recovered sorry. -/
elab "poch_try" seq:tacticSeq : tactic => do
  let state ← saveState
  let hadErrors := (← getThe Core.State).messages.hasErrors
  try
    Term.withoutErrToSorry <| withoutRecover do
      evalTacticSeq seq
      Term.synthesizeSyntheticMVarsNoPostponing
      if !hadErrors && (← getThe Core.State).messages.hasErrors then
        state.restore
  catch _ => state.restore

/-- Instantiate finite-domain premises only at indices whose bounds can be
proved in the current branch. No regularity assumption is introduced. -/
elab "poch_domain_at " idx:term : tactic => withMainContext do
  try
    let value ← Term.withoutErrToSorry do
      let value ← Term.elabTerm idx (some (mkConst ``Nat))
      Term.synthesizeSyntheticMVarsNoPostponing
      instantiateMVars value
    if value.hasMVar || value.hasSorry then return
  catch _ => return
  let ctx ← getLCtx
  for decl in ctx do
    if !decl.isImplementationDetail && decl.type.isForall && (← Meta.isProp decl.type) then
      let h := mkIdent decl.userName
      let fact := mkIdent (← Meta.getUnusedUserName `ptFullDomain)
      let state ← saveState
      try
        Term.withoutErrToSorry <| withoutRecover <| evalTactic (← `(tactic|
          have $fact := $h $idx (by first | omega | (simp only [Finset.mem_range]; omega))))
        let code := "simp only [FiniteQBenchmark.pochList_cons, FiniteQBenchmark.pochList_nil, " ++
          "one_mul, mul_one, mul_ne_zero_iff] at " ++ fact.getId.toString
        evalTactic (← ofExcept (Parser.runParserCategory (← getEnv) `tactic code))
      catch _ => state.restore

/-- Transport the products occurring in the goal from actual nonzero longer
prefixes. Both base/parameter equality and the prefix bound are checked. -/
elab "poch_prefix_facts" : tactic => withMainContext do
  let collected ← IO.mkRef (#[] : Array Expr)
  (← getMainTarget).forEach fun e => do
    if e.isAppOf ``FiniteQBenchmark.poch then
      collected.modify fun xs => if xs.contains e then xs else xs.push e
  let mut pending : Array Expr := #[]
  for decl in (← getLCtx) do
    if ← Meta.isProp decl.type then pending := pending.push (mkFVar decl.fvarId)
  let mut sources : Array Expr := #[]
  while !pending.isEmpty do
    let proof := pending.back!
    pending := pending.pop
    let type ← Meta.inferType proof
    if type.isAppOf ``And then
      pending := pending.push (← Meta.mkAppM ``And.left #[proof])
      pending := pending.push (← Meta.mkAppM ``And.right #[proof])
    else if type.isAppOf ``Ne then
      sources := sources.push proof
  for atom in (← collected.get) do
    let xs := atom.getAppArgs
    if xs.size != 5 then continue
    for source in sources do
      let state ← saveState
      try
        let t ← Meta.inferType source
        let ys := t.getAppArgs[1]!.getAppArgs
        unless t.getAppArgs[1]!.isAppOf ``FiniteQBenchmark.poch && ys.size == 5 do continue
        unless ← Meta.isDefEq xs[2]! ys[2]! do continue
        unless ← Meta.isDefEq xs[3]! ys[3]! do continue
        let bound ← Meta.mkAppM ``LE.le #[xs[4]!, ys[4]!]
        let obligation ← Meta.mkFreshExprSyntheticOpaqueMVar bound
        let goal ← getMainGoal
        setGoals [obligation.mvarId!]
        evalTactic (← `(tactic| omega))
        unless (← getGoals).isEmpty do throwError "prefix bound unproved"
        setGoals [goal]
        let proof ← Meta.mkAppM ``FiniteQShift.prefix_ne
          #[xs[2]!, xs[3]!, xs[4]!, ys[4]!, obligation, source]
        let name ← Meta.getUnusedUserName `ptAtomPrefix
        let g ← goal.assert name (← Meta.inferType proof) proof
        let (_, g) ← g.intro1P
        replaceMainGoal [g]
        break
      catch _ => state.restore

/-- Drop already-expanded auxiliary sequence definitions before normalizing
local rational identities. This avoids rewriting entire recurrences at each
power abstraction. Dependencies still used by the goal cannot be cleared. -/
elab "poch_clear_context" : tactic => withMainContext do
  let declarations := (← getLCtx).foldl (init := (#[] : Array LocalDecl)) fun ds d => ds.push d
  for decl in declarations.reverse do
    let name := decl.userName.toString
    if name == "psC" || name == "psTelescoping" || name.startsWith "psSource" ||
        #["psS0", "psS1", "psF0", "psF1", "psB0", "psB1", "psG0", "psG1",
          "psH0", "psH1"].contains name then
      try
        replaceMainGoal [← (← getMainGoal).clear decl.fvarId]
      catch _ => pure ()

/-- Normalize rational product parameters before interval rewriting, without
cross-multiplying all denominators of the surrounding summation identity. -/
elab "poch_normalize_arguments" : tactic => withMainContext do
  let collected ← IO.mkRef (#[] : Array Expr)
  (← getMainTarget).forEach fun e => do
    if e.isAppOf ``FiniteQBenchmark.poch then
      let xs := e.getAppArgs
      if xs.size == 5 then
        let a := xs[2]!
        collected.modify fun xs => if xs.contains a then xs else xs.push a
  let args ← collected.get
  let disch ← Mathlib.Tactic.FieldSimp.parseDischarger none none
  let mut names : Array String := #[]
  for a in args do
    try
      let result ← Mathlib.Tactic.AtomM.run .reducible
        (Mathlib.Tactic.FieldSimp.reduceExpr disch a)
      if result.expr != a then
        let proof ← result.getProof
        let name := "paArgument" ++ toString names.size
        let g ← (← getMainGoal).assert (Name.mkSimple name) (← Meta.inferType proof) proof
        let (_, g) ← g.intro1P
        replaceMainGoal [g]
        names := names.push name
    catch _ => pure ()
  if !names.isEmpty then
    let code := "try simp only [" ++ String.intercalate ", " names.toList ++ "]"
    evalTactic (← ofExcept (Parser.runParserCategory (← getEnv) `tactic code))

/-- Normalize only generated domain facts, not whole recursive sum hypotheses. -/
private def normalizePochFacts (includeTarget : Bool) : TacticM Unit := withMainContext do
  let existing := (← getLCtx).foldl (init := (#[] : Array Name)) fun names decl =>
    names.push decl.userName
  for decl in (← getLCtx) do
    let name := decl.userName.toString
    if (name.startsWith "ptScalar" || name.startsWith "ptComposite" || name.startsWith "ptSplit") &&
        !name.endsWith "Neg" && !existing.contains (Name.mkSimple (name ++ "Neg")) then
      let h := mkIdent decl.userName
      let hn := mkIdent (Name.mkSimple (name ++ "Neg"))
      evalTactic (← `(tactic| have $hn := neg_ne_zero.mpr $h))
  let ctx := (← (← getMainGoal).getDecl).lctx
  let mut names : Array String := #[]
  for decl in ctx do
    let name := decl.userName.toString
    if name.startsWith "pd" || name.startsWith "pt" then
      names := names.push name
  if names.isEmpty && !includeTarget then return
  let code := "ring_nf (ifUnchanged := .silent) at " ++ String.intercalate " " names.toList ++
    (if includeTarget then " ⊢" else "")
  let stx ← ofExcept (Parser.runParserCategory (← getEnv) `tactic code)
  evalTactic stx

elab "poch_normalize_facts" : tactic => normalizePochFacts true

/-- Prepare domain evidence once, without normalizing the large target. -/
elab "poch_prepare_facts" : tactic => normalizePochFacts false

elab "poch_normalize_powers" : tactic => withMainContext do
  let ctx ← getLCtx
  let mut names : Array String := #[]
  for decl in ctx do
    let name := decl.userName.toString
    if name.startsWith "pd" || name.startsWith "pt" then
      names := names.push name
  let code := "try simp only [inv_pow, pow_mul, pow_add, pow_succ, pow_zero, pow_one, mul_pow, div_eq_mul_inv, mul_inv_rev, inv_inv, one_mul, mul_one] at " ++
    String.intercalate " " names.toList ++ " ⊢"
  let stx ← ofExcept (Parser.runParserCategory (← getEnv) `tactic code)
  evalTactic stx


/-- Orient constant inner powers before abstracting q^n. -/
elab "poch_orient_powers" : tactic => withMainContext do
  let collected ← IO.mkRef (#[] : Array Expr)
  let scan := fun (target : Expr) => target.forEach fun e => do
    if e.isAppOf ``HPow.hPow then
      let xs := e.getAppArgs
      if xs.size == 6 then
        let inner := xs[4]!
        if inner.isAppOf ``HPow.hPow then
          let ys := inner.getAppArgs
          if ys.size == 6 then
            let m := ys[5]!
            let literal := m.isAppOf ``OfNat.ofNat || (match m with
              | .lit (.natVal _) => true
              | _ => false)
            if literal then
              collected.modify fun es => if es.contains e then es else es.push e
  scan (← getMainTarget)
  let mut locations : Array String := #[]
  for decl in (← getLCtx) do
    let name := decl.userName.toString
    if name.startsWith "pd" || name.startsWith "pt" then
      locations := locations.push name
      scan decl.type
  let mut names : Array String := #[]
  for e in (← collected.get) do
    try
      let xs := e.getAppArgs
      let ys := xs[4]!.getAppArgs
      let proof ← Meta.mkAppM ``pow_right_comm #[ys[4]!, ys[5]!, xs[5]!]
      let name := "paPower" ++ toString names.size
      let g ← (← getMainGoal).assert (Name.mkSimple name) (← Meta.inferType proof) proof
      let (_, g) ← g.intro1P
      replaceMainGoal [g]
      names := names.push name
    catch _ => pure ()
  if !names.isEmpty then
    let code := "try simp only [" ++ String.intercalate ", " names.toList ++ "] at " ++
      String.intercalate " " locations.toList ++ " ⊢"
    evalTactic (← ofExcept (Parser.runParserCategory (← getEnv) `tactic code))

/-- Transport product nonzero evidence through the same interval rewrites as
used for the target; keep every factor of a split denominator available. -/
elab "poch_rewrite_facts" "[" rules:ident,* "]" : tactic => withMainContext do
  let mut names : Array String := #[]
  for decl in (← getLCtx) do
    let name := decl.userName.toString
    if name.startsWith "pdFull" || name.startsWith "pdPrefix" ||
        name.startsWith "ptAtom" || name.startsWith "ptFull" ||
        name.startsWith "ptForFactor" then
      names := names.push name
  if !names.isEmpty then
    let where_ := String.intercalate " " names.toList
    let norm := "ring_nf (ifUnchanged := .silent) at " ++ where_
    evalTactic (← ofExcept (Parser.runParserCategory (← getEnv) `tactic norm))
    let lemmas := rules.getElems.toList.map fun r => r.getId.toString
    let code := "try simp only [" ++ String.intercalate ", " (lemmas ++ ["mul_ne_zero_iff"]) ++
      "] at " ++ where_
    evalTactic (← ofExcept (Parser.runParserCategory (← getEnv) `tactic code))
    -- Expose conjuncts once. The field simplifier can then use each nonzero
    -- proof directly instead of repeatedly searching a large logical context.
    if (← getGoals).isEmpty then return
    withMainContext do
      let ctx ← getLCtx
      let mut pending : Array Expr := #[]
      let mut used : Array Name := #[]
      for decl in ctx do
        used := used.push decl.userName
        if names.contains decl.userName.toString && decl.type.isAppOf ``And then
          pending := pending.push (mkFVar decl.fvarId)
      let mut index := 0
      while !pending.isEmpty do
        let proof := pending.back!
        pending := pending.pop
        let type ← Meta.inferType proof
        if type.isAppOf ``And then
          pending := pending.push (← Meta.mkAppM ``And.left #[proof])
          pending := pending.push (← Meta.mkAppM ``And.right #[proof])
        else
          while used.contains (Name.mkSimple ("ptSplit" ++ toString index)) do
            index := index + 1
          let name := Name.mkSimple ("ptSplit" ++ toString index)
          index := index + 1
          let g ← (← getMainGoal).assert name type proof
          let (_, g) ← g.intro1P
          replaceMainGoal [g]

/-- Supply only nonzero premises to denominator simplification. In particular,
do not unfold the complete recurrence hypotheses while checking a local term. -/
elab "poch_rewrite_all_facts" : tactic => withMainContext do
  let mut names : Array String := #[]
  for decl in (← getLCtx) do
    let name := decl.userName.toString
    if name.startsWith "pcNorm" || name.startsWith "pcAtom" || name.startsWith "pcShort" then
      names := names.push name
  let code := "poch_rewrite_facts [" ++ String.intercalate ", " names.toList ++ "]"
  evalTactic (← ofExcept (Parser.runParserCategory (← getEnv) `tactic code))

elab "poch_clear_denominators" : tactic => withMainContext do
  -- Interval equalities have already rewritten the target. Do not let the
  -- discharger revisit their large or universally quantified product terms.
  let declarations := (← getLCtx).foldl (init := (#[] : Array LocalDecl)) fun ds d => ds.push d
  for decl in declarations.reverse do
    let name := decl.userName.toString
    if name.startsWith "pcNorm" || name.startsWith "pcAtom" || name.startsWith "pcShort" then
      try
        replaceMainGoal [← (← getMainGoal).clear decl.fvarId]
      catch _ => pure ()
  evalTactic (← `(tactic| try field_simp (disch := first
    | field_simp_discharge
    | (poch_normalize_facts; first | assumption | tauto))))
