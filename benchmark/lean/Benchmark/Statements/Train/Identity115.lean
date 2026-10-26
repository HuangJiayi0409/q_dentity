import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.Ex23 — 双底数 q-Lagrange 的有限系数反演
Original representative source: GR2-3.Ex23
Frozen statement: formulas/train/FQI-SRC-GR2-3.Ex23.md
Source formula:
f_j=\sum_{n=0}^jB_{jn}c_n\quad\Longleftrightarrow\quad c_n=\sum_{j=0}^nA_{nj}f_j.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity115
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b p q : K) (N : ℕ) (f c : ℕ → K)
 (hp : regular p) (hq : regular q) (ha : a ≠ 0) (hb : b ≠ 0)
 (hA : ∀ n ≤ N, ∀ j ≤ n, inverseADefined a b p q n j)
 (hB : ∀ j ≤ N, ∀ m ≤ j, pochList [q,a*q^(1+2*m)/b] q (j-m) ≠ 0) :
 (∀ j ≤ N, f j = ∑ n ∈ Finset.range (j+1), inverseB a b p q j n*c n) ↔
 (∀ n ≤ N, c n = ∑ j ∈ Finset.range (n+1), inverseA a b p q n j*f j) := by
  sorry

end FiniteQBenchmark.Identity115
