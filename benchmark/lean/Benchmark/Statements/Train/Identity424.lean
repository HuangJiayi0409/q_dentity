import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-5.1 — 有限 q 幂的高阶导数
Original representative source: KAC-CHEUNG-5.1
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-5.1.md
Source formula:
D_q^jP_n(x,-a;q)=\frac{[n]_q!}{[n-j]_q!}P_{n-j}(x,-a;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity424
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x a : ℂ) (n j : ℕ) (hq : q ≠ 0) (hq1 : q ≠ 1) (hj : j ≤ n) (hden : qFactorial q (n-j) ≠ 0) :
 ((jackson q)^[j]) (fun y => kacPowerNat y (-a) q n) x =
 qFactorial q n/qFactorial q (n-j)*kacPowerNat x (-a) q (n-j) := by
  sorry

end FiniteQBenchmark.Identity424
