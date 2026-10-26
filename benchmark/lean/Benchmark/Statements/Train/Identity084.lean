import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex35ii — Gasper 离散分式积分的有限展开（二）
Original representative source: GR2-2.Ex35ii
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex35ii.md
Source formula:
{}_3\phi_2^{[n]}(\alpha,\beta,q^{-n};\gamma,\delta;q,q)=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_q\frac{(\lambda,\delta/\sigma;q)_k(\gamma/\lambda;q)_{n-k}}{(\gamma;q)_n(\delta;q)_k}\lambda^n(\sigma/\lambda)^k{}_3\phi_2^{[k]}(\alpha/\sigma,\beta,q^{-k};\lambda,\delta/\sigma;q,q){}_3\phi_2^{[n-k]}(\sigma,\beta/\lambda,q^{k-n};\gamma/\lambda,\delta q^k;q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity084
variable {K : Type*} [Field K]

theorem statement (a b g d l s q : K) (n : ℕ) (hq : regular q)
 (hl0 : l ≠ 0) (hs0 : s ≠ 0) (hl : phiDefined [g,d] q n)
 (hi : ∀ k ≤ n, phiDefined [l,d/s] q k ∧ phiDefined [g/l,d*q^k] q (n-k)) :
 phi [a,b,q^(-(n : ℤ))] [g,d] q q n =
 ∑ k ∈ Finset.range (n+1), gaussian q n k *
 pochList [l,d/s] q k*poch (g/l) q (n-k)/(poch g q n*poch d q k)*l^n*(s/l)^k *
 phi [a/s,b,q^(-(k : ℤ))] [l,d/s] q q k *
 phi [s,b/l,q^((k : ℤ)-n)] [g/l,d*q^k] q q (n-k) := by
  sorry

end FiniteQBenchmark.Identity084
