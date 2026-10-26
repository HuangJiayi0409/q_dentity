import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-4.3 — Bn有限常数项恒等式（Conjecture4.3修订）
Original representative source: AQ-4.3
Frozen statement: formulas/train/FQI-SRC-AQ-4.3.md
Source formula:
\operatorname{CT}_{x_1,\ldots,x_n}\left[\prod_{i=1}^n(x_i,q/x_i;q)_a\prod_{i<j}(x_ix_j,q/(x_ix_j),x_i/x_j,qx_j/x_i;q)_b\right]=\frac{(q;q)_{nb}}{(q;q)_b^n}\prod_{j=0}^{n-1}\frac{(q;q)_{2a+2jb}(q;q)_{2jb}}{(q;q)_{a+(n+j-1)b}(q;q)_{a+jb}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity341
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n a b : ℕ)
 (hn : 1 ≤ n)
 (h_domain : ((pochList [q] q (b))^n) ≠ 0 ∧
    ∀ j ∈ Finset.range (n), (((pochList [q] q (a+(n+j-1)*b)) * (pochList [q] q (a+j*b))) ≠ 0)) :
 ((bnProduct q n a b).coeff 0) = (((pochList [q] q (n*b)) / ((pochList [q] q (b))^n)) * (∏ j ∈ Finset.range (n), (((pochList [q] q (2*a+2*j*b)) * (pochList [q] q (2*j*b))) / ((pochList [q] q (a+(n+j-1)*b)) * (pochList [q] q (a+j*b)))))) := by
  sorry

end FiniteQBenchmark.Identity341
