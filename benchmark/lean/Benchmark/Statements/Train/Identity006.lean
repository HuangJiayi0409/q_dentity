import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-RECTANGLE-PARTITIONS — 矩形分拆的 Gaussian 生成多项式
Original representative source: GR2-1.NoteEx2-partition
Frozen statement: formulas/train/FQI-RECTANGLE-PARTITIONS.md
Source formula:
\begin{bmatrix}n\\k\end{bmatrix}_q=\sum_{\substack{n-k\ge\lambda_1\ge\cdots\ge\lambda_k\ge0}}q^{\lambda_1+\cdots+\lambda_k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity006
variable {K : Type*} [Field K]

theorem statement (q : K) (n k : ℕ) (hk : k ≤ n) :
 gaussian q n k = rectangleWeight q (n-k) k := by
  sorry

end FiniteQBenchmark.Identity006
