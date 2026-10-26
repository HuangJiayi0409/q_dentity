import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-FINITE-Q-BINOMIAL — 有限 q-二项式定理
Original representative source: SILLS-1.56
Frozen statement: formulas/train/FQI-FINITE-Q-BINOMIAL.md
Source formula:
\sum_{k=0}^n(-1)^kz^kq^{k(k-1)/2}\begin{bmatrix}n\\k\end{bmatrix}_q=(z;q)_n.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity005
variable {K : Type*} [Field K]

theorem statement (q z : K) (n : ℕ) :
 (∑ k ∈ Finset.range (n+1), (-1)^k*z^k*q^(k*(k-1)/2)*gaussian q n k) = poch z q n := by
  sorry

end FiniteQBenchmark.Identity005
