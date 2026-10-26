import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-4.coeff — 基本级数有限系数差分
Original representative source: FINE-4.coeff
Frozen statement: formulas/train/FQI-SRC-FINE-4.coeff.md
Source formula:
c_n-c_{n-1}=\frac{(b-a)q^n}{1-aq^n}c_n.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity344
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (n : ℕ)
 (hn : 1 ≤ n)
 (h_domain : poch (b*q) q (n) ≠ 0 ∧
    poch (b*q) q (n-1) ≠ 0 ∧
    (1 - (a * (q^n))) ≠ 0) :
 ((fineC a b q (n)) - (fineC a b q (n-1))) = ((((b - a) * (q^n)) / (1 - (a * (q^n)))) * (fineC a b q (n))) := by
  sorry

end FiniteQBenchmark.Identity344
