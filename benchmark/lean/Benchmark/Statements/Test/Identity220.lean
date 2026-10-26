import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-07 — 有限乘积反向排列
Original representative source: GR2-I-07
Frozen statement: formulas/test/FQI-SRC-GR2-I-07.md
Source formula:
(a;q)_n=(-a)^nq^{n(n-1)/2}(q^{1-n}/a;q)_n
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity220
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n : ℕ)
 (hbase : regular q) (ha : a ≠ 0)
 (h_domain : a ≠ 0) :
 (pochList [a] q (n)) = ((((-a)^n) * (q^(((n : ℤ)*((n : ℤ)-1)/2) : ℤ))) * (pochList [((q^((1-(n : ℤ)) : ℤ)) / a)] q (n))) := by
  sorry

end FiniteQBenchmark.Identity220
