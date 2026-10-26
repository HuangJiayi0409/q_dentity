import Benchmark.P1Atoms

namespace FiniteQP1
open scoped BigOperators
open FiniteQBenchmark
variable {K : Type*} [Field K]

theorem fall_zero (x a q : K) : kacPowerNat x a q 0 = 1 := by
  simp [kacPowerNat]

/-- The defining finite product recurrence, with no nonzero assumptions. -/
theorem fall_succ (x a q : K) (n : ℕ) :
    kacPowerNat x a q (n+1) = kacPowerNat x a q n * (x-q^n*a) := by
  exact Finset.prod_range_succ (fun i => x-q^i*a) n

theorem product_eq_fall (x a q : K) (n : ℕ) :
    (∏ i ∈ Finset.range n, (x-a*q^i)) = kacPowerNat x a q n := by
  unfold kacPowerNat
  apply Finset.prod_congr rfl
  intro i hi
  ring

end FiniteQP1
