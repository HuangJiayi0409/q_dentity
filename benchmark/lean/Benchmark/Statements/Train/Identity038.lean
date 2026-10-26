import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SCHUR-EVEN-RECIPROCAL — Schur D 偶指标倒数的两种展开
Original representative source: SILLS-4.23
Frozen statement: formulas/train/FQI-SCHUR-EVEN-RECIPROCAL.md
Source formula:
q^{m^2}D_{2m}(q^{-1})=\sum_{j=0}^mq^{j^2}\begin{bmatrix}m+j\\2j\end{bmatrix}_q=\sum_{k=-m-2}^{m+2}\left(q^{15k^2-k}\begin{bmatrix}2m\\m+5k\end{bmatrix}_q-q^{15k^2-11k+2}\begin{bmatrix}2m\\m+5k-2\end{bmatrix}_q\right).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity038
variable {K : Type*} [Field K]

theorem statement (q : K) (m : ℕ) (hq : q ≠ 0) :
 q^(m*m)*schurD q⁻¹ (2*m) =
 (∑ j ∈ Finset.range (m+1), q^(j*j)*gaussian q (m+j) (2*j)) ∧
 (∑ j ∈ Finset.range (m+1), q^(j*j)*gaussian q (m+j) (2*j)) =
 ∑ k ∈ Finset.Icc (-(m : ℤ)-2) ((m : ℤ)+2),
 (q^(15*k^2-k)*gaussianInt q (2*m) ((m : ℤ)+5*k) -
 q^(15*k^2-11*k+2)*gaussianInt q (2*m) ((m : ℤ)+5*k-2)) := by
  sorry

end FiniteQBenchmark.Identity038
