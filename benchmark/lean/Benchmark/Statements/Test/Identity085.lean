import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex35iii — Gasper 离散分式积分的有限展开（三）
Original representative source: GR2-2.Ex35iii
Frozen statement: formulas/test/FQI-SRC-GR2-2.Ex35iii.md
Source formula:
{}_3\phi_2^{[n]}(\alpha,\beta,q^{-n};\gamma,\delta;q,q)=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_q\frac{(\nu;q)_n(\lambda;q)_k(\gamma\mu/(\lambda\nu);q)_{n-k}}{(\gamma,\mu;q)_n}\lambda^{n-k}{}_3\phi_2^{[n-k]}(\mu/\nu,\gamma/\nu,q^{k-n};\gamma\mu/(\lambda\nu),q^{1-n}/\nu;q,q^{1-k}/\lambda){}_4\phi_3^{[k]}(\alpha,\beta,\mu,q^{-k};\lambda,\nu,\delta;q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity085
variable {K : Type*} [Field K]

theorem statement (a b g d l u v q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [g,l,u,v], x ≠ 0) (hl : phiDefined [g,d] q n)
 (hf : pochList [g,u] q n ≠ 0)
 (hi : ∀ k ≤ n, phiDefined [g*u/(l*v),q^(1-(n : ℤ))/v] q (n-k) ∧ phiDefined [l,v,d] q k) :
 phi [a,b,q^(-(n : ℤ))] [g,d] q q n =
 ∑ k ∈ Finset.range (n+1), gaussian q n k *
 poch v q n*poch l q k*poch (g*u/(l*v)) q (n-k)/pochList [g,u] q n * l^(n-k) *
 phi [u/v,g/v,q^((k : ℤ)-n)] [g*u/(l*v),q^(1-(n : ℤ))/v] q (q^(1-(k : ℤ))/l) (n-k) *
 phi [a,b,u,q^(-(k : ℤ))] [l,v,d] q q k := by
  sorry

end FiniteQBenchmark.Identity085
