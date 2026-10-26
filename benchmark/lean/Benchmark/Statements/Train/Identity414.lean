import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-1.15 — 幂代换的 q 链式规则
Original representative source: KAC-CHEUNG-1.15
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-1.15.md
Source formula:
D_q(f\circ u)(x)=(D_{q^\beta}f)(u(x))D_qu(x),\qquad u(x)=\alpha x^\beta.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity414
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x a : ℂ) (beta : ℤ) (f : ℂ → ℂ) (hq : q ≠ 0) (hq1 : q ≠ 1)
 (hb : beta ≠ 0) (hax : a*x ≠ 0) (hqb : q^beta ≠ 1) :
 jackson q (fun y => f (a*y^beta)) x = jackson (q^beta) f (a*x^beta)*jackson q (fun y => a*y^beta) x := by
  sorry

end FiniteQBenchmark.Identity414
