import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex17 — Carlitz 有限变换
Original representative source: GR2-1.Ex17
Frozen statement: formulas/test/FQI-SRC-GR2-1.Ex17.md
Source formula:
\sum_{k=0}^n\frac{(a,b;q)_k}{(q;q)_k}(-ab)^{n-k}q^{(n-k)(n+k-1)/2}=(a;q)_{n+1}\sum_{k=0}^n\frac{(-b)^kq^{k(k-1)/2}}{(q;q)_k(q;q)_{n-k}(1-aq^{n-k})}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity056
variable {K : Type*} [Field K]

theorem statement (a b q : K) (n : ℕ) (hq : regular q)
 (hd : ∀ k ≤ n, 1-a*q^(n-k) ≠ 0) :
 (∑ k ∈ Finset.range (n+1), pochList [a,b] q k/poch q q k * (-a*b)^(n-k)*q^((n-k)*(n+k-1)/2)) =
 poch a q (n+1) * ∑ k ∈ Finset.range (n+1), (-b)^k*q^(k*(k-1)/2) /
 (poch q q k * poch q q (n-k)*(1-a*q^(n-k))) := by
  sorry

end FiniteQBenchmark.Identity056
