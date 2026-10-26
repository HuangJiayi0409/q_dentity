import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex29 — 终止级数的 q-Jacobi 型连接展开
Original representative source: GR2-2.Ex29
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex29.md
Source formula:
{}_{r+2}\phi_{r+1}^{[n]}(q^{-n},cdq^{n+1},\boldsymbol u;cq,\boldsymbol v;q,z)=\sum_{k=0}^n\frac{(-1)^kq^{k(k+1)/2}(aq,cdq^{n+1},q^{-n};q)_k}{(q,cq,abq^{k+1};q)_k}{}_3\phi_2^{[n-k]}(q^{k-n},cdq^{n+k+1},aq^{k+1};cq^{k+1},abq^{2k+2};q,q){}_{r+2}\phi_{r+1}^{[k]}(q^{-k},abq^{k+1},\boldsymbol u;aq,\boldsymbol v;q,z).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity082
variable {K : Type*} [Field K]

theorem statement (a b c d q z : K) (us vs : List K) (n : ℕ) (hq : regular q)
 (hlen : us.length = vs.length) (hl : phiDefined (c*q :: vs) q n)
 (ho : ∀ k ≤ n, pochList [q,c*q,a*b*q^(k+1)] q k ≠ 0)
 (hi : ∀ k ≤ n, phiDefined [c*q^(k+1),a*b*q^(2*k+2)] q (n-k) ∧ phiDefined (a*q :: vs) q k) :
 phi ([q^(-(n : ℤ)),c*d*q^(n+1)] ++ us) (c*q :: vs) q z n =
 ∑ k ∈ Finset.range (n+1),
 (-1)^k*q^(k*(k+1)/2)*pochList [a*q,c*d*q^(n+1),q^(-(n : ℤ))] q k /
 pochList [q,c*q,a*b*q^(k+1)] q k *
 phi [q^((k : ℤ)-n),c*d*q^(n+k+1),a*q^(k+1)] [c*q^(k+1),a*b*q^(2*k+2)] q q (n-k) *
 phi ([q^(-(k : ℤ)),a*b*q^(k+1)] ++ us) (a*q :: vs) q z k := by
  sorry

end FiniteQBenchmark.Identity082
