import Benchmark.Gaussian
import Mathlib.Algebra.BigOperators.Group.Finset.Defs

namespace FiniteQP1
open scoped BigOperators
open FiniteQBenchmark

/-- Reindex the whole finite bilateral support, including both endpoints. -/
theorem sum_bilateral_range {A : Type*} [AddCommMonoid A] (f : ℤ → A) (n : ℕ) :
    (∑ j ∈ Finset.Icc (-(n:ℤ)) (n:ℤ), f j) =
      ∑ k ∈ Finset.range (2*n+1), f ((k:ℤ)-(n:ℤ)) := by
  symm
  refine Finset.sum_bij (fun k _ => (k:ℤ)-(n:ℤ)) ?_ ?_ ?_ ?_
  · intro k hk
    simp only [Finset.mem_range] at hk
    simp only [Finset.mem_Icc]
    omega
  · intro a ha b hb hab
    omega
  · intro j hj
    simp only [Finset.mem_Icc] at hj
    refine ⟨(j+(n:ℤ)).toNat, ?_, ?_⟩
    · simp only [Finset.mem_range]
      omega
    · omega
  · intro k hk
    rfl

/-- On the reindexed support the integer Gaussian uses its polynomial branch. -/
theorem gaussianInt_centered {K : Type*} [CommRing K] (q : K)
    (n k : ℕ) (hk : k ≤ 2*n) :
    gaussianInt q (2*(n:ℤ)) ((n:ℤ)+((k:ℤ)-(n:ℤ))) = gaussian q (2*n) k := by
  have h : (n:ℤ)+((k:ℤ)-(n:ℤ)) = (k:ℤ) := by omega
  rw [h]
  simp only [gaussianInt]
  have he : 0 ≤ 2*(n:ℤ) ∧ 0 ≤ (k:ℤ) ∧ (k:ℤ) ≤ 2*(n:ℤ) := by
    constructor
    · omega
    · constructor
      · omega
      · exact_mod_cast hk
  rw [if_pos he]
  norm_cast

end FiniteQP1

#print axioms FiniteQP1.sum_bilateral_range
#print axioms FiniteQP1.gaussianInt_centered
