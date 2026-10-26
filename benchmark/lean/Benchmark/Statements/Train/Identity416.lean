import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-3.6 — 有限 q 幂的指标相加
Original representative source: KAC-CHEUNG-3.6
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-3.6.md
Source formula:
P_{m+n}(x,a;q)=P_m(x,a;q)P_n(x,q^ma;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity416
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x a : K) (m n : ℤ)
 (hq : q ≠ 0) (hq1 : q ≠ 1)
 (h_domain : kacPowerDefined x a q (m+n) ∧
    kacPowerDefined x a q (m) ∧
    kacPowerDefined x (q^m*a) q (n)) :
 (kacPower x a q (m+n)) = ((kacPower x a q (m)) * (kacPower x (q^m*a) q (n))) := by
  sorry

end FiniteQBenchmark.Identity416
