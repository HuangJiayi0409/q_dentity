import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.3.2 — 终止 Bailey–Daum 的有限积求值
Original representative source: GR2-2.3.2
Frozen statement: formulas/train/FQI-SRC-GR2-2.3.2.md
Source formula:
{}_2\phi_1^{[m]}(A,q^{-m};Aq^{m+1};q,-q^{m+1})=(-q;q)_m\frac{(Aq;q^2)_{\ell}}{(Aq^{2\lfloor m/2\rfloor+2};q^2)_{\ell}},\quad\ell=\lceil m/2\rceil.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity064
variable {K : Type*} [Field K]

theorem statement (a q : K) (m : ℕ) (hq : regular q)
 (hl : phiDefined [a*q^(m+1)] q m)
 (hr : poch (a*q^(2*(m/2)+2)) (q^2) ((m+1)/2) ≠ 0) :
 phi [a,q^(-(m : ℤ))] [a*q^(m+1)] q (-q^(m+1)) m =
 poch (-q) q m * poch (a*q) (q^2) ((m+1)/2) /
 poch (a*q^(2*(m/2)+2)) (q^2) ((m+1)/2) := by
  sorry

end FiniteQBenchmark.Identity064
