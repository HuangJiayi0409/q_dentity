import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.10.11 — 终止 4φ3 的二次变换
Original representative source: GR2-3.10.11
Frozen statement: formulas/train/FQI-SRC-GR2-3.10.11.md
Source formula:
{}_4\phi_3^{[n]}(a,b,-w/b,q^{-n};aq/b,-bq^{-n},w;q,q)=\frac{(w/a,-aq/b;q)_n}{(w,-q/b;q)_n}{}_4\phi_3^{[n]}(a,a^2q^2/w^2,aq/b^2,q^{-2n};a^2q^2/b^2,aq^{1-n}/w,aq^{2-n}/w;q^2,q^2).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity103
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b w q : K) (n : ℕ)
 (hbase : regular q) (ha : a ≠ 0) (hb : b ≠ 0) (hw : w ≠ 0)
 (h_domain : b ≠ 0 ∧
    phiDefined [((a * q) / b),((-b) * (q^((-(n : ℤ)) : ℤ))),w] q (n) ∧
    a ≠ 0 ∧
    (pochList [w,((-q) / b)] q (n)) ≠ 0 ∧
    (w * w) ≠ 0 ∧
    (b * b) ≠ 0 ∧
    w ≠ 0 ∧
    phiDefined [((((a * a) * q) * q) / (b * b)),((a * (q^((1-(n : ℤ)) : ℤ))) / w),((a * (q^((2-(n : ℤ)) : ℤ))) / w)] (q * q) (n)) :
 (phi [a,b,((-w) / b),(q^((-(n : ℤ)) : ℤ))] [((a * q) / b),((-b) * (q^((-(n : ℤ)) : ℤ))),w] q q (n)) = (((pochList [(w / a),(((-a) * q) / b)] q (n)) / (pochList [w,((-q) / b)] q (n))) * (phi [a,((((a * a) * q) * q) / (w * w)),((a * q) / (b * b)),(q^((-2*(n : ℤ)) : ℤ))] [((((a * a) * q) * q) / (b * b)),((a * (q^((1-(n : ℤ)) : ℤ))) / w),((a * (q^((2-(n : ℤ)) : ℤ))) / w)] (q * q) (q * q) (n))) := by
  sorry

end FiniteQBenchmark.Identity103
