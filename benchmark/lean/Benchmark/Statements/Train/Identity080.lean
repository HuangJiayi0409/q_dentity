import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex27 — 平衡参数对的终止级数展开
Original representative source: GR2-2.Ex27
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex27.md
Source formula:
{}_{r+3}\phi_{r+2}^{[n]}(q^{-n},c,ab/c,\boldsymbol u;a,b,\boldsymbol v;q,z)=\frac{(c,ab/c;q)_n}{(a,b;q)_n}\sum_{k=0}^n\frac{(q^{-n},c/a,c/b;q)_kq^k}{(q,c,cq^{1-n}/(ab);q)_k}{}_{r+2}\phi_{r+1}^{[n-k]}(q^{k-n},c,\boldsymbol u;cq^k,\boldsymbol v;q,z).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity080
variable {K : Type*} [Field K]

theorem statement (a b c q z : K) (us vs : List K) (n : ℕ) (hq : regular q)
 (hlen : us.length = vs.length) (hp : ∀ x ∈ [a,b,c], x ≠ 0)
 (hl : phiDefined ([a,b] ++ vs) q n)
 (ho : phiDefined [c,c*q^(1-(n : ℤ))/(a*b)] q n)
 (hi : ∀ k ≤ n, phiDefined (c*q^k :: vs) q (n-k)) :
 phi ([q^(-(n : ℤ)),c,a*b/c] ++ us) ([a,b] ++ vs) q z n =
 pochList [c,a*b/c] q n/pochList [a,b] q n *
 ∑ k ∈ Finset.range (n+1),
 pochList [q^(-(n : ℤ)),c/a,c/b] q k*q^k/pochList [q,c,c*q^(1-(n : ℤ))/(a*b)] q k *
 phi ([q^((k : ℤ)-n),c] ++ us) (c*q^k :: vs) q z (n-k) := by
  sorry

end FiniteQBenchmark.Identity080
