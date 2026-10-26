import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-CHU-VANDERMONDE-Q — q-Chu–Vandermonde：自变量 q
Original representative source: GR2-II-06
Frozen statement: formulas/train/FQI-CHU-VANDERMONDE-Q.md
Source formula:
{}_2\phi_1^{[n]}\!\left[\begin{matrix}a,q^{-n}\\c\end{matrix};q,q\right]=a^n\frac{(c/a;q)_n}{(c;q)_n}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity012
variable {K : Type*} [Field K]

theorem statement (a c q : K) (n : ℕ) (hq : q ≠ 0) (ha : a ≠ 0)
    (hden : phiDefined [c] q n) :
    phi [a, q ^ (-(n : ℤ))] [c] q q n =
      a^n * poch (c/a) q n / poch c q n := by
  sorry

end FiniteQBenchmark.Identity012
