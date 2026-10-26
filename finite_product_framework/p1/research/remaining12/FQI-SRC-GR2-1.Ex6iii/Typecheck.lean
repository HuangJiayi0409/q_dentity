import Lean
import Benchmark.P1Atoms

open Lean Elab Tactic Meta
elab "p1_typecheck" : tactic => withMainContext do
  logInfo m!"P1_ELABORATED_GOAL: {← getMainTarget}"
  throwError "P1_TYPECHECK_ONLY"

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex6iii — 终止 2φ0 求值
Original representative source: GR2-1.Ex6iii
Frozen statement: formulas/train/FQI-SRC-GR2-1.Ex6iii.md
Source formula:
{}_2\phi_0^{[n]}\!\left[\begin{matrix}a,q^{-n}\\-\end{matrix};q,q^n/a\right]=a^{-n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity053
variable {K : Type*} [Field K]

theorem statement (a q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 0) :
 phi [a,q^(-(n : ℤ))] [] q (q^n/a) n = a^(-(n : ℤ)) := by
  p1_typecheck
end FiniteQBenchmark.Identity053
