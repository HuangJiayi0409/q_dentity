import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-TERMINATING-6PHI5 — 终止 very-well-poised 6φ5
Original representative source: GR2-II-21
Frozen statement: formulas/train/FQI-TERMINATING-6PHI5.md
Source formula:
W_6^{[n]}(a;b,c,q^{-n};q,aq^{n+1}/(bc))=\frac{(aq,aq/(bc);q)_n}{(aq/b,aq/c;q)_n}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity015
variable {K : Type*} [Field K]

theorem statement (a b c q : K) (n : ℕ) (hq : q ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0)
 (hl : phiDefined [a*q/b,a*q/c,a*q^(n+1)] q n)
 (hr : pochList [a*q/b,a*q/c] q n ≠ 0) :
 wellPoised a [b,c,q^(-(n : ℤ))] q (a*q^(n+1)/(b*c)) n =
 pochList [a*q,a*q/(b*c)] q n / pochList [a*q/b,a*q/c] q n := by
  sorry

end FiniteQBenchmark.Identity015
