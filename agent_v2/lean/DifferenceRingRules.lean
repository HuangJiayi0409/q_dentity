import Benchmark.Auxiliary
import Mathlib.Tactic.LinearCombination

/-! A source-derived evaluated product tower. The step relation is proved from
the actual finite product and original natural-index hypothesis before it is
used in the polynomial reduction. No relation is added to the original Γ. -/
namespace AgentV2DifferenceRing

universe u
variable {K : Type u} [CommRing K]

/-- Evaluation of the last product step at the original index `n - 1`. -/
theorem source_step (a q : K) (n : ℕ) (hn : 1 ≤ n) :
    FiniteQBenchmark.pochList [a*q] q n =
      FiniteQBenchmark.pochList [a*q] q (n-1) * (1-(a*q)*q^(n-1)) := by
  have step := FiniteQBenchmark.poch_succ (a*q) q (n-1)
  rw [Nat.sub_add_cancel hn] at step
  simpa [FiniteQBenchmark.pochList] using step

/-- The original-relation multiplier is one. It is replayed only after the
evaluated tower relation above has been proved in the original ring. -/
theorem source_increment (a q : K) (n : ℕ) (hn : 1 ≤ n) :
    FiniteQBenchmark.pochList [a*q] q n - FiniteQBenchmark.pochList [a*q] q (n-1) =
      -((a*q)*q^(n-1))*FiniteQBenchmark.pochList [a*q] q (n-1) := by
  have source_step := source_step a q n hn
  linear_combination source_step

end AgentV2DifferenceRing
