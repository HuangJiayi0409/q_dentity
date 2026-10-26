import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-6.19 — Schur 辅助系数的有限乘积
Original representative source: AQ-6.19
Frozen statement: formulas/train/FQI-SRC-AQ-6.19.md
Source formula:
a_n(q)=\frac{(-q,-q^2;q^3)_n}{(q^3;q^3)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity320
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ)
 (hstep : ∀ j ∈ Finset.Icc 1 n, 1-q^(3*j) ≠ 0) (hden : ∀ j ≤ n, poch (q^3) (q^3) j ≠ 0)
 (h_domain : (pochList [(q^3)] (q^3) (n)) ≠ 0) :
 (aqSchurCoeff q n) = ((pochList [(-q),(-(q^2))] (q^3) (n)) / (pochList [(q^3)] (q^3) (n))) := by
  sorry

end FiniteQBenchmark.Identity320
