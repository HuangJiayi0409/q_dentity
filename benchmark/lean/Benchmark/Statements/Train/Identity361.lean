import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-1.79 — q-二项式级数的有限系数递推
Original representative source: SILLS-1.79
Frozen statement: formulas/train/FQI-SRC-SILLS-1.79.md
Source formula:
(1-q^n)A_n=(1-aq^{n-1})A_{n-1},\quad A_n=\frac{(a;q)_n}{(q;q)_n},\quad A_0=1.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity361
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n : ℕ)
 (hn : 1 ≤ n)
 (h_domain : (pochList [q] q (n)) ≠ 0 ∧
    (pochList [q] q (n-1)) ≠ 0 ∧
    (pochList [q] q (0)) ≠ 0) :
 (((1 - (q^n)) * (pochList [a] q (n))) / (pochList [q] q (n))) = (((1 - (a * (q^(n-1)))) * (pochList [a] q (n-1))) / (pochList [q] q (n-1))) ∧
 ((pochList [a] q (0)) / (pochList [q] q (0))) = 1 := by
  sorry

end FiniteQBenchmark.Identity361
