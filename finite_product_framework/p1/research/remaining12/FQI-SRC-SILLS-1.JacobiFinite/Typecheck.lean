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

/- FQI-SRC-SILLS-1.JacobiFinite — Jacobi 乘积证明中的有限双边二项式
Original representative source: SILLS-1.JacobiFinite
Frozen statement: formulas/train/FQI-SRC-SILLS-1.JacobiFinite.md
Source formula:
(q/x,x;q)_m=\sum_{j=-m}^m(-1)^jq^{j(j-1)/2}x^j\begin{bmatrix}2m\\m+j\end{bmatrix}_q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity358
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x : K) (m : ℕ)
 (hx : x ≠ 0)
 (h_domain : x ≠ 0) :
 (pochList [(q / x),x] q (m)) = (∑ j ∈ Finset.Icc (-(m:ℤ) : ℤ) (m : ℤ), (((-1:K)^j*q^(j*(j-1)/2).toNat*x^j) * (gaussianInt q (2*(m:ℤ)) ((m:ℤ)+j)))) := by
  p1_typecheck
end FiniteQBenchmark.Identity358
