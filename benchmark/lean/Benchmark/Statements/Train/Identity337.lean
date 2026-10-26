import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-10.32 — Euler 乘积指数的有限反求
Original representative source: AQ-10.32
Frozen statement: formulas/train/FQI-SRC-AQ-10.32.md
Source formula:
na_n=nb_n-\sum_{\substack{d\mid n\\d<n}}d\,a_d-\sum_{j=1}^{n-1}D_jb_{n-j},\qquad D_j=\sum_{d\mid j}d\,a_d.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity337
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a : ℕ → ℤ) (n : ℕ) (hn : 1 ≤ n) :
 (n:ℚ)*(a n:ℚ) = (n:ℚ)*eulerTransformCoeff a n -
 (∑ d ∈ n.divisors.filter (· < n), (d:ℚ)*(a d:ℚ)) -
 ∑ j ∈ Finset.Icc 1 (n-1), (divisorWeight a j:ℚ)*eulerTransformCoeff a (n-j) := by
  sorry

end FiniteQBenchmark.Identity337
