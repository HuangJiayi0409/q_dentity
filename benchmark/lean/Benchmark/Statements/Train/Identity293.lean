import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-9.3.8 — 空矩形的振荡初值
Original representative source: AP-9.3.8
Frozen statement: formulas/train/FQI-SRC-AP-9.3.8.md
Source formula:
P_{k,i}(0,b;\mu;q)=P_{k,i}(a,0;\mu;q)=M_{k,i}(0,b;\mu;q)=M_{k,i}(a,0;\mu;q)=0.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity293
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (k i a b mu : ℕ) (hi : 1 ≤ i) (hki : i ≤ k) (hm : 1 ≤ mu) :
 (oscillationPoly q true k i (0) (b) (mu)) = 0 ∧ (oscillationPoly q true k i (a) (0) (mu)) = 0 ∧
 (oscillationPoly q false k i (0) (b) (mu)) = 0 ∧ (oscillationPoly q false k i (a) (0) (mu)) = 0 := by
  sorry

end FiniteQBenchmark.Identity293
