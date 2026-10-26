import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-4.25 — 奇数 D 多项式的倒数对偶
Original representative source: SILLS-4.25
Frozen statement: formulas/test/FQI-SRC-SILLS-4.25.md
Source formula:
q^{m(m+1)}D_{2m+1}(q^{-1})=\sum_{j=0}^mq^{j(j+1)}\begin{bmatrix}m+j+1\\2j+1\end{bmatrix}_q=\sum_{k=-m-2}^{m+2}\left(q^{15k^2+4k}\begin{bmatrix}2m+1\\m+5k+1\end{bmatrix}_q-q^{15k^2+14k+3}\begin{bmatrix}2m+1\\m+5k+3\end{bmatrix}_q\right).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity390
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (m : ℕ)
 (hq : q ≠ 0)
 (h_domain : True) :
 ((q^(m*(m+1))) * (schurD q⁻¹ (2*m+1))) = (∑ j ∈ Finset.range (m+1), ((q^(j*(j+1))) * (gaussian q (m+j+1) (2*j+1)))) ∧
 (∑ j ∈ Finset.range (m+1), ((q^(j*(j+1))) * (gaussian q (m+j+1) (2*j+1)))) = (∑ k ∈ Finset.Icc (-(m:ℤ)-2 : ℤ) ((m:ℤ)+2 : ℤ), (((q^(15*k*k+4*k).toNat) * (gaussianInt q (2*(m:ℤ)+1) ((m:ℤ)+5*k+1))) - ((q^(15*k*k+14*k+3).toNat) * (gaussianInt q (2*(m:ℤ)+1) ((m:ℤ)+5*k+3))))) := by
  sorry

end FiniteQBenchmark.Identity390
