import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-20.69 — Rogers–Szegő 在 q^{-1/2} 处的特殊值
Original representative source: FINE-20.69
Frozen statement: formulas/test/FQI-SRC-FINE-20.69.md
Source formula:
f_n(q^{-1/2})=q^{-n/2}f_n(q^{1/2}).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity352
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (s q : K) (n : ℕ)
 (hs : s^2 = q) (hq : q ≠ 0)
 (h_domain : True) :
 (rogersSzego (s⁻¹) q (n)) = ((s^((-(n : ℤ)) : ℤ)) * (rogersSzego (s) q (n))) := by
  sorry

end FiniteQBenchmark.Identity352
