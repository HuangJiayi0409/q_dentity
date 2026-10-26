import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-GOLLNITZ-SHIFT — Göllnitz 参数移位
Original representative source: AQ-10.18
Frozen statement: formulas/train/FQI-GOLLNITZ-SHIFT.md
Source formula:
d_{6n+3}(t)-tq^{6n+2}d_{6n-3}(t)=(1+tq^2)(1+tq^4)(1+tq^5)d_{6n-7}(tq^6).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity027
variable {K : Type*} [Field K]

theorem statement (t q : K) (n : ℤ) (hn : 1 ≤ n) :
 gollnitz t q (6*n+3)-t*q^(6*n+2)*gollnitz t q (6*n-3) =
 (1+t*q^2)*(1+t*q^4)*(1+t*q^5)*gollnitz (t*q^6) q (6*n-7) := by
  sorry

end FiniteQBenchmark.Identity027
