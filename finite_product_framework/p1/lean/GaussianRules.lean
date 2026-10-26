import Benchmark.Gaussian
import Mathlib.Tactic.LinearCombination
import Mathlib.Data.Nat.Choose.Basic
open FiniteQBenchmark
namespace FiniteQP1
variable {K : Type*} [Field K]
/-- An alternate local recurrence for the Gaussian definition, independent of any sum identity. -/
theorem gaussian_pascal (q : K) (n k : ℕ) (hk : k ≤ n) :
    gaussian q (n+1) (k+1) = gaussian q n (k+1) + q^(n-k)*gaussian q n k := by
  induction n generalizing k with
  | zero =>
    have : k = 0 := by omega
    subst k
    simp [gaussian]
  | succ n ih =>
    by_cases he : k = n+1
    · subst k
      simp [gaussian_self, gaussian_above q (by omega : n+1 < n+1+1)]
    · have hkn : k ≤ n := by omega
      cases k with
      | zero =>
        have h := ih 0 (by omega)
        simp only [Nat.sub_zero, gaussian_zero_right] at h ⊢
        rw [gaussian, gaussian_zero_right]
        rw [h, pow_succ]
        simp only [gaussian, gaussian_zero_right, mul_one] at h
        linear_combination h
      | succ k =>
        have h0 := ih k (by omega)
        have h1 := ih (k+1) hkn
        have hp : n-k = (n-(k+1))+1 := by omega
        simp only [Nat.succ_sub_succ_eq_sub]
        simp only [gaussian] at h0 h1 ⊢
        rw [hp, pow_succ] at h0 ⊢
        simp only [pow_succ] at h0 h1 ⊢
        linear_combination h0 + (q^k*q*q) * h1
/-- Adjacent lower indices, valid as a polynomial identity at every base. -/
theorem gaussian_adjacent (q : K) (n k : ℕ) (hk : k ≤ n) :
    (1-q^(k+1))*gaussian q n (k+1) = (1-q^(n-k))*gaussian q n k := by
  have h := gaussian_pascal q n k hk
  rw [gaussian] at h
  linear_combination -h
end FiniteQP1
