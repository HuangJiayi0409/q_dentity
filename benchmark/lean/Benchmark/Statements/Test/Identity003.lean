import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-PASCAL-Q-K — Gaussian Pascal：权 q^k
Original representative source: SILLS-1.51
Frozen statement: formulas/test/FQI-PASCAL-Q-K.md
Source formula:
\begin{bmatrix}n\\k\end{bmatrix}_q=q^k\begin{bmatrix}n-1\\k\end{bmatrix}_q+\begin{bmatrix}n-1\\k-1\end{bmatrix}_q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity003
variable {K : Type*} [Field K]

theorem statement (q : K) (n k : ℕ) (hn : 1 ≤ n) (hk : k ≤ n) :
 gaussian q n k = q^k*gaussianInt q ((n : ℤ)-1) k +
 gaussianInt q ((n : ℤ)-1) ((k : ℤ)-1) := by
  sorry

end FiniteQBenchmark.Identity003
