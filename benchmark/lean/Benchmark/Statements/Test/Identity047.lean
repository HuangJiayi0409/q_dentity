import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex1ii — 独立负移位的有限乘积
Original representative source: GR2-1.Ex1ii
Frozen statement: formulas/test/FQI-SRC-GR2-1.Ex1ii.md
Source formula:
(aq^{-k-n};q)_n=\frac{(q/a;q)_{n+k}}{(q/a;q)_k}(-a/q)^nq^{-nk-n(n-1)/2}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity047
variable {K : Type*} [Field K]

theorem statement (a q : K) (k n : ℕ) (hq : regular q) (ha : a ≠ 0)
 (hd : poch (q/a) q k ≠ 0) :
 poch (a*q^(-(k : ℤ)-n)) q n =
 poch (q/a) q (n+k)/poch (q/a) q k * (-a/q)^n*q^(-(n : ℤ)*k-(n : ℤ)*(n-1)/2) := by
  sorry

end FiniteQBenchmark.Identity047
