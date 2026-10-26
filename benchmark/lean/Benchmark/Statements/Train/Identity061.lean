import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex35 — 非交换有限 q 二项式的双底数表示
Original representative source: GR2-1.Ex35
Frozen statement: formulas/train/FQI-SRC-GR2-1.Ex35.md
Source formula:
(X+Y)^n=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_qY^kX^{n-k}=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_{q^{-1}}X^kY^{n-k},\qquad XY=qYX.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity061
variable {K : Type*} [Field K]

theorem statement (R : Type*) [Ring R] [Algebra K R] (q : K) (X Y : R) (n : ℕ)
 (hq : regular q) (hcomm : X*Y = algebraMap K R q * Y*X) :
 (X+Y)^n = (∑ k ∈ Finset.range (n+1), algebraMap K R (gaussian q n k)*Y^k*X^(n-k)) ∧
 (X+Y)^n = (∑ k ∈ Finset.range (n+1), algebraMap K R (gaussian q⁻¹ n k)*X^k*Y^(n-k)) := by
  sorry

end FiniteQBenchmark.Identity061
