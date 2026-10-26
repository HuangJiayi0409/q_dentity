import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-8.46 — 硬六角 G 多项式三阶递推
Original representative source: AQ-8.46
Frozen statement: formulas/test/FQI-SRC-AQ-8.46.md
Source formula:
G_N(\sigma)=G_{N-1}(\sigma)+qG_{N-2}(\sigma)-(q-q^{N-1})G_{N-3}(\sigma),\quad G_0(0)=1,\ G_0(1)=0,\ G_1(\sigma)=1,\ G_2(0)=1+q,\ G_2(1)=1.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity324
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (sigma : Bool) (N : ℕ) (hN : 3 ≤ N) :
 aqG q sigma N = aqG q sigma (N-1)+q*aqG q sigma (N-2)-(q-q^(N-1))*aqG q sigma (N-3) ∧
 aqG q false 0 = 1 ∧ aqG q true 0 = 0 ∧ aqG q sigma 1 = 1 ∧
 aqG q false 2 = 1+q ∧ aqG q true 2 = 1 := by
  sorry

end FiniteQBenchmark.Identity324
