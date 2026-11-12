import Benchmark.Definitions
import Mathlib.Algebra.BigOperators.Intervals

/-! Source-bound triangular kernel action. The fixed profile places the retained
`FiniteQKernel.transpose_triangle` rules before this file. The original natural
subtraction, all finite bounds and the N = 0 boundary are unchanged. -/
namespace AgentV2KernelTransform
open scoped BigOperators

universe u
variable {R : Type u} [CommRing R]

/-- Move the source coefficient inside its finite row, then transpose the
complete triangular support. The outer target coefficient is not extracted. -/
theorem source_transpose (N : ℕ) (alpha delta u v : ℕ → R) :
    (∑ n ∈ Finset.range (N+1),
      alpha n * ∑ r ∈ Finset.Icc n N, delta r * u (r-n) * v (r+n)) =
    ∑ r ∈ Finset.range (N+1), ∑ n ∈ Finset.range (r+1),
      alpha n * (delta r * u (r-n) * v (r+n)) := by
  simp_rw [Finset.mul_sum]
  exact FiniteQKernel.transpose_triangle N
    (fun n r => alpha n * (delta r * u (r-n) * v (r+n)))

end AgentV2KernelTransform
