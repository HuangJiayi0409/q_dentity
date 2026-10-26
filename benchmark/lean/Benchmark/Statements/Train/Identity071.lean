import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex6 — 终止 4φ3 的奇偶求和
Original representative source: GR2-2.Ex6
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex6.md
Source formula:
{}_4\phi_3^{[n]}(q^{-n},b,c,-q^{1-n}/(bc);q^{1-n}/b,q^{1-n}/c,-bc;q,q)=\begin{cases}0,&n=2m+1,\\\dfrac{(q,b^2,c^2;q^2)_m(bc;q)_{2m}}{(b,c;q)_{2m}(b^2c^2;q^2)_m},&n=2m.\end{cases}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity071
variable {K : Type*} [Field K]

theorem statement (b c q : K) (n : ℕ) (hq : regular q) (hb : b ≠ 0) (hc : c ≠ 0)
 (hl : phiDefined [q^(1-(n : ℤ))/b,q^(1-(n : ℤ))/c,-b*c] q n)
 (hr : n%2=0 → pochList [b,c] q n*poch (b^2*c^2) (q^2) (n/2) ≠ 0) :
 phi [q^(-(n : ℤ)),b,c,-q^(1-(n : ℤ))/(b*c)]
 [q^(1-(n : ℤ))/b,q^(1-(n : ℤ))/c,-b*c] q q n =
 if n%2=0 then pochList [q,b^2,c^2] (q^2) (n/2)*poch (b*c) q n /
 (pochList [b,c] q n*poch (b^2*c^2) (q^2) (n/2)) else 0 := by
  sorry

end FiniteQBenchmark.Identity071
