import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-3.11 — 第二变量的有限 q 幂导数
Original representative source: KAC-CHEUNG-3.11
Frozen statement: formulas/test/FQI-SRC-KAC-CHEUNG-3.11.md
Source formula:
D_{q,x}P_n(a,x;q)=-[n]_qP_{n-1}(a,qx;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity419
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x a : ℂ) (n : ℤ)
 (hq : q ≠ 0) (hq1 : q ≠ 1) (hx : x ≠ 0)
 (h_domain : kacPowerDefined a x q (n) ∧
    kacPowerDefined a (q * x) q (n) ∧
    kacPowerDefined a (q * x) q (n-1)) :
 (jackson q (fun y => kacPower a y q (n)) x) = ((-(qInteger q n)) * (kacPower a (q * x) q (n-1))) := by
  sorry

end FiniteQBenchmark.Identity419
