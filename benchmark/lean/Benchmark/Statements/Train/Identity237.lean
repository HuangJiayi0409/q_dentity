import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-26 — 按模 3 拆分
Original representative source: GR2-I-26
Frozen statement: formulas/train/FQI-SRC-GR2-I-26.md
Source formula:
(a;q)_{3n}=(a;q^3)_n(aq;q^3)_n(aq^2;q^3)_n
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity237
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n : ℕ)
 (hbase : regular q) 
 (h_domain : True) :
 (pochList [a] q (3*n)) = (((pochList [a] (q^3) (n)) * (pochList [(a * q)] (q^3) (n))) * (pochList [(a * (q^2))] (q^3) (n))) := by
  sorry

end FiniteQBenchmark.Identity237
