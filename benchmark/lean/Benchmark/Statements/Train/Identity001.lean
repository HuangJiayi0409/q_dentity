import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-GAUSSIAN-SYMMETRY — Gaussian 对称性
Original representative source: GR2-I-39
Frozen statement: formulas/train/FQI-GAUSSIAN-SYMMETRY.md
Source formula:
\begin{bmatrix}n\\k\end{bmatrix}_q=\begin{bmatrix}n\\n-k\end{bmatrix}_q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity001
variable {K : Type*} [Field K]

theorem statement (q : K) (n : ℕ) (k : ℤ) :
 gaussianInt q n k = gaussianInt q n ((n : ℤ)-k) := by
  sorry

end FiniteQBenchmark.Identity001
