import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-5.7 — 乘法算子和 q 移位的交换
Original representative source: KAC-CHEUNG-5.7
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-5.7.md
Source formula:
M_qX=qXM_q,\qquad (Xf)(x)=xf(x),\quad(M_qf)(x)=f(qx).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity425
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (f : Polynomial K) (hq : q ≠ 0) (hq1 : q ≠ 1) :
 kacM q (kacX f) = q • kacX (kacM q f) := by
  sorry

end FiniteQBenchmark.Identity425
