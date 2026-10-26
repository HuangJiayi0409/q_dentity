import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-3.5.MULTIPROD — q-多项系数的 Gaussian 乘积分解
Original representative source: AP-3.5.MULTIPROD
Frozen statement: formulas/train/FQI-SRC-AP-3.5.MULTIPROD.md
Source formula:
\frac{(q;q)_{m_1+\cdots+m_r}}{\prod_{i=1}^r(q;q)_{m_i}}=\prod_{j=2}^r\begin{bmatrix}m_1+\cdots+m_j\\m_1+\cdots+m_{j-1}\end{bmatrix}_{q}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity289
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (r : ℕ) (m : Fin r → ℕ) (hr : 0 < r)
 (hden : (∏ i, poch q q (m i)) ≠ 0) :
 poch q q (∑ i, m i)/(∏ i, poch q q (m i)) =
 ∏ j ∈ (Finset.univ : Finset (Fin r)).filter (fun j => 1 ≤ j.val),
 gaussian q (∑ i ∈ Finset.univ.filter (· ≤ j), m i)
   (∑ i ∈ Finset.univ.filter (· < j), m i) := by
  sorry

end FiniteQBenchmark.Identity289
