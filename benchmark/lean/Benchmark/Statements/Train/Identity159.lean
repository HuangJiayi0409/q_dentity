import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.1.4 — 任意序列的有限乘积展开
Original representative source: GR2-8.1.4
Frozen statement: formulas/train/FQI-SRC-GR2-8.1.4.md
Source formula:
\left[\sum_{j=0}^n\frac{(q^{-n},aq^n;q)_jB_j}{(q,b;q)_j}\right]\left[\sum_{k=0}^n\frac{(q^{-n},aq^n;q)_kC_k}{(q,c;q)_k}\right]=\sum_{m=0}^n(q^{-n},aq^n;q)_m\sum_{k=0}^m\frac{C_kq^{k^2-mk}}{(q,c;q)_k(q,b;q)_{m-k}}\sum_{j=0}^k\frac{(q^{-k},aq^m;q)_jB_{m-k+j}}{(q,bq^{m-k};q)_j}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity159
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c q : K) (n : ℕ) (B C : ℕ → K)
 (hbase : regular q) 
 (h_domain : ∀ j ∈ Finset.range (n+1), ((pochList [q,b] q (j)) ≠ 0) ∧
    ∀ k ∈ Finset.range (n+1), ((pochList [q,c] q (k)) ≠ 0) ∧
    ∀ m ∈ Finset.range (n+1), (∀ k ∈ Finset.range (m+1), (((pochList [q,c] q (k)) * (pochList [q,b] q (m-k))) ≠ 0 ∧
    ∀ j ∈ Finset.range (k+1), ((pochList [q,(b * (q^(((m : ℤ)-(k : ℤ)) : ℤ)))] q (j)) ≠ 0)))) :
 ((∑ j ∈ Finset.range (n+1), (((pochList [(q^((-(n : ℤ)) : ℤ)),(a * (q^(((n : ℤ)) : ℤ)))] q (j)) * (B j)) / (pochList [q,b] q (j)))) * (∑ k ∈ Finset.range (n+1), (((pochList [(q^((-(n : ℤ)) : ℤ)),(a * (q^(((n : ℤ)) : ℤ)))] q (k)) * (C k)) / (pochList [q,c] q (k))))) = (∑ m ∈ Finset.range (n+1), ((pochList [(q^((-(n : ℤ)) : ℤ)),(a * (q^(((n : ℤ)) : ℤ)))] q (m)) * (∑ k ∈ Finset.range (m+1), ((((C k) * (q^(((k : ℤ)*(k : ℤ)-(m : ℤ)*(k : ℤ)) : ℤ))) / ((pochList [q,c] q (k)) * (pochList [q,b] q (m-k)))) * (∑ j ∈ Finset.range (k+1), (((pochList [(q^((-(k : ℤ)) : ℤ)),(a * (q^(((m : ℤ)) : ℤ)))] q (j)) * (B (m-k+j))) / (pochList [q,(b * (q^(((m : ℤ)-(k : ℤ)) : ℤ)))] q (j)))))))) := by
  sorry

end FiniteQBenchmark.Identity159
