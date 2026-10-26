import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.3.25 — 对称 q 指数的有限系数递推
Original representative source: GR2-1.3.25
Frozen statement: formulas/train/FQI-SRC-GR2-1.3.25.md
Source formula:
A_{n+1}=\frac{1-q}{1-q^{n+1}}q^{n/2}A_n,\quad A_0=1,\quad A_n=\frac{(1-q)^nq^{n(n-1)/4}}{(q;q)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity042
variable {K : Type*} [Field K]

theorem statement (q u : K) (A : PowerSeries K) (n : ℕ) (hq : regular q) (hu : u^2 = q)
 (hzero : PowerSeries.coeff 0 A = 1)
 (hIVP : PowerSeries.rescale u A - PowerSeries.rescale u⁻¹ A =
 PowerSeries.C (u-u⁻¹) * PowerSeries.X * A) :
 PowerSeries.coeff (n+1) A = (1-q)/(1-q^(n+1))*u^n*PowerSeries.coeff n A ∧
 PowerSeries.coeff 0 A = 1 ∧
 PowerSeries.coeff n A = (1-q)^n*u^(n*(n-1)/2)/poch q q n := by
  sorry

end FiniteQBenchmark.Identity042
