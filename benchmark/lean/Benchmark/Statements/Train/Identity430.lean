import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-7.8 — Galois 数递推
Original representative source: KAC-CHEUNG-7.8
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-7.8.md
Source formula:
G_{n+1}=2G_n+(q^n-1)G_{n-1},\quad G_0=1,\quad G_1=2.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity430
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ) (hq : q ≠ 0) (hq1 : q ≠ 1) (hn : 1 ≤ n) :
 galoisNumber q (n+1)=2*galoisNumber q n+(q^n-1)*galoisNumber q (n-1) ∧
 galoisNumber q 0=1 ∧ galoisNumber q 1=2 := by
  sorry

end FiniteQBenchmark.Identity430
