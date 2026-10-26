import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-6.5 — Gaussian 的加权子集表示
Original representative source: KAC-CHEUNG-6.5
Frozen statement: formulas/test/FQI-SRC-KAC-CHEUNG-6.5.md
Source formula:
\begin{bmatrix}n\\j\end{bmatrix}_q=\sum_{\substack{S\subseteq\{1,\ldots,n\}\\|S|=j}}q^{\sum_{s\in S}s-j(j+1)/2}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity427
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n j : ℕ) (hq : q ≠ 0) (hq1 : q ≠ 1) (hj : j ≤ n) :
 gaussian q n j = ∑ s ∈ (Finset.Icc 1 n).powersetCard j, q^(((∑ i ∈ s, i):ℤ)-(j:ℤ)*(j+1)/2) := by
  sorry

end FiniteQBenchmark.Identity427
