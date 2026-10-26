import Benchmark.CombinatorialRules
import Benchmark.GaussianRules
import Mathlib.Algebra.BigOperators.Ring.Finset

namespace FiniteQCombinatorial
open scoped BigOperators
open FiniteQBenchmark
variable {K : Type*} [Field K]

lemma triangle_succ (k : ℕ) :
    (k+1)*(k+1+1)/2 = k*(k+1)/2+(k+1) := by
  have h : (k+1)*(k+1+1) = k*(k+1)+2*(k+1) := by ring
  omega

/-- Representation bridge built by disjoint weighted subset bijections.
    The raw weights are products, so the theorem also holds at q=0. -/
theorem geometric_subsets (q : K) (n k : ℕ) :
    (∑ s ∈ (Finset.Icc 1 n).powersetCard k, ∏ i ∈ s, q^i) =
      q^(k*(k+1)/2)*gaussian q n k := by
  induction n generalizing k with
  | zero =>
    cases k with
    | zero => simp [gaussian]
    | succ k =>
      have he : (∅ : Finset ℕ).powersetCard (k+1) = ∅ :=
        Finset.powersetCard_eq_empty.mpr (by simp)
      simp [gaussian, he]
  | succ n ih =>
    cases k with
    | zero => simp [gaussian_zero_right]
    | succ k =>
      by_cases hk : k ≤ n
      · have hs : Finset.Icc 1 (n+1) = insert (n+1) (Finset.Icc 1 n) := by
          ext i; simp only [Finset.mem_Icc, Finset.mem_insert]; omega
        have hn : n+1 ∉ Finset.Icc 1 n := by simp
        rw [hs, subset_split _ _ hn]
        have hp : (∑ s ∈ (Finset.Icc 1 n).powersetCard k, ∏ i ∈ insert (n+1) s, q^i) =
            q^(n+1) * ∑ s ∈ (Finset.Icc 1 n).powersetCard k, ∏ i ∈ s, q^i := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro s hs
          apply Finset.prod_insert
          intro h; exact hn ((Finset.mem_powersetCard.mp hs).1 h)
        rw [hp, ih, ih, FiniteQP1.gaussian_pascal q n k hk]
        have he : q^((k+1)*(k+1+1)/2)*q^(n-k) = q^(n+1)*q^(k*(k+1)/2) := by
          rw [← pow_add, ← pow_add]
          congr 1
          rw [triangle_succ]
          omega
        linear_combination -(gaussian q n k) * he
      · have he : (Finset.Icc 1 (n+1)).powersetCard (k+1) = ∅ := by
          apply Finset.powersetCard_eq_empty.mpr
          simp only [Nat.card_Icc]; omega
        rw [he, Finset.sum_empty, gaussian_above q (by omega), mul_zero]

theorem normalize_subset_weights (q : K) (hq : q ≠ 0) (s : Finset ℕ) (j : ℕ) :
    (∑ t ∈ s.powersetCard j, q^(((∑ i ∈ t, i) : ℤ)-(j:ℤ)*(j+1)/2)) =
    q^(-((j:ℤ)*(j+1)/2)) * (∑ t ∈ s.powersetCard j, ∏ i ∈ t, q^i) := by
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro t ht
  rw [Finset.prod_pow_eq_pow_sum, zpow_sub₀ hq, zpow_neg]
  have he : (∑ i ∈ t, (i : ℤ)) = ((∑ i ∈ t, i : ℕ) : ℤ) := (Nat.cast_sum t (fun i : ℕ => i)).symm
  rw [he, zpow_natCast]
  ring

lemma normalized_geometric_factor (q : K) (hq : q ≠ 0) (j : ℕ) :
    q^(-((j:ℤ)*(j+1)/2))*q^(j*(j+1)/2) = 1 := by
  rw [← zpow_natCast q (j*(j+1)/2)]
  have he : ((j*(j+1)/2 : ℕ) : ℤ) = (j:ℤ)*(j+1)/2 := by
    simp
  rw [he, ← zpow_add₀ hq, neg_add_cancel, zpow_zero]

end FiniteQCombinatorial

namespace FiniteQCombinatorial
open scoped BigOperators
open FiniteQBenchmark
variable {K : Type*} [Field K]

/-- Zero-based subset weights: no division, so specialization at q=0 is valid.
    The induction is the insert/erase decomposition of the object family. -/
theorem range_geometric_subsets (q : K) (n k : ℕ) :
    (∑ s ∈ (Finset.range n).powersetCard k, ∏ i ∈ s, q^i) =
      q^(k*(k-1)/2)*gaussian q n k := by
  induction n generalizing k with
  | zero =>
    cases k with
    | zero => simp [gaussian]
    | succ k => simp [gaussian, Finset.powersetCard_eq_empty.mpr (by simp : (∅ : Finset ℕ).card < k+1)]
  | succ n ih =>
    cases k with
    | zero => simp [gaussian_zero_right]
    | succ k =>
      by_cases hk : k ≤ n
      · rw [Finset.range_add_one, subset_split _ _ (by simp)]
        have hp : (∑ s ∈ (Finset.range n).powersetCard k, ∏ i ∈ insert n s, q^i) =
            q^n * ∑ s ∈ (Finset.range n).powersetCard k, ∏ i ∈ s, q^i := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro s hs
          apply Finset.prod_insert
          intro h
          have := (Finset.mem_powersetCard.mp hs).1 h
          simpa using this
        rw [hp, ih, ih, FiniteQP1.gaussian_pascal q n k hk]
        have ht : (k+1)*((k+1)-1)/2 = k*(k-1)/2+k := by
          cases k with
          | zero => decide
          | succ k =>
            simp only [Nat.add_sub_cancel, Nat.succ_sub_one]
            have h : (k+1+1)*(k+1) = (k+1)*k+2*(k+1) := by ring
            omega
        have he : q^((k+1)*((k+1)-1)/2)*q^(n-k) = q^n*q^(k*(k-1)/2) := by
          rw [← pow_add, ← pow_add]
          congr 1
          omega
        linear_combination -(gaussian q n k) * he
      · have he : (Finset.range (n+1)).powersetCard (k+1) = ∅ := by
          apply Finset.powersetCard_eq_empty.mpr
          simp only [Finset.card_range]; omega
        rw [he, Finset.sum_empty, gaussian_above q (by omega), mul_zero]

/-- Rank stratification, retaining an arbitrary coefficient for each rank.
    The maps are s ↦ (card s,s) and (k,s) ↦ s on the disjoint rank fibers. -/
theorem geometric_rank_sum (q : K) (a : ℕ → K) (n : ℕ) :
    (∑ k ∈ Finset.range (n+1), a k * (q^(k*(k-1)/2)*gaussian q n k)) =
      ∑ s ∈ (Finset.range n).powerset, a s.card * ∏ i ∈ s, q^i := by
  rw [Finset.sum_powerset]
  simp only [Finset.card_range]
  apply Finset.sum_congr rfl
  intro k hk
  rw [← range_geometric_subsets, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro s hs
  rw [(Finset.mem_powersetCard.mp hs).2]

/-- Binary choices ↔ subsets, with multiplicative weights. The library lemma
    prod_one_add is proved by the choice/subset bijection, not interpolation. -/
theorem weighted_choices {α : Type*} (s : Finset α) (z : K) (w : α → K) :
    (∑ t ∈ s.powerset, z^t.card * ∏ i ∈ t, w i) = ∏ i ∈ s, (1+z*w i) := by
  rw [Finset.prod_one_add]
  apply Finset.sum_congr rfl
  intro t ht
  simp [Finset.prod_mul_distrib]

end FiniteQCombinatorial

namespace FiniteQCombinatorial
open scoped BigOperators
open FiniteQBenchmark
variable {K : Type*} [Field K]

/-- Local symmetry of a single Gaussian coefficient. This is a disclosed
    foundational identity, proved from the definition and local Pascal rule;
    it is not a summation solver or an assumed Rogers--Szego theorem. -/
theorem gaussian_rank_symmetry (q : K) (n k : ℕ) (hk : k ≤ n) :
    gaussian q n (n-k) = gaussian q n k := by
  induction n generalizing k with
  | zero =>
    have : k = 0 := by omega
    subst k
    rfl
  | succ n ih =>
    by_cases h0 : k = 0
    · subst k; simp [gaussian_self, gaussian_zero_right]
    by_cases hn : k = n+1
    · subst k; simp [gaussian_self, gaussian_zero_right]
    obtain ⟨j,rfl⟩ := Nat.exists_eq_succ_of_ne_zero h0
    have hj : j+1 ≤ n := by omega
    have he : n+1-(j+1) = (n-(j+1))+1 := by omega
    rw [he, FiniteQP1.gaussian_pascal q n (n-(j+1)) (by omega)]
    have h1 : n-(j+1)+1 = n-j := by omega
    rw [h1, ih j (by omega), ih (j+1) hj]
    have h2 : n-(n-(j+1)) = j+1 := by omega
    rw [h2, gaussian]

/-- Rank reflection with arbitrary coefficient weights, verified termwise.
    The symmetry bridge is shared and explicit, not a copied recurrence solver. -/
theorem gaussian_rank_reflect (q : K) (n : ℕ) (a b : ℕ → K)
    (hw : ∀ k ≤ n, a k = b (n-k)) :
    (∑ k ∈ Finset.range (n+1), gaussian q n k * a k) =
      ∑ k ∈ Finset.range (n+1), gaussian q n k * b k := by
  apply range_bijection
  intro k hk
  simp only [Nat.add_sub_cancel]
  rw [gaussian_rank_symmetry q n k (by omega), hw k (by omega)]

/-- Reciprocal monomial weight transport, independent of any Gaussian sum. -/
theorem reciprocal_weight (u : K) (hu : u ≠ 0) (n k : ℕ) (hk : k ≤ n) :
    (u⁻¹)^k = u^(-(n:ℤ)) * u^(n-k) := by
  rw [inv_pow, ← zpow_natCast, ← zpow_natCast u (n-k), ← zpow_add₀ hu]
  rw [Nat.cast_sub hk]
  have he : -(n:ℤ)+((n:ℤ)-(k:ℤ)) = -(k:ℤ) := by ring
  rw [he, zpow_neg]

end FiniteQCombinatorial
