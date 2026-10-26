import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-3.9 — 有限 q 幂的交换与倒序
Original representative source: KAC-CHEUNG-3.9
Frozen statement: formulas/test/FQI-SRC-KAC-CHEUNG-3.9.md
Source formula:
P_n(a,x;q)=(-1)^nq^{n(n-1)/2}P_n(x,q^{1-n}a;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity417
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x a : K) (n : ℤ)
 (hq : q ≠ 0) (hq1 : q ≠ 1)
 (h_domain : kacPowerDefined a x q (n) ∧
    kacPowerDefined x (q^(1-n)*a) q (n)) :
 (kacPower a x q (n)) = (((-1:K)^n*q^(n*(n-1)/2)) * (kacPower x (q^(1-n)*a) q (n))) := by
  sorry

end FiniteQBenchmark.Identity417
