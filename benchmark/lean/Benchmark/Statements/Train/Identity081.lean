import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex28 — 良配终止级数的有限展开
Original representative source: GR2-2.Ex28
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex28.md
Source formula:
{}_{r+3}\phi_{r+2}^{[n]}(a,\boldsymbol b,c,q^{-n};aq/\boldsymbol b,aq/c,aq^{n+1};q,qz)=\frac{(aq/(cz),q^{1-n}/c;q)_n}{(aq/c,q^{1-n}/(cz);q)_n}\sum_{k=0}^n\frac{(q^{-n}/(cz),1/z,q^{-n}/a,q^{-n};q)_k(1-q^{2k-n}/(cz))}{(q,aq/(cz),q/(cz),q^{1-n}/c;q)_k(1-q^{-n}/(cz))}\left(\frac{aq^{n+1}}c\right)^k{}_{r+3}\phi_{r+2}^{[n-k]}(a,\boldsymbol b,czq^{-k},q^{k-n};aq/\boldsymbol b,aq^{k+1}/(cz),aq^{n+1-k};q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity081
variable {K : Type*} [Field K]

theorem statement (a c q z : K) (bs : List K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,c,z] ++ bs, x ≠ 0)
 (hl : phiDefined (bs.map (fun b => a*q/b) ++ [a*q/c,a*q^(n+1)]) q n)
 (hf : pochList [a*q/c,q^(1-(n : ℤ))/(c*z)] q n ≠ 0)
 (hc : 1-q^(-(n : ℤ))/(c*z) ≠ 0)
 (ho : phiDefined [a*q/(c*z),q/(c*z),q^(1-(n : ℤ))/c] q n)
 (hi : ∀ k ≤ n, phiDefined (bs.map (fun b => a*q/b) ++ [a*q^(k+1)/(c*z),a*q^(n+1-k)]) q (n-k)) :
 phi ([a] ++ bs ++ [c,q^(-(n : ℤ))]) (bs.map (fun b => a*q/b) ++ [a*q/c,a*q^(n+1)]) q (q*z) n =
 pochList [a*q/(c*z),q^(1-(n : ℤ))/c] q n/pochList [a*q/c,q^(1-(n : ℤ))/(c*z)] q n *
 ∑ k ∈ Finset.range (n+1),
 pochList [q^(-(n : ℤ))/(c*z),1/z,q^(-(n : ℤ))/a,q^(-(n : ℤ))] q k * (1-q^(2*(k : ℤ)-n)/(c*z)) /
 (pochList [q,a*q/(c*z),q/(c*z),q^(1-(n : ℤ))/c] q k * (1-q^(-(n : ℤ))/(c*z))) *
 (a*q^(n+1)/c)^k *
 phi ([a] ++ bs ++ [c*z*q^(-(k : ℤ)),q^((k : ℤ)-n)])
 (bs.map (fun b => a*q/b) ++ [a*q^(k+1)/(c*z),a*q^(n+1-k)]) q q (n-k) := by
  sorry

end FiniteQBenchmark.Identity081
