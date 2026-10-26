import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-6.18 — Schur 辅助系数递推
Original representative source: AQ-6.18
Frozen statement: formulas/train/FQI-SRC-AQ-6.18.md
Source formula:
a_0(q)=1,\quad a_n(q)=\frac{(1+q^{3n-1})(1+q^{3n-2})}{1-q^{3n}}a_{n-1}(q)\quad(n\ge1).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity319
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ) (hn : 1 ≤ n)
 (hden : ∀ j ≤ n, poch (q^3) (q^3) j ≠ 0) (hstep : ∀ j ∈ Finset.Icc 1 n, 1-q^(3*j) ≠ 0) :
 aqSchurCoeff q 0 = 1 ∧ aqSchurCoeff q n =
 (1+q^(3*n-1))*(1+q^(3*n-2))/(1-q^(3*n))*aqSchurCoeff q (n-1) := by
  sorry

end FiniteQBenchmark.Identity319
