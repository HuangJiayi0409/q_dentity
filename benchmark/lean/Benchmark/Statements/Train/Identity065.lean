import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.3.4 — 终止 very-well-poised 4φ3 消去
Original representative source: GR2-2.3.4
Frozen statement: formulas/train/FQI-SRC-GR2-2.3.4.md
Source formula:
\sum_{k=0}^n\frac{1-aq^{2k}}{1-a}\frac{(a,q^{-n};q)_k}{(q,aq^{n+1};q)_k}q^{nk}=\delta_{n,0}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity065
variable {K : Type*} [Field K]

theorem statement (a q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 1)
 (hd : phiDefined [a*q^(n+1)] q n) :
 (∑ k ∈ Finset.range (n+1), (1-a*q^(2*k))/(1-a)*
 pochList [a,q^(-(n : ℤ))] q k/pochList [q,a*q^(n+1)] q k*q^(n*k)) =
 if n=0 then 1 else 0 := by
  sorry

end FiniteQBenchmark.Identity065
