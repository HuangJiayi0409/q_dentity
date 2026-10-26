import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-10 — 长度 n−k 的反向改写
Original representative source: GR2-I-10
Frozen statement: formulas/train/FQI-SRC-GR2-I-10.md
Source formula:
(a;q)_{n-k}=\frac{(-q/a)^kq^{k(k-1)/2-nk}(a;q)_n}{(q^{1-n}/a;q)_k}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity223
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n k : ℕ)
 (hbase : regular q) (hk : k ≤ n) (ha : a ≠ 0)
 (h_domain : a ≠ 0 ∧
    (pochList [((q^((1-(n : ℤ)) : ℤ)) / a)] q (k)) ≠ 0) :
 (pochList [a] q (n-k)) = ((((((-q) / a)^k) * (q^(((k : ℤ)*((k : ℤ)-1)/2-(n : ℤ)*(k : ℤ)) : ℤ))) * (pochList [a] q (n))) / (pochList [((q^((1-(n : ℤ)) : ℤ)) / a)] q (k))) := by
  sorry

end FiniteQBenchmark.Identity223
