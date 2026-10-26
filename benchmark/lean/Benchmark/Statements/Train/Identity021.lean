import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-Q-DYSON — A 型 q-Dyson 常数项
Original representative source: GR2-2.NoteEx31
Frozen statement: formulas/train/FQI-Q-DYSON.md
Source formula:
\operatorname{CT}_{x_1,\ldots,x_m}\prod_{1\le i<j\le m}(x_i/x_j;q)_{a_i}(qx_j/x_i;q)_{a_j}=\frac{(q;q)_{a_1+\cdots+a_m}}{\prod_{i=1}^m(q;q)_{a_i}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity021
variable {K : Type*} [Field K]

theorem statement (q : K) (m : ℕ) (hm : 1 ≤ m) (a : Fin m → ℕ)
 (hden : ∀ i, poch q q (a i) ≠ 0) :
 (dysonProduct q a).coeff 0 = poch q q (∑ i, a i) / ∏ i, poch q q (a i) := by
  sorry

end FiniteQBenchmark.Identity021
