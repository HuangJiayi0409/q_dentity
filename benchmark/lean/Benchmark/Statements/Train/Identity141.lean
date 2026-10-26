import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.7.6 — Askey–Wilson 差分算子作用于有限积
Original representative source: GR2-7.7.6
Frozen statement: formulas/train/FQI-SRC-GR2-7.7.6.md
Source formula:
\mathcal D_q(az,a/z;q)_n=-\frac{2a(1-q^n)}{1-q}(asz,as/z;q)_{n-1},\quad s^2=q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity141
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z a s q : K) [CharZero K] (n : ℕ)
 (hbase : regular q) (hn : 1 ≤ n) (hs : s^2 = q) (hz : z ≠ 0)
 (h_domain : (s * z) ≠ 0 ∧
    s ≠ 0 ∧
    (z / s) ≠ 0 ∧
    z ≠ 0 ∧
    2 ≠ 0 ∧
    (((s - (1 / s)) * (z - (1 / z))) / 2) ≠ 0 ∧
    (1 - q) ≠ 0) :
 (((pochList [(a * (s * z)),(a / (s * z))] q (n)) - (pochList [(a * (z / s)),(a / (z / s))] q (n))) / (((s - (1 / s)) * (z - (1 / z))) / 2)) = ((((-2 * a) * (1 - (q^(((n : ℤ)) : ℤ)))) / (1 - q)) * (pochList [((a * s) * z),((a * s) / z)] q (n-1))) := by
  sorry

end FiniteQBenchmark.Identity141
