import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-42 — Gaussian 的终止参数表示
Original representative source: GR2-I-42
Frozen statement: formulas/train/FQI-SRC-GR2-I-42.md
Source formula:
\begin{bmatrix}n\\k\end{bmatrix}_q=(-q^n)^kq^{-k(k-1)/2}\frac{(q^{-n};q)_k}{(q;q)_k}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity240
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n k : ℕ)
 (hbase : regular q) (hk : k ≤ n)
 (h_domain : (pochList [q] q (k)) ≠ 0) :
 (gaussian q n k) = (((((-(q^(((n : ℤ)) : ℤ)))^k) * (q^((-(k : ℤ)*((k : ℤ)-1)/2) : ℤ))) * (pochList [(q^((-(n : ℤ)) : ℤ))] q (k))) / (pochList [q] q (k))) := by
  sorry

end FiniteQBenchmark.Identity240
