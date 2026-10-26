import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.9.11 — 终止 q-Karlsson–Minton 消去
Original representative source: GR2-1.9.11
Frozen statement: formulas/train/FQI-SRC-GR2-1.9.11.md
Source formula:
{}_{r+1}\phi_r^{[n]}\!\left[\begin{matrix}q^{-n},b_1q^{m_1},\ldots,b_rq^{m_r}\\b_1,\ldots,b_r\end{matrix};q,q\right]=0.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity044
variable {K : Type*} [Field K]

theorem statement (q : K) (r n : ℕ) (bs : Fin r → K) (ms : Fin r → ℕ)
 (hq : regular q) (hn : (∑ i, ms i) < n) (hd : phiDefined (List.ofFn bs) q n) :
 phi (q^(-(n : ℤ)) :: List.ofFn (fun i => bs i*q^(ms i))) (List.ofFn bs) q q n = 0 := by
  sorry

end FiniteQBenchmark.Identity044
