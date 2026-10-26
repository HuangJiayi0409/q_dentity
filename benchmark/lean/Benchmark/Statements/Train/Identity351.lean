import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-20.66b — Rogers–Szegő 倒数变换
Original representative source: FINE-20.66b
Frozen statement: formulas/train/FQI-SRC-FINE-20.66b.md
Source formula:
f_n(u^{-1})=u^{-n}f_n(u).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity351
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (u q : K) (n : ℕ)
 (hu : u ≠ 0)
 (h_domain : True) :
 (rogersSzego (u⁻¹) q (n)) = ((u^((-(n : ℤ)) : ℤ)) * (rogersSzego (u) q (n))) := by
  sorry

end FiniteQBenchmark.Identity351
