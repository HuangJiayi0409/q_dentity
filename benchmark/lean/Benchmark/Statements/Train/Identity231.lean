import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-18 — 交换两个移位长度
Original representative source: GR2-I-18
Frozen statement: formulas/train/FQI-SRC-GR2-I-18.md
Source formula:
(aq^n;q)_k=\frac{(aq^k;q)_n(a;q)_k}{(a;q)_n}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity231
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n k : ℕ)
 (hbase : regular q) 
 (h_domain : (pochList [a] q (n)) ≠ 0) :
 (pochList [(a * (q^(((n : ℤ)) : ℤ)))] q (k)) = (((pochList [(a * (q^(((k : ℤ)) : ℤ)))] q (n)) * (pochList [a] q (k))) / (pochList [a] q (n))) := by
  sorry

end FiniteQBenchmark.Identity231
