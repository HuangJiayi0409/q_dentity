import Benchmark.BatchDefinitions
import Mathlib.Algebra.Polynomial.Roots

/-! A bounded finite-zero certificate for a single source tail factor.
Both coefficient atoms remain symbolic. The two nodes are 0 and 1, which are
distinct in every field, so no characteristic or nonzero-parameter assumption
is introduced. Polynomial equality is obtained from the degree/root theorem. -/
namespace AgentV2Interpolation
open Polynomial
noncomputable section
universe u
variable {K : Type u} [Field K]

def factorLeft (u v : K) : Polynomial K := 1 - X * C u * C v

def factorRight (u v : K) : Polynomial K := 1 - X * (C u * C v)

theorem factorLeft_degree (u v : K) : (factorLeft u v).natDegree ≤ 1 := by
  apply (natDegree_sub_le _ _).trans
  apply max_le
  · simp
  · exact (natDegree_mul_C_le _ v).trans
      ((natDegree_mul_C_le _ u).trans (by simp))

theorem factorRight_degree (u v : K) : (factorRight u v).natDegree ≤ 1 := by
  unfold factorRight
  rw [← C_mul]
  apply (natDegree_sub_le _ _).trans
  apply max_le
  · simp
  · exact (natDegree_mul_C_le _ (u*v)).trans (by simp)

/-- Two exact evaluations suffice for a degree-at-most-one polynomial.
The proof explicitly bounds the difference and uses two distinct roots. -/
theorem eq_of_degree_one_nodes (p r : Polynomial K)
    (hp : p.natDegree ≤ 1) (hr : r.natDegree ≤ 1)
    (hzero : p.eval 0 = r.eval 0) (hone : p.eval 1 = r.eval 1) : p = r := by
  apply sub_eq_zero.mp
  apply Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero (p-r)
    (f := fun b : Bool => if b then (1 : K) else 0)
  · intro i j hij
    cases i <;> cases j <;> simp_all
  · intro b
    cases b
    · simpa only [Bool.false_eq_true, ↓reduceIte, eval_sub] using sub_eq_zero.mpr hzero
    · simpa only [↓reduceIte, eval_sub] using sub_eq_zero.mpr hone
  · have hdegree : (p-r).natDegree ≤ 1 :=
      (natDegree_sub_le p r).trans (max_le hp hr)
    simpa using Nat.lt_succ_of_le hdegree

theorem factor_polynomials (u v : K) : factorLeft u v = factorRight u v := by
  apply eq_of_degree_one_nodes _ _ (factorLeft_degree u v) (factorRight_degree u v)
  · simp [factorLeft, factorRight]
  · simp [factorLeft, factorRight]

/-- Evaluate the interpolation equality at the original arbitrary parameter. -/
theorem scalar_factor (a u v : K) : 1 - (a*u)*v = 1 - a*(u*v) := by
  have heval := congrArg (Polynomial.eval a) (factor_polynomials u v)
  simpa only [factorLeft, factorRight, eval_sub, eval_one, eval_mul, eval_X,
    eval_C] using heval

/-- The original integer exponent is a natural cast; no regularity is needed
for this factor bridge. The original tail index remains universally quantified. -/
theorem source_factor (a q : K) (k j : ℕ) :
    1 - (a * q^(((k : ℤ) : ℤ))) * q^j = 1 - a * q^(k+j) := by
  rw [zpow_natCast, pow_add]
  exact scalar_factor a (q^k) (q^j)

end
end AgentV2Interpolation
