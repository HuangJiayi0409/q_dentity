import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.2.5 — 两个平衡终止 4φ3 的一般乘积展开
Original representative source: GR2-8.2.5
Frozen statement: formulas/train/FQI-SRC-GR2-8.2.5.md
Source formula:
F_n(b,b_1,b_2,b_3)F_n(c,c_1,c_2,c_3)=\sum_{m=0}^n\frac{(q^{-n},aq^n,c_1,c_2,qab_1/(bb_3),qab_2/(bb_3);q)_mq^m}{(q,c,c_3,qa/(bb_3),qac_1c_2/(cc_3),qab_1b_2/(bb_3);q)_m}\sum_{j=0}^m\frac{1-\lambda_mq^{2j}}{1-\lambda_m}\frac{(\lambda_m,b_1,b_2,bq^{-m}/a,b_3q^{-m}/a,q^{-m};q)_j}{(q,bb_3q^{-m}/(ab_1),bb_3q^{-m}/(ab_2),b_3,b,bb_3/a;q)_j}\left(\frac{bb_3q^m}{b_1b_2}\right)^j{}_5\phi_4^{[j]}(q^{-j},q^{1-m}/c,q^{1-m}/c_3,\lambda_mq^j,cc_3q^{-m}/(ac_1c_2);q^{1-m}/c_1,q^{1-m}/c_2,bq^{-m}/a,b_3q^{-m}/a;q,q),\quad\lambda_m=bb_3q^{-m-1}/a.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity160
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b b1 b2 b3 c c1 c2 c3 q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [a,b,b1,b2,b3,c,c1,c2,c3], v ≠ 0)
 (h_domain : (b * b3) ≠ 0 ∧
    phiDefined [b,b3,((((q * a) * b1) * b2) / (b * b3))] q (n) ∧
    (c * c3) ≠ 0 ∧
    phiDefined [c,c3,((((q * a) * c1) * c2) / (c * c3))] q (n) ∧
    ∀ m ∈ Finset.range (n+1), ((b * b3) ≠ 0 ∧
    (c * c3) ≠ 0 ∧
    (pochList [q,c,c3,((q * a) / (b * b3)),((((q * a) * c1) * c2) / (c * c3)),((((q * a) * b1) * b2) / (b * b3))] q (m)) ≠ 0 ∧
    ∀ j ∈ Finset.range (m+1), (a ≠ 0 ∧
    (1 - (((b * b3) * (q^((-(m : ℤ)-1) : ℤ))) / a)) ≠ 0 ∧
    (a * b1) ≠ 0 ∧
    (a * b2) ≠ 0 ∧
    (pochList [q,(((b * b3) * (q^((-(m : ℤ)) : ℤ))) / (a * b1)),(((b * b3) * (q^((-(m : ℤ)) : ℤ))) / (a * b2)),b3,b,((b * b3) / a)] q (j)) ≠ 0 ∧
    (b1 * b2) ≠ 0 ∧
    c ≠ 0 ∧
    c3 ≠ 0 ∧
    ((a * c1) * c2) ≠ 0 ∧
    c1 ≠ 0 ∧
    c2 ≠ 0 ∧
    phiDefined [((q^((1-(m : ℤ)) : ℤ)) / c1),((q^((1-(m : ℤ)) : ℤ)) / c2),((b * (q^((-(m : ℤ)) : ℤ))) / a),((b3 * (q^((-(m : ℤ)) : ℤ))) / a)] q (j)))) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),(a * (q^(((n : ℤ)) : ℤ))),b1,b2] [b,b3,((((q * a) * b1) * b2) / (b * b3))] q q (n)) * (phi [(q^((-((n : ℤ))) : ℤ)),(a * (q^(((n : ℤ)) : ℤ))),c1,c2] [c,c3,((((q * a) * c1) * c2) / (c * c3))] q q (n))) = (∑ m ∈ Finset.range (n+1), ((((pochList [(q^((-(n : ℤ)) : ℤ)),(a * (q^(((n : ℤ)) : ℤ))),c1,c2,(((q * a) * b1) / (b * b3)),(((q * a) * b2) / (b * b3))] q (m)) * (q^(((m : ℤ)) : ℤ))) / (pochList [q,c,c3,((q * a) / (b * b3)),((((q * a) * c1) * c2) / (c * c3)),((((q * a) * b1) * b2) / (b * b3))] q (m))) * (∑ j ∈ Finset.range (m+1), ((((((1 - ((((b * b3) * (q^((-(m : ℤ)-1) : ℤ))) / a) * (q^((2*(j : ℤ)) : ℤ)))) / (1 - (((b * b3) * (q^((-(m : ℤ)-1) : ℤ))) / a))) * (pochList [(((b * b3) * (q^((-(m : ℤ)-1) : ℤ))) / a),b1,b2,((b * (q^((-(m : ℤ)) : ℤ))) / a),((b3 * (q^((-(m : ℤ)) : ℤ))) / a),(q^((-(m : ℤ)) : ℤ))] q (j))) / (pochList [q,(((b * b3) * (q^((-(m : ℤ)) : ℤ))) / (a * b1)),(((b * b3) * (q^((-(m : ℤ)) : ℤ))) / (a * b2)),b3,b,((b * b3) / a)] q (j))) * ((((b * b3) * (q^(((m : ℤ)) : ℤ))) / (b1 * b2))^(((j : ℤ)) : ℤ))) * (phi [(q^((-(j : ℤ)) : ℤ)),((q^((1-(m : ℤ)) : ℤ)) / c),((q^((1-(m : ℤ)) : ℤ)) / c3),((((b * b3) * (q^((-(m : ℤ)-1) : ℤ))) / a) * (q^(((j : ℤ)) : ℤ))),(((c * c3) * (q^((-(m : ℤ)) : ℤ))) / ((a * c1) * c2))] [((q^((1-(m : ℤ)) : ℤ)) / c1),((q^((1-(m : ℤ)) : ℤ)) / c2),((b * (q^((-(m : ℤ)) : ℤ))) / a),((b3 * (q^((-(m : ℤ)) : ℤ))) / a)] q q (j)))))) := by
  sorry

end FiniteQBenchmark.Identity160
