import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.6.6 — 双底数乘积的差分
Original representative source: GR2-3.6.6
Frozen statement: formulas/test/FQI-SRC-GR2-3.6.6.md
Source formula:
T_k-T_{k-1}=\frac{(1-ap^kq^k)(1-bp^kq^{-k})(a,b;p)_k(c,a/(bc);q)_kq^k}{(1-a)(1-b)(q,aq/b;q)_k(ap/c,bcp;p)_k},\quad T_k=\frac{(ap,bp;p)_k(cq,aq/(bc);q)_k}{(q,aq/b;q)_k(ap/c,bcp;p)_k},\quad T_{-1}=0.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity090
variable {K : Type*} [Field K]

theorem statement (a b c p q : K) (k : ℕ) (hp : regular p) (hq : regular q)
 (hnz : ∀ x ∈ [a,b,c], x ≠ 0) (ha : a ≠ 1) (hb : b ≠ 1)
 (hd : pochList [q,a*q/b] q k*pochList [a*p/c,b*c*p] p k ≠ 0)
 (hprev : 0 < k → pochList [q,a*q/b] q (k-1)*pochList [a*p/c,b*c*p] p (k-1) ≠ 0) :
 bibasicT a b c p q k - bibasicT a b c p q ((k : ℤ)-1) =
 (1-a*p^k*q^k)*(1-b*p^k*q^(-(k : ℤ)))*pochList [a,b] p k*pochList [c,a/(b*c)] q k*q^k /
 ((1-a)*(1-b)*pochList [q,a*q/b] q k*pochList [a*p/c,b*c*p] p k) := by
  sorry

end FiniteQBenchmark.Identity090
