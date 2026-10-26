import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.10.5 — 有限双底数求和（一）
Original representative source: GR2-3.10.5
Frozen statement: formulas/train/FQI-SRC-GR2-3.10.5.md
Source formula:
\Phi_n[a^2,aq^2,-aq^2;a,-a\mid-aq/w,q^{-n};w,-aq^{n+1};q^2,q;wq^{n-1}/a]=\frac{(-aq,aq^2/w,w/(aq);q)_n}{(-q,aq/w,w;q)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity099
variable {K : Type*} [Field K]

theorem statement (a w q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 0) (hw : w ≠ 0)
 (hl : phiDefined [a,-a] (q^2) n)
 (hb : ∀ k ≤ n, pochList [w,-a*q^(n+1)] q k ≠ 0)
 (hr : pochList [-q,a*q/w,w] q n ≠ 0) :
 bibasicPhi [a^2,a*q^2,-a*q^2] [a,-a] [-a*q/w,q^(-(n : ℤ))] [w,-a*q^(n+1)]
 (q^2) q (w*q^((n : ℤ)-1)/a) n =
 pochList [-a*q,a*q^2/w,w/(a*q)] q n/pochList [-q,a*q/w,w] q n := by
  sorry

end FiniteQBenchmark.Identity099
