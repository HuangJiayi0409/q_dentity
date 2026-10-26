import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.6.10 — 四参数双底数乘积差分
Original representative source: GR2-3.6.10
Frozen statement: formulas/train/FQI-SRC-GR2-3.6.10.md
Source formula:
S_k-S_{k-1}=\frac{d(1-c/d)(1-ad/(bc))(1-adp^kq^k)(1-bp^k/(dq^k))}{(1-a)(1-b)(1-c)(1-ad^2/(bc))}\frac{(a,b;p)_k(c,ad^2/(bc);q)_kq^k}{(dq,adq/b;q)_k(adp/c,bcp/d;p)_k},\quad S_k=\frac{(ap,bp;p)_k(cq,ad^2q/(bc);q)_k}{(dq,adq/b;q)_k(adp/c,bcp/d;p)_k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity091
variable {K : Type*} [Field K]

theorem statement (a b c d p q : K) (k : ℤ) (hp : regular p) (hq : regular q)
 (hnz : ∀ x ∈ [a,b,c,d], x ≠ 0)
 (hc : (1-a)*(1-b)*(1-c)*(1-a*d^2/(b*c)) ≠ 0)
 (hs : bibasicSDefined a b c d p q k ∧ bibasicSDefined a b c d p q (k-1))
 (hi : pochListIntDefined [a,b] p k ∧ pochListIntDefined [c,a*d^2/(b*c)] q k) :
 bibasicS a b c d p q k-bibasicS a b c d p q (k-1) =
 d*(1-c/d)*(1-a*d/(b*c))*(1-a*d*p^k*q^k)*(1-b*p^k/(d*q^k)) /
 ((1-a)*(1-b)*(1-c)*(1-a*d^2/(b*c))) *
 pochListInt [a,b] p k*pochListInt [c,a*d^2/(b*c)] q k*q^k /
 (pochListInt [d*q,a*d*q/b] q k*pochListInt [a*d*p/c,b*c*p/d] p k) := by
  sorry

end FiniteQBenchmark.Identity091
