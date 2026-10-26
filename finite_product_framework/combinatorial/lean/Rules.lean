import Mathlib.Algebra.BigOperators.Group.Finset.Powerset
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic

namespace FiniteQCombinatorial
open scoped BigOperators

/-- The two disjoint classes are encoded by identity and insert/erase.
    This is a weighted bijection, valid for arbitrary weights. -/
theorem subset_split {α R : Type*} [DecidableEq α] [AddCommMonoid R]
    (s : Finset α) (a : α) (ha : a ∉ s) (k : ℕ) (w : Finset α → R) :
    (∑ t ∈ (insert a s).powersetCard (k+1), w t) =
      (∑ t ∈ s.powersetCard (k+1), w t) +
      ∑ t ∈ s.powersetCard k, w (insert a t) := by
  rw [Finset.powersetCard_succ_insert ha, Finset.sum_union, Finset.sum_image]
  · intro x hx y hy he
    have hx' : a ∉ x := fun h => ha ((Finset.mem_powersetCard.mp hx).1 h)
    have hy' : a ∉ y := fun h => ha ((Finset.mem_powersetCard.mp hy).1 h)
    simpa [hx',hy'] using congrArg (Finset.erase · a) he
  · apply Finset.disjoint_left.mpr
    intro t ht hi
    obtain ⟨u, hu, rfl⟩ := Finset.mem_image.mp hi
    exact ha ((Finset.mem_powersetCard.mp ht).1 (Finset.mem_insert_self _ _))

/-- Reflection has both a forward and an inverse map; no sample enumeration. -/
theorem range_bijection {R : Type*} [AddCommMonoid R] (n : ℕ) (f g : ℕ → R)
    (hw : ∀ i < n, f i = g (n-1-i)) :
    (∑ i ∈ Finset.range n, f i) = ∑ i ∈ Finset.range n, g i := by
  apply Finset.sum_bij (fun i _ => n-1-i)
  · intro i hi; simp only [Finset.mem_range] at *; omega
  · intro i hi j hj he; simp only [Finset.mem_range] at *; omega
  · intro j hj
    refine ⟨n-1-j, ?_, ?_⟩ <;> simp only [Finset.mem_range] at * <;> omega
  · intro i hi; exact hw i (Finset.mem_range.mp hi)

theorem interval_bijection {R : Type*} [AddCommMonoid R] (a b : ℤ) (f g : ℤ → R)
    (hw : ∀ i ∈ Finset.Icc a b, f i = g (a+b-i)) :
    (∑ i ∈ Finset.Icc a b, f i) = ∑ i ∈ Finset.Icc a b, g i := by
  apply Finset.sum_bij (fun i _ => a+b-i)
  · intro i hi; simp only [Finset.mem_Icc] at *; omega
  · intro i hi j hj he; omega
  · intro j hj
    refine ⟨a+b-j, ?_, ?_⟩ <;> simp only [Finset.mem_Icc] at * <;> omega
  · exact hw

/-- Fixed points must carry zero weight. This works even in characteristic two. -/
theorem cancel {α R : Type*} [AddCommGroup R] (s : Finset α) (w : α → R) (f : α → α)
    (hmem : ∀ i ∈ s, f i ∈ s) (hinv : ∀ i ∈ s, f (f i) = i)
    (hweight : ∀ i ∈ s, w i + w (f i) = 0)
    (hfixed : ∀ i ∈ s, f i = i → w i = 0) : (∑ i ∈ s, w i) = 0 := by
  apply Finset.sum_involution (fun i _ => f i)
  · exact hweight
  · intro i hi hn he; exact hn (hfixed i hi he)
  · exact hmem
  · exact hinv

theorem range_cancel {R : Type*} [AddCommGroup R] (n : ℕ) (w : ℕ → R)
    (hw : ∀ i < n, w i + w (n-1-i) = 0)
    (hf : ∀ i < n, n-1-i = i → w i = 0) :
    (∑ i ∈ Finset.range n, w i) = 0 := by
  apply cancel _ _ (fun i => n-1-i)
  · intro i hi; simp only [Finset.mem_range] at *; omega
  · intro i hi; simp only [Finset.mem_range] at *; omega
  · intro i hi; exact hw i (Finset.mem_range.mp hi)
  · intro i hi; exact hf i (Finset.mem_range.mp hi)

theorem interval_cancel {R : Type*} [AddCommGroup R] (a b : ℤ) (w : ℤ → R)
    (hw : ∀ i ∈ Finset.Icc a b, w i + w (a+b-i) = 0)
    (hf : ∀ i ∈ Finset.Icc a b, a+b-i = i → w i = 0) :
    (∑ i ∈ Finset.Icc a b, w i) = 0 := by
  apply cancel _ _ (fun i => a+b-i)
  · intro i hi; simp only [Finset.mem_Icc] at *; omega
  · intro i hi; omega
  · exact hw
  · exact hf

def toggle {α : Type*} [DecidableEq α] (a : α) (t : Finset α) : Finset α :=
  if a ∈ t then t.erase a else insert a t

lemma toggle_mem {α : Type*} [DecidableEq α] (a : α) (t : Finset α) :
    a ∈ toggle a t ↔ a ∉ t := by
  by_cases h : a ∈ t <;> simp [toggle,h]

lemma toggle_involutive {α : Type*} [DecidableEq α] (a : α) (t : Finset α) :
    toggle a (toggle a t) = t := by
  by_cases h : a ∈ t <;> simp [toggle,h]

lemma toggle_subset {α : Type*} [DecidableEq α] (a : α) (s t : Finset α)
    (ha : a ∈ s) (ht : t ⊆ s) : toggle a t ⊆ s := by
  by_cases h : a ∈ t
  · simpa [toggle,h] using (Finset.erase_subset a t).trans ht
  · simpa [toggle,h] using Finset.insert_subset ha ht

theorem toggle_cancel {α R : Type*} [DecidableEq α] [AddCommGroup R]
    (s : Finset α) (a : α) (ha : a ∈ s) (w : Finset α → R)
    (hw : ∀ t ∈ s.powerset, w t + w (toggle a t) = 0) :
    (∑ t ∈ s.powerset, w t) = 0 := by
  apply cancel _ _ (toggle a)
  · intro t ht
    exact Finset.mem_powerset.mpr (toggle_subset a s t ha (Finset.mem_powerset.mp ht))
  · intro t _; exact toggle_involutive a t
  · exact hw
  · intro t _ he
    have h := toggle_mem a t
    rw [he] at h
    tauto

lemma toggle_sign {R : Type*} [Ring R] {α : Type*} [DecidableEq α]
    (a : α) (t : Finset α) :
    (-1 : R)^t.card + (-1 : R)^(toggle a t).card = 0 := by
  by_cases h : a ∈ t
  · have ht : t = insert a (t.erase a) := (Finset.insert_erase h).symm
    conv_lhs => lhs; rw [ht, Finset.card_insert_of_notMem (Finset.notMem_erase a t)]
    simp [toggle,h,pow_succ]
  · simp [toggle,h,Finset.card_insert_of_notMem h,pow_succ]

lemma toggle_erase {α : Type*} [DecidableEq α] (a : α) (t : Finset α) :
    (toggle a t).erase a = t.erase a := by
  by_cases h : a ∈ t <;> simp [toggle,h]

lemma toggle_signed_weight {R : Type*} [Ring R] {α : Type*} [DecidableEq α]
    (a : α) (t : Finset α) (w : Finset α → R) :
    (-1 : R)^t.card * w (t.erase a) +
      (-1 : R)^(toggle a t).card * w ((toggle a t).erase a) = 0 := by
  rw [toggle_erase, ← add_mul, toggle_sign, zero_mul]

end FiniteQCombinatorial

namespace FiniteQCombinatorial
open scoped BigOperators

/-- Only nonfixed objects cancel; fixed objects retain their full weight.
    No cancellation by 2 and no characteristic restriction are used. -/
theorem involution_remainder {α R : Type*} [DecidableEq α] [AddCommGroup R]
    (s : Finset α) (w : α → R) (f : α → α)
    (hmem : ∀ i ∈ s, f i ∈ s) (hinv : ∀ i ∈ s, f (f i) = i)
    (hweight : ∀ i ∈ s, f i ≠ i → w i + w (f i) = 0) :
    (∑ i ∈ s, w i) = ∑ i ∈ s.filter (fun i => f i = i), w i := by
  classical
  have hz : (∑ i ∈ s.filter (fun i => f i ≠ i), w i) = 0 := by
    apply cancel _ _ f
    · intro i hi
      obtain ⟨hi, hn⟩ := Finset.mem_filter.mp hi
      apply Finset.mem_filter.mpr
      refine ⟨hmem i hi, ?_⟩
      rw [hinv i hi]
      exact Ne.symm hn
    · intro i hi
      exact hinv i (Finset.mem_filter.mp hi).1
    · intro i hi
      exact hweight i (Finset.mem_filter.mp hi).1 (Finset.mem_filter.mp hi).2
    · intro i hi he
      exact False.elim ((Finset.mem_filter.mp hi).2 he)
  have h := Finset.sum_filter_add_sum_filter_not s (fun i => f i = i) w
  simpa only [hz, add_zero] using h.symm

theorem range_remainder {R : Type*} [AddCommGroup R] (n : ℕ) (w : ℕ → R)
    (hw : ∀ i < n, n-1-i ≠ i → w i + w (n-1-i) = 0) :
    (∑ i ∈ Finset.range n, w i) =
      ∑ i ∈ (Finset.range n).filter (fun i => n-1-i = i), w i := by
  apply involution_remainder _ _ (fun i => n-1-i)
  · intro i hi; simp only [Finset.mem_range] at *; omega
  · intro i hi; simp only [Finset.mem_range] at *; omega
  · intro i hi hn; exact hw i (Finset.mem_range.mp hi) hn

end FiniteQCombinatorial

namespace FiniteQCombinatorial
open scoped BigOperators

/-- Complement is its own inverse on subsets; weights are arbitrary. -/
theorem subset_complement {α R : Type*} [DecidableEq α] [AddCommMonoid R]
    (s : Finset α) (f g : Finset α → R)
    (hw : ∀ t ⊆ s, f t = g (s \ t)) :
    (∑ t ∈ s.powerset, f t) = ∑ t ∈ s.powerset, g t := by
  apply Finset.sum_bij (fun t _ => s \ t)
  · intro t ht; exact Finset.mem_powerset.mpr Finset.sdiff_subset
  · intro t ht u hu he
    have := congrArg (s \ ·) he
    simpa [Finset.sdiff_sdiff_eq_self (Finset.mem_powerset.mp ht),
      Finset.sdiff_sdiff_eq_self (Finset.mem_powerset.mp hu)] using this
  · intro t ht
    exact ⟨s \ t, Finset.mem_powerset.mpr Finset.sdiff_subset,
      Finset.sdiff_sdiff_eq_self (Finset.mem_powerset.mp ht)⟩
  · intro t ht; exact hw t (Finset.mem_powerset.mp ht)

/-- Disjoint block objects: union, inverse intersections. Arbitrary weights
    allow subsequent rank filters without assuming a Gaussian identity. -/
theorem subset_blocks {α R : Type*} [DecidableEq α] [AddCommMonoid R]
    (s t : Finset α) (hd : Disjoint s t) (w : Finset α → R) :
    (∑ u ∈ (s ∪ t).powerset, w u) =
      ∑ a ∈ s.powerset, ∑ b ∈ t.powerset, w (a ∪ b) := by
  rw [← Finset.sum_product s.powerset t.powerset (fun p => w (p.1 ∪ p.2))]
  symm
  apply Finset.sum_bij (fun p _ => p.1 ∪ p.2)
  · intro p hp
    rcases Finset.mem_product.mp hp with ⟨ha,hb⟩
    exact Finset.mem_powerset.mpr (Finset.union_subset_union
      (Finset.mem_powerset.mp ha) (Finset.mem_powerset.mp hb))
  · intro p hp r hr he
    rcases Finset.mem_product.mp hp with ⟨ha,hb⟩
    rcases Finset.mem_product.mp hr with ⟨hc,he'⟩
    have ha := Finset.mem_powerset.mp ha
    have hb := Finset.mem_powerset.mp hb
    have hc := Finset.mem_powerset.mp hc
    have he' := Finset.mem_powerset.mp he'
    have hd := Finset.disjoint_left.mp hd
    apply Prod.ext <;> ext x
    · have hx := Finset.ext_iff.mp he x
      simp only [Finset.mem_union] at hx
      constructor <;> intro h
      · rcases hx.mp (Or.inl h) with h'|h'
        · exact h'
        · exact False.elim (hd (ha h) (he' h'))
      · rcases hx.mpr (Or.inl h) with h'|h'
        · exact h'
        · exact False.elim (hd (hc h) (hb h'))
    · have hx := Finset.ext_iff.mp he x
      simp only [Finset.mem_union] at hx
      constructor <;> intro h
      · rcases hx.mp (Or.inr h) with h'|h'
        · exact False.elim (hd (hc h') (hb h))
        · exact h'
      · rcases hx.mpr (Or.inr h) with h'|h'
        · exact False.elim (hd (ha h') (he' h))
        · exact h'
  · intro u hu
    refine ⟨(u ∩ s,u ∩ t), ?_, ?_⟩
    · exact Finset.mem_product.mpr ⟨Finset.mem_powerset.mpr Finset.inter_subset_right,
        Finset.mem_powerset.mpr Finset.inter_subset_right⟩
    · have hu := Finset.mem_powerset.mp hu
      ext x
      simp only [Finset.mem_union, Finset.mem_inter]
      constructor
      · tauto
      · intro h; rcases Finset.mem_union.mp (hu h) with hs|ht
        · exact Or.inl ⟨h,hs⟩
        · exact Or.inr ⟨h,ht⟩
  · intro p hp; rfl

end FiniteQCombinatorial

namespace FiniteQCombinatorial
open scoped BigOperators

/-- Odd rank reflection cancels any symmetric coefficient family. There are
    no fixed ranks, so the argument is also valid in characteristic two. -/
theorem odd_rank_cancel {R : Type*} [Ring R] (n : ℕ) (w : ℕ → R)
    (hn : Odd n) (hw : ∀ k ≤ n, w (n-k) = w k) :
    (∑ k ∈ Finset.range (n+1), (-1)^k*w k) = 0 := by
  have hn' : n%2 = 1 := Nat.odd_iff.mp hn
  apply range_cancel
  · intro k hk
    have hk' : k ≤ n := by omega
    simp only [Nat.add_sub_cancel]
    rw [hw k hk', ← add_mul]
    have hs : (-1:R)^k + (-1:R)^(n-k) = 0 := by
      by_cases he : k%2 = 0
      · have ho : ¬(n-k)%2 = 0 := by omega
        simp [neg_one_pow_eq_ite, Nat.even_iff, he, ho]
      · have ho : (n-k)%2 = 0 := by omega
        simp [neg_one_pow_eq_ite, Nat.even_iff, he, ho]
    rw [hs, zero_mul]
  · intro k hk hf
    simp only [Nat.add_sub_cancel] at hf
    omega

/-- Fixed-rank block decomposition retains the rank condition explicitly. -/
theorem subset_blocks_rank {α R : Type*} [DecidableEq α] [AddCommMonoid R]
    (s t : Finset α) (hd : Disjoint s t) (h : ℕ) (w : Finset α → R) :
    (∑ u ∈ (s ∪ t).powersetCard h, w u) =
      ∑ a ∈ s.powerset, ∑ b ∈ t.powerset,
        if a.card+b.card = h then w (a ∪ b) else 0 := by
  have hf : (s ∪ t).powersetCard h = (s ∪ t).powerset.filter (fun u => u.card = h) := by
    ext u; simp
  rw [hf, Finset.sum_filter, subset_blocks s t hd]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  have hd' : Disjoint a b := hd.mono (Finset.mem_powerset.mp ha) (Finset.mem_powerset.mp hb)
  rw [Finset.card_union_of_disjoint hd']

end FiniteQCombinatorial
