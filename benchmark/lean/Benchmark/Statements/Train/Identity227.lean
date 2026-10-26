import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-14 — 互补长度的负移位
Original representative source: GR2-I-14
Frozen statement: formulas/train/FQI-SRC-GR2-I-14.md
Source formula:
(aq^{-n};q)_{n-k}=\frac{(q/a;q)_n}{(q/a;q)_k}(-a/q)^{n-k}q^{k(k-1)/2-n(n-1)/2}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity227
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n k : ℕ)
 (hbase : regular q) (hk : k ≤ n) (ha : a ≠ 0)
 (h_domain : a ≠ 0 ∧
    (pochList [(q / a)] q (k)) ≠ 0 ∧
    q ≠ 0) :
 (pochList [(a * (q^((-(n : ℤ)) : ℤ)))] q (n-k)) = ((((pochList [(q / a)] q (n)) / (pochList [(q / a)] q (k))) * (((-a) / q)^(n-k))) * (q^(((k : ℤ)*((k : ℤ)-1)/2-(n : ℤ)*((n : ℤ)-1)/2) : ℤ))) := by
  sorry

end FiniteQBenchmark.Identity227
