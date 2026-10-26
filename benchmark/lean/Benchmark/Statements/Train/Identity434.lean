import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-15.cancellation — 双边求和证明中的有限乘积消去
Original representative source: KAC-CHEUNG-15.cancellation
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-15.cancellation.md
Source formula:
\frac{(q/(ax);q)_{M-1}x^{M-1}}{(q^{1-M}ax;q)_{M-1}}=(-1)^{M-1}q^{M(M-1)/2}a^{1-M}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity434
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q a x : K) (M : ℕ)
 (hq : q ≠ 0) (hq1 : q ≠ 1) (hM : 1 ≤ M) (hax : a*x ≠ 0)
 (h_domain : (a * x) ≠ 0 ∧
    (pochList [(((q^((1-(M : ℤ)) : ℤ)) * a) * x)] q (M-1)) ≠ 0) :
 (((pochList [(q / (a * x))] q (M-1)) * (x^(M-1))) / (pochList [(((q^((1-(M : ℤ)) : ℤ)) * a) * x)] q (M-1))) = ((((-1:K)^(M-1)) * (q^(M*(M-1)/2))) * (a^(1-(M:ℤ)))) := by
  sorry

end FiniteQBenchmark.Identity434
