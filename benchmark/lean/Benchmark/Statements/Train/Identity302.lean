import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-4.2.COMPOSITIONS — 有界有序组成的有限生成多项式
Original representative source: AP-4.2.COMPOSITIONS
Frozen statement: formulas/train/FQI-SRC-AP-4.2.COMPOSITIONS.md
Source formula:
\sum_{n=M}^{MN}c(N,M,n)q^n=\left(\sum_{j=1}^{N}q^j\right)^M.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity302
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (N M : ℕ) (hN : 0 < N) (hM : 0 < M) :
 (∑ n ∈ Finset.Icc M (M*N), (boundedCompositionCount N M n : K)*q^n) =
 (∑ j ∈ Finset.Icc 1 N, q^j)^M := by
  sorry

end FiniteQBenchmark.Identity302
