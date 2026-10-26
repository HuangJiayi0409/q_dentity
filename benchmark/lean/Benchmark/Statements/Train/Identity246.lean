import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-II-14 — 终止 q-Dixon 的 4φ3 形式
Original representative source: GR2-II-14
Frozen statement: formulas/train/FQI-SRC-GR2-II-14.md
Source formula:
{}_4\phi_3^{[n]}\!\left[\begin{matrix}a,-qs,b,q^{-n}\\-s,aq/b,aq^{n+1}\end{matrix};q,sq^{n+1}/b\right]=\frac{(aq,sq/b;q)_n}{(sq,aq/b;q)_n}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity246
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b s q : K) (n : ℕ)
 (hbase : regular q) (hs : s ≠ 0) (hb : b ≠ 0) (ha : a = s^2)
 (h_domain : b ≠ 0 ∧
    phiDefined [(-s),((a * q) / b),(a * (q^(((n : ℤ)+1) : ℤ)))] q (n) ∧
    (pochList [(s * q),((a * q) / b)] q (n)) ≠ 0) :
 (phi [a,((-q) * s),b,(q^((-(n : ℤ)) : ℤ))] [(-s),((a * q) / b),(a * (q^(((n : ℤ)+1) : ℤ)))] q ((s * (q^(((n : ℤ)+1) : ℤ))) / b) (n)) = ((pochList [(a * q),((s * q) / b)] q (n)) / (pochList [(s * q),((a * q) / b)] q (n))) := by
  sorry

end FiniteQBenchmark.Identity246
