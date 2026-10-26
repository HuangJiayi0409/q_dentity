import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-1.11-12 — q 导数乘法规则
Original representative source: KAC-CHEUNG-1.11-12
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-1.11-12.md
Source formula:
D_q(fg)(x)=f(qx)D_qg(x)+g(x)D_qf(x)=f(x)D_qg(x)+g(qx)D_qf(x).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity412
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x : ℂ) (f g : ℂ → ℂ) (hq : q ≠ 0) (hq1 : q ≠ 1) (hx : x ≠ 0) :
 jackson q (fun y => f y*g y) x = f (q*x)*jackson q g x+g x*jackson q f x ∧
 f (q*x)*jackson q g x+g x*jackson q f x = f x*jackson q g x+g (q*x)*jackson q f x := by
  sorry

end FiniteQBenchmark.Identity412
