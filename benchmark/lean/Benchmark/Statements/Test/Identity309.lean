import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-2.40 — 终止 Heine 变换的有限乘积形式
Original representative source: AQ-2.40
Frozen statement: formulas/test/FQI-SRC-AQ-2.40.md
Source formula:
\sum_{j=0}^n\frac{(a,q^{-n};q)_jz^j}{(q,c;q)_j}=\frac1{(c;q)_n}\sum_{j=0}^n\frac{(q^{-n},azq^{-n}/c;q)_j(cq^n)^j}{(q;q)_j}(zq^{j-n};q)_{n-j}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity309
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a c z q : K) (n : ℕ)
 (hq : q ≠ 0) (hc : c ≠ 0)
 (h_domain : ∀ j ∈ Finset.range (n+1), ((pochList [q,c] q (j)) ≠ 0) ∧
    (pochList [c] q (n)) ≠ 0 ∧
    ∀ j ∈ Finset.range (n+1), (c ≠ 0 ∧
    (pochList [q] q (j)) ≠ 0)) :
 (∑ j ∈ Finset.range (n+1), (((pochList [a,(q^((-(n : ℤ)) : ℤ))] q (j)) * (z^j)) / (pochList [q,c] q (j)))) = ((1 / (pochList [c] q (n))) * (∑ j ∈ Finset.range (n+1), ((((pochList [(q^((-(n : ℤ)) : ℤ)),(((a * z) * (q^((-(n : ℤ)) : ℤ))) / c)] q (j)) * ((c * (q^(((n : ℤ)) : ℤ)))^j)) / (pochList [q] q (j))) * (pochList [(z * (q^(((j : ℤ)-(n : ℤ)) : ℤ)))] q (n-j))))) := by
  sorry

end FiniteQBenchmark.Identity309
