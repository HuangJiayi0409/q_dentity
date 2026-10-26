import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-5.Ex19ii — Gaussian 立方的奇数上指标有限和
Original representative source: GR2-5.Ex19ii
Frozen statement: formulas/train/FQI-SRC-GR2-5.Ex19ii.md
Source formula:
\sum_{k=-n-1}^n(-1)^k\begin{bmatrix}2n+1\\n+k+1\end{bmatrix}_q^3q^{k(3k+1)/2}=\frac{(q;q)_{3n+1}}{(q;q)_n^3}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity123
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ)
 (hbase : regular q) 
 (h_domain : ((pochList [q] q (n))^3) ≠ 0) :
 (∑ k ∈ Finset.Icc (-(n:ℤ)-1) ((n:ℤ)), ((((-1:K)^(((k : ℤ)) : ℤ)) * ((gaussianInt q (2*(n : ℤ)+1) ((n : ℤ)+(k : ℤ)+1))^3)) * (q^(((k : ℤ)*(3*(k : ℤ)+1)/2) : ℤ)))) = ((pochList [q] q (3*n+1)) / ((pochList [q] q (n))^3)) := by
  sorry

end FiniteQBenchmark.Identity123
