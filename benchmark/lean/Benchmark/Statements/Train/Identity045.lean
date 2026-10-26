import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.9.12 — 单位自变量的终止 q-Karlsson–Minton
Original representative source: GR2-1.9.12
Frozen statement: formulas/train/FQI-SRC-GR2-1.9.12.md
Source formula:
{}_{r+1}\phi_r^{[n]}\!\left[\begin{matrix}q^{-n},b_1q^{m_1},\ldots,b_rq^{m_r}\\b_1,\ldots,b_r\end{matrix};q,1\right]=\frac{(-1)^n(q;q)_nq^{-n(n+1)/2}}{\prod_{i=1}^r(b_i;q)_{m_i}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity045
variable {K : Type*} [Field K]

theorem statement (q : K) (r n : ℕ) (bs : Fin r → K) (ms : Fin r → ℕ)
 (hq : regular q) (hn : (∑ i, ms i) ≤ n) (hd : phiDefined (List.ofFn bs) q n)
 (hr : ∀ i, poch (bs i) q (ms i) ≠ 0) :
 phi (q^(-(n : ℤ)) :: List.ofFn (fun i => bs i*q^(ms i))) (List.ofFn bs) q 1 n =
 (-1)^n*poch q q n*q^(-((n : ℤ)*(n+1)/2)) / ∏ i, poch (bs i) q (ms i) := by
  sorry

end FiniteQBenchmark.Identity045
