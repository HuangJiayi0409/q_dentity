import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex15i — Jackson 终止 2φ1 到 3φ2 变换
Original representative source: GR2-1.Ex15i
Frozen statement: formulas/train/FQI-SRC-GR2-1.Ex15i.md
Source formula:
{}_2\phi_1^{[n]}\!\left[\begin{matrix}q^{-n},b\\c\end{matrix};q,z\right]=(bzq^{-n}/c;q)_n\,{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},c/b,0\\c,cq/(bz)\end{matrix};q,q\right].
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity055
variable {K : Type*} [Field K]

theorem statement (b c q z : K) (n : ℕ) (hq : regular q) (hp : ∀ x ∈ [b,c,z], x ≠ 0)
 (hl : phiDefined [c] q n) (hr : phiDefined [c,c*q/(b*z)] q n) :
 phi [q^(-(n : ℤ)),b] [c] q z n = poch (b*z*q^(-(n : ℤ))/c) q n *
 phi [q^(-(n : ℤ)),c/b,0] [c,c*q/(b*z)] q q n := by
  sorry

end FiniteQBenchmark.Identity055
