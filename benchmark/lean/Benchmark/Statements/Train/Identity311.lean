import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-3.17 — Rogers 有限交错和（奇上指标）
Original representative source: AQ-3.17
Frozen statement: formulas/train/FQI-SRC-AQ-3.17.md
Source formula:
\sum_{r=-n}^{n-1}(-1)^rq^{r(3r+1)/2}\begin{bmatrix}2n-1\\n-1-r\end{bmatrix}_q=(q^n;q)_n.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity311
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ)
 (hn : 1 ≤ n)
 (h_domain : True) :
 (∑ r ∈ Finset.Icc (-(n:ℤ) : ℤ) ((n:ℤ)-1 : ℤ), (((-1:K)^r*q^(r*(3*r+1)/2).toNat) * (gaussianInt q (2*(n:ℤ)-1) ((n:ℤ)-1-r)))) = (pochList [(q^n)] q (n)) := by
  sorry

end FiniteQBenchmark.Identity311
