import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-2.30 — Bailey 关系的终止超几何重写
Original representative source: SILLS-2.30
Frozen statement: formulas/train/FQI-SRC-SILLS-2.30.md
Source formula:
\beta_n=\frac1{(q,xq;q)_n}\sum_{r=0}^n\frac{(q^{-n};q)_r}{(xq^{n+1};q)_r}(-1)^rq^{nr-r(r-1)/2}\alpha_r.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity369
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (alpha : ℕ → K) (n : ℕ)
 (hq : q ≠ 0)
 (h_domain : baileyDefined x q n ∧
    (pochList [q,(x * q)] q (n)) ≠ 0 ∧
    ∀ r ∈ Finset.range (n+1), ((pochList [(x * (q^(((n : ℤ)+1) : ℤ)))] q (r)) ≠ 0)) :
 (baileySum x q alpha n) = ((1 / (pochList [q,(x * q)] q (n))) * (∑ r ∈ Finset.range (n+1), (((((pochList [(q^((-(n : ℤ)) : ℤ))] q (r)) / (pochList [(x * (q^(((n : ℤ)+1) : ℤ)))] q (r))) * ((-1:K)^r)) * (q^(((n : ℤ)*(r : ℤ)-(r : ℤ)*((r : ℤ)-1)/2) : ℤ))) * (alpha r)))) := by
  sorry

end FiniteQBenchmark.Identity369
