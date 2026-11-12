import Benchmark.Auxiliary
import Mathlib.Algebra.BigOperators.NatAntidiagonal
import Mathlib.Algebra.Polynomial.Coeff
import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.Tactic.Ring

/-! Fixed source representation and finite Cauchy extraction. No Gaussian
coefficient formula, benchmark statement, or previously proved identity is used.
The rules hold in every commutative ring, including characteristic two and q=0. -/
namespace AgentV2Coefficient
open scoped BigOperators
open Polynomial
noncomputable section
variable {K : Type*} [CommRing K]

def pochPolynomial (q : K) (n : ℕ) : Polynomial K :=
  ∏ j ∈ Finset.range n, (1 - C (q^j) * X)

theorem pochPolynomial_succ (q : K) (n : ℕ) :
    pochPolynomial q (n+1) = pochPolynomial q n * (1 - C (q^n) * X) := by
  simp only [pochPolynomial, Finset.prod_range_succ]

/-- Evaluation at the original free parameter is the actual source Pochhammer. -/
theorem eval_pochPolynomial (q z : K) (n : ℕ) :
    (pochPolynomial q n).eval z = FiniteQBenchmark.poch z q n := by
  induction n with
  | zero => simp [pochPolynomial]
  | succ n ih =>
    rw [pochPolynomial_succ, Polynomial.eval_mul, ih, FiniteQBenchmark.poch_succ]
    simp only [Polynomial.eval_sub, Polynomial.eval_one, Polynomial.eval_mul,
      Polynomial.eval_C, Polynomial.eval_X, mul_comm (q^n) z]

/-- The common foundational Cauchy identity, with the affine-factor index first.
This is just Mathlib coeff_mul and the natural antidiagonal/range bijection. -/
theorem coefficient_convolution (p f : Polynomial K) (m : ℕ) :
    (p * f).coeff m =
      ∑ i ∈ Finset.range (m+1), p.coeff (m-i) * f.coeff i := by
  rw [mul_comm p f, Polynomial.coeff_mul,
    Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]
  apply Finset.sum_congr rfl
  intro i hi
  exact mul_comm _ _

theorem affine_coeff_zero (a : K) :
    (1 - C a * X : Polynomial K).coeff 0 = 1 := by
  simp

theorem affine_coeff_one (a : K) :
    (1 - C a * X : Polynomial K).coeff 1 = -a := by
  simp [Polynomial.coeff_one]

theorem affine_coeff_higher (a : K) (i : ℕ) :
    (1 - C a * X : Polynomial K).coeff (i+2) = 0 := by
  simp [Polynomial.coeff_one]

/-- The zero coefficient slice exported to the ring core is exactly z0*1. -/
theorem coefficient_zero_extraction (p : Polynomial K) (a : K) :
    (p * (1 - C a * X)).coeff 0 = p.coeff 0 * 1 := by
  rw [coefficient_convolution]
  simp only [Nat.zero_add, Finset.sum_range_one, Nat.sub_zero, affine_coeff_zero]

/-- All natural positive indices: finite Cauchy convolution has only two terms.
The displayed right side is precisely the symbolic core's v*1+u*(-w) input. -/
theorem coefficient_succ_extraction (p : Polynomial K) (a : K) (k : ℕ) :
    (p * (1 - C a * X)).coeff (k+1) = p.coeff (k+1) * 1 + p.coeff k * (-a) := by
  rw [coefficient_convolution, Finset.sum_range_succ', Finset.sum_range_succ']
  simp only [Nat.sub_zero, affine_coeff_zero, affine_coeff_one,
    Nat.add_sub_cancel_right, affine_coeff_higher, mul_zero, Finset.sum_const_zero,
    zero_add]
  exact add_comm _ _

/-- Exact ring normalization of the two extracted slices; no division occurs. -/
theorem extracted_normal_forms (u v w z0 : K) :
    (v * 1 + u * (-w) = v - w*u) ∧ (z0 * 1 = z0) := by
  constructor <;> ring

/-- One local certificate. The original Gaussian generating identity stays open. -/
theorem product_coefficients (q z : K) (n : ℕ) :
    (pochPolynomial q n).eval z = FiniteQBenchmark.poch z q n ∧
    (pochPolynomial q (n+1)).coeff 0 = (pochPolynomial q n).coeff 0 ∧
    ∀ k : ℕ, (pochPolynomial q (n+1)).coeff (k+1) =
      (pochPolynomial q n).coeff (k+1) - q^n * (pochPolynomial q n).coeff k := by
  refine ⟨eval_pochPolynomial q z n, ?_, ?_⟩
  · rw [pochPolynomial_succ, coefficient_zero_extraction]
    exact (extracted_normal_forms (0 : K) 0 0 ((pochPolynomial q n).coeff 0)).2
  · intro k
    rw [pochPolynomial_succ, coefficient_succ_extraction]
    exact (extracted_normal_forms ((pochPolynomial q n).coeff k)
      ((pochPolynomial q n).coeff (k+1)) (q^n) 0).1

end
end AgentV2Coefficient
