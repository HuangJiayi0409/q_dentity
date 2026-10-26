import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-POCHHAMMER-RESIDUES — 有限乘积按剩余类拆分
Original representative source: GR2-I-27
Frozen statement: formulas/train/FQI-POCHHAMMER-RESIDUES.md
Source formula:
(a;q)_{mn}=\prod_{j=0}^{m-1}(aq^j;q^m)_n
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity023
variable {K : Type*} [Field K]

theorem statement (a q : K) (m n : ℕ) (hm : 0 < m) :
    poch a q (m*n) = ∏ j ∈ Finset.range m, poch (a*q^j) (q^m) n := by
  sorry

end FiniteQBenchmark.Identity023
