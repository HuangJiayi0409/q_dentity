import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-3.4.4 — major index（原书 greater index）的 q-多项系数生成式
Original representative source: AP-3.4.4
Frozen statement: formulas/train/FQI-SRC-AP-3.4.4.md
Source formula:
\sum_{s=0}^{S}\operatorname{ind}(m_1,\ldots,m_r;s)q^s=\frac{(q;q)_{m_1+\cdots+m_r}}{\prod_{i=1}^r(q;q)_{m_i}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity276
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (r : ℕ) (m : Fin r → ℕ)
 (hr : 0 < r)
 (h_domain : (∏ i, poch q q (m i)) ≠ 0) :
 (∑ s ∈ Finset.range (pairMultiplicity m+1), (((wordStatisticCount m wordIndex s : ℕ) : K) * (q^s))) = ((pochList [q] q (∑ i, m i)) / (∏ i, poch q q (m i))) := by
  sorry

end FiniteQBenchmark.Identity276
