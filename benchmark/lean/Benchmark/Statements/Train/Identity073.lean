import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex11 — Askey–Wilson 参数交换与奇偶关系
Original representative source: GR2-2.Ex11
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex11.md
Source formula:
p_n(x;a,b,c,d\mid q)=p_n(x;b,a,c,d\mid q),\qquad p_n(-x;a,b,c,d\mid q)=(-1)^np_n(x;-a,-b,-c,-d\mid q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity073
variable {K : Type*} [Field K]

theorem statement (t a b c d q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,t], x ≠ 0)
 (hl : phiDefined [a*b,a*c,a*d] q n) (hr : phiDefined [b*a,b*c,b*d] q n) :
 askeyWilson t a b c d q n = askeyWilson t b a c d q n ∧
 askeyWilson (-t) a b c d q n = (-1)^n*askeyWilson t (-a) (-b) (-c) (-d) q n := by
  sorry

end FiniteQBenchmark.Identity073
