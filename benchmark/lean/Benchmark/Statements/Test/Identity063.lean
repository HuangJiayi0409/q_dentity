import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.2.4 — 终止基本超几何级数的降阶展开
Original representative source: GR2-2.2.4
Frozen statement: formulas/test/FQI-SRC-GR2-2.2.4.md
Source formula:
{}_{r+4}\phi_{r+3}^{[n]}(a,b,c,\boldsymbol u,q^{-n};aq/b,aq/c,\boldsymbol v;q,z)=\sum_{j=0}^n\frac{(aq/(bc),\boldsymbol u,q^{-n};q)_j(a;q)_{2j}}{(q,aq/b,aq/c,\boldsymbol v;q)_j}\left(-\frac{bcz}{aq}\right)^jq^{-j(j-1)/2}{}_{r+2}\phi_{r+1}^{[n-j]}(aq^{2j},q^j\boldsymbol u,q^{j-n};q^j\boldsymbol v;q,bcz/(aq^{j+1})).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity063
variable {K : Type*} [Field K]

theorem statement (a b c q z : K) (us vs : List K) (n : ℕ) (hq : regular q)
 (hlen : vs.length = us.length+1) (hp : ∀ x ∈ [a,b,c], x ≠ 0)
 (ho : phiDefined ([a*q/b,a*q/c] ++ vs) q n)
 (hi : ∀ j ≤ n, phiDefined (vs.map (fun v => q^j*v)) q (n-j)) :
 phi ([a,b,c] ++ us ++ [q^(-(n : ℤ))]) ([a*q/b,a*q/c] ++ vs) q z n =
 ∑ j ∈ Finset.range (n+1),
 pochList ([a*q/(b*c)] ++ us ++ [q^(-(n : ℤ))]) q j * poch a q (2*j) /
 pochList ([q,a*q/b,a*q/c] ++ vs) q j * (-b*c*z/(a*q))^j * q^(-((j : ℤ)*(j-1)/2)) *
 phi ([a*q^(2*j)] ++ us.map (fun u => q^j*u) ++ [q^((j : ℤ)-n)])
 (vs.map (fun v => q^j*v)) q (b*c*z/(a*q^(j+1))) (n-j) := by
  sorry

end FiniteQBenchmark.Identity063
