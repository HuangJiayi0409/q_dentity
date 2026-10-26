import Benchmark.P1Atoms
import Mathlib.Order.Interval.Finset.Nat
import Mathlib.Algebra.Order.BigOperators.Group.Finset

namespace FiniteQP1
open FiniteQBenchmark
open scoped BigOperators
variable {K : Type*} [Field K]

theorem sum_Icc_reverse (f : ℕ → K) (n : ℕ) :
    (∑ k ∈ Finset.Icc 1 (n+1), f (n+1-k)) = ∑ j ∈ Finset.range (n+1), f j := by
  apply Finset.sum_bij (fun k _ => n+1-k)
  · intro k hk
    simp only [Finset.mem_Icc] at hk
    simp only [Finset.mem_range]
    omega
  · intro a ha b hb he
    simp only [Finset.mem_Icc] at ha hb
    omega
  · intro b hb
    simp only [Finset.mem_range] at hb
    refine ⟨n+1-b, ?_, ?_⟩
    · simp only [Finset.mem_Icc]; omega
    · omega
  · intro a ha; rfl

/-- Weighted finite sums inherit a verified triangular kernel relation. -/
theorem triangular_recurrence (U : ℕ → K) (P : ℕ → K) (W : ℕ → ℕ → K)
    (a b : ℕ → K)
    (hstep : ∀ m k, k ≤ m → P (m+1)*W (m+1) k = a m * (P m*W m k))
    (hend : ∀ m, P (m+1)*W (m+1) (m+1) = b m) (m : ℕ) :
    P (m+1)*(∑ k ∈ Finset.range (m+2), W (m+1) k*U k) =
      a m*(P m*(∑ k ∈ Finset.range (m+1), W m k*U k)) + b m*U (m+1) := by
  rw [show m+2 = (m+1)+1 by omega, Finset.sum_range_succ, mul_add]
  congr 1
  · simp only [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro k hk
    have h := hstep m k (by simpa only [Finset.mem_range, Nat.lt_succ_iff] using hk)
    linear_combination (U k)*h
  · rw [← mul_assoc, hend]
end FiniteQP1
