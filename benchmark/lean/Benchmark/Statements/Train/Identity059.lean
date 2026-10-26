import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex31-term — 有限超几何项的算子关系
Original representative source: GR2-1.Ex31-term
Frozen statement: formulas/train/FQI-SRC-GR2-1.Ex31-term.md
Source formula:
(\Delta_1\Delta_{b_1/q}\cdots\Delta_{b_s/q})v_n(z)=z(\Delta_{a_1}\cdots\Delta_{a_r})v_{n-1}(zq^{1+s-r}).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity059
variable {K : Type*} [Field K]

theorem statement (as bs : List K) (q z : K) (n : ℕ) (hn : 1 ≤ n) (hq : regular q)
 (hd : phiDefined bs q n) :
 deltaList q (1 :: bs.map (fun b => b/q)) (fun x => phiTerm as bs q x n) z =
 z * deltaList q as (fun x => phiTerm as bs q x (n-1))
 (z*q^((1 : ℤ)+bs.length-as.length)) := by
  sorry

end FiniteQBenchmark.Identity059
