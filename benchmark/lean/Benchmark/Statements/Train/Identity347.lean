import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-15.31 — Fine 系数的一阶递推
Original representative source: FINE-15.31
Frozen statement: formulas/train/FQI-SRC-FINE-15.31.md
Source formula:
(1-bq^n)A_n=-aq^n A_{n-1}+\frac{(-1)^n(1-b)q^{n(n+1)/2}}{(q;q)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity347
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (n : ℕ)
 (hn : 1 ≤ n)
 (h_domain : ∀ j ≤ (n), poch q q j ≠ 0 ∧ poch (b*q) q j ≠ 0 ∧
    ∀ j ≤ (n-1), poch q q j ≠ 0 ∧ poch (b*q) q j ≠ 0 ∧
    (pochList [q] q (n)) ≠ 0) :
 ((1 - (b * (q^n))) * (fineA a b q (n))) = ((((-a) * (q^n)) * (fineA a b q (n-1))) + (((((-1:K)^n) * (1 - b)) * (q^(n*(n+1)/2))) / (pochList [q] q (n)))) := by
  sorry

end FiniteQBenchmark.Identity347
