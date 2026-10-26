import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-PFAFF-SAALSCHUETZ — 终止 q-Pfaff–Saalschütz
Original representative source: GR2-II-12
Frozen statement: formulas/train/FQI-PFAFF-SAALSCHUETZ.md
Source formula:
{}_3\phi_2^{[n]}\!\left[\begin{matrix}a,b,q^{-n}\\c,abq^{1-n}/c\end{matrix};q,q\right]=\frac{(c/a,c/b;q)_n}{(c,c/(ab);q)_n}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity014
variable {K : Type*} [Field K]

theorem statement (a b c q : K) (n : ℕ) (hq : q ≠ 0)
    (ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0)
    (hleft : phiDefined [c, a*b*q^(1-(n : ℤ))/c] q n)
    (hright : pochList [c, c/(a*b)] q n ≠ 0) :
    phi [a,b,q^(-(n : ℤ))] [c,a*b*q^(1-(n : ℤ))/c] q q n =
      pochList [c/a,c/b] q n / pochList [c,c/(a*b)] q n := by
  sorry

end FiniteQBenchmark.Identity014
