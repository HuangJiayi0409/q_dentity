import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.Ex17 — 连续 q-超球在零点的奇偶求值
Original representative source: GR2-7.Ex17
Frozen statement: formulas/test/FQI-SRC-GR2-7.Ex17.md
Source formula:
C_n(i;\beta)=\begin{cases}0&n\text{为奇数},\\(-1)^{n/2}(\beta^2;q^2)_{n/2}/(q^2;q^2)_{n/2}&n\text{为偶数}.\end{cases}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity150
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (beta q : ℂ) (n : ℕ) (hq : regular q) :
 ultraspherical beta Complex.I q n =
 if n%2 = 1 then 0 else (-1)^(n/2)*poch (beta^2) (q^2) (n/2)/poch (q^2) (q^2) (n/2) := by
  sorry

end FiniteQBenchmark.Identity150
