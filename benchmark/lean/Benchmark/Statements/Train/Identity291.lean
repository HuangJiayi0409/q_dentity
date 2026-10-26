import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-9.3.6 — 振荡分拆的P混合差分递推
Original representative source: AP-9.3.6
Frozen statement: formulas/train/FQI-SRC-AP-9.3.6.md
Source formula:
P_{k,i}(a,b;\mu;q)-P_{k,i}(a-1,b;\mu;q)-P_{k,i}(a,b-1;\mu;q)+P_{k,i}(a-1,b-1;\mu;q)=q^{a+b-1}\begin{cases}M_{k,i}(a-1,b-1;\mu-1;q),&a-b>2k-i-1,\\P_{k,i}(a-1,b-1;\mu;q),&a-b\le2k-i-1.\end{cases}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity291
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (k i a b mu : ℕ)
 (hi : 1 ≤ i) (hki : i ≤ k) (ha : 1 ≤ a) (hb : 1 ≤ b) (hmu : 1 ≤ mu)
 (h_domain : True) :
 ((((oscillationPoly q true k i (a) (b) (mu)) - (oscillationPoly q true k i (a-1) (b) (mu))) - (oscillationPoly q true k i (a) (b-1) (mu))) + (oscillationPoly q true k i (a-1) (b-1) (mu))) = ((q^(a+b-1)) * (if (a:ℤ)-b > 2*(k:ℤ)-i-1 then (oscillationPoly q false k i (a-1) (b-1) (mu-1)) else (oscillationPoly q true k i (a-1) (b-1) (mu)))) := by
  sorry

end FiniteQBenchmark.Identity291
