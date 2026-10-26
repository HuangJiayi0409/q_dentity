import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-2.35 — Rogers 连接系数的有限反演关系
Original representative source: AQ-2.35
Frozen statement: formulas/test/FQI-SRC-AQ-2.35.md
Source formula:
\sum_{j=0}^{\lfloor N/2\rfloor}\begin{bmatrix}r+2j\\j\end{bmatrix}_q T(r+2j,N-2j)=\delta_{N,0}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity306
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (r N : ℕ)
 
 (h_domain : True) :
 (∑ j ∈ Finset.range (N/2+1), ((gaussian q (r+2*j) (j)) * (aqInverseT q (r+2*j) (N-2*j)))) = (if (N) = (0) then (1 : K) else 0) := by
  sorry

end FiniteQBenchmark.Identity306
