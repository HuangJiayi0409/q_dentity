import Benchmark.P2Atoms
import Benchmark.GaussianRules
import Mathlib.Algebra.Polynomial.Eval.Degree
import Mathlib.Tactic

open scoped BigOperators
open FiniteQBenchmark
namespace FiniteQP2
noncomputable section
variable {K : Type*} [Field K]

/-- A finite polynomial representation, not a pre-proved sum identity. -/
def gaussianPoly (q : K) (n : ℕ) : Polynomial K :=
  ∑ k ∈ Finset.range (n+1), Polynomial.monomial k (gaussian q n k)

/-- Certified source-to-polynomial bridge, valid also at q=0 and roots of unity. -/
theorem eval_gaussianPoly (x q : K) (n : ℕ) :
    (gaussianPoly q n).eval x = rogersSzego x q n := by
  simp only [gaussianPoly, rogersSzego, Polynomial.eval_finsetSum, Polynomial.eval_monomial]

/-- Zero extension removes support guards only because the coefficients vanish. -/
theorem coeff_gaussianPoly (q : K) (n k : ℕ) :
    (gaussianPoly q n).coeff k = gaussian q n k := by
  classical
  simp only [gaussianPoly, Polynomial.finsetSum_coeff, Polynomial.coeff_monomial]
  rw [Finset.sum_ite_eq']
  by_cases h : k ∈ Finset.range (n+1)
  · simp [h]
  · simp only [h, ite_false]
    have hk : n < k := by simpa only [Finset.mem_range, not_lt, Nat.succ_le_iff] using h
    exact (gaussian_above q hk).symm

/-- Adjacent coefficient relation. This is local Gaussian algebra, not a
recurrence-solving procedure for the original polynomial identity. -/
theorem gaussian_weighted_step (q : K) (n k : ℕ) :
    (1-q^(n+1))*gaussian q n k = (1-q^(k+1))*gaussian q (n+1) (k+1) := by
  by_cases h : k ≤ n
  · have ha := FiniteQP1.gaussian_adjacent q n k h
    have he : k+1+(n-k) = n+1 := by omega
    have hp : q^(n+1) = q^(k+1)*q^(n-k) := by rw [← pow_add, he]
    rw [hp, gaussian]
    linear_combination -(q^(k+1))*ha
  · simp only [gaussian_above q (by omega : n < k),
      gaussian_above q (by omega : n+1 < k+1), mul_zero]

theorem gaussian_weighted_pred (q : K) (n k : ℕ) (h : 1 ≤ n) :
    (1-q^n)*gaussian q (n-1) k = (1-q^(k+1))*gaussian q n (k+1) := by
  simpa only [Nat.sub_add_cancel h] using gaussian_weighted_step q (n-1) k

/-- Polynomial equality is sufficient for equality at the original evaluation point. -/
theorem eval_of_poly_eq (x : K) (p r : Polynomial K) (h : p = r) : p.eval x = r.eval x :=
  congrArg (Polynomial.eval x) h

/-- Coefficient algebra only: evaluation is already certified by the lifting step. -/
macro "p2_polynomial_coefficients" : tactic => `(tactic| (
  simp (config := { failIfUnchanged := false }) only [
    Polynomial.X_mul_C, mul_pow, ← Polynomial.C_pow, mul_assoc,
    Polynomial.comp_X, Polynomial.comp_zero, ← Polynomial.coeff_zero_eq_eval_zero, map_zero, map_one,
    Polynomial.coeff_add, Polynomial.coeff_sub, Polynomial.coeff_neg,
    Polynomial.comp_C_mul_X_coeff, Polynomial.coeff_C_mul, Polynomial.coeff_mul_C,
    Polynomial.coeff_X_mul, Polynomial.coeff_mul_X,
    Polynomial.coeff_X_mul_zero, Polynomial.coeff_mul_X_zero,
    Polynomial.coeff_zero, Polynomial.coeff_one, Polynomial.coeff_C,
    Polynomial.finsetSum_coeff, Polynomial.coeff_monomial,
    Polynomial.coeff_X_pow, Polynomial.coeff_X,
    mul_ite, Finset.sum_ite_eq, Finset.sum_ite_eq', Finset.mem_range,
    FiniteQP2.coeff_gaussianPoly,
    FiniteQBenchmark.gaussian_zero_right,
    pow_zero, mul_one, one_mul, mul_zero, zero_mul, add_zero, zero_add,
    sub_self, sub_zero, Nat.succ_ne_zero, ite_true, ite_false]
  all_goals simp (config := { failIfUnchanged := false }) (disch := omega) only [
    FiniteQP2.gaussian_weighted_pred]
  all_goals simp (config := { failIfUnchanged := false }) (disch := omega) only [
    one_pow, zero_pow, Nat.succ_ne_zero,
    sub_self, mul_zero, zero_mul, sub_zero, one_mul, add_zero]))

end
end FiniteQP2
