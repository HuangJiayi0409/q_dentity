import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-20 — 从有限乘积截出尾段
Original representative source: GR2-I-20
Frozen statement: formulas/train/FQI-SRC-GR2-I-20.md
Source formula:
(aq^k;q)_{n-k}=\frac{(a;q)_n}{(a;q)_k}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity233
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n k : ℕ)
 (hbase : regular q) (hk : k ≤ n) (ha : a ≠ 0)
 (h_domain : (pochList [a] q (k)) ≠ 0) :
 (pochList [(a * (q^(((k : ℤ)) : ℤ)))] q (n-k)) = ((pochList [a] q (n)) / (pochList [a] q (k))) := by
  sorry

end FiniteQBenchmark.Identity233
