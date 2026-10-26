import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-09 — 负移位乘积之比
Original representative source: GR2-I-09
Frozen statement: formulas/train/FQI-SRC-GR2-I-09.md
Source formula:
\frac{(aq^{-n};q)_n}{(bq^{-n};q)_n}=\frac{(q/a;q)_n}{(q/b;q)_n}(a/b)^n.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity222
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (n : ℕ)
 (hbase : regular q) (hab : a*b ≠ 0)
 (h_domain : (pochList [(b * (q^((-(n : ℤ)) : ℤ)))] q (n)) ≠ 0 ∧
    a ≠ 0 ∧
    b ≠ 0 ∧
    (pochList [(q / b)] q (n)) ≠ 0) :
 ((pochList [(a * (q^((-(n : ℤ)) : ℤ)))] q (n)) / (pochList [(b * (q^((-(n : ℤ)) : ℤ)))] q (n))) = (((pochList [(q / a)] q (n)) / (pochList [(q / b)] q (n))) * ((a / b)^n)) := by
  sorry

end FiniteQBenchmark.Identity222
