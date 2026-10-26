import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex14ii — 近良配6φ5到12φ11变换
Original representative source: GR2-2.Ex14ii
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex14ii.md
Source formula:
{}_6\phi_5^{[n]}(s^2,qs,b,c,d,q^{-n};s,s^2q/b,s^2q/c,s^2q/d,s^4q^{1-n}/\lambda^2;q,q)=\frac{(\lambda/s^2,\lambda^2/s^2,-\lambda q/s;q)_n}{(\lambda q,\lambda^2/s^4,-\lambda/s;q)_n}\sum_{k=0}^n\frac{(1-\lambda q^{2k})(\lambda,\lambda b/s^2,\lambda c/s^2,\lambda d/s^2,qs,-s,\lambda^2q^n/s^2,q^{-n};q)_k(s^2q;q^2)_kq^k}{(1-\lambda)(q,s^2q/b,s^2q/c,s^2q/d,\lambda/s,-\lambda q/s,s^2q^{1-n}/\lambda,\lambda q^{n+1};q)_k(\lambda^2q/s^2;q^2)_k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity077
variable {K : Type*} [Field K]

theorem statement (s b c d l q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [s,b,c,d,l], x ≠ 0) (hdef : l = q*s^4/(b*c*d)) (hl1 : l ≠ 1)
 (hl : phiDefined [s,s^2*q/b,s^2*q/c,s^2*q/d,s^4*q^(1-(n : ℤ))/l^2] q n)
 (hf : pochList [l*q,l^2/s^4,-l/s] q n ≠ 0)
 (hr : ∀ k ≤ n,
 pochList [q,s^2*q/b,s^2*q/c,s^2*q/d,l/s,-l*q/s,s^2*q^(1-(n : ℤ))/l,l*q^(n+1)] q k *
 poch (l^2*q/s^2) (q^2) k ≠ 0) :
 phi [s^2,q*s,b,c,d,q^(-(n : ℤ))]
 [s,s^2*q/b,s^2*q/c,s^2*q/d,s^4*q^(1-(n : ℤ))/l^2] q q n =
 pochList [l/s^2,l^2/s^2,-l*q/s] q n/pochList [l*q,l^2/s^4,-l/s] q n *
 ∑ k ∈ Finset.range (n+1),
 (1-l*q^(2*k))*pochList [l,l*b/s^2,l*c/s^2,l*d/s^2,q*s,-s,l^2*q^n/s^2,q^(-(n : ℤ))] q k *
 poch (s^2*q) (q^2) k*q^k /
 ((1-l)*pochList [q,s^2*q/b,s^2*q/c,s^2*q/d,l/s,-l*q/s,s^2*q^(1-(n : ℤ))/l,l*q^(n+1)] q k *
 poch (l^2*q/s^2) (q^2) k) := by
  sorry

end FiniteQBenchmark.Identity077
