import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-15 — 双倍负移位
Original representative source: GR2-I-15
Frozen statement: formulas/train/FQI-SRC-GR2-I-15.md
Source formula:
(aq^{-2n};q)_n=\frac{(q/a;q)_{2n}}{(q/a;q)_n}(-a/q^2)^nq^{-3n(n-1)/2}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity228
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n : ℕ)
 (hbase : regular q) (ha : a ≠ 0)
 (h_domain : a ≠ 0 ∧
    (pochList [(q / a)] q (n)) ≠ 0 ∧
    (q^2) ≠ 0) :
 (pochList [(a * (q^((-2*(n : ℤ)) : ℤ)))] q (n)) = ((((pochList [(q / a)] q (2*n)) / (pochList [(q / a)] q (n))) * (((-a) / (q^2))^n)) * (q^((-3*(n : ℤ)*((n : ℤ)-1)/2) : ℤ))) := by
  sorry

end FiniteQBenchmark.Identity228
