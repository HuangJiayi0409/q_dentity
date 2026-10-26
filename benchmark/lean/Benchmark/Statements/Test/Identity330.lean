import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-9.26 — D 奇指标倒数恒等式
Original representative source: AQ-9.26
Frozen statement: formulas/test/FQI-SRC-AQ-9.26.md
Source formula:
q^{N(N+1)}D_{2N+1}(q^{-1})=\sum_{n=0}^Nq^{n(n+1)}\begin{bmatrix}N+n+1\\2n+1\end{bmatrix}_q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity330
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (N : ℕ)
 (hq : q ≠ 0)
 (h_domain : True) :
 ((q^(N*(N+1))) * (schurD q⁻¹ (2*N+1))) = (∑ n ∈ Finset.range (N+1), ((q^(n*(n+1))) * (gaussian q (N+n+1) (2*n+1)))) := by
  sorry

end FiniteQBenchmark.Identity330
