import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex12 — 成对参数的终止 10φ9 求和
Original representative source: GR2-2.Ex12
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex12.md
Source formula:
\sum_{k=0}^n\frac{1-aq^{2k}}{1-a}\frac{(a,a/b,a^2q^{n+1}/b,q^{-n};q)_k(b,bq;q^2)_kq^k}{(q,bq,bq^{-n}/a,aq^{n+1};q)_k(a^2q^2/b,a^2q/b;q^2)_k}=\frac{(aq,a^2q/b^2;q)_n}{(aq/b,a^2q/b;q)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity074
variable {K : Type*} [Field K]

theorem statement (a b q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 0) (hb : b ≠ 0) (ha1 : a ≠ 1)
 (hl : ∀ k ≤ n, pochList [q,b*q,b*q^(-(n : ℤ))/a,a*q^(n+1)] q k *
 pochList [a^2*q^2/b,a^2*q/b] (q^2) k ≠ 0)
 (hr : pochList [a*q/b,a^2*q/b] q n ≠ 0) :
 (∑ k ∈ Finset.range (n+1), (1-a*q^(2*k))/(1-a)*
 pochList [a,a/b,a^2*q^(n+1)/b,q^(-(n : ℤ))] q k * pochList [b,b*q] (q^2) k*q^k /
 (pochList [q,b*q,b*q^(-(n : ℤ))/a,a*q^(n+1)] q k * pochList [a^2*q^2/b,a^2*q/b] (q^2) k)) =
 pochList [a*q,a^2*q/b^2] q n/pochList [a*q/b,a^2*q/b] q n := by
  sorry

end FiniteQBenchmark.Identity074
