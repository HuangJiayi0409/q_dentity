import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic
import Mathlib.FieldTheory.KummerExtension

/- Generic finite-index certificates. No q-identity is assumed here. -/
namespace FiniteQProduct
open scoped BigOperators

theorem prod_range_blocks {M : Type*} [CommMonoid M] (f : ℕ → M) (m n : ℕ) :
    (∏ k ∈ Finset.range (m*n), f k) =
      ∏ i ∈ Finset.range n, ∏ j ∈ Finset.range m, f (m*i+j) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Nat.mul_succ, Finset.prod_range_add, ih, Finset.prod_range_succ]

theorem prod_range_residues {M : Type*} [CommMonoid M] (f : ℕ → M) (m n : ℕ) :
    (∏ k ∈ Finset.range (m*n), f k) =
      ∏ j ∈ Finset.range m, ∏ i ∈ Finset.range n, f (m*i+j) := by
  rw [prod_range_blocks, Finset.prod_comm]

/-- Split off the first actual factor, with the nonempty-domain obligation. -/
theorem prod_range_head {M : Type*} [CommMonoid M] (f : ℕ → M)
    (n : ℕ) (hn : 0 < n) :
    (∏ k ∈ Finset.range n, f k) = f 0 * ∏ k ∈ Finset.range (n-1), f (k+1) := by
  obtain ⟨j, rfl⟩ : ∃ j, n = j+1 := ⟨n-1, by omega⟩
  simpa only [Nat.add_sub_cancel, mul_comm] using Finset.prod_range_succ' f j

/-- Evaluate the general factorization of X^m-C(x^m) at X=1.
    This is a polynomial factor certificate, not a Pochhammer identity. -/
theorem prod_root_factors {R : Type*} [CommRing R] [IsDomain R]
    (x w : R) (m : ℕ) (hm : 0 < m) (hw : IsPrimitiveRoot w m) :
    (∏ j ∈ Finset.range m, (1-x*w^j)) = 1-x^m := by
  have h := X_pow_sub_C_eq_prod hw hm (rfl : x^m = x^m)
  have he := congrArg (Polynomial.eval (1:R)) h
  simpa only [Polynomial.eval_sub, Polynomial.eval_pow, Polynomial.eval_X,
    Polynomial.eval_C, Polynomial.eval_prod, one_pow, mul_comm] using he.symm

theorem prod_root_factors_weight {R : Type*} [CommRing R] [IsDomain R]
    (a b w : R) (m : ℕ) (hm : 0 < m) (hw : IsPrimitiveRoot w m) :
    (∏ j ∈ Finset.range m, (1-(a*w^j)*b)) = 1-(a*b)^m := by
  calc
    _ = ∏ j ∈ Finset.range m, (1-(a*b)*w^j) := by
      apply Finset.prod_congr rfl
      intro j hj
      congr 1 <;> ring
    _ = _ := prod_root_factors (a*b) w m hm hw

end FiniteQProduct

open Lean Elab Tactic
/-- Bounded proof reconstruction: product congruence and exact ring normalization.
    This deliberately has no q-summation or identity-specific theorem database. -/
syntax "product_finish" num : tactic
elab_rules : tactic
| `(tactic| product_finish $fuel:num) => do
  let n := fuel.getNat
  if n == 0 then throwError "product congruence depth exhausted"
  let rest := Syntax.mkNumLit (toString (n-1))
  evalTactic (← `(tactic|
    first
    | rfl
    | (ring; done)
    | ((try simp only [pow_add, pow_mul, mul_pow, pow_zero, pow_one, zpow_natCast]) <;> ring; done)
    | (rw [FiniteQProduct.prod_root_factors_weight _ _ _ _ (by omega) (by assumption)];
        product_finish $rest)
    | (rw [FiniteQProduct.prod_root_factors _ _ _ (by omega) (by assumption)];
        product_finish $rest)
    | (apply Finset.prod_congr rfl; intro _ _; product_finish $rest)
    | (congr 1 <;> product_finish $rest)))
