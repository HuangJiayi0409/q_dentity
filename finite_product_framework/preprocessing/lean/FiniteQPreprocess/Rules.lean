import Benchmark.Definitions
import Mathlib.Algebra.BigOperators.Intervals

/-! Small method-neutral rewrites. No target identities, certificate search, or
    global simp attributes. -/
namespace FiniteQPreprocess
open FiniteQBenchmark
open scoped BigOperators

theorem poch_zero {K : Type*} [CommRing K] (a q : K) : poch a q 0 = 1 := by
  simp [poch]

theorem pochList_nil {K : Type*} [CommRing K] (q : K) (n : ℕ) :
    pochList [] q n = 1 := by
  simp [pochList]

theorem pochList_cons {K : Type*} [CommRing K] (a q : K) (as : List K) (n : ℕ) :
    pochList (a :: as) q n = poch a q n * pochList as q n := by
  simp only [pochList, List.map_cons, List.prod_cons]

/-- Same-domain merging preserves the entire finite domain, including empty sets. -/
theorem merge_sum {ι M : Type*} [AddCommMonoid M] (s : Finset ι) (f g : ι → M) :
    (∑ i ∈ s, f i) + (∑ i ∈ s, g i) = ∑ i ∈ s, (f i + g i) := by
  exact (Finset.sum_add_distrib).symm

/-- Range synchronization is boundary-aware; Nat subtraction stays truncated. -/
theorem nat_Ico_sum {M : Type*} [AddCommMonoid M] (f : ℕ → M) (a b : ℕ) :
    (∑ k ∈ Finset.Ico a b, f k) = ∑ j ∈ Finset.range (b - a), f (a + j) := by
  exact Finset.sum_Ico_eq_sum_range f a b

theorem nat_Ico_prod {M : Type*} [CommMonoid M] (f : ℕ → M) (a b : ℕ) :
    (∏ k ∈ Finset.Ico a b, f k) = ∏ j ∈ Finset.range (b - a), f (a + j) := by
  exact Finset.prod_Ico_eq_prod_range f a b

/-- Pull scalars out without commuting factors. -/
theorem sum_right_factor {ι R : Type*} [Semiring R] (s : Finset ι) (f : ι → R) (a : R) :
    (∑ i ∈ s, f i * a) = (∑ i ∈ s, f i) * a := by
  exact (Finset.sum_mul s f a).symm

theorem sum_left_factor {ι R : Type*} [Semiring R] (s : Finset ι) (f : ι → R) (a : R) :
    (∑ i ∈ s, a * f i) = a * (∑ i ∈ s, f i) := by
  exact (Finset.mul_sum s f a).symm

/-- Closed Nat intervals retain empty-range semantics when b < a. -/
theorem nat_Icc_sum {M : Type*} [AddCommMonoid M] (f : ℕ → M) (a b : ℕ) :
    (∑ k ∈ Finset.Icc a b, f k) = ∑ j ∈ Finset.range (b + 1 - a), f (a + j) := by
  rw [← Finset.Ico_add_one_right_eq_Icc]
  exact Finset.sum_Ico_eq_sum_range f a (b + 1)

theorem nat_Icc_prod {M : Type*} [CommMonoid M] (f : ℕ → M) (a b : ℕ) :
    (∏ k ∈ Finset.Icc a b, f k) = ∏ j ∈ Finset.range (b + 1 - a), f (a + j) := by
  rw [← Finset.Ico_add_one_right_eq_Icc]
  exact Finset.prod_Ico_eq_prod_range f a (b + 1)

/-- Available as a certified relation, not an eager expansion rule. -/
theorem poch_shift {K : Type*} [CommRing K] (a q : K) (n : ℕ) :
    poch a q (n + 1) = poch a q n * (1 - a * q ^ n) := by
  simp [poch, Finset.prod_range_succ]

end FiniteQPreprocess
