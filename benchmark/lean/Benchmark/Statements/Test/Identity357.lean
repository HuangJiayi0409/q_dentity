import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-25.shell — 固定最大部件与 rank 的有限生成多项式
Original representative source: FINE-25.shell
Frozen statement: formulas/test/FQI-SRC-FINE-25.shell.md
Source formula:
\sum_{\substack{\lambda_1=L\\\lambda_1-\ell(\lambda)=r}}q^{|\lambda|}=q^{2L-r-1}\begin{bmatrix}2L-r-2\\L-1\end{bmatrix}_q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity357
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (L r : ℕ) (hL : 1 ≤ L) (hr : r < L) :
 (∑ l ∈ shellPartitions L r, q^(∑ i, (l i).val)) =
 q^(2*L-r-1)*gaussian q (2*L-r-2) (L-1) := by
  sorry

end FiniteQBenchmark.Identity357
