import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-8.32 — 硬六角 F 多项式递推
Original representative source: AQ-8.32
Frozen statement: formulas/train/FQI-SRC-AQ-8.32.md
Source formula:
F_N(\sigma;q)=F_{N-1}(\sigma;q)+q^{N-1}F_{N-2}(\sigma;q),\quad F_1(\sigma)=1,\quad F_2(0)=1+q,\ F_2(1)=1.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity321
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (sigma : Bool) (N : ℕ) (hN : 3 ≤ N) :
 aqF q sigma N = aqF q sigma (N-1)+q^(N-1)*aqF q sigma (N-2) ∧
 aqF q sigma 1 = 1 ∧ aqF q false 2 = 1+q ∧ aqF q true 2 = 1 := by
  sorry

end FiniteQBenchmark.Identity321
