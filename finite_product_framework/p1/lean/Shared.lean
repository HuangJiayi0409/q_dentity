import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.BigOperators.Group.Finset.Sigma
import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination

/-! Shared proof assembly for P1. These theorems do not search for local relations. -/
namespace FiniteQP1
open scoped BigOperators
variable {K : Type*} [CommRing K]

theorem telescope (G : ℕ → K) (m : ℕ) :
    (∑ k ∈ Finset.range m, (G (k+1) - G k)) = G m - G 0 := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ, ih]
    ring

/-- Inclusive primitive, with only differences inside the finite input domain. -/
theorem sum_inclusive_antidifference (F H : ℕ → K) (n : ℕ)
    (initial : F 0 = H 0)
    (step : ∀ k < n, F (k+1) = H (k+1)-H k) :
    (∑ k ∈ Finset.range (n+1), F k) = H n := by
  induction n with
  | zero => simpa using initial
  | succ n ih =>
    rw [Finset.sum_range_succ, ih (fun k hk => step k (by omega)), step n (by omega)]
    ring

/-- A growing range has an extra upper term, even when the local relation telescopes. -/
theorem growing_sum_recurrence (F G : ℕ → ℕ → K) (c : ℕ → K)
    (n : ℕ)
    (hlocal : ∀ k ∈ Finset.range (n+1),
      F (n+1) k - c n * F n k = G n (k+1) - G n k) :
    (∑ k ∈ Finset.range (n+2), F (n+1) k) =
      c n * (∑ k ∈ Finset.range (n+1), F n k) +
        (G n (n+1) - G n 0 + F (n+1) (n+1)) := by
  have h := Finset.sum_congr rfl hlocal
  rw [Finset.sum_sub_distrib, ← Finset.mul_sum, telescope] at h
  rw [show n+2 = (n+1)+1 by rfl, Finset.sum_range_succ]
  calc
    _ = ((∑ k ∈ Finset.range (n+1), F (n+1) k) -
        c n * (∑ k ∈ Finset.range (n+1), F n k)) +
        c n * (∑ k ∈ Finset.range (n+1), F n k) + F (n+1) (n+1) := by ring
    _ = _ := by rw [h]; ring

/-- Forward monic recurrence: c n may vanish. No division by the target is needed. -/
theorem first_order_unique (S T c b : ℕ → K)
    (initial : S 0 = T 0)
    (left : ∀ n, S (n+1) = c n * S n + b n)
    (right : ∀ n, T (n+1) = c n * T n + b n) :
    ∀ n, S n = T n := by
  intro n
  induction n with
  | zero => exact initial
  | succ n ih => rw [left, right, ih]

/-- A monic recurrence of any positive order, including sparse/step recurrences. -/
theorem higher_order_unique (r : ℕ) (hr : 0 < r)
    (S T : ℕ → K) (c : ℕ → ℕ → K) (b : ℕ → K)
    (initial : ∀ j < r, S j = T j)
    (left : ∀ n, S (n+r) = -(∑ j ∈ Finset.range r, c n j * S (n+j)) + b n)
    (right : ∀ n, T (n+r) = -(∑ j ∈ Finset.range r, c n j * T (n+j)) + b n) :
    ∀ n, S n = T n := by
  intro m
  induction m using Nat.strong_induction_on with
  | h m ih =>
    by_cases hm : m < r
    · exact initial m hm
    · have he : m-r+r = m := Nat.sub_add_cancel (by omega)
      rw [← he, left, right]
      congr 2
      apply Finset.sum_congr rfl
      intro j hj
      rw [ih (m-r+j) (by simp only [Finset.mem_range] at hj; omega)]

/-- Enlarge a finite support; no formal quotient is evaluated outside support. -/
theorem sum_zero_extend (F : ℕ → ℕ → K)
    (support : ∀ n k, n < k → F n k = 0) (n M : ℕ) (hn : n ≤ M) :
    (∑ k ∈ Finset.range (M+1), F n k) = ∑ k ∈ Finset.range (n+1), F n k := by
  symm
  apply Finset.sum_subset (Finset.range_mono (by omega))
  intro k hk hnot
  apply support
  simp only [Finset.mem_range] at hnot
  omega

/-- Sum a monic telescoper on the largest actual support, retaining its boundary. -/
theorem telescoper_sum (F G : ℕ → ℕ → K) (r : ℕ) (c : ℕ → ℕ → K)
    (support : ∀ n k, n < k → F n k = 0) (n : ℕ)
    (hlocal : ∀ k ∈ Finset.range (n+r+1),
      F (n+r) k + (∑ j ∈ Finset.range r, c n j * F (n+j) k) =
        G n (k+1) - G n k) :
    (∑ k ∈ Finset.range (n+r+1), F (n+r) k) =
      -(∑ j ∈ Finset.range r, c n j * (∑ k ∈ Finset.range (n+j+1), F (n+j) k)) +
        (G n (n+r+1) - G n 0) := by
  have h := Finset.sum_congr rfl hlocal
  rw [Finset.sum_add_distrib, telescope] at h
  rw [Finset.sum_comm] at h
  have he : (∑ j ∈ Finset.range r, ∑ k ∈ Finset.range (n+r+1), c n j * F (n+j) k) =
      ∑ j ∈ Finset.range r, c n j * (∑ k ∈ Finset.range (n+j+1), F (n+j) k) := by
    apply Finset.sum_congr rfl
    intro j hj
    rw [← Finset.mul_sum, sum_zero_extend F support (n+j) (n+r) (by
      simp only [Finset.mem_range] at hj; omega)]
  rw [he] at h
  linear_combination h

/-- Assemble a complete sum identity once the branch discharges every local obligation. -/
theorem prove_growing_sum (F G : ℕ → ℕ → K) (T c b : ℕ → K)
    (hlocal : ∀ n k, k ∈ Finset.range (n+1) →
      F (n+1) k - c n * F n k = G n (k+1) - G n k)
    (boundary : ∀ n, G n (n+1) - G n 0 + F (n+1) (n+1) = b n)
    (initial : F 0 0 = T 0)
    (target : ∀ n, T (n+1) = c n * T n + b n) :
    ∀ n, (∑ k ∈ Finset.range (n+1), F n k) = T n := by
  apply first_order_unique (fun n => ∑ k ∈ Finset.range (n+1), F n k) T c b
  · simpa using initial
  · intro n
    rw [growing_sum_recurrence F G c n (hlocal n), boundary n]
  · exact target

#print axioms telescope
#print axioms growing_sum_recurrence
#print axioms first_order_unique
#print axioms higher_order_unique
#print axioms sum_zero_extend
#print axioms telescoper_sum
#print axioms prove_growing_sum
end FiniteQP1
