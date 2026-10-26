import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-2.39 — Rogers 连接系数乘积公式
Original representative source: AQ-2.39
Frozen statement: formulas/test/FQI-SRC-AQ-2.39.md
Source formula:
T(r,0)=1,\quad T(r,2n+1)=0,\quad T(r,2n)=\frac{(-1)^nq^{n(n-1)/2}(q^{r+1};q)_{n-1}(1-q^{r+2n})}{(q;q)_n}\ (n\ge1).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity308
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (r n : ℕ)
 
 (h_domain : True) :
 (aqInverseT q r 0) = 1 ∧
 (aqInverseT q r (2*n+1)) = 0 ∧
 (1 ≤ n → ((pochList [q] q (n)) ≠ 0) → aqInverseT q r (2*n) = ((((((-1:K)^n) * (q^(n*(n-1)/2))) * (pochList [(q^(r+1))] q (n-1))) * (1 - (q^(r+2*n)))) / (pochList [q] q (n)))) := by
  sorry

end FiniteQBenchmark.Identity308
