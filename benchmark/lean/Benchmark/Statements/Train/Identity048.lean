import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex3i — 乘积参数的两种有限 q 卷积
Original representative source: GR2-1.Ex3i
Frozen statement: formulas/train/FQI-SRC-GR2-1.Ex3i.md
Source formula:
(ab;q)_n=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_qb^k(a;q)_k(b;q)_{n-k}=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_qa^{n-k}(a;q)_k(b;q)_{n-k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity048
variable {K : Type*} [Field K]

theorem statement (a b q : K) (n : ℕ) :
 poch (a*b) q n = (∑ k ∈ Finset.range (n+1), gaussian q n k*b^k*poch a q k*poch b q (n-k)) ∧
 poch (a*b) q n = (∑ k ∈ Finset.range (n+1), gaussian q n k*a^(n-k)*poch a q k*poch b q (n-k)) := by
  sorry

end FiniteQBenchmark.Identity048
