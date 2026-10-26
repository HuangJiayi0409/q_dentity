import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.8.15 — 长度两倍的有限双底数二次变换
Original representative source: GR2-3.8.15
Frozen statement: formulas/test/FQI-SRC-GR2-3.8.15.md
Source formula:
\sum_{k=0}^{2n}\frac{1-acq^{3k}}{1-ac}\frac{(d,f,a^2c^2q/(df);q^2)_k(a,cq^{2n+1},q^{-2n};q)_kq^k}{(acq/d,acq/f,df/(ac);q)_k(cq^2,aq^{1-2n},acq^{2n+2};q^2)_k}=\frac{(acq^2,dq/(ac),fq/(ac),acq^2/(df);q^2)_n}{(q/(ac),acq^2/d,acq^2/f,dfq/(ac);q^2)_n}W_{10}^{[n]}(acq^{-2n-1};c,d,f,a^2c^2q/(df),aq^{-2n-1},q^{1-2n},q^{-2n};q^2,q^2).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity096
variable {K : Type*} [Field K]

theorem statement (a c d f q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,c,d,f], x ≠ 0) (hac : a*c ≠ 1)
 (hl : ∀ k ≤ 2*n, pochList [a*c*q/d,a*c*q/f,d*f/(a*c)] q k *
 pochList [c*q^2,a*q^(1-2*(n : ℤ)),a*c*q^(2*n+2)] (q^2) k ≠ 0)
 (hf : pochList [q/(a*c),a*c*q^2/d,a*c*q^2/f,d*f*q/(a*c)] (q^2) n ≠ 0)
 (hw : wDefined (a*c*q^(-2*(n : ℤ)-1))
 [c,d,f,a^2*c^2*q/(d*f),a*q^(-2*(n : ℤ)-1),q^(1-2*(n : ℤ)),q^(-2*(n : ℤ))] (q^2) n) :
 (∑ k ∈ Finset.range (2*n+1), (1-a*c*q^(3*k))/(1-a*c)*
 pochList [d,f,a^2*c^2*q/(d*f)] (q^2) k*pochList [a,c*q^(2*n+1),q^(-2*(n : ℤ))] q k*q^k /
 (pochList [a*c*q/d,a*c*q/f,d*f/(a*c)] q k * pochList [c*q^2,a*q^(1-2*(n : ℤ)),a*c*q^(2*n+2)] (q^2) k)) =
 pochList [a*c*q^2,d*q/(a*c),f*q/(a*c),a*c*q^2/(d*f)] (q^2) n /
 pochList [q/(a*c),a*c*q^2/d,a*c*q^2/f,d*f*q/(a*c)] (q^2) n *
 wellPoisedRaw (a*c*q^(-2*(n : ℤ)-1))
 [c,d,f,a^2*c^2*q/(d*f),a*q^(-2*(n : ℤ)-1),q^(1-2*(n : ℤ)),q^(-2*(n : ℤ))] (q^2) (q^2) n := by
  sorry

end FiniteQBenchmark.Identity096
