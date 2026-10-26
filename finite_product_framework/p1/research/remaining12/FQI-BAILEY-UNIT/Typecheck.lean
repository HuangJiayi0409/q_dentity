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

/- FQI-BAILEY-UNIT — 一般参数单位 Bailey 对
Original representative source: AQ-3.48
Frozen statement: formulas/train/FQI-BAILEY-UNIT.md
Source formula:
\sum_{r=0}^n\frac{u_r(a)}{(q;q)_{n-r}(aq;q)_{n+r}}=\delta_{n,0},\quad u_0(a)=1,\quad u_r(a)=\frac{(-1)^rq^{r(r-1)/2}(1-aq^{2r})(aq;q)_{r-1}}{(q;q)_r}\ (r\ge1).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity020
variable {K : Type*} [Field K]

theorem statement (a q : K) (n : ℕ)
    (hunit : ∀ r ≤ n, poch q q r ≠ 0)
    (hden : ∀ r ≤ n, poch q q (n-r) * poch (a*q) q (n+r) ≠ 0) :
    (∑ r ∈ Finset.range (n+1), unitBailey a q r /
      (poch q q (n-r) * poch (a*q) q (n+r))) = if n = 0 then 1 else 0 := by
  p1_typecheck
end FiniteQBenchmark.Identity020
