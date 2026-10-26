import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-3.18 — Rogers 有限交错和（偶上指标）
Original representative source: AQ-3.18
Frozen statement: formulas/train/FQI-SRC-AQ-3.18.md
Source formula:
\sum_{r=-n}^{n}(-1)^rq^{r(3r+1)/2}\begin{bmatrix}2n\\n-r\end{bmatrix}_q=(q^{n+1};q)_n.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity312
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ)
 
 (h_domain : True) :
 (∑ r ∈ Finset.Icc (-(n:ℤ) : ℤ) (n : ℤ), (((-1:K)^r*q^(r*(3*r+1)/2).toNat) * (gaussianInt q (2*(n:ℤ)) ((n:ℤ)-r)))) = (pochList [(q^(n+1))] q (n)) := by
  sorry

end FiniteQBenchmark.Identity312
