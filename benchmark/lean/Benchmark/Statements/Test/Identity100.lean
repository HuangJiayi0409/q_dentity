import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.10.6 — 有限双底数求和（二）
Original representative source: GR2-3.10.6
Frozen statement: formulas/test/FQI-SRC-GR2-3.10.6.md
Source formula:
\Phi_n[a^2,-aq^2,b^2;-a,a^2q^2/b^2\mid-aq^n/b^2,q^{-n};b^2q^{1-n},-aq^{n+1};q^2,q;q^2]=\frac{(q^n/b^2,-aq;q)_n(aq/b^2,aq^2/b^2;q^2)_n}{(aq^n/b^2,-q;q)_n(q/b^2,a^2q^2/b^2;q^2)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity100
variable {K : Type*} [Field K]

theorem statement (a b q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 0) (hb : b ≠ 0)
 (hl : phiDefined [-a,a^2*q^2/b^2] (q^2) n)
 (ho : ∀ k ≤ n, pochList [b^2*q^(1-(n : ℤ)),-a*q^(n+1)] q k ≠ 0)
 (hr : pochList [a*q^n/b^2,-q] q n*pochList [q/b^2,a^2*q^2/b^2] (q^2) n ≠ 0) :
 bibasicPhi [a^2,-a*q^2,b^2] [-a,a^2*q^2/b^2]
 [-a*q^n/b^2,q^(-(n : ℤ))] [b^2*q^(1-(n : ℤ)),-a*q^(n+1)] (q^2) q (q^2) n =
 pochList [q^n/b^2,-a*q] q n*pochList [a*q/b^2,a*q^2/b^2] (q^2) n /
 (pochList [a*q^n/b^2,-q] q n*pochList [q/b^2,a^2*q^2/b^2] (q^2) n) := by
  sorry

end FiniteQBenchmark.Identity100
