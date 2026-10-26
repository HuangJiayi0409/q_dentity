import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-10.7A — Rogers–Ramanujan 系数的递推与乘积
Original representative source: AQ-10.7A
Frozen statement: formulas/train/FQI-SRC-AQ-10.7A.md
Source formula:
a_0=1,\quad a_n=\frac{q^{2n-1}}{1-q^n}a_{n-1}=\frac{q^{n^2}}{(q;q)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity338
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ)
 (hn : 1 ≤ n) (hden : ∀ j ∈ Finset.Icc 1 n, 1-q^j ≠ 0)
 (h_domain : (1 - (q^n)) ≠ 0 ∧
    (pochList [q] q (n)) ≠ 0) :
 (aqRRCoeff q 0) = 1 ∧
 (aqRRCoeff q n) = (((q^(2*n-1)) / (1 - (q^n))) * (aqRRCoeff q (n-1))) ∧
 (((q^(2*n-1)) / (1 - (q^n))) * (aqRRCoeff q (n-1))) = ((q^(n*n)) / (pochList [q] q (n))) := by
  sorry

end FiniteQBenchmark.Identity338
