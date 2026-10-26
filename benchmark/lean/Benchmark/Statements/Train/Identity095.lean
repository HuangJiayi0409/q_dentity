import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.8.14 — 有限双底数和到二次 10φ9
Original representative source: GR2-3.8.14
Frozen statement: formulas/train/FQI-SRC-GR2-3.8.14.md
Source formula:
\sum_{k=0}^n\frac{1-acq^{3k}}{1-ac}\frac{(a,b,cq/b;q)_k(f,a^2c^2q^{2n+1}/f,q^{-2n};q^2)_kq^k}{(cq^2,acq^2/b,abq;q^2)_k(acq/f,fq^{-2n}/(ac),acq^{2n+1};q)_k}=\frac{(acq;q)_{2n}(ac^2q^2/(bf),abq/f;q^2)_n}{(acq/f;q)_{2n}(abq,ac^2q^2/b;q^2)_n}W_{10}^{[n]}(ac^2/b;f,ac/b,c,cq/b,cq^2/b,a^2c^2q^{2n+1}/f,q^{-2n};q^2,q^2).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity095
variable {K : Type*} [Field K]

theorem statement (a b c f q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c,f], x ≠ 0) (hac : a*c ≠ 1)
 (hl : ∀ k ≤ n, pochList [c*q^2,a*c*q^2/b,a*b*q] (q^2) k *
 pochList [a*c*q/f,f*q^(-2*(n : ℤ))/(a*c),a*c*q^(2*n+1)] q k ≠ 0)
 (hf : poch (a*c*q/f) q (2*n)*pochList [a*b*q,a*c^2*q^2/b] (q^2) n ≠ 0)
 (hw : wDefined (a*c^2/b) [f,a*c/b,c,c*q/b,c*q^2/b,a^2*c^2*q^(2*n+1)/f,q^(-2*(n : ℤ))] (q^2) n) :
 (∑ k ∈ Finset.range (n+1), (1-a*c*q^(3*k))/(1-a*c)*
 pochList [a,b,c*q/b] q k*pochList [f,a^2*c^2*q^(2*n+1)/f,q^(-2*(n : ℤ))] (q^2) k*q^k /
 (pochList [c*q^2,a*c*q^2/b,a*b*q] (q^2) k * pochList [a*c*q/f,f*q^(-2*(n : ℤ))/(a*c),a*c*q^(2*n+1)] q k)) =
 poch (a*c*q) q (2*n)*pochList [a*c^2*q^2/(b*f),a*b*q/f] (q^2) n /
 (poch (a*c*q/f) q (2*n)*pochList [a*b*q,a*c^2*q^2/b] (q^2) n) *
 wellPoisedRaw (a*c^2/b) [f,a*c/b,c,c*q/b,c*q^2/b,a^2*c^2*q^(2*n+1)/f,q^(-2*(n : ℤ))] (q^2) (q^2) n := by
  sorry

end FiniteQBenchmark.Identity095
