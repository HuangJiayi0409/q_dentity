import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.2.12 — Bateman 型终止乘积公式
Original representative source: GR2-8.2.12
Frozen statement: formulas/train/FQI-SRC-GR2-8.2.12.md
Source formula:
F_n(b,b_1,b_2,b_3)F_n(b,bb_3c_1/(aq),bb_3/(b_1b_2c_1),b_3)=\frac{(aq/b,aq/b_3;q)_n}{(b,b_3;q)_n}\left(\frac{bb_3}{aq}\right)^n\sum_{m=0}^n\frac{(q^{-n},aq^n,b_1c_1,b_2c_1,aq/(b_1b_2c_1);q)_mq^m}{(q,aq/b,aq/b_3,b_1b_2c_1,bb_3/(b_1b_2);q)_m}W_{10}^{[m]}(\mu;b_1,b_2,b_1b_2c_1/b,b_1b_2c_1/b_3,bb_3c_1/(aq),aq^m,q^{-m};q,q),\quad\mu=b_1b_2c_1/q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity162
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b b1 b2 b3 c1 q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [a,b,b1,b2,b3,c1], v ≠ 0)
 (h_domain : (b * b3) ≠ 0 ∧
    phiDefined [b,b3,((((q * a) * b1) * b2) / (b * b3))] q (n) ∧
    (a * q) ≠ 0 ∧
    ((b1 * b2) * c1) ≠ 0 ∧
    phiDefined [b,b3,((((q * a) * (((b * b3) * c1) / (a * q))) * ((b * b3) / ((b1 * b2) * c1))) / (b * b3))] q (n) ∧
    b ≠ 0 ∧
    b3 ≠ 0 ∧
    (pochList [b,b3] q (n)) ≠ 0 ∧
    ∀ m ∈ Finset.range (n+1), (((b1 * b2) * c1) ≠ 0 ∧
    b ≠ 0 ∧
    b3 ≠ 0 ∧
    (b1 * b2) ≠ 0 ∧
    (pochList [q,((a * q) / b),((a * q) / b3),((b1 * b2) * c1),((b * b3) / (b1 * b2))] q (m)) ≠ 0 ∧
    q ≠ 0 ∧
    (a * q) ≠ 0 ∧
    wDefined (((b1 * b2) * c1) / q) [b1,b2,(((b1 * b2) * c1) / b),(((b1 * b2) * c1) / b3),(((b * b3) * c1) / (a * q)),(a * (q^(((m : ℤ)) : ℤ))),(q^((-(m : ℤ)) : ℤ))] q (m))) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),(a * (q^(((n : ℤ)) : ℤ))),b1,b2] [b,b3,((((q * a) * b1) * b2) / (b * b3))] q q (n)) * (phi [(q^((-((n : ℤ))) : ℤ)),(a * (q^(((n : ℤ)) : ℤ))),(((b * b3) * c1) / (a * q)),((b * b3) / ((b1 * b2) * c1))] [b,b3,((((q * a) * (((b * b3) * c1) / (a * q))) * ((b * b3) / ((b1 * b2) * c1))) / (b * b3))] q q (n))) = ((((pochList [((a * q) / b),((a * q) / b3)] q (n)) / (pochList [b,b3] q (n))) * (((b * b3) / (a * q))^(((n : ℤ)) : ℤ))) * (∑ m ∈ Finset.range (n+1), ((((pochList [(q^((-(n : ℤ)) : ℤ)),(a * (q^(((n : ℤ)) : ℤ))),(b1 * c1),(b2 * c1),((a * q) / ((b1 * b2) * c1))] q (m)) * (q^(((m : ℤ)) : ℤ))) / (pochList [q,((a * q) / b),((a * q) / b3),((b1 * b2) * c1),((b * b3) / (b1 * b2))] q (m))) * (wellPoisedRaw (((b1 * b2) * c1) / q) [b1,b2,(((b1 * b2) * c1) / b),(((b1 * b2) * c1) / b3),(((b * b3) * c1) / (a * q)),(a * (q^(((m : ℤ)) : ℤ))),(q^((-(m : ℤ)) : ℤ))] q q (m))))) := by
  sorry

end FiniteQBenchmark.Identity162
