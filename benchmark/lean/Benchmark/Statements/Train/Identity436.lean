import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-26.5 — 对称 q 导数乘法规则
Original representative source: KAC-CHEUNG-26.5
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-26.5.md
Source formula:
\widetilde D_q(fg)(x)=f(qx)\widetilde D_qg(x)+g(q^{-1}x)\widetilde D_qf(x)=f(q^{-1}x)\widetilde D_qg(x)+g(qx)\widetilde D_qf(x).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity436
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x : ℂ) (f g : ℂ → ℂ) (hq : q ≠ 0) (hq2 : q^2 ≠ 1) (hx : x ≠ 0) :
 symJackson q (fun y => f y*g y) x = f (q*x)*symJackson q g x+g (q⁻¹*x)*symJackson q f x ∧
 f (q*x)*symJackson q g x+g (q⁻¹*x)*symJackson q f x =
 f (q⁻¹*x)*symJackson q g x+g (q*x)*symJackson q f x := by
  sorry

end FiniteQBenchmark.Identity436
