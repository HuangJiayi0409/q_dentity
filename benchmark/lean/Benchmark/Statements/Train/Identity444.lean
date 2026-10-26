import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-26.22 — 相同伸缩参数下的根和递推
Original representative source: KAC-CHEUNG-26.22
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-26.22.md
Source formula:
s_n=\frac{nq}{n-1}s_{n-1}+\frac{n(h+h^{\prime})}{2}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity444
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q h h' a : ℂ) (n : ℕ) (T : ℕ → Polynomial ℂ)
 (hq : q ≠ 0) (hq1 : q ≠ 1) (hh : h ≠ h') (hn : 2 ≤ n)
 (hT : quantumTaylorFamily q q h h' a T n) :
 quantumRootSum T n = (n:ℂ)*q/((n:ℂ)-1)*quantumRootSum T (n-1)+(n:ℂ)*(h+h')/2 := by
  sorry

end FiniteQBenchmark.Identity444
