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

/- FQI-CHU-VANDERMONDE-BALANCED — q-Chu–Vandermonde：自变量 cq^n/a
Original representative source: GR2-II-07
Frozen statement: formulas/train/FQI-CHU-VANDERMONDE-BALANCED.md
Source formula:
{}_2\phi_1^{[n]}\!\left[\begin{matrix}a,q^{-n}\\c\end{matrix};q,cq^n/a\right]=\frac{(c/a;q)_n}{(c;q)_n}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity013
variable {K : Type*} [Field K]

theorem statement (a c q : K) (n : ℕ) (hq : q ≠ 0) (ha : a ≠ 0)
    (hden : phiDefined [c] q n) :
    phi [a, q ^ (-(n : ℤ))] [c] q (c*q^n/a) n =
      poch (c/a) q n / poch c q n := by
  p1_typecheck
end FiniteQBenchmark.Identity013
