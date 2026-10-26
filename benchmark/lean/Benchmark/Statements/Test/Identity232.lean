import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-19 — 整数倍长度的尾段
Original representative source: GR2-I-19
Frozen statement: formulas/test/FQI-SRC-GR2-I-19.md
Source formula:
(aq^{kn};q)_n=\frac{(a;q)_{(k+1)n}}{(a;q)_{kn}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity232
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n k : ℕ)
 (hbase : regular q) 
 (h_domain : (pochList [a] q (k*n)) ≠ 0) :
 (pochList [(a * (q^(((k : ℤ)*(n : ℤ)) : ℤ)))] q (n)) = ((pochList [a] q ((k+1)*n)) / (pochList [a] q (k*n))) := by
  sorry

end FiniteQBenchmark.Identity232
