import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-08 — 负移位、非负长度的乘积
Original representative source: GR2-I-08
Frozen statement: formulas/train/FQI-SRC-GR2-I-08.md
Source formula:
(aq^{-n};q)_n=(-a/q)^nq^{-n(n-1)/2}(q/a;q)_n
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity221
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n : ℕ)
 (hbase : regular q) (ha : a ≠ 0)
 (h_domain : q ≠ 0 ∧
    a ≠ 0) :
 (pochList [(a * (q^((-(n : ℤ)) : ℤ)))] q (n)) = (((((-a) / q)^n) * (q^((-(n : ℤ)*((n : ℤ)-1)/2) : ℤ))) * (pochList [(q / a)] q (n))) := by
  sorry

end FiniteQBenchmark.Identity221
