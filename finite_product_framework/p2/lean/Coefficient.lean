import Benchmark.P2Atoms
import Mathlib.Algebra.BigOperators.NatAntidiagonal
import Mathlib.Algebra.Polynomial.Coeff
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic

open scoped BigOperators
namespace FiniteQP2

/-- Cauchy multiplication, with the exact finite support used by the frontend. -/
theorem coeff_mul_range {R : Type*} [Semiring R] (f g : PowerSeries R) (n : ℕ) :
    PowerSeries.coeff n (f * g) =
      ∑ k ∈ Finset.range (n + 1), PowerSeries.coeff k f * PowerSeries.coeff (n-k) g := by
  rw [PowerSeries.coeff_mul, Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]

theorem polynomial_coeff_mul_range {R : Type*} [Semiring R]
    (f g : Polynomial R) (n : ℕ) :
    (f * g).coeff n =
      ∑ k ∈ Finset.range (n + 1), f.coeff k * g.coeff (n-k) := by
  rw [Polynomial.coeff_mul, Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]

/-- Only logical decomposition and coefficient extensionality, never induction or
another solving backend. Each resulting branch remains a proof obligation. -/
macro "p2_goals" : tactic => `(tactic| (
  repeat' first | apply And.intro | intro
  all_goals first
    | (apply PowerSeries.ext; intro p2_degree)
    | (apply Polynomial.ext; intro p2_degree)
    | skip))

/-- A deliberately explicit whitelist. Inverses and unknown functions stay atoms. -/
macro "p2_coefficients" : tactic => `(tactic|
  simp (config := { failIfUnchanged := false }) only [
    PowerSeries.coeff_C_mul, PowerSeries.coeff_mul_C,
    PowerSeries.coeff_succ_mul_X, PowerSeries.coeff_succ_X_mul,
    PowerSeries.coeff_zero_mul_X, PowerSeries.coeff_zero_X_mul,
    Polynomial.coeff_C_mul, Polynomial.coeff_mul_C,
    Polynomial.coeff_mul_X, Polynomial.coeff_X_mul,
    FiniteQP2.coeff_mul_range, FiniteQP2.polynomial_coeff_mul_range,
    PowerSeries.coeff_mk, PowerSeries.coeff_rescale,
    PowerSeries.coeff_monomial, PowerSeries.coeff_C, PowerSeries.coeff_one,
    map_add, map_sub, map_neg, map_sum, map_zero,
    Polynomial.coeff_add, Polynomial.coeff_sub, Polynomial.coeff_neg,
    Polynomial.finsetSum_coeff, Polynomial.coeff_zero,
    Polynomial.coeff_monomial, Polynomial.coeff_C, Polynomial.coeff_one,
    Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk,
    Finset.sum_range_diag_flip,
    Finset.sum_mul, Finset.mul_sum, Finset.sum_neg_distrib,
    mul_zero, zero_mul, add_zero, zero_add, mul_one, one_mul,
    sub_zero, zero_sub, ite_true, ite_false, ite_self])

/-- Collect equal finite domains before descending; no unknown sum evaluation. -/
macro "p2_collect" : tactic => `(tactic|
  simp (config := { failIfUnchanged := false }) only [
    ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib])

macro "p2_descend" : tactic => `(tactic|
  first
    | (apply Finset.sum_congr rfl; intro p2_index p2_member)
    | (apply Finset.sum_eq_zero; intro p2_index p2_member)
    | skip)

end FiniteQP2
