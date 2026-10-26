import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-17 — 有限乘积拼接
Original representative source: GR2-I-17
Frozen statement: formulas/train/FQI-SRC-GR2-I-17.md
Source formula:
(a;q)_{n+k}=(a;q)_n(aq^n;q)_k
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity230
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n k : ℕ)
 (hbase : regular q) 
 (h_domain : True) :
 (pochList [a] q (n+k)) = ((pochList [a] q (n)) * (pochList [(a * (q^(((n : ℤ)) : ℤ)))] q (k))) := by
  sorry

end FiniteQBenchmark.Identity230
