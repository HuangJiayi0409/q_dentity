import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SCHUR-RR-SECOND — Schur 第二有限 Rogers–Ramanujan
Original representative source: SILLS-4.16
Frozen statement: formulas/train/FQI-SCHUR-RR-SECOND.md
Source formula:
E_n=\sum_{j=0}^{\lfloor n/2\rfloor}q^{j(j+1)}\begin{bmatrix}n-j\\j\end{bmatrix}_q=\sum_{j=-n-2}^{n+2}(-1)^jq^{j(5j+3)/2}\begin{bmatrix}n+1\\\lfloor(n+5j+3)/2\rfloor\end{bmatrix}_q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity037
variable {K : Type*} [Field K]

theorem statement (q : K) (n : ℕ) :
 schurE q n = ∑ j ∈ Finset.Icc (-(n : ℤ)-2) ((n : ℤ)+2),
 (-1)^j*q^(j*(5*j+3)/2)*gaussianInt q (n+1) (((n : ℤ)+5*j+3)/2) := by
  sorry

end FiniteQBenchmark.Identity037
