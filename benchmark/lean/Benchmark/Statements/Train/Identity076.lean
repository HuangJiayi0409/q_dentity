import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex14i — Bailey 的终止 4φ3 求和
Original representative source: GR2-2.Ex14i
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex14i.md
Source formula:
{}_4\phi_3^{[n]}(s^2,qs,b,q^{-n};s,s^2q/b,b^2q^{1-n};q,q)=\frac{(s^2/b^2,1/b,-qs/b;q)_n}{(1/b^2,s^2q/b,-s/b;q)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity076
variable {K : Type*} [Field K]

theorem statement (s b q : K) (n : ℕ) (hq : regular q) (hb : b ≠ 0)
 (hl : phiDefined [s,s^2*q/b,b^2*q^(1-(n : ℤ))] q n)
 (hr : pochList [1/b^2,s^2*q/b,-s/b] q n ≠ 0) :
 phi [s^2,q*s,b,q^(-(n : ℤ))] [s,s^2*q/b,b^2*q^(1-(n : ℤ))] q q n =
 pochList [s^2/b^2,1/b,-q*s/b] q n/pochList [1/b^2,s^2*q/b,-s/b] q n := by
  sorry

end FiniteQBenchmark.Identity076
