import Benchmark.DifferenceAtoms
import Mathlib.Tactic

namespace FiniteQDifference
open scoped BigOperators
open FiniteQBenchmark

/-- Evaluation of a constructed difference-field antidifference, including both endpoints. -/
theorem telescope {K : Type*} [CommRing K] (G : ℕ → K) (m : ℕ) :
    (∑ k ∈ Finset.range m, (G (k+1)-G k)) = G m-G 0 := by
  induction m with
  | zero => simp
  | succ m ih => rw [Finset.sum_range_succ, ih]; ring

/-- Evaluation intertwines the product extension with the shift. -/
theorem poch_shift {K : Type*} [CommRing K] (a q : K) (n : ℕ) :
    poch a q (n+1) = poch a q n * (1-a*q^n) := by
  exact Finset.prod_range_succ _ _

theorem poch_initial {K : Type*} [CommRing K] (a q : K) : poch a q 0 = 1 := by
  simp [poch]

end FiniteQDifference

open Lean Meta Elab Tactic
/-- Split actual conjunction hypotheses so denominator proofs can use them. -/
elab "dr_split_hypotheses" : tactic => do
  let mut found := true
  while found do
    found ← withMainContext do
      for decl in ← getLCtx do
        if !decl.isImplementationDetail && decl.type.isAppOfArity ``And 2 then
          evalTactic (← `(tactic| obtain ⟨_, _⟩ := $(mkIdent decl.userName)))
          evalTactic (← `(tactic| try clear $(mkIdent decl.userName)))
          return true
      return false

/-- Stable printable names for reconstruction after induction creates inaccessible locals. -/
elab "dr_name_locals" : tactic => do
  let mut goal ← getMainGoal
  let ids ← goal.withContext do
    let mut ids : Array FVarId := #[]
    for decl in ← getLCtx do
      unless decl.isImplementationDetail do ids := ids.push decl.fvarId
    pure ids
  for i in [:ids.size] do
    goal ← goal.rename ids[i]! (Name.mkSimple ("dr_v" ++ toString i))
  replaceMainGoal [goal]

/-- Leave polynomial towers intact for CAS reduction. For rational expressions,
    all original nonzero hypotheses are explicit simplifier inputs. -/
elab "dr_clear_denominators" : tactic => withMainContext do
  let target ← getMainTarget
  if (target.find? fun e => e.isAppOf ``HDiv.hDiv || e.isAppOf ``Inv.inv).isSome then
    evalTactic (← `(tactic| try simp only [← mul_assoc] at *))
    evalTactic (← `(tactic| try field_simp [*]))

macro "dr_expand" : tactic => `(tactic|
  try simp only [FiniteQBenchmark.fineC, FiniteQBenchmark.pochList,
    List.map_cons, List.map_nil, List.prod_cons, List.prod_nil, mul_one] at *)

/-- The primitive shift laws come from evaluation, not independent assumptions.
    Parameter-dependent denominators are cleared only by kernel-checked tactics. -/
macro "dr_shift" : tactic => `(tactic|
  (try simp only [FiniteQDifference.poch_shift, FiniteQDifference.poch_initial,
    Finset.sum_range_succ, Finset.prod_range_succ,
    Finset.sum_range_zero, Finset.prod_range_zero, pow_succ, pow_zero,
    Nat.cast_add, Nat.cast_one, Nat.cast_zero, Nat.cast_succ] at *)
  <;> (try simp only [ne_eq, mul_eq_zero, not_or, mul_assoc, mul_left_comm, mul_comm] at *)
  <;> dr_split_hypotheses
  <;> dr_name_locals
  <;> dr_clear_denominators
  <;> (try simp only [zero_add, add_zero, one_mul, mul_one, zero_mul, mul_zero] at *))
