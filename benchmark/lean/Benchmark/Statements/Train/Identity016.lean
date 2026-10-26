import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-WATSON-8PHI7 — Watson 终止 8φ7→4φ3
Original representative source: GR2-III-18
Frozen statement: formulas/train/FQI-WATSON-8PHI7.md
Source formula:
W_8^{[n]}(a;b,c,d,e,q^{-n};q,a^2q^{n+2}/(bcde))=\frac{(aq,aq/(de);q)_n}{(aq/d,aq/e;q)_n}{}_4\phi_3^{[n]}\!\left[\begin{matrix}aq/(bc),d,e,q^{-n}\\aq/b,aq/c,deq^{-n}/a\end{matrix};q,q\right]
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity016
variable {K : Type*} [Field K]

theorem statement (a b c d e q : K) (n : ℕ) (hq : q ≠ 0) (ha1 : a ≠ 1)
 (hp : ∀ x ∈ [a,b,c,d,e], x ≠ 0)
 (hl : phiDefined [a*q/b,a*q/c,a*q/d,a*q/e,a*q^(n+1)] q n)
 (hr : phiDefined [a*q/b,a*q/c,d*e*q^(-(n : ℤ))/a] q n)
 (hf : pochList [a*q/d,a*q/e] q n ≠ 0) :
 wellPoisedRaw a [b,c,d,e,q^(-(n : ℤ))] q (a^2*q^(n+2)/(b*c*d*e)) n =
 pochList [a*q,a*q/(d*e)] q n / pochList [a*q/d,a*q/e] q n *
 phi [a*q/(b*c),d,e,q^(-(n : ℤ))] [a*q/b,a*q/c,d*e*q^(-(n : ℤ))/a] q q n := by
  sorry

end FiniteQBenchmark.Identity016
