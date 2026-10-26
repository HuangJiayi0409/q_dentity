import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-5.6-8 — Motivated proof 中的有限系数多项式递推
Original representative source: SILLS-5.6-8
Frozen statement: formulas/test/FQI-SRC-SILLS-5.6-8.md
Source formula:
A_{i+1}=A_i+B_i,\quad B_{i+1}=q^iA_i,\quad A_3=1,\ B_3=0;\qquad A_{i+1}=A_i+q^{i-1}A_{i-1}\ (i\ge4).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity410
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (i : ℕ) (hi : 3 ≤ i) :
 motivatedA q (i+1)=motivatedA q i+motivatedB q i ∧
 motivatedB q (i+1)=q^i*motivatedA q i ∧
 motivatedA q 3=1 ∧ motivatedB q 3=0 ∧ motivatedA q 4=1 ∧
 (4 ≤ i → motivatedA q (i+1)=motivatedA q i+q^(i-1)*motivatedA q (i-1)) := by
  sorry

end FiniteQBenchmark.Identity410
