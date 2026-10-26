import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-GOLLNITZ-ELIMINATION — Göllnitz 消元式
Original representative source: AQ-10.23
Frozen statement: formulas/test/FQI-GOLLNITZ-ELIMINATION.md
Source formula:
\begin{aligned}d_{6n+3}(t)-tq^{6n+2}d_{6n-3}(t)={}&d_{6n+5}(t)-tq^{6n+2}(1+q^2+q^3)d_{6n-1}(t)\\&+t^2q^{12n}(1+q+q^3)d_{6n-7}(t)-t^3q^{18n-7}d_{6n-13}(t).\end{aligned}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity029
variable {K : Type*} [Field K]

theorem statement (t q : K) (n : ℤ) (hn : 2 ≤ n) :
 gollnitz t q (6*n+3)-t*q^(6*n+2)*gollnitz t q (6*n-3) =
 gollnitz t q (6*n+5)-t*q^(6*n+2)*(1+q^2+q^3)*gollnitz t q (6*n-1) +
 t^2*q^(12*n)*(1+q+q^3)*gollnitz t q (6*n-7)-t^3*q^(18*n-7)*gollnitz t q (6*n-13) := by
  sorry

end FiniteQBenchmark.Identity029
