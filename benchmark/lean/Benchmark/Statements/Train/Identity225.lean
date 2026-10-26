import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-12 — 终止参数 q^{-n} 的乘积
Original representative source: GR2-I-12
Frozen statement: formulas/train/FQI-SRC-GR2-I-12.md
Source formula:
(q^{-n};q)_k=(-1)^kq^{k(k-1)/2-nk}\frac{(q;q)_n}{(q;q)_{n-k}}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity225
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n k : ℕ)
 (hbase : regular q) (hk : k ≤ n)
 (h_domain : (pochList [q] q (n-k)) ≠ 0) :
 (pochList [(q^((-(n : ℤ)) : ℤ))] q (k)) = (((((-1 : K)^k) * (q^(((k : ℤ)*((k : ℤ)-1)/2-(n : ℤ)*(k : ℤ)) : ℤ))) * (pochList [q] q (n))) / (pochList [q] q (n-k))) := by
  sorry

end FiniteQBenchmark.Identity225
