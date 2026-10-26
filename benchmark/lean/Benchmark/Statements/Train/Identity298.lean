import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-9.3.19 — P振荡闭式的剩余参数域
Original representative source: AP-9.3.19
Frozen statement: formulas/train/FQI-SRC-AP-9.3.19.md
Source formula:
P_{k,i}(b+2k-i-1+r,b-1;2\mu;q)=F(2b+2k-i-2,b+2k-i-(2k+1)\mu,r,\mu((4k+2)\mu-2k+2i-1)).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity298
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (k i b mu : ℕ) (r : ℤ)
 (hq : q ≠ 0) (hi : 1 ≤ i) (hki : i ≤ k) (hp : 1 ≤ b) (hm : 1 ≤ mu) (hr : 0 ≤ r)
 (h_domain : True) :
 (oscillationPoly q true k i (((b:ℤ)+2*k-i-1+r).toNat) (b-1) (2*mu)) = (sieveF q (2*(b:ℤ)+2*k-i-2) ((b:ℤ)+2*k-i-(2*k+1)*mu) (r) ((mu:ℤ)*((4*k+2)*mu-2*k+2*i-1))) := by
  sorry

end FiniteQBenchmark.Identity298
