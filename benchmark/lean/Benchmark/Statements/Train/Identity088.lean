import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex36iii — 任意阶终止级数的 Gasper 展开
Original representative source: GR2-2.Ex36iii
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex36iii.md
Source formula:
{}_{r+2}\phi_{s+1}^{[n]}(q^{-n},\nu,\boldsymbol a;\gamma,\boldsymbol b;q,z)=\frac{(\lambda,\nu;q)_n}{(\gamma,\mu;q)_n}\sum_{k=0}^n\frac{(q^{-n},\gamma\mu/(\lambda\nu);q)_{n-k}}{(q,q^{1-n}/\lambda;q)_{n-k}}q^{n-k}{}_3\phi_2^{[n-k]}(\mu/\nu,\gamma/\nu,q^{k-n};\gamma\mu/(\lambda\nu),q^{1-n}/\nu;q,q^{1-k}/\lambda){}_{r+2}\phi_{s+1}^{[k]}(q^{-k},\mu,\boldsymbol a;\lambda,\boldsymbol b;q,z).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity088
variable {K : Type*} [Field K]

theorem statement (v g l u q z : K) (as bs : List K) (n : ℕ) (hq : regular q)
 (hl0 : l ≠ 0) (hv0 : v ≠ 0) (hl : phiDefined (g :: bs) q n)
 (hf : pochList [g,u] q n ≠ 0)
 (ho : ∀ k ≤ n, pochList [q,q^(1-(n : ℤ))/l] q (n-k) ≠ 0)
 (hi : ∀ k ≤ n, phiDefined [g*u/(l*v),q^(1-(n : ℤ))/v] q (n-k) ∧ phiDefined (l :: bs) q k) :
 phi ([q^(-(n : ℤ)),v] ++ as) (g :: bs) q z n =
 pochList [l,v] q n/pochList [g,u] q n * ∑ k ∈ Finset.range (n+1),
 pochList [q^(-(n : ℤ)),g*u/(l*v)] q (n-k)/pochList [q,q^(1-(n : ℤ))/l] q (n-k)*q^(n-k) *
 phi [u/v,g/v,q^((k : ℤ)-n)] [g*u/(l*v),q^(1-(n : ℤ))/v] q (q^(1-(k : ℤ))/l) (n-k) *
 phi ([q^(-(k : ℤ)),u] ++ as) (l :: bs) q z k := by
  sorry

end FiniteQBenchmark.Identity088
