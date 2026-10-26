import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-16 — 整数倍负移位
Original representative source: GR2-I-16
Frozen statement: formulas/train/FQI-SRC-GR2-I-16.md
Source formula:
(aq^{-kn};q)_n=\frac{(q/a;q)_{kn}}{(q/a;q)_{(k-1)n}}(-a)^nq^{n(n-1)/2-kn^2}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity229
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n k : ℕ)
 (hbase : regular q) (hk : 1 ≤ k) (ha : a ≠ 0)
 (h_domain : a ≠ 0 ∧
    (pochList [(q / a)] q ((k-1)*n)) ≠ 0) :
 (pochList [(a * (q^((-(k : ℤ)*(n : ℤ)) : ℤ)))] q (n)) = ((((pochList [(q / a)] q (k*n)) / (pochList [(q / a)] q ((k-1)*n))) * ((-a)^n)) * (q^(((n : ℤ)*((n : ℤ)-1)/2-(k : ℤ)*(n : ℤ)^2) : ℤ))) := by
  sorry

end FiniteQBenchmark.Identity229
