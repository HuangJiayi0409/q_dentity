import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex33 — 小 q-Jacobi 多项式的有限连接公式
Original representative source: GR2-1.Ex33
Frozen statement: formulas/train/FQI-SRC-GR2-1.Ex33.md
Source formula:
p_n(x;c,d;q)=\sum_{k=0}^n A_{k,n}p_k(x;a,b;q),\quad A_{k,n}=\frac{(-1)^kq^{k(k+1)/2}(q^{-n},aq,cdq^{n+1};q)_k}{(q,cq,abq^{k+1};q)_k}{}_3\phi_2^{[n-k]}\!\left[\begin{matrix}q^{k-n},cdq^{n+k+1},aq^{k+1}\\cq^{k+1},abq^{2k+2}\end{matrix};q,q\right].
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity060
variable {K : Type*} [Field K]

theorem statement (a b c d q x : K) (n : ℕ) (hq : regular q)
 (hl : phiDefined [c*q] q n)
 (hp : ∀ k ≤ n, phiDefined [a*q] q k)
 (hc : ∀ k ≤ n, pochList [q,c*q,a*b*q^(k+1)] q k ≠ 0 ∧
 phiDefined [c*q^(k+1),a*b*q^(2*k+2)] q (n-k)) :
 littleJacobi x c d q n = ∑ k ∈ Finset.range (n+1),
 ((-1)^k*q^(k*(k+1)/2)*pochList [q^(-(n : ℤ)),a*q,c*d*q^(n+1)] q k /
 pochList [q,c*q,a*b*q^(k+1)] q k *
 phi [q^((k : ℤ)-n),c*d*q^(n+k+1),a*q^(k+1)]
 [c*q^(k+1),a*b*q^(2*k+2)] q q (n-k))*littleJacobi x a b q k := by
  sorry

end FiniteQBenchmark.Identity060
