import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-4.6 — 第一 q-Fibonacci 多项式递推
Original representative source: SILLS-4.6
Frozen statement: formulas/train/FQI-SRC-SILLS-4.6.md
Source formula:
D_n=D_{n-1}+q^{n-1}D_{n-2},\quad D_0=D_1=1.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity386
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ) (hn : 2 ≤ n) :
 schurD q n = schurD q (n-1)+q^(n-1)*schurD q (n-2) ∧ schurD q 0 = 1 ∧ schurD q 1 = 1 := by
  sorry

end FiniteQBenchmark.Identity386
