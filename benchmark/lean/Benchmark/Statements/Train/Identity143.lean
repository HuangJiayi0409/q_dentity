import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.7.7 — Askey–Wilson 多项式降阶差分
Original representative source: GR2-7.7.7
Frozen statement: formulas/train/FQI-SRC-GR2-7.7.7.md
Source formula:
\mathcal D_qP_n(z;a,b,c,d)=\frac{2q^{(1-n)/2}(1-q^n)(1-abcdq^{n-1})}{1-q}P_{n-1}(z;as,bs,cs,ds),\quad s^2=q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity143
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z a b c d s q : K) [CharZero K] (n : ℕ)
 (hbase : regular q) (hn : 1 ≤ n) (hs : s^2 = q) (hnz : ∀ v ∈ [a,z], v ≠ 0)
 (h_domain : (s * z) ≠ 0 ∧
    phiDefined [(a * b),(a * c),(a * d)] q (n) ∧
    a ≠ 0 ∧
    s ≠ 0 ∧
    (z / s) ≠ 0 ∧
    z ≠ 0 ∧
    2 ≠ 0 ∧
    (((s - (1 / s)) * (z - (1 / z))) / 2) ≠ 0 ∧
    (1 - q) ≠ 0 ∧
    phiDefined [((a * s) * (b * s)),((a * s) * (c * s)),((a * s) * (d * s))] q (n-1) ∧
    (a * s) ≠ 0) :
 (((askeyWilson ((s * z)) (a) (b) (c) (d) (q) (n)) - (askeyWilson ((z / s)) (a) (b) (c) (d) (q) (n))) / (((s - (1 / s)) * (z - (1 / z))) / 2)) = (((((2 * (s^((1-(n : ℤ)) : ℤ))) * (1 - (q^(((n : ℤ)) : ℤ)))) * (1 - ((((a * b) * c) * d) * (q^(((n : ℤ)-1) : ℤ))))) / (1 - q)) * (askeyWilson (z) ((a * s)) ((b * s)) ((c * s)) ((d * s)) (q) (n-1))) := by
  sorry

end FiniteQBenchmark.Identity143
