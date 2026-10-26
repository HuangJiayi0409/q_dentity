import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex31-monomial — q 差分算子的单项式作用
Original representative source: GR2-1.Ex31-monomial
Frozen statement: formulas/test/FQI-SRC-GR2-1.Ex31-monomial.md
Source formula:
\Delta_bx^n=(bq^n-1)x^n,\qquad\Delta_bf(x)=bf(qx)-f(x).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity058
variable {K : Type*} [Field K]

theorem statement (b q x : K) (n : ℕ) : deltaOp q b (fun y => y^n) x = (b*q^n-1)*x^n := by
  sorry

end FiniteQBenchmark.Identity058
