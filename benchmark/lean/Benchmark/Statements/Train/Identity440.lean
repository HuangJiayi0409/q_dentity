import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-26.12 — 对称有限 q 二项式定理
Original representative source: KAC-CHEUNG-26.12
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-26.12.md
Source formula:
S_n(x,-a;q)=\sum_{j=0}^n\left\langle{n\atop j}\right\rangle_q a^{n-j}x^j.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity440
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x a : K) (n : ℕ) (hq : q ≠ 0) (hq2 : q^2 ≠ 1)
 (hden : ∀ j ≤ n, symFactorial q j*symFactorial q (n-j) ≠ 0) :
 symPower x (-a) q n = ∑ j ∈ Finset.range (n+1), symGaussian q n j*a^(n-j)*x^j := by
  sorry

end FiniteQBenchmark.Identity440
