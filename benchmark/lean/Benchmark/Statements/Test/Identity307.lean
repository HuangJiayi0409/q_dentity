import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-2.38 — 连接系数递推
Original representative source: AQ-2.38
Frozen statement: formulas/test/FQI-SRC-AQ-2.38.md
Source formula:
T(r,0)=1,\qquad T(r,N)=-\sum_{j=1}^{\lfloor N/2\rfloor}\begin{bmatrix}r+2j\\j\end{bmatrix}_q T(r+2j,N-2j)\quad(N\ge1).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity307
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (r N : ℕ) (hN : 1 ≤ N) :
 aqInverseT q r 0 = 1 ∧ aqInverseT q r N =
 -(∑ j ∈ Finset.Icc 1 (N/2), gaussian q (r+2*j) j*aqInverseT q (r+2*j) (N-2*j)) := by
  sorry

end FiniteQBenchmark.Identity307
