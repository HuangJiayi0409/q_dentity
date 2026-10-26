import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.Ex4-odd — 有限 3φ1 的奇数消去
Original representative source: GR2-3.Ex4-odd
Frozen statement: formulas/train/FQI-SRC-GR2-3.Ex4-odd.md
Source formula:
\sum_{k=0}^{2m+1}\frac{(q^{-2m-1},b,-b;q)_k}{(q,b^2;q)_k}q^{(2m+1)k-k(k-1)/2}=0.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity108
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (b q : K) (m : ℕ)
 (hbase : regular q) 
 (h_domain : ∀ k ∈ Finset.range (2*m+1+1), ((pochList [q,(b * b)] q (k)) ≠ 0)) :
 (∑ k ∈ Finset.range (2*m+1+1), (((pochList [(q^((-2*(m : ℤ)-1) : ℤ)),b,(-b)] q (k)) / (pochList [q,(b * b)] q (k))) * (q^(((2*(m : ℤ)+1)*(k : ℤ)-(k : ℤ)*((k : ℤ)-1)/2) : ℤ)))) = 0 := by
  sorry

end FiniteQBenchmark.Identity108
