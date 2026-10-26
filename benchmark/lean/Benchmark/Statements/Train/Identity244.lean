import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-46 — 移位上指标的互补下指标
Original representative source: GR2-I-46
Frozen statement: formulas/train/FQI-SRC-GR2-I-46.md
Source formula:
\begin{bmatrix}n+\alpha\\n-k\end{bmatrix}_q=\frac{(q^{\alpha+1};q)_n}{(q;q)_{n-k}(q^{\alpha+1};q)_k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity244
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q L alpha : ℂ) (n k : ℕ)
 (hbase : regular q) (hlog : Complex.exp L = q) (hk : k ≤ n)
 (h_domain : ((pochList [q] q (n-k)) * (pochList [(Complex.exp (L*(alpha+1)))] q (k))) ≠ 0) :
 (generalizedGaussian L (n+alpha) ((n-k:ℕ))) = ((pochList [(Complex.exp (L*(alpha+1)))] q (n)) / ((pochList [q] q (n-k)) * (pochList [(Complex.exp (L*(alpha+1)))] q (k)))) := by
  sorry

end FiniteQBenchmark.Identity244
