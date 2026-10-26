import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.2.26 — 有限超几何项的相邻项递推
Original representative source: GR2-1.2.26
Frozen statement: formulas/train/FQI-SRC-GR2-1.2.26.md
Source formula:
(1-q^{n+1})\prod_{j=1}^s(1-b_jq^n)v_{n+1}=z(-q^n)^{1+s-r}\prod_{i=1}^r(1-a_iq^n)v_n.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity039
variable {K : Type*} [Field K]

theorem statement (as bs : List K) (q z : K) (n : ℕ) (hq : q ≠ 0)
    (hden : phiDefined bs q (n+1)) :
    (1-q^(n+1)) * (bs.map (fun b => 1-b*q^n)).prod * phiTerm as bs q z (n+1) =
      z * (-q^n)^((1 : ℤ)+bs.length-as.length) *
        (as.map (fun a => 1-a*q^n)).prod * phiTerm as bs q z n := by
  sorry

end FiniteQBenchmark.Identity039
