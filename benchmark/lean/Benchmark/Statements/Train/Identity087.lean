import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex36ii — 平衡终止 4φ3 的双级数展开
Original representative source: GR2-2.Ex36ii
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex36ii.md
Source formula:
{}_4\phi_3^{[n]}(\alpha,\beta,\nu q^n,q^{-n};\gamma,\delta,\rho;q,q)=\frac{(\gamma/\lambda,\nu q/\gamma;q)_n}{(\gamma,\lambda\nu q/\gamma;q)_n}\lambda^n\sum_{k=0}^n\frac{(\lambda\nu/\gamma,\lambda,\rho/\alpha,\delta/\sigma,\nu q^n,q^{-n};q)_k(\lambda\nu q/\gamma;q)_{2k}}{(q,\nu q/\gamma,\delta,\rho\sigma/\alpha,\lambda q^{1-n}/\gamma,\nu\lambda q^{n+1}/\gamma;q)_k(\lambda\nu/\gamma;q)_{2k}}(\sigma q/\gamma)^k{}_4\phi_3^{[k]}(\alpha/\sigma,\beta,\lambda\nu q^k/\gamma,q^{-k};\lambda,\delta/\sigma,\rho;q,q){}_4\phi_3^{[n-k]}(\sigma,\beta/\lambda,\nu q^{n+k},q^{k-n};\gamma/\lambda,\delta q^k,\sigma\rho q^k/\alpha;q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity087
variable {K : Type*} [Field K]

theorem statement (a b v g d r l s q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,l,g,s,v], x ≠ 0) (hbal : a*b*v*q = d*g*r)
 (hl : phiDefined [g,d,r] q n) (hf : pochList [g,l*v*q/g] q n ≠ 0)
 (ho : ∀ k ≤ n,
 pochList [q,v*q/g,d,r*s/a,l*q^(1-(n : ℤ))/g,v*l*q^(n+1)/g] q k*poch (l*v/g) q (2*k) ≠ 0)
 (hi : ∀ k ≤ n, phiDefined [l,d/s,r] q k ∧ phiDefined [g/l,d*q^k,s*r*q^k/a] q (n-k)) :
 phi [a,b,v*q^n,q^(-(n : ℤ))] [g,d,r] q q n =
 pochList [g/l,v*q/g] q n/pochList [g,l*v*q/g] q n*l^n *
 ∑ k ∈ Finset.range (n+1),
 pochList [l*v/g,l,r/a,d/s,v*q^n,q^(-(n : ℤ))] q k * poch (l*v*q/g) q (2*k) /
 (pochList [q,v*q/g,d,r*s/a,l*q^(1-(n : ℤ))/g,v*l*q^(n+1)/g] q k*poch (l*v/g) q (2*k)) *
 (s*q/g)^k *
 phi [a/s,b,l*v*q^k/g,q^(-(k : ℤ))] [l,d/s,r] q q k *
 phi [s,b/l,v*q^(n+k),q^((k : ℤ)-n)] [g/l,d*q^k,s*r*q^k/a] q q (n-k) := by
  sorry

end FiniteQBenchmark.Identity087
