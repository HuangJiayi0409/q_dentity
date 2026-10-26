import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-3.5 — 有限 q 幂的降阶导数
Original representative source: KAC-CHEUNG-3.5
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-3.5.md
Source formula:
D_qP_n(x,a;q)=[n]_qP_{n-1}(x,a;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity415
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x a : ℂ) (n : ℤ)
 (hq : q ≠ 0) (hq1 : q ≠ 1) (hx : x ≠ 0)
 (h_domain : kacPowerDefined x a q (n) ∧
    kacPowerDefined (q * x) a q (n) ∧
    kacPowerDefined x a q (n-1)) :
 (jackson q (fun y => kacPower y a q (n)) x) = ((qInteger q n) * (kacPower x a q (n-1))) := by
  sorry

end FiniteQBenchmark.Identity415
