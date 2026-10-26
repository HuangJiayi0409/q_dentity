import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SCHUR-RR-FIRST — Schur 第一有限 Rogers–Ramanujan
Original representative source: SILLS-4.14
Frozen statement: formulas/train/FQI-SCHUR-RR-FIRST.md
Source formula:
\sum_{j=0}^{\lfloor n/2\rfloor}q^{j^2}\begin{bmatrix}n-j\\j\end{bmatrix}_q=\sum_{j=-n-1}^{n+1}(-1)^jq^{j(5j+1)/2}\begin{bmatrix}n\\\lfloor(n+5j+1)/2\rfloor\end{bmatrix}_q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity036
variable {K : Type*} [Field K]

theorem statement (q : K) (n : ℕ) :
 schurD q n = ∑ j ∈ Finset.Icc (-(n : ℤ)-1) ((n : ℤ)+1),
 (-1)^j*q^(j*(5*j+1)/2)*gaussianInt q n (((n : ℤ)+5*j+1)/2) := by
  sorry

end FiniteQBenchmark.Identity036
