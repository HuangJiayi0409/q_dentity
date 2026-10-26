import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-22 — 整数倍移位与互补长度
Original representative source: GR2-I-22
Frozen statement: formulas/train/FQI-SRC-GR2-I-22.md
Source formula:
(aq^{jk};q)_{n-k}=\frac{(a;q)_n(aq^n;q)_{(j-1)k}}{(a;q)_{jk}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity235
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n k j : ℕ)
 (hbase : regular q) (hk : k ≤ n) (hj : 1 ≤ j)
 (h_domain : (pochList [a] q (j*k)) ≠ 0) :
 (pochList [(a * (q^(((j : ℤ)*(k : ℤ)) : ℤ)))] q (n-k)) = (((pochList [a] q (n)) * (pochList [(a * (q^(((n : ℤ)) : ℤ)))] q ((j-1)*k))) / (pochList [a] q (j*k))) := by
  sorry

end FiniteQBenchmark.Identity235
