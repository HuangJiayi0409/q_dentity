import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-2.3 — 基本级数有限系数比递推
Original representative source: FINE-2.3
Frozen statement: formulas/train/FQI-SRC-FINE-2.3.md
Source formula:
(1-bq^{n+1})c_{n+1}=(1-aq^{n+1})c_n.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity343
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (n : ℕ)
 
 (h_domain : poch (b*q) q (n+1) ≠ 0 ∧
    poch (b*q) q (n) ≠ 0) :
 ((1 - (b * (q^(n+1)))) * (fineC a b q (n+1))) = ((1 - (a * (q^(n+1)))) * (fineC a b q (n))) := by
  sorry

end FiniteQBenchmark.Identity343
