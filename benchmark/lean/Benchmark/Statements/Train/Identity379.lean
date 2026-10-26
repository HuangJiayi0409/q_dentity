import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-2.75 — Schur 有界分拆的有限 q-三项式恒等式
Original representative source: SILLS-2.75
Frozen statement: formulas/train/FQI-SRC-SILLS-2.75.md
Source formula:
S_{3n-1}(x,q)=\sum_{j=-n}^nx^jq^{j(3j-1)/2}C_n(j;q^3).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity379
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (n : ℕ) (hx : x ≠ 0) :
 sillsS x q (3*(n:ℤ)-1) = ∑ j ∈ Finset.Icc (-(n:ℤ)) (n:ℤ),
 x^j*q^(j*(3*j-1)/2).toNat*sillsC (q^3) n j := by
  sorry

end FiniteQBenchmark.Identity379
