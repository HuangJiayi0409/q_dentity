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

/- FQI-SRC-SILLS-2.Pair122 — 二步长 Bailey 有限和
Original representative source: SILLS-2.Pair122
Frozen statement: formulas/train/FQI-SRC-SILLS-2.Pair122.md
Source formula:
\mathcal B_n[\alpha;x^2,q^2]=1/((q^2;q^2)_n(-xq;q)_{2n}),\qquad \alpha_r=\alpha_r^{(1,2,2)}(x^2,q^2)
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity371
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (n : ℕ)
 
 (h_domain : ∀ r ∈ Finset.range (n+1), (1 ∣ r → (1-x)*poch (q^1) (q^1) (r/1) ≠ 0 ∧
    ((pochList [(q^2)] (q^2) (n-r)) * (pochList [((x^2) * (q^2))] (q^2) (n+r))) ≠ 0) ∧
    ((pochList [(q^2)] (q^2) (n)) * (pochList [((-x) * q)] q (2*n))) ≠ 0) :
 (∑ r ∈ Finset.range (n+1), ((sillsAlpha x q 1 2 r) / ((pochList [(q^2)] (q^2) (n-r)) * (pochList [((x^2) * (q^2))] (q^2) (n+r))))) = (1 / ((pochList [(q^2)] (q^2) (n)) * (pochList [((-x) * q)] q (2*n)))) := by
  p1_typecheck
end FiniteQBenchmark.Identity371
