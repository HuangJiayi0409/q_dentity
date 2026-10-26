import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-GAUSSIAN-RECIPROCITY — 普通 Gaussian 倒底数
Original representative source: SILLS-1.53
Frozen statement: formulas/test/FQI-GAUSSIAN-RECIPROCITY.md
Source formula:
\begin{bmatrix}n\\k\end{bmatrix}_{1/q}=q^{k(k-n)}\begin{bmatrix}n\\k\end{bmatrix}_q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity004
variable {K : Type*} [Field K]

theorem statement (q : K) (n k : ℕ) (hq : q ≠ 0) (hk : k ≤ n) :
 gaussian q⁻¹ n k = q^((k : ℤ)*((k : ℤ)-n))*gaussian q n k := by
  sorry

end FiniteQBenchmark.Identity004
