import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-19.telescoping — Jackson 证明中的有限伸缩和
Original representative source: KAC-CHEUNG-19.telescoping
Frozen statement: formulas/test/FQI-SRC-KAC-CHEUNG-19.telescoping.md
Source formula:
(1-q)x\sum_{j=0}^Nq^j(D_qF)(q^jx)=F(x)-F(q^{N+1}x).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity435
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x : ℂ) (F : ℂ → ℂ) (N : ℕ) (hq : q ≠ 0) (hq1 : q ≠ 1) (hx : x ≠ 0) :
 (1-q)*x*(∑ j ∈ Finset.range (N+1), q^j*jackson q F (q^j*x)) = F x-F (q^(N+1)*x) := by
  sorry

end FiniteQBenchmark.Identity435
