import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-26.10 — 对称有限 q 幂的降阶导数
Original representative source: KAC-CHEUNG-26.10
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-26.10.md
Source formula:
\widetilde D_qS_n(x,a;q)=\langle n\rangle_qS_{n-1}(x,a;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity439
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x a : ℂ) (n : ℕ) (hq : q ≠ 0) (hq2 : q^2 ≠ 1) (hn : 1 ≤ n) :
 symJackson q (fun y => symPower y a q n) x = symNumber q n*symPower x a q (n-1) := by
  sorry

end FiniteQBenchmark.Identity439
