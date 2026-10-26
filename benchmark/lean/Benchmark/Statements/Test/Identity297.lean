import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-9.3.18 — M振荡闭式的剩余参数域
Original representative source: AP-9.3.18
Frozen statement: formulas/test/FQI-SRC-AP-9.3.18.md
Source formula:
M_{k,i}(a-1,a+i-1+r;2\mu-1;q)=F(2a+i-3,a-(2k+1)\mu+2k,r+1,(2\mu-1)((2k+1)\mu-2k+i-1)).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity297
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (k i a mu : ℕ) (r : ℤ)
 (hq : q ≠ 0) (hi : 1 ≤ i) (hki : i ≤ k) (hp : 1 ≤ a) (hm : 1 ≤ mu) (hr : -1 ≤ r)
 (h_domain : True) :
 (oscillationPoly q false k i (a-1) (((a:ℤ)+i-1+r).toNat) (2*mu-1)) = (sieveF q (2*(a:ℤ)+i-3) ((a:ℤ)-(2*k+1)*mu+2*k) (r+1) ((2*(mu:ℤ)-1)*((2*k+1)*mu-2*k+i-1))) := by
  sorry

end FiniteQBenchmark.Identity297
