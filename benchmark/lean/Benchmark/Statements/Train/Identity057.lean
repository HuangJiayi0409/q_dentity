import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex29 — 连续 q 超球多项式的两种终止表示
Original representative source: GR2-1.Ex29
Frozen statement: formulas/train/FQI-SRC-GR2-1.Ex29.md
Source formula:
C_n((t+t^{-1})/2;\beta\mid q)=\frac{(\beta;q)_nt^n}{(q;q)_n}{}_2\phi_1^{[n]}\!\left[\begin{matrix}q^{-n},\beta\\\beta^{-1}q^{1-n}\end{matrix};q,q/(\beta t^2)\right]=\frac{(\beta^2;q)_nt^{-n}\beta^{-n}}{(q;q)_n}{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},\beta,\beta t^2\\\beta^2,0\end{matrix};q,q\right].
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity057
variable {K : Type*} [Field K]

theorem statement (beta t q : K) (n : ℕ) (hq : regular q) (hb : beta ≠ 0) (ht : t ≠ 0)
 (hl : phiDefined [beta⁻¹*q^(1-(n : ℤ))] q n)
 (hr : phiDefined [beta^2,0] q n) :
 ultraspherical beta t q n =
 poch beta q n*t^n/poch q q n *
 phi [q^(-(n : ℤ)),beta] [beta⁻¹*q^(1-(n : ℤ))] q (q/(beta*t^2)) n ∧
 ultraspherical beta t q n =
 poch (beta^2) q n*t^(-(n : ℤ))*beta^(-(n : ℤ))/poch q q n *
 phi [q^(-(n : ℤ)),beta,beta*t^2] [beta^2,0] q q n := by
  sorry

end FiniteQBenchmark.Identity057
