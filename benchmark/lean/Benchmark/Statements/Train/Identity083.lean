import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex35i — 终止3φ2有限卷积
Original representative source: GR2-2.Ex35i
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex35i.md
Source formula:
{}_3\phi_2^{[n]}(\alpha,\beta,q^{-n};\gamma,\delta;q,q)=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_q\frac{(\lambda,\mu\delta/(\alpha\beta);q)_k(\gamma/\lambda;q)_{n-k}}{(\gamma;q)_n(\delta;q)_k}\lambda^n(\alpha\beta/(\lambda\mu))^k{}_3\phi_2^{[k]}(\mu/\alpha,\mu/\beta,q^{-k};\lambda,\delta\mu/(\alpha\beta);q,q){}_3\phi_2^{[n-k]}(\alpha\beta/\mu,\mu/\lambda,q^{k-n};\gamma/\lambda,\delta q^k;q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity083
variable {K : Type*} [Field K]

theorem statement (a b g d l u q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,g,d,l,u], x ≠ 0) (hl : phiDefined [g,d] q n)
 (hi : ∀ k ≤ n, phiDefined [l,d*u/(a*b)] q k ∧ phiDefined [g/l,d*q^k] q (n-k)) :
 phi [a,b,q^(-(n : ℤ))] [g,d] q q n =
 ∑ k ∈ Finset.range (n+1), gaussian q n k *
 pochList [l,u*d/(a*b)] q k * poch (g/l) q (n-k) /
 (poch g q n*poch d q k) * l^n*(a*b/(l*u))^k *
 phi [u/a,u/b,q^(-(k : ℤ))] [l,d*u/(a*b)] q q k *
 phi [a*b/u,u/l,q^((k : ℤ)-n)] [g/l,d*q^k] q q (n-k) := by
  sorry

end FiniteQBenchmark.Identity083
