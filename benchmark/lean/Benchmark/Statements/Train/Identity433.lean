import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-14.higher — 第二变量有限 q 幂的高阶导数
Original representative source: KAC-CHEUNG-14.higher
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-14.higher.md
Source formula:
D_q^jP_n(1,-x;q)=q^{j(j-1)/2}\frac{[n]_q!}{[n-j]_q!}P_{n-j}(1,-q^jx;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity433
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x : ℂ) (n j : ℕ) (hq : q ≠ 0) (hq1 : q ≠ 1) (hj : j ≤ n) (hden : qFactorial q (n-j) ≠ 0) :
 ((jackson q)^[j]) (fun y => kacPowerNat 1 (-y) q n) x =
 q^(j*(j-1)/2)*(qFactorial q n/qFactorial q (n-j))*kacPowerNat 1 (-q^j*x) q (n-j) := by
  sorry

end FiniteQBenchmark.Identity433
