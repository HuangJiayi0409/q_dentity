import Mathlib.Algebra.BigOperators.Field
import Mathlib.Tactic

/-! Finite-range assembly for computed telescopers. No summation identities. -/
namespace FiniteQGeneralSum
open scoped BigOperators

variable {K : Type*} [Field K]

theorem telescope (G : ℕ → K) (m : ℕ) :
    (∑ k ∈ Finset.range m, (G (k+1)-G k)) = G m-G 0 := by
  induction m with
  | zero => simp
  | succ m ih => rw [Finset.sum_range_succ, ih]; ring

/-- Common prefix plus the actual tails of each shifted summation domain.
No support/vanishing or monicity premise is hidden in this identity. -/
theorem telescoper_range (F : ℕ → ℕ → K) (G : ℕ → K)
    (c : ℕ → K) (r m : ℕ) (tail : ℕ → ℕ)
    (hlocal : ∀ k < m, (∑ j ∈ Finset.range (r+1), c j * F j k) =
      G (k+1)-G k) :
    (∑ j ∈ Finset.range (r+1), c j * (∑ k ∈ Finset.range (m+tail j), F j k)) =
      G m-G 0 + ∑ j ∈ Finset.range (r+1), c j * (∑ t ∈ Finset.range (tail j), F j (m+t)) := by
  have h := Finset.sum_congr rfl (fun k hk => hlocal k (Finset.mem_range.mp hk))
  rw [Finset.sum_comm, telescope] at h
  have split : ∀ j, c j * (∑ k ∈ Finset.range (m+tail j), F j k) =
      c j * (∑ k ∈ Finset.range m, F j k) +
      c j * (∑ t ∈ Finset.range (tail j), F j (m+t)) := by
    intro j
    rw [Finset.sum_range_add, mul_add]
  simp_rw [split]
  rw [Finset.sum_add_distrib]
  simp_rw [← Finset.mul_sum] at h
  rw [h]

/-- Bounded uniqueness, retaining zero-leading-coefficient indices as explicit
proof obligations instead of assuming generic parameters in the original field. -/
theorem recurrence_unique (S T : ℕ → K) (c : ℕ → ℕ → K)
    (r N : ℕ) (hr : 0 < r)
    (initial : ∀ j < r, j ≤ N → S j = T j)
    (step : ∀ n, n+r ≤ N →
      (∑ j ∈ Finset.range (r+1), c n j * S (n+j)) =
      ∑ j ∈ Finset.range (r+1), c n j * T (n+j))
    (singular : ∀ n, n+r ≤ N → c n r = 0 → S (n+r) = T (n+r)) : S N = T N := by
  have all : ∀ m, m ≤ N → S m = T m := by
    intro m
    induction m using Nat.strong_induction_on with
    | h m ih =>
      intro hm
      by_cases small : m < r
      · exact initial m small hm
      · have index : m-r+r = m := Nat.sub_add_cancel (by omega)
        have h := step (m-r) (by omega)
        by_cases hz : c (m-r) r = 0
        · simpa only [index] using singular (m-r) (by omega) hz
        · rw [Finset.sum_range_succ, Finset.sum_range_succ] at h
          have hs : (∑ j ∈ Finset.range r, c (m-r) j * S (m-r+j)) =
              ∑ j ∈ Finset.range r, c (m-r) j * T (m-r+j) := by
            apply Finset.sum_congr rfl
            intro j hj
            have hj' := Finset.mem_range.mp hj
            rw [ih (m-r+j) (by omega) (by omega)]
          rw [hs, index] at h
          exact mul_left_cancel₀ hz (add_left_cancel h)
  exact all N le_rfl

end FiniteQGeneralSum
