import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.9.9-finite — 边界长度的 q-Karlsson–Minton 求值
Original representative source: GR2-1.9.9-finite
Frozen statement: formulas/train/FQI-SRC-GR2-1.9.9-finite.md
Source formula:
{}_{r+1}\phi_r^{[M]}\!\left[\begin{matrix}q^{-M},b_1q^{m_1},\ldots,b_rq^{m_r}\\b_1,\ldots,b_r\end{matrix};q,q\right]=(-1)^M(q;q)_M\prod_{i=1}^r\frac{b_i^{m_i}q^{m_i(m_i-1)/2}}{(b_i;q)_{m_i}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity046
variable {K : Type*} [Field K]

theorem statement (q : K) (r : ℕ) (bs : Fin r → K) (ms : Fin r → ℕ)
 (hq : regular q) (hd : phiDefined (List.ofFn bs) q (∑ i, ms i))
 (hr : ∀ i, poch (bs i) q (ms i) ≠ 0) :
 phi (q^(-((∑ i, ms i : ℕ) : ℤ)) :: List.ofFn (fun i => bs i*q^(ms i)))
 (List.ofFn bs) q q (∑ i, ms i) =
 (-1)^(∑ i, ms i)*poch q q (∑ i, ms i) *
 ∏ i, (bs i)^(ms i)*q^(ms i*(ms i-1)/2)/poch (bs i) q (ms i) := by
  sorry

end FiniteQBenchmark.Identity046
