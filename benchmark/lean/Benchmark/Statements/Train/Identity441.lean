import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-26.14 — 对称有限乘积的交换
Original representative source: KAC-CHEUNG-26.14
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-26.14.md
Source formula:
S_n(1,x;q)=(-1)^nS_n(x,1;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity441
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x : K) (n : ℕ) (hq : q ≠ 0) (hq1 : q ≠ 1) :
 symPower 1 x q n = (-1)^n*symPower x 1 q n := by
  sorry

end FiniteQBenchmark.Identity441
