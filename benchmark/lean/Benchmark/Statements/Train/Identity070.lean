import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex5 — 不定 very-well-poised 有限和
Original representative source: GR2-2.Ex5
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex5.md
Source formula:
W_6^{[n]}(a;b,c,a/(bc);q,q)=\frac{(aq,bq,cq,aq/(bc);q)_n}{(q,aq/b,aq/c,bcq;q)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity070
variable {K : Type*} [Field K]

theorem statement (a b c q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c], x ≠ 0) (hw : wDefined a [b,c,a/(b*c)] q n)
 (hd : pochList [q,a*q/b,a*q/c,b*c*q] q n ≠ 0) :
 wellPoisedRaw a [b,c,a/(b*c)] q q n =
 pochList [a*q,b*q,c*q,a*q/(b*c)] q n/pochList [q,a*q/b,a*q/c,b*c*q] q n := by
  sorry

end FiniteQBenchmark.Identity070
