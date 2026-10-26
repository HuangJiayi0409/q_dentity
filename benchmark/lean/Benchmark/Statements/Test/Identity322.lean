import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-8.44 — G_N(0) 的 Schur 型有限展开
Original representative source: AQ-8.44
Frozen statement: formulas/test/FQI-SRC-AQ-8.44.md
Source formula:
G_N(0;q)=\sum_{\lambda=-N-2}^{N+2}(-1)^\lambda q^{\lambda(5\lambda+1)}\begin{bmatrix}N\\\lfloor(N-5\lambda)/2\rfloor+0\end{bmatrix}_q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity322
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (N : ℕ)
 
 (h_domain : True) :
 (aqG q false N) = (∑ j ∈ Finset.Icc (-(N:ℤ)-2 : ℤ) ((N:ℤ)+2 : ℤ), (((-1:K)^j*q^(j*(5*j+1)).toNat) * (gaussianInt q (N) (((N:ℤ)-5*j)/2+0)))) := by
  sorry

end FiniteQBenchmark.Identity322
