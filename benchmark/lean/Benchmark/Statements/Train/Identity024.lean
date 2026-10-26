import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-POCHHAMMER-ROOTS — 单位根参数有限乘积分解
Original representative source: GR2-I-30
Frozen statement: formulas/train/FQI-POCHHAMMER-ROOTS.md
Source formula:
(a^m;q^m)_n=\prod_{j=0}^{m-1}(a\omega_m^j;q)_n,\qquad\omega_m=e^{2\pi i/m}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity024
variable {K : Type*} [Field K]

theorem statement (a q w : ℂ) (m n : ℕ) (hm : 0 < m) (hw : IsPrimitiveRoot w m) :
 poch (a^m) (q^m) n = ∏ j ∈ Finset.range m, poch (a*w^j) q n := by
  sorry

end FiniteQBenchmark.Identity024
