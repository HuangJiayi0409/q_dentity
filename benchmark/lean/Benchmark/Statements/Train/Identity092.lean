import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.6.16 — 终止双底数求和与消去
Original representative source: GR2-3.6.16
Frozen statement: formulas/train/FQI-SRC-GR2-3.6.16.md
Source formula:
\sum_{k=0}^n\frac{(1-adp^kq^k)(1-bp^k/(dq^k))(a,b;p)_k(q^{-n},ad^2q^n/b;q)_kq^k}{(1-ad)(1-b/d)(dq,adq/b;q)_k(adpq^n,bpq^{-n}/d;p)_k}=\frac{(1-d)(1-ad/b)(1-adq^n)(1-dq^n/b)}{(1-ad)(1-d/b)(1-dq^n)(1-adq^n/b)}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity092
variable {K : Type*} [Field K]

theorem statement (a b d p q : K) (n : ℕ) (hp : regular p) (hq : regular q)
 (hnz : ∀ x ∈ [a,b,d], x ≠ 0)
 (hc : (1-a*d)*(1-b/d) ≠ 0)
 (hl : ∀ k ≤ n, pochList [d*q,a*d*q/b] q k*pochList [a*d*p*q^n,b*p*q^(-(n : ℤ))/d] p k ≠ 0)
 (hr : (1-a*d)*(1-d/b)*(1-d*q^n)*(1-a*d*q^n/b) ≠ 0) :
 (∑ k ∈ Finset.range (n+1),
 (1-a*d*p^k*q^k)*(1-b*p^k/(d*q^k))*pochList [a,b] p k*pochList [q^(-(n : ℤ)),a*d^2*q^n/b] q k*q^k /
 ((1-a*d)*(1-b/d)*pochList [d*q,a*d*q/b] q k*pochList [a*d*p*q^n,b*p*q^(-(n : ℤ))/d] p k)) =
 (1-d)*(1-a*d/b)*(1-a*d*q^n)*(1-d*q^n/b) /
 ((1-a*d)*(1-d/b)*(1-d*q^n)*(1-a*d*q^n/b)) := by
  sorry

end FiniteQBenchmark.Identity092
