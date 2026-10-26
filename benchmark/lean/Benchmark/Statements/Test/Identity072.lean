import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex10 — q-Racah 多项式反射变换
Original representative source: GR2-2.Ex10
Frozen statement: formulas/test/FQI-SRC-GR2-2.Ex10.md
Source formula:
R_n(x;a,b,c,N;q)=\frac{(aq/c,bq;q)_n}{(aq,bcq;q)_n}c^nR_n(N-x;b,a,c^{-1},N;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity072
variable {K : Type*} [Field K]

theorem statement (t a b c q : K) (N n : ℕ) (hq : regular q) (hn : n ≤ N) (hc : c ≠ 0) (ht : t ≠ 0)
 (hl : phiDefined [a*q,b*c*q,q^(-(N : ℤ))] q n)
 (hr : phiDefined [b*q,a/c*q,q^(-(N : ℤ))] q n) :
 qRacah t a b c q N n = pochList [a*q/c,b*q] q n/pochList [a*q,b*c*q] q n*c^n*
 qRacah (q^N/t) b a c⁻¹ q N n := by
  sorry

end FiniteQBenchmark.Identity072
