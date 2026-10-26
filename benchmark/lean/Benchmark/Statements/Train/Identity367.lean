import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-1.ExDistinct — 有界不同部件分拆的有限生成多项式
Original representative source: SILLS-1.ExDistinct
Frozen statement: formulas/train/FQI-SRC-SILLS-1.ExDistinct.md
Source formula:
\sum_{r=0}^{j(j+1)/2}\sum_{\ell=0}^jQ(j,\ell,r)z^\ell q^r=(-zq;q)_j.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity367
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q z : K) (j : ℕ)
 
 (h_domain : True) :
 (∑ r ∈ Finset.range (j*(j+1)/2+1), (∑ l ∈ Finset.range (j+1), ((((distinctPartitionCount j l r : ℕ) : K) * (z^l)) * (q^r)))) = (pochList [((-z) * q)] q (j)) := by
  sorry

end FiniteQBenchmark.Identity367
