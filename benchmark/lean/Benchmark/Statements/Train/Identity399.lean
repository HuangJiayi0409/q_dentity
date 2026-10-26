import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-4.48 — T₁ 与 T₀ 的 q-三项式递推
Original representative source: SILLS-4.48
Frozen statement: formulas/train/FQI-SRC-SILLS-4.48.md
Source formula:
T_1(n,j;q)=T_1(n-1,j;q)+q^{n+j}T_0(n-1,j+1;q)+q^{n-j}T_0(n-1,j-1;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity399
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ) (j : ℤ) (hn : 1 ≤ n) (hq : q ≠ 0) :
 sillsT01 q true n j = sillsT01 q true (n-1) j +
 q^((n:ℤ)+j)*sillsT01 q false (n-1) (j+1)+q^((n:ℤ)-j)*sillsT01 q false (n-1) (j-1) := by
  sorry

end FiniteQBenchmark.Identity399
