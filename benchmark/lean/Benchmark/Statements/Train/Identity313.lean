import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-3.23 — Bailey 转置求和（有限支持特化）
Original representative source: AQ-3.23
Frozen statement: formulas/train/FQI-SRC-AQ-3.23.md
Source formula:
\sum_{n=0}^N\alpha_n\sum_{r=n}^N\delta_r u_{r-n}v_{r+n}=\sum_{r=0}^N\delta_r\sum_{n=0}^r\alpha_n u_{r-n}v_{r+n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity313
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement {R : Type*} [CommRing R] (N : ℕ) (alpha delta u v : ℕ → R) :
 (∑ n ∈ Finset.range (N+1), alpha n * ∑ r ∈ Finset.Icc n N, delta r*u (r-n)*v (r+n)) =
 ∑ r ∈ Finset.range (N+1), delta r * ∑ n ∈ Finset.range (r+1), alpha n*u (r-n)*v (r+n) := by
  sorry

end FiniteQBenchmark.Identity313
