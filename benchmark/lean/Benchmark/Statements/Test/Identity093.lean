import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.6.17 — Bressoud–Gasper 双底数正交核
Original representative source: GR2-3.6.17
Frozen statement: formulas/test/FQI-SRC-GR2-3.6.17.md
Source formula:
\sum_{k=0}^n\frac{(1-ap^kq^k)(1-bp^kq^{-k})(a,b;p)_k(q^{-n},aq^n/b;q)_kq^k}{(1-a)(1-b)(q,aq/b;q)_k(apq^n,bpq^{-n};p)_k}=\delta_{n,0}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity093
variable {K : Type*} [Field K]

theorem statement (a b p q : K) (n : ℕ) (hp : regular p) (hq : regular q)
 (ha : a ≠ 0) (hb : b ≠ 0) (hc : (1-a)*(1-b) ≠ 0)
 (hd : ∀ k ≤ n, pochList [q,a*q/b] q k*pochList [a*p*q^n,b*p*q^(-(n : ℤ))] p k ≠ 0) :
 (∑ k ∈ Finset.range (n+1),
 (1-a*p^k*q^k)*(1-b*p^k*q^(-(k : ℤ)))*pochList [a,b] p k*pochList [q^(-(n : ℤ)),a*q^n/b] q k*q^k /
 ((1-a)*(1-b)*pochList [q,a*q/b] q k*pochList [a*p*q^n,b*p*q^(-(n : ℤ))] p k)) =
 if n=0 then 1 else 0 := by
  sorry

end FiniteQBenchmark.Identity093
