import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-21 — 双倍移位与互补长度
Original representative source: GR2-I-21
Frozen statement: formulas/test/FQI-SRC-GR2-I-21.md
Source formula:
(aq^{2k};q)_{n-k}=\frac{(a;q)_n(aq^n;q)_k}{(a;q)_{2k}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity234
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n k : ℕ)
 (hbase : regular q) (hk : k ≤ n)
 (h_domain : (pochList [a] q (2*k)) ≠ 0) :
 (pochList [(a * (q^((2*(k : ℤ)) : ℤ)))] q (n-k)) = (((pochList [a] q (n)) * (pochList [(a * (q^(((n : ℤ)) : ℤ)))] q (k))) / (pochList [a] q (2*k))) := by
  sorry

end FiniteQBenchmark.Identity234
