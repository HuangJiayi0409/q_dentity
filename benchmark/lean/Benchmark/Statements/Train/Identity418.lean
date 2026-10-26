import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-3.10 — 有限 q 幂倒数的导数
Original representative source: KAC-CHEUNG-3.10
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-3.10.md
Source formula:
D_q\frac1{P_n(x,a;q)}=[-n]_qP_{-n-1}(x,q^na;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity418
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x a : ℂ) (n : ℤ)
 (hq : q ≠ 0) (hq1 : q ≠ 1) (hx : x ≠ 0)
 (h_domain : kacPowerDefined x a q (n) ∧
    kacPowerDefined (q * x) a q (n) ∧
    (kacPower x a q (n)) ≠ 0 ∧
    (kacPower (q * x) a q (n)) ≠ 0 ∧
    kacPowerDefined x (q^n*a) q (-n-1)) :
 (jackson q (fun y => 1/kacPower y a q (n)) x) = ((qInteger q (-n)) * (kacPower x (q^n*a) q (-n-1))) := by
  sorry

end FiniteQBenchmark.Identity418
