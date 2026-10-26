import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-10.27 — Göllnitz 递推算子的相容关系
Original representative source: AQ-10.27
Frozen statement: formulas/test/FQI-SRC-AQ-10.27.md
Source formula:
\begin{aligned}\mathcal F(n-1,tq^6;G_n,G_{n-1},G_{n-2},G_{n-3},G_{n-4})={}&J_{n+1}-tq^{6n-6}(q^2+q^4+q^5)J_n\\&+t^2q^{12n-12}(1+q+q^3)J_{n-1}-t^3q^{18n-25}J_{n-2}.\end{aligned}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity335
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q t : K) (n : ℤ) (hn : 5 ≤ n) (hq : q ≠ 0) (d : ℤ → K) :
 aqOperator q (t*q^6) (n-1) (aqOperatorG q t d n) (aqOperatorG q t d (n-1))
 (aqOperatorG q t d (n-2)) (aqOperatorG q t d (n-3)) (aqOperatorG q t d (n-4)) =
 aqJ q t d (n+1)-t*q^(6*n-6)*(q^2+q^4+q^5)*aqJ q t d n +
 t^2*q^(12*n-12)*(1+q+q^3)*aqJ q t d (n-1)-t^3*q^(18*n-25)*aqJ q t d (n-2) := by
  sorry

end FiniteQBenchmark.Identity335
