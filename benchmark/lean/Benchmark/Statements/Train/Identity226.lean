import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-13 — 独立长度的负移位
Original representative source: GR2-I-13
Frozen statement: formulas/train/FQI-SRC-GR2-I-13.md
Source formula:
(aq^{-n};q)_k=\frac{(a;q)_k(q/a;q)_n}{(q^{1-k}/a;q)_n}q^{-nk}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity226
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n k : ℕ)
 (hbase : regular q) (ha : a ≠ 0)
 (h_domain : a ≠ 0 ∧
    (pochList [((q^((1-(k : ℤ)) : ℤ)) / a)] q (n)) ≠ 0) :
 (pochList [(a * (q^((-(n : ℤ)) : ℤ)))] q (k)) = ((((pochList [a] q (k)) * (pochList [(q / a)] q (n))) / (pochList [((q^((1-(k : ℤ)) : ℤ)) / a)] q (n))) * (q^((-(n : ℤ)*(k : ℤ)) : ℤ))) := by
  sorry

end FiniteQBenchmark.Identity226
