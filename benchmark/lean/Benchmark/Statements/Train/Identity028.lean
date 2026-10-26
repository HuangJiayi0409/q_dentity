import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-GOLLNITZ-ORDER4 — Göllnitz 四阶递推
Original representative source: AQ-10.21
Frozen statement: formulas/train/FQI-GOLLNITZ-ORDER4.md
Source formula:
\begin{aligned}d_{6n-1}(t)={}&(1+tq^{6n}(q^{-1}+q^{-2}+q^{-4}))d_{6n-7}(t)\\&+t^2q^{6n}(q^{-3}+q^{-5}+q^{-6})(1-q^{6n-6})d_{6n-13}(t)\\&+t^3q^{12n-13}(t(q^{-1}+q^{-2}+q^{-4})+q^{6n-12})d_{6n-19}(t)+t^6q^{18n-32}d_{6n-25}(t).\end{aligned}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity028
variable {K : Type*} [Field K]

theorem statement (t q : K) (n : ℤ) (hn : 3 ≤ n) (hq : q ≠ 0) :
 gollnitz t q (6*n-1) =
 (1+t*q^(6*n)*(q^(-1 : ℤ)+q^(-2 : ℤ)+q^(-4 : ℤ)))*gollnitz t q (6*n-7) +
 t^2*q^(6*n)*(q^(-3 : ℤ)+q^(-5 : ℤ)+q^(-6 : ℤ))*(1-q^(6*n-6))*gollnitz t q (6*n-13) +
 t^3*q^(12*n-13)*(t*(q^(-1 : ℤ)+q^(-2 : ℤ)+q^(-4 : ℤ))+q^(6*n-12))*gollnitz t q (6*n-19) +
 t^6*q^(18*n-32)*gollnitz t q (6*n-25) := by
  sorry

end FiniteQBenchmark.Identity028
