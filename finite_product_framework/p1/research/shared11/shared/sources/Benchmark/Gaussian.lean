import Benchmark.Auxiliary
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

namespace FiniteQBenchmark
open scoped BigOperators
variable {K : Type*} [Field K]

theorem gaussian_zero_right (q : K) (n : ℕ) : gaussian q n 0 = 1 := by
  cases n <;> rfl

theorem gaussian_above (q : K) {n k : ℕ} (h : n < k) : gaussian q n k = 0 := by
  induction n generalizing k with
  | zero => cases k with
    | zero => omega
    | succ k => rfl
  | succ n ih =>
    cases k with
    | zero => omega
    | succ k => simp only [gaussian, ih (by omega : n < k), ih (by omega : n < k+1), mul_zero, add_zero]

theorem gaussian_self (q : K) (n : ℕ) : gaussian q n n = 1 := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [gaussian, ih, gaussian_above q (by omega : n < n+1), mul_zero, add_zero]

/-- Algebraic recurrence for the quotient; every denominator hypothesis is explicit. -/
theorem quotient_step (q : K) (k l : ℕ)
    (hk : poch q q k ≠ 0) (hl : poch q q l ≠ 0)
    (hk1 : poch q q (k+1) ≠ 0) (hl1 : poch q q (l+1) ≠ 0) :
    poch q q (k+1+l) / (poch q q k * poch q q (l+1)) +
      q^(k+1) * (poch q q (k+1+l) / (poch q q (k+1) * poch q q l)) =
    poch q q (k+1+l+1) / (poch q q (k+1) * poch q q (l+1)) := by
  have hqk : 1-q*q^k ≠ 0 := (mul_ne_zero_iff.mp (by simpa only [poch_succ] using hk1)).2
  have hql : 1-q*q^l ≠ 0 := (mul_ne_zero_iff.mp (by simpa only [poch_succ] using hl1)).2
  rw [poch_succ q q (k+1+l), poch_succ q q k, poch_succ q q l]
  simp only [pow_add, pow_one]
  field_simp [hk, hl, hqk, hql]
  <;> ring

/-- This is the auxiliary bridge to the original quotient definition, not an axiom. -/
theorem gaussian_eq_quotient (q : K) (n k : ℕ)
    (hden : ∀ j ≤ n, poch q q j ≠ 0) :
    gaussian q n k = gaussianQuotient q n k := by
  induction n generalizing k with
  | zero =>
    cases k with
    | zero => simp [gaussian, gaussianQuotient]
    | succ k => simp [gaussian, gaussianQuotient]
  | succ n ih =>
    by_cases hkn : k ≤ n+1
    · cases k with
      | zero => simp only [gaussian_zero_right, gaussianQuotient, Nat.zero_le, ite_eq_left, poch_zero, Nat.sub_zero, one_mul, div_self (hden (n+1) le_rfl)]
      | succ k =>
        by_cases heq : k = n
        · subst k
          simp only [gaussian_self, gaussianQuotient, le_refl, ite_eq_left, Nat.sub_self, poch_zero, mul_one, div_self (hden (n+1) le_rfl)]
        · have hk : k+1 ≤ n := by omega
          have hn : ∀ j ≤ n, poch q q j ≠ 0 := fun j hj => hden j (by omega)
          rw [gaussian, ih k hn, ih (k+1) hn]
          simp only [gaussianQuotient, if_pos (by omega : k ≤ n), if_pos hk, if_pos hkn]
          have he := quotient_step q k (n-(k+1)) (hn k (by omega))
            (hn _ (by omega)) (hn _ hk) (hn _ (by omega))
          simpa only [show k+1+(n-(k+1)) = n by omega,
            show n-(k+1)+1 = n-k by omega,
            show n+1-(k+1) = n-k by omega] using he
    · rw [gaussian_above q (by omega)]
      simp [gaussianQuotient, hkn]
end FiniteQBenchmark
#print axioms FiniteQBenchmark.gaussian_eq_quotient
