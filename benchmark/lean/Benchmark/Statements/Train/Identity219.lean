import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-03 — q-Pochhammer 倒底数
Original representative source: GR2-I-03
Frozen statement: formulas/train/FQI-SRC-GR2-I-03.md
Source formula:
(a;q^{-1})_n=(-a)^nq^{-n(n-1)/2}(a^{-1};q)_n
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity219
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n : ℕ)
 (hbase : regular q) (ha : a ≠ 0)
 (h_domain : q ≠ 0 ∧
    a ≠ 0) :
 (pochList [a] (1 / q) (n)) = ((((-a)^n) * (q^((-(n : ℤ)*((n : ℤ)-1)/2) : ℤ))) * (pochList [(1 / a)] q (n))) := by
  sorry

end FiniteQBenchmark.Identity219
