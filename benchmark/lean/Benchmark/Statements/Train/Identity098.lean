import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.10.3 — Nassrallah–Rahman 有限二次变换
Original representative source: GR2-3.10.3
Frozen statement: formulas/train/FQI-SRC-GR2-3.10.3.md
Source formula:
\Phi_n[a^2,-aq^2,b^2,c^2;-a,a^2q^2/b^2,a^2q^2/c^2\mid-aq/w,q^{-n};w,-aq^{n+1};q^2,q;awq^{n+2}/(b^2c^2)]=\frac{(w/a,-aq;q)_n}{(w,-q;q)_n}{}_5\phi_4^{[n]}(a,aq,a^2q^2/w^2,a^2q^2/(b^2c^2),q^{-2n};a^2q^2/b^2,a^2q^2/c^2,aq^{1-n}/w,aq^{2-n}/w;q^2,q^2).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity098
variable {K : Type*} [Field K]

theorem statement (a b c w q : K) (n : ℕ) (hq : regular q) (hp : ∀ x ∈ [a,b,c,w], x ≠ 0)
 (hl : phiDefined [-a,a^2*q^2/b^2,a^2*q^2/c^2] (q^2) n)
 (hb : ∀ k ≤ n, pochList [w,-a*q^(n+1)] q k ≠ 0)
 (hf : pochList [w,-q] q n ≠ 0)
 (hr : phiDefined [a^2*q^2/b^2,a^2*q^2/c^2,a*q^(1-(n : ℤ))/w,a*q^(2-(n : ℤ))/w] (q^2) n) :
 bibasicPhi [a^2,-a*q^2,b^2,c^2] [-a,a^2*q^2/b^2,a^2*q^2/c^2]
 [-a*q/w,q^(-(n : ℤ))] [w,-a*q^(n+1)] (q^2) q (a*w*q^(n+2)/(b^2*c^2)) n =
 pochList [w/a,-a*q] q n/pochList [w,-q] q n *
 phi [a,a*q,a^2*q^2/w^2,a^2*q^2/(b^2*c^2),q^(-2*(n : ℤ))]
 [a^2*q^2/b^2,a^2*q^2/c^2,a*q^(1-(n : ℤ))/w,a*q^(2-(n : ℤ))/w] (q^2) (q^2) n := by
  sorry

end FiniteQBenchmark.Identity098
