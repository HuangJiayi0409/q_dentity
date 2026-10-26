import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex36i — 平衡终止4φ3有限卷积
Original representative source: GR2-2.Ex36i
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex36i.md
Source formula:
{}_4\phi_3^{[n]}(\alpha,\beta,\nu q^n,q^{-n};\gamma,\delta,\rho;q,q)=\frac{(\gamma/\lambda,\nu q/\gamma;q)_n}{(\gamma,\lambda\nu q/\gamma;q)_n}\lambda^n\sum_{k=0}^n\frac{(\lambda\nu/\gamma,\lambda,\delta\mu/(\alpha\beta),\mu\rho/(\alpha\beta),\nu q^n,q^{-n};q)_k(\lambda\nu q/\gamma;q)_{2k}}{(q,\nu q/\gamma,\rho,\delta,\lambda q^{1-n}/\gamma,\lambda\nu q^{n+1}/\gamma;q)_k(\lambda\nu/\gamma;q)_{2k}}(\delta\rho/(\mu\nu))^k{}_4\phi_3^{[k]}(\mu/\alpha,\mu/\beta,\lambda\nu q^k/\gamma,q^{-k};\lambda,\delta\mu/(\alpha\beta),\mu\rho/(\alpha\beta);q,q){}_4\phi_3^{[n-k]}(\alpha\beta/\mu,\mu/\lambda,\nu q^{k+n},q^{k-n};\gamma/\lambda,\delta q^k,\rho q^k;q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity086
variable {K : Type*} [Field K]

theorem statement (a b v g d r l u q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,v,g,d,r,l,u], x ≠ 0) (hbal : a*b*v*q = d*g*r)
 (hl : phiDefined [g,d,r] q n) (hf : pochList [g,l*v*q/g] q n ≠ 0)
 (ho : ∀ k ≤ n,
 pochList [q,v*q/g,r,d,l*q^(1-(n : ℤ))/g,l*v*q^(n+1)/g] q k * poch (l*v/g) q (2*k) ≠ 0)
 (hi : ∀ k ≤ n, phiDefined [l,d*u/(a*b),u*r/(a*b)] q k ∧ phiDefined [g/l,d*q^k,r*q^k] q (n-k)) :
 phi [a,b,v*q^n,q^(-(n : ℤ))] [g,d,r] q q n =
 pochList [g/l,v*q/g] q n/pochList [g,l*v*q/g] q n*l^n *
 ∑ k ∈ Finset.range (n+1),
 pochList [l*v/g,l,d*u/(a*b),u*r/(a*b),v*q^n,q^(-(n : ℤ))] q k * poch (l*v*q/g) q (2*k) /
 (pochList [q,v*q/g,r,d,l*q^(1-(n : ℤ))/g,l*v*q^(n+1)/g] q k*poch (l*v/g) q (2*k)) *
 (d*r/(u*v))^k *
 phi [u/a,u/b,l*v*q^k/g,q^(-(k : ℤ))] [l,d*u/(a*b),u*r/(a*b)] q q k *
 phi [a*b/u,u/l,v*q^(k+n),q^((k : ℤ)-n)] [g/l,d*q^k,r*q^k] q q (n-k) := by
  sorry

end FiniteQBenchmark.Identity086
