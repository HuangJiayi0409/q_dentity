import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex6i — 双步长终止 2φ1 求和
Original representative source: GR2-1.Ex6i
Frozen statement: formulas/test/FQI-SRC-GR2-1.Ex6i.md
Source formula:
{}_2\phi_1^{[\lfloor n/2\rfloor]}\!\left[\begin{matrix}q^{-n},q^{1-n}\\qb^2\end{matrix};q^2,q^2\right]=\frac{(b^2;q^2)_n}{(b^2;q)_n}q^{-n(n-1)/2}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity052
variable {K : Type*} [Field K]

theorem statement (b q : K) (n : ℕ) (hq : regular q)
 (hd : phiDefined [q*b^2] (q^2) (n/2)) (hr : poch (b^2) q n ≠ 0) :
 phi [q^(-(n : ℤ)),q^(1-(n : ℤ))] [q*b^2] (q^2) (q^2) (n/2) =
 poch (b^2) (q^2) n/poch (b^2) q n*q^(-((n : ℤ)*(n-1)/2)) := by
  sorry

end FiniteQBenchmark.Identity052
