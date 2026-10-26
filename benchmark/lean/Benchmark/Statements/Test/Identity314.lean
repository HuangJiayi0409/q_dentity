import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-3.35 — Rogers–Ramanujan Bailey 对的有限等式
Original representative source: AQ-3.35
Frozen statement: formulas/test/FQI-SRC-AQ-3.35.md
Source formula:
\frac1{(q;q)_n}=\frac1{(q;q)_n^2}+\sum_{r=1}^n\frac{(-1)^rq^{r(3r-1)/2}(1+q^r)}{(q;q)_{n-r}(q;q)_{n+r}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity314
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ)
 
 (h_domain : (pochList [q] q (n)) ≠ 0 ∧
    ((pochList [q] q (n))^2) ≠ 0 ∧
    ∀ r ∈ Finset.Icc (1) (n), (((pochList [q] q (n-r)) * (pochList [q] q (n+r))) ≠ 0)) :
 (1 / (pochList [q] q (n))) = ((1 / ((pochList [q] q (n))^2)) + (∑ r ∈ Finset.Icc (1) (n), (((((-1:K)^r) * (q^(r*(3*r-1)/2))) * (1 + (q^r))) / ((pochList [q] q (n-r)) * (pochList [q] q (n+r)))))) := by
  sorry

end FiniteQBenchmark.Identity314
