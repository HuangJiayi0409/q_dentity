import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.1.2 — 成对有限积的线性化
Original representative source: GR2-8.1.2
Frozen statement: formulas/train/FQI-SRC-GR2-8.1.2.md
Source formula:
(t,a/t;q)_j(t,a/t;q)_k=(q;q)_j(q;q)_k(a;q)_{j+k}\sum_{m=\max(j,k)}^{j+k}\frac{(t,a/t;q)_m(-1)^{j+k+m}q^{\binom j2+\binom k2+\binom{m+1}2-m(j+k)}}{(a;q)_m(q;q)_{m-j}(q;q)_{m-k}(q;q)_{j+k-m}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity158
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (t a q : K) (j k : ℕ)
 (hbase : regular q) (ht : t ≠ 0)
 (h_domain : t ≠ 0 ∧
    ∀ m ∈ Finset.Icc (max j k) (j+k), (t ≠ 0 ∧
    ((((pochList [a] q (m)) * (pochList [q] q (m-j))) * (pochList [q] q (m-k))) * (pochList [q] q (j+k-m))) ≠ 0)) :
 ((pochList [t,(a / t)] q (j)) * (pochList [t,(a / t)] q (k))) = ((((pochList [q] q (j)) * (pochList [q] q (k))) * (pochList [a] q (j+k))) * (∑ m ∈ Finset.Icc (max j k) (j+k), ((((pochList [t,(a / t)] q (m)) * ((-1:K)^(((j : ℤ)+(k : ℤ)+(m : ℤ)) : ℤ))) * (q^(((j : ℤ)*((j : ℤ)-1)/2+(k : ℤ)*((k : ℤ)-1)/2+(m : ℤ)*((m : ℤ)+1)/2-(m : ℤ)*((j : ℤ)+(k : ℤ))) : ℤ))) / ((((pochList [a] q (m)) * (pochList [q] q (m-j))) * (pochList [q] q (m-k))) * (pochList [q] q (j+k-m)))))) := by
  sorry

end FiniteQBenchmark.Identity158
