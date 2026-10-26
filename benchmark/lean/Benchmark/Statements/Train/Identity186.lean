import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex15 — 终止 4φ3 到 12W11 的变换
Original representative source: GR2-8.Ex15
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex15.md
Source formula:
{}_4\phi_3^{[n]}(a,b,c,d;bq/a,cq/a,dq/a;q,q^2/a^2)=\frac{(q^{1-n}/d,acq^{-n}/d;q)_n}{(aq^{-n}/d,cq^{1-n}/d;q)_n}W_{12}^{[n]}(bc/d;v,-v,u,-u,ab/d,ac/d,a,b,c;q,q/a),\quad b=q^{-n},\ u^2=bcq^2/(ad),\ v^2=bcq/(ad).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity186
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d u v q : K) (n : ℕ)
 (hbase : regular q) (hb : b = q^(-(n:ℤ))) (hu : u^2 = b*c*q^2/(a*d)) (hv : v^2 = b*c*q/(a*d)) (hnz : ∀ v ∈ [a,b,c,d], v ≠ 0)
 (h_domain : a ≠ 0 ∧
    (a * a) ≠ 0 ∧
    phiDefined [((b * q) / a),((c * q) / a),((d * q) / a)] q (n) ∧
    d ≠ 0 ∧
    (pochList [((a * (q^((-(n : ℤ)) : ℤ))) / d),((c * (q^((1-(n : ℤ)) : ℤ))) / d)] q (n)) ≠ 0 ∧
    wDefined ((b * c) / d) [v,(-v),u,(-u),((a * b) / d),((a * c) / d),a,b,c] q (n)) :
 (phi [a,b,c,d] [((b * q) / a),((c * q) / a),((d * q) / a)] q ((q * q) / (a * a)) (n)) = (((pochList [((q^((1-(n : ℤ)) : ℤ)) / d),(((a * c) * (q^((-(n : ℤ)) : ℤ))) / d)] q (n)) / (pochList [((a * (q^((-(n : ℤ)) : ℤ))) / d),((c * (q^((1-(n : ℤ)) : ℤ))) / d)] q (n))) * (wellPoisedRaw ((b * c) / d) [v,(-v),u,(-u),((a * b) / d),((a * c) / d),a,b,c] q (q / a) (n))) := by
  sorry

end FiniteQBenchmark.Identity186
