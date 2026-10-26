import Benchmark.StructuralAtoms
import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.SimpRw
import Mathlib.LinearAlgebra.Matrix.Notation

open scoped BigOperators
namespace FiniteQSpectral
/-- Discrete weighted self-adjointness, with all endpoints present in the finite matrix. -/
theorem balance {K I : Type*} [CommRing K] [Fintype I]
    (w : I → K) (A : I → I → K) (f g : I → K)
    (h : ∀ i j, w i * A i j = w j * A j i) :
    (∑ i, w i * (∑ j, A i j * f j) * g i) =
    ∑ i, w i * f i * (∑ j, A i j * g j) := by
  simp_rw [Finset.mul_sum, Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  calc
    w j * (A j i * f i) * g j = (w j * A j i) * f i * g j := by ring
    _ = (w i * A i j) * f i * g j := by rw [h j i]
    _ = w i * f i * (A i j * g j) := by ring

/-- Spectral separation is required; no positivity or characteristic-zero assumption. -/
theorem orthogonal {K I : Type*} [Field K] [Fintype I]
    (w : I → K) (A : I → I → K) (f g : I → K) (l m : K)
    (hb : ∀ i j, w i * A i j = w j * A j i)
    (hf : ∀ i, ∑ j, A i j * f j = l * f i)
    (hg : ∀ i, ∑ j, A i j * g j = m * g i)
    (hs : l ≠ m) : (∑ i, w i * f i * g i) = 0 := by
  have h := balance w A f g hb
  simp_rw [hf, hg] at h
  have h1 : (∑ i, w i * (l * f i) * g i) = l * (∑ i, w i * f i * g i) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i hi
    ring
  have h2 : (∑ i, w i * f i * (m * g i)) = m * (∑ i, w i * f i * g i) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i hi
    ring
  rw [h1,h2] at h
  apply (mul_eq_zero.mp (show (l-m)*(∑ i, w i*f i*g i)=0 by linear_combination h)).resolve_left
  exact sub_ne_zero.mpr hs
/-- Norms are separate obligations; spectral orthogonality alone never supplies them. -/
theorem orthogonal_family {K I J : Type*} [Field K] [Fintype I] [DecidableEq J]
    (w : I → K) (A : I → I → K) (P : J → I → K) (eigen norm : J → K)
    (m n : J) (hb : ∀ i j, w i*A i j = w j*A j i)
    (he : ∀ t i, ∑ j, A i j * P t j = eigen t * P t i)
    (hinj : Function.Injective eigen)
    (hn : ∀ t, ∑ i, w i*P t i*P t i = norm t) :
    (∑ i, w i*P m i*P n i) = if m=n then norm n else 0 := by
  by_cases h : m=n
  · subst m
    simpa using hn n
  · simp only [if_neg h]
    exact orthogonal w A (P m) (P n) (eigen m) (eigen n) hb (he m) (he n)
      (fun hh => h (hinj hh))
end FiniteQSpectral

open Lean Meta Elab Tactic
/-- Enumerate actual local operator/eigenvalue terms; no identity-name dispatch. -/
elab "spectral_certificate" : tactic => do
  let (operators, scalars, functions) ← withMainContext do
    let target ← getMainTarget
    unless target.isAppOfArity ``Eq 3 do throwError "scalar equality required"
    let carrier := target.getAppArgs[0]!
    let mut ops : Array Name := #[]
    let mut vals : Array Name := #[]
    let mut fns : Array Name := #[]
    for d in ← getLCtx do
      unless d.isImplementationDetail do
        if ← isDefEq d.type carrier then vals := vals.push d.userName
        let isOperator ← forallTelescopeReducing d.type fun xs ty => do
          if xs.size != 2 then return false
          isDefEq ty carrier
        if isOperator then ops := ops.push d.userName
        let isFunction ← forallTelescopeReducing d.type fun xs ty => do
          if xs.size != 1 then return false
          isDefEq ty carrier
        if isFunction then fns := fns.push d.userName
    pure (ops, vals, fns)
  for a in operators do
    for e in functions do
      let state ← saveState
      try
        evalTactic (← `(tactic| (apply FiniteQSpectral.orthogonal_family (A := $(mkIdent a)) (eigen := $(mkIdent e)) <;> assumption)))
        if (← getGoals).isEmpty then return
        state.restore
      catch _ => state.restore
    for l in scalars do
      for m in scalars do
        let state ← saveState
        try
          evalTactic (← `(tactic| (
            apply FiniteQSpectral.orthogonal (A := $(mkIdent a)) (l := $(mkIdent l)) (m := $(mkIdent m))
            all_goals
              first
              | assumption
              | (intro i; fin_cases i <;> (try (intro j; fin_cases j)) <;> simp_all [Fin.sum_univ_succ] <;> ring)
              | (intros; simp_all [Fin.sum_univ_succ] <;> ring))))
          if (← getGoals).isEmpty then return
          state.restore
        catch _ => state.restore
  throwError "spectral obligations unresolved: operator, balance, eigenrelations or separated eigenvalues"
