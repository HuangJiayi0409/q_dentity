import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-2.29 — q-Hermite 的有限 Fourier 展开
Original representative source: AQ-2.29
Frozen statement: formulas/train/FQI-SRC-AQ-2.29.md
Source formula:
A_r(e^{i\theta})=\sum_{j=0}^r\begin{bmatrix}r\\j\end{bmatrix}_q\cos((r-2j)\theta)=\sum_{j=0}^r\begin{bmatrix}r\\j\end{bmatrix}_q e^{i(r-2j)\theta}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity305
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : ℂ) (theta : ℝ) (r : ℕ) :
 aqHermite (Complex.exp (Complex.I*(theta:ℂ))) q r =
 (∑ j ∈ Finset.range (r+1), gaussian q r j*(Real.cos (((r:ℝ)-2*j)*theta) : ℂ)) ∧
 (∑ j ∈ Finset.range (r+1), gaussian q r j*(Real.cos (((r:ℝ)-2*j)*theta) : ℂ)) =
 (∑ j ∈ Finset.range (r+1), gaussian q r j*Complex.exp (Complex.I*((r:ℂ)-2*j)*(theta:ℂ))) := by
  sorry

end FiniteQBenchmark.Identity305
