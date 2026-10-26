import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.7.5 — Rogers–Ramanujan 证明中的有限变换
Original representative source: GR2-2.7.5
Frozen statement: formulas/train/FQI-SRC-GR2-2.7.5.md
Source formula:
\sum_{k=0}^n\frac{(a;q)_k(1-aq^{2k})(q^{-n};q)_k}{(q;q)_k(1-a)(aq^{n+1};q)_k}q^{2k^2}(a^2q^n)^k=(aq;q)_n\sum_{k=0}^n\frac{(q^{-n};q)_k}{(q;q)_k}(-aq^{n+1})^kq^{k(k-1)/2}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity066
variable {K : Type*} [Field K]

theorem statement (a q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 1)
 (hd : phiDefined [a*q^(n+1)] q n) :
 (∑ k ∈ Finset.range (n+1), poch a q k*(1-a*q^(2*k))*poch (q^(-(n : ℤ))) q k /
 (poch q q k*(1-a)*poch (a*q^(n+1)) q k)*q^(2*k^2)*(a^2*q^n)^k) =
 poch (a*q) q n * ∑ k ∈ Finset.range (n+1),
 poch (q^(-(n : ℤ))) q k/poch q q k*(-a*q^(n+1))^k*q^(k*(k-1)/2) := by
  sorry

end FiniteQBenchmark.Identity066
