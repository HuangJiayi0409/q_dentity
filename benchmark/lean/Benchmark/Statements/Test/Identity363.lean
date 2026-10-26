import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-1.90 — q-三项式 Laurent 多项式递推
Original representative source: SILLS-1.90
Frozen statement: formulas/test/FQI-SRC-SILLS-1.90.md
Source formula:
\mathcal T_n(x,q)=(1+xq^{3n-2}+x^{-1}q^{3n-1})\mathcal T_{n-1}(x,q)+q^{3n-3}(1-q^{3n-3})\mathcal T_{n-2}(x,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity363
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (n : ℕ) (hn : 2 ≤ n) (hx : x ≠ 0) :
 sillsT x q n = (1+x*q^(3*n-2)+x⁻¹*q^(3*n-1))*sillsT x q (n-1)+q^(3*n-3)*(1-q^(3*n-3))*sillsT x q (n-2) ∧
 sillsT x q 0 = 1 ∧ sillsT x q 1 = 1+x*q+x⁻¹*q^2 := by
  sorry

end FiniteQBenchmark.Identity363
