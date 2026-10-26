import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.2.6 — Bailey 型终止 4φ3 乘积公式
Original representative source: GR2-8.2.6
Frozen statement: formulas/test/FQI-SRC-GR2-8.2.6.md
Source formula:
F_n(b,b_1,b_2,b_3)F_n(aq/b,c_1,c_2,aq/b_3)=S_n,\quad S_n=\sum_{m=0}^n\frac{(q^{-n},aq^n,c_1,c_2,qab_1/(bb_3),qab_2/(bb_3);q)_mq^m}{(q,aq/b,aq/b_3,aq/(bb_3),qab_1b_2/(bb_3),bb_3c_1c_2/(aq);q)_m}W_{10}^{[m]}(bb_3q^{-m-1}/a;b_1,b_2,bb_3c_1/(aq),bb_3c_2/(aq),bq^{-m}/a,b_3q^{-m}/a,q^{-m};q,aq^2/(b_1b_2c_1c_2)).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity161
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b b1 b2 b3 c1 c2 q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [a,b,b1,b2,b3,c1,c2], v ≠ 0)
 (h_domain : (b * b3) ≠ 0 ∧
    phiDefined [b,b3,((((q * a) * b1) * b2) / (b * b3))] q (n) ∧
    b ≠ 0 ∧
    b3 ≠ 0 ∧
    (((a * q) / b) * ((a * q) / b3)) ≠ 0 ∧
    phiDefined [((a * q) / b),((a * q) / b3),((((q * a) * c1) * c2) / (((a * q) / b) * ((a * q) / b3)))] q (n) ∧
    ∀ m ∈ Finset.range (n+1), ((b * b3) ≠ 0 ∧
    b ≠ 0 ∧
    b3 ≠ 0 ∧
    (a * q) ≠ 0 ∧
    (pochList [q,((a * q) / b),((a * q) / b3),((a * q) / (b * b3)),((((q * a) * b1) * b2) / (b * b3)),((((b * b3) * c1) * c2) / (a * q))] q (m)) ≠ 0 ∧
    a ≠ 0 ∧
    (((b1 * b2) * c1) * c2) ≠ 0 ∧
    wDefined (((b * b3) * (q^((-(m : ℤ)-1) : ℤ))) / a) [b1,b2,(((b * b3) * c1) / (a * q)),(((b * b3) * c2) / (a * q)),((b * (q^((-(m : ℤ)) : ℤ))) / a),((b3 * (q^((-(m : ℤ)) : ℤ))) / a),(q^((-(m : ℤ)) : ℤ))] q (m))) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),(a * (q^(((n : ℤ)) : ℤ))),b1,b2] [b,b3,((((q * a) * b1) * b2) / (b * b3))] q q (n)) * (phi [(q^((-((n : ℤ))) : ℤ)),(a * (q^(((n : ℤ)) : ℤ))),c1,c2] [((a * q) / b),((a * q) / b3),((((q * a) * c1) * c2) / (((a * q) / b) * ((a * q) / b3)))] q q (n))) = (∑ m ∈ Finset.range (n+1), ((((pochList [(q^((-(n : ℤ)) : ℤ)),(a * (q^(((n : ℤ)) : ℤ))),c1,c2,(((q * a) * b1) / (b * b3)),(((q * a) * b2) / (b * b3))] q (m)) * (q^(((m : ℤ)) : ℤ))) / (pochList [q,((a * q) / b),((a * q) / b3),((a * q) / (b * b3)),((((q * a) * b1) * b2) / (b * b3)),((((b * b3) * c1) * c2) / (a * q))] q (m))) * (wellPoisedRaw (((b * b3) * (q^((-(m : ℤ)-1) : ℤ))) / a) [b1,b2,(((b * b3) * c1) / (a * q)),(((b * b3) * c2) / (a * q)),((b * (q^((-(m : ℤ)) : ℤ))) / a),((b3 * (q^((-(m : ℤ)) : ℤ))) / a),(q^((-(m : ℤ)) : ℤ))] q (((a * q) * q) / (((b1 * b2) * c1) * c2)) (m)))) := by
  sorry

end FiniteQBenchmark.Identity161
