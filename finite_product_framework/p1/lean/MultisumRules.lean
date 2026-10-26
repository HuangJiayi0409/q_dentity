import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Sigma
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination

/-! Finite-domain divergence, valid in any dimension. No boundary is assumed zero. -/
namespace FiniteQP1
open scoped BigOperators
variable {K α ι : Type*} [CommRing K] [DecidableEq α]

theorem directional_boundary (D : Finset α) (shift : α ↪ α) (G : α → K) :
    (∑ x ∈ D, (G (shift x) - G x)) =
      (∑ x ∈ D.map shift \ D, G x) - (∑ x ∈ D \ D.map shift, G x) := by
  rw [Finset.sum_sub_distrib, Finset.sum_sdiff_sub_sum_sdiff]
  simp only [Finset.sum_map]

theorem multisum_boundary (D : Finset α) (directions : Finset ι)
    (shift : ι → α ↪ α) (G : ι → α → K) (F : α → K)
    (local_relation : ∀ x ∈ D, F x = ∑ i ∈ directions, (G i (shift i x) - G i x)) :
    (∑ x ∈ D, F x) = ∑ i ∈ directions,
      ((∑ x ∈ D.map (shift i) \ D, G i x) - (∑ x ∈ D \ D.map (shift i), G i x)) := by
  calc
    _ = ∑ x ∈ D, ∑ i ∈ directions, (G i (shift i x) - G i x) :=
      Finset.sum_congr rfl local_relation
    _ = ∑ i ∈ directions, ∑ x ∈ D, (G i (shift i x) - G i x) := Finset.sum_comm
    _ = _ := Finset.sum_congr rfl (fun i _ => directional_boundary D (shift i) (G i))

/-- The moving support correction is independent of the divergence boundary. -/
theorem moving_support_difference (D E : Finset α) (F H : α → K) (c : K) :
    (∑ x ∈ E, F x) - c * (∑ x ∈ D, H x) =
      (∑ x ∈ D, (F x - c * H x)) +
      ((∑ x ∈ E \ D, F x) - (∑ x ∈ D \ E, F x)) := by
  rw [Finset.sum_sub_distrib, ← Finset.mul_sum, Finset.sum_sdiff_sub_sum_sdiff]
  ring

def triangleSum (F : ℕ → ℕ → K) (n : ℕ) : K :=
  ∑ j ∈ Finset.range (n+1), ∑ k ∈ Finset.range (n-j+1), F j k

theorem triangle_as_box (F : ℕ → ℕ → K) (n : ℕ) :
    triangleSum F n = ∑ j ∈ Finset.range (n+1), ∑ k ∈ Finset.range (n+1),
      if j+k ≤ n then F j k else 0 := by
  unfold triangleSum
  apply Finset.sum_congr rfl
  intro j hj
  simp only [Finset.mem_range] at hj
  apply Finset.sum_subset_zero_on_sdiff (Finset.range_mono (by omega))
  · intro k hk
    simp only [Finset.mem_sdiff, Finset.mem_range] at hk
    rw [ite_eq_right (by omega)]
  · intro k hk
    simp only [Finset.mem_range] at hk
    rw [ite_eq_left (by omega)]

theorem triangle_transpose (F : ℕ → ℕ → K) (n : ℕ) :
    triangleSum F n = triangleSum (fun j k => F k j) n := by
  rw [triangle_as_box, triangle_as_box, Finset.sum_comm]
  simp only [Nat.add_comm]

theorem multisum_telescope (G : ℕ → K) (m : ℕ) :
    (∑ k ∈ Finset.range m, (G (k+1)-G k)) = G m-G 0 := by
  induction m with
  | zero => simp
  | succ m ih => rw [Finset.sum_range_succ, ih]; ring

theorem triangle_divergence (G H : ℕ → ℕ → K) (n : ℕ) :
    triangleSum (fun j k => (G (j+1) k-G j k)+(H j (k+1)-H j k)) n =
      (∑ k ∈ Finset.range (n+1), (G (n-k+1) k-G 0 k)) +
      (∑ j ∈ Finset.range (n+1), (H j (n-j+1)-H j 0)) := by
  have split : triangleSum (fun j k => (G (j+1) k-G j k)+(H j (k+1)-H j k)) n =
      triangleSum (fun j k => G (j+1) k-G j k) n +
      triangleSum (fun j k => H j (k+1)-H j k) n := by
    simp only [triangleSum, Finset.sum_add_distrib]
  rw [split, triangle_transpose (fun j k => G (j+1) k-G j k)]
  simp only [triangleSum]
  congr 1
  · apply Finset.sum_congr rfl
    intro k _
    exact multisum_telescope (fun j => G j k) (n-k+1)
  · apply Finset.sum_congr rfl
    intro j _
    exact multisum_telescope (H j) (n-j+1)

theorem triangle_shell (F : ℕ → ℕ → K) (n : ℕ) :
    triangleSum F (n+1) = triangleSum F n +
      ∑ j ∈ Finset.range (n+2), F j (n+1-j) := by
  unfold triangleSum
  rw [Finset.sum_range_succ]
  have h : (∑ j ∈ Finset.range (n+1), ∑ k ∈ Finset.range (n+1-j+1), F j k) =
      (∑ j ∈ Finset.range (n+1), ∑ k ∈ Finset.range (n-j+1), F j k) +
      ∑ j ∈ Finset.range (n+1), F j (n+1-j) := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j hj
    simp only [Finset.mem_range] at hj
    rw [show n+1-j+1 = (n-j+1)+1 by omega, Finset.sum_range_succ]
    rw [show n-j+1 = n+1-j by omega]
  rw [h, show n+2 = (n+1)+1 by omega,
    Finset.sum_range_succ (fun j => F j (n+1-j)) (n+1)]
  simp only [Nat.sub_self, zero_add, Finset.sum_range_one]
  ring

theorem triangle_recurrence (F : ℕ → ℕ → ℕ → K)
    (G H : ℕ → ℕ → K) (c : K) (n : ℕ)
    (local_relation : ∀ j k, j+k ≤ n →
      F (n+1) j k-c*F n j k = (G (j+1) k-G j k)+(H j (k+1)-H j k)) :
    triangleSum (F (n+1)) (n+1) = c*triangleSum (F n) n +
      (∑ k ∈ Finset.range (n+1), (G (n-k+1) k-G 0 k)) +
      (∑ j ∈ Finset.range (n+1), (H j (n-j+1)-H j 0)) +
      (∑ j ∈ Finset.range (n+2), F (n+1) j (n+1-j)) := by
  have h : triangleSum (fun j k => F (n+1) j k-c*F n j k) n =
      triangleSum (fun j k => (G (j+1) k-G j k)+(H j (k+1)-H j k)) n := by
    apply Finset.sum_congr rfl
    intro j hj
    apply Finset.sum_congr rfl
    intro k hk
    apply local_relation
    simp only [Finset.mem_range] at hj hk
    omega
  rw [triangle_divergence] at h
  have hl : triangleSum (fun j k => F (n+1) j k-c*F n j k) n =
      triangleSum (F (n+1)) n-c*triangleSum (F n) n := by
    simp only [triangleSum, Finset.sum_sub_distrib, Finset.mul_sum]
  rw [hl] at h
  rw [triangle_shell]
  linear_combination h

theorem triangle_upper_reindex (G : ℕ → ℕ → K) (n : ℕ) :
    (∑ k ∈ Finset.range (n+1), G (n-k+1) k) =
      ∑ j ∈ Finset.range (n+1), G (j+1) (n-j) := by
  apply Finset.sum_bij (fun k _ => n-k)
  · intro k hk
    simp only [Finset.mem_range] at hk ⊢
    omega
  · intro a ha b hb he
    simp only [Finset.mem_range] at ha hb
    omega
  · intro b hb
    refine ⟨n-b, ?_, ?_⟩
    · simp only [Finset.mem_range] at hb ⊢; omega
    · simp only [Finset.mem_range] at hb; omega
  · intro a ha
    simp only [Finset.mem_range] at ha
    rw [show n-(n-a)=a by omega]

theorem triangle_boundary_cancel (F G H : ℕ → ℕ → K) (n : ℕ)
    (gzero : ∀ k, G 0 k=0) (hzero : ∀ j, H j 0=0)
    (upper : ∀ j, j ≤ n+1 → G j (n+1-j)+H j (n+1-j)+F j (n+1-j)=0) :
    (∑ k ∈ Finset.range (n+1), (G (n-k+1) k-G 0 k)) +
      (∑ j ∈ Finset.range (n+1), (H j (n-j+1)-H j 0)) +
      (∑ j ∈ Finset.range (n+2), F j (n+1-j)) = 0 := by
  simp only [gzero, hzero, sub_zero]
  rw [triangle_upper_reindex]
  have hg : (∑ j ∈ Finset.range (n+1), G (j+1) (n-j)) =
      ∑ j ∈ Finset.range (n+2), G j (n+1-j) := by
    rw [show n+2=(n+1)+1 by omega,
      Finset.sum_range_succ' (fun j => G j (n+1-j)) (n+1)]
    simp only [gzero, add_zero]
    apply Finset.sum_congr rfl
    intro j hj
    rw [show n+1-(j+1)=n-j by omega]
  have hh : (∑ j ∈ Finset.range (n+1), H j (n-j+1)) =
      ∑ j ∈ Finset.range (n+2), H j (n+1-j) := by
    rw [show n+2=(n+1)+1 by omega,
      Finset.sum_range_succ (fun j => H j (n+1-j)) (n+1)]
    simp only [Nat.sub_self, hzero, add_zero]
    apply Finset.sum_congr rfl
    intro j hj
    simp only [Finset.mem_range] at hj
    rw [show n-j+1=n+1-j by omega]
  rw [hg, hh, ← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  apply Finset.sum_eq_zero
  intro j hj
  apply upper
  simp only [Finset.mem_range] at hj
  omega

theorem triangle_homogeneous (F : ℕ → ℕ → ℕ → K)
    (G H : ℕ → ℕ → K) (c : K) (n : ℕ)
    (local_relation : ∀ j k, j+k ≤ n →
      F (n+1) j k-c*F n j k = (G (j+1) k-G j k)+(H j (k+1)-H j k))
    (gzero : ∀ k, G 0 k=0) (hzero : ∀ j, H j 0=0)
    (upper : ∀ j, j ≤ n+1 →
      G j (n+1-j)+H j (n+1-j)+F (n+1) j (n+1-j)=0) :
    triangleSum (F (n+1)) (n+1) = c*triangleSum (F n) n := by
  have h := triangle_recurrence F G H c n local_relation
  have b := triangle_boundary_cancel (F (n+1)) G H n gzero hzero upper
  linear_combination h+b

end FiniteQP1

#print axioms FiniteQP1.directional_boundary
#print axioms FiniteQP1.multisum_boundary
#print axioms FiniteQP1.moving_support_difference

#print axioms FiniteQP1.triangle_homogeneous
