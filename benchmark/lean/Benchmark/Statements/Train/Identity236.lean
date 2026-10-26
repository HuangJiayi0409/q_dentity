import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-25 — 按偶数和奇数位置拆分
Original representative source: GR2-I-25
Frozen statement: formulas/train/FQI-SRC-GR2-I-25.md
Source formula:
(a;q)_{2n}=(a;q^2)_n(aq;q^2)_n
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity236
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n : ℕ)
 (hbase : regular q) 
 (h_domain : True) :
 (pochList [a] q (2*n)) = ((pochList [a] (q^2) (n)) * (pochList [(a * q)] (q^2) (n))) := by
  sorry

end FiniteQBenchmark.Identity236
