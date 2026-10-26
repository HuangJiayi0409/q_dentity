import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-4.26-corrected — 偶数 E 多项式的倒数对偶
Original representative source: SILLS-4.26-corrected
Frozen statement: formulas/train/FQI-SRC-SILLS-4.26-corrected.md
Source formula:
q^{m(m+1)}E_{2m}(q^{-1})=\sum_{j=0}^mq^{j(j+1)}\begin{bmatrix}m+j\\2j\end{bmatrix}_q=\sum_{k=-m-2}^{m+2}\left(q^{15k^2+2k}\begin{bmatrix}2m+1\\m+5k+1\end{bmatrix}_q-q^{15k^2+8k+1}\begin{bmatrix}2m+1\\m+5k+2\end{bmatrix}_q\right).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity391
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (m : ℕ)
 (hq : q ≠ 0)
 (h_domain : True) :
 ((q^(m*(m+1))) * (schurE q⁻¹ (2*m))) = (∑ j ∈ Finset.range (m+1), ((q^(j*(j+1))) * (gaussian q (m+j) (2*j)))) ∧
 (∑ j ∈ Finset.range (m+1), ((q^(j*(j+1))) * (gaussian q (m+j) (2*j)))) = (∑ k ∈ Finset.Icc (-(m:ℤ)-2 : ℤ) ((m:ℤ)+2 : ℤ), (((q^(15*k*k+2*k).toNat) * (gaussianInt q (2*(m:ℤ)+1) ((m:ℤ)+5*k+1))) - ((q^(15*k*k+8*k+1).toNat) * (gaussianInt q (2*(m:ℤ)+1) ((m:ℤ)+5*k+2))))) := by
  sorry

end FiniteQBenchmark.Identity391
