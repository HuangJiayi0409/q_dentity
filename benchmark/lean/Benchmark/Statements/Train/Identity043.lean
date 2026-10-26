import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.9.10 — 终止 q-Karlsson–Minton 求和
Original representative source: GR2-1.9.10
Frozen statement: formulas/train/FQI-SRC-GR2-1.9.10.md
Source formula:
{}_{r+2}\phi_{r+1}^{[n]}\!\left[\begin{matrix}q^{-n},b,b_1q^{m_1},\ldots,b_rq^{m_r}\\bq,b_1,\ldots,b_r\end{matrix};q,q\right]=\frac{b^n(q;q)_n}{(bq;q)_n}\prod_{i=1}^r\frac{(b_i/b;q)_{m_i}}{(b_i;q)_{m_i}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity043
variable {K : Type*} [Field K]

theorem statement (q b : K) (r n : ℕ) (bs : Fin r → K) (ms : Fin r → ℕ)
 (hq : regular q) (hb : b ≠ 0) (hn : (∑ i, ms i) ≤ n)
 (hd : phiDefined (b*q :: List.ofFn bs) q n)
 (hr : ∀ i, poch (bs i) q (ms i) ≠ 0) :
 phi (q^(-(n : ℤ)) :: b :: List.ofFn (fun i => bs i*q^(ms i)))
 (b*q :: List.ofFn bs) q q n =
 b^n*poch q q n/poch (b*q) q n * ∏ i, poch (bs i/b) q (ms i)/poch (bs i) q (ms i) := by
  sorry

end FiniteQBenchmark.Identity043
