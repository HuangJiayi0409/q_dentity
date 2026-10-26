import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.2.6 — 终止 type-II 3φ2 变换
Original representative source: GR2-3.2.6
Frozen statement: formulas/train/FQI-SRC-GR2-3.2.6.md
Source formula:
{}_3\phi_2^{[n]}(q^{-n},aq^n,b;d,e;q,de/(ab))=\frac{(aq/d,aq/e;q)_n}{(d,e;q)_n}(de/(aq))^n{}_3\phi_2^{[n]}(q^{-n},aq^n,abq/(de);aq/d,aq/e;q,q/b).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity089
variable {K : Type*} [Field K]

theorem statement (a b d e q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,d,e], x ≠ 0)
 (hl : phiDefined [d,e] q n) (hr : phiDefined [a*q/d,a*q/e] q n) :
 phi [q^(-(n : ℤ)),a*q^n,b] [d,e] q (d*e/(a*b)) n =
 pochList [a*q/d,a*q/e] q n/pochList [d,e] q n*(d*e/(a*q))^n *
 phi [q^(-(n : ℤ)),a*q^n,a*b*q/(d*e)] [a*q/d,a*q/e] q (q/b) n := by
  sorry

end FiniteQBenchmark.Identity089
