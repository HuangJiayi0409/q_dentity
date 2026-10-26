import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SEARS-4PHI3-II — Sears 平衡 4φ3 第二形式
Original representative source: GR2-III-16
Frozen statement: formulas/train/FQI-SEARS-4PHI3-II.md
Source formula:
{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},a,b,c\\d,e,f\end{matrix};q,q\right]=\frac{(a,ef/(ab),ef/(ac);q)_n}{(e,f,ef/(abc);q)_n}{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},e/a,f/a,ef/(abc)\\ef/(ab),ef/(ac),q^{1-n}/a\end{matrix};q,q\right]
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity017
variable {K : Type*} [Field K]

theorem statement (a b c d e f q : K) (n : ℕ) (hq : q ≠ 0)
 (hp : ∀ x ∈ [a,b,c,e,f], x ≠ 0)
 (hbal : d*e*f = a*b*c*q^(1-(n : ℤ)))
 (hl : phiDefined [d,e,f] q n)
 (hr : phiDefined [e*f/(a*b),e*f/(a*c),q^(1-(n : ℤ))/a] q n)
 (hf : pochList [e,f,e*f/(a*b*c)] q n ≠ 0) :
 phi [q^(-(n : ℤ)),a,b,c] [d,e,f] q q n =
 pochList [a,e*f/(a*b),e*f/(a*c)] q n / pochList [e,f,e*f/(a*b*c)] q n *
 phi [q^(-(n : ℤ)),e/a,f/a,e*f/(a*b*c)] [e*f/(a*b),e*f/(a*c),q^(1-(n : ℤ))/a] q q n := by
  sorry

end FiniteQBenchmark.Identity017
