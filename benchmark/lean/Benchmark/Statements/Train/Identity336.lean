import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-10.30 — Euler 乘积系数的有限递推
Original representative source: AQ-10.30
Frozen statement: formulas/train/FQI-SRC-AQ-10.30.md
Source formula:
b_0=1,\quad D_j=\sum_{d\mid j}d\,a_d,\quad nb_n=\sum_{j=1}^nD_jb_{n-j}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity336
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a : ℕ → ℤ) (n : ℕ) (hn : 1 ≤ n) :
 eulerTransformCoeff a 0 = 1 ∧ (n:ℚ)*eulerTransformCoeff a n =
 ∑ j ∈ Finset.Icc 1 n, (divisorWeight a j : ℚ)*eulerTransformCoeff a (n-j) := by
  sorry

end FiniteQBenchmark.Identity336
