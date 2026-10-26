import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.10.14 — 第二类有限双底数二次变换
Original representative source: GR2-3.10.14
Frozen statement: formulas/train/FQI-SRC-GR2-3.10.14.md
Source formula:
\Phi_n[a^2,aq^2,-aq^2,b^2,c^2;a,-a,a^2q^2/b^2,a^2q^2/c^2\mid-aq/w,q^{-n};w,-aq^{n+1};q^2,q;awq^{n+1}/(b^2c^2)]=\frac{(-aq,aq^2/w,w/(aq);q)_n}{(-q,aq/w,w;q)_n}{}_5\phi_4^{[n]}(aq,aq^2,a^2q^2/(b^2c^2),a^2q^2/w^2,q^{-2n};a^2q^2/b^2,a^2q^2/c^2,aq^{2-n}/w,aq^{3-n}/w;q^2,q^2).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity104
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c w q : K) (n : ℕ)
 (hbase : regular q) (ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0) (hw : w ≠ 0)
 (h_domain : (b * b) ≠ 0 ∧
    (c * c) ≠ 0 ∧
    w ≠ 0 ∧
    (((b * b) * c) * c) ≠ 0 ∧
    phiDefined [a,(-a),((((a * a) * q) * q) / (b * b)),((((a * a) * q) * q) / (c * c))] (q^2) (n) ∧
    ∀ k ≤ (n), pochList [w,((-a) * (q^(((n : ℤ)+1) : ℤ)))] q k ≠ 0 ∧
    (a * q) ≠ 0 ∧
    (pochList [(-q),((a * q) / w),w] q (n)) ≠ 0 ∧
    (w * w) ≠ 0 ∧
    phiDefined [((((a * a) * q) * q) / (b * b)),((((a * a) * q) * q) / (c * c)),((a * (q^((2-(n : ℤ)) : ℤ))) / w),((a * (q^((3-(n : ℤ)) : ℤ))) / w)] (q * q) (n)) :
 (bibasicPhi [(a * a),((a * q) * q),(((-a) * q) * q),(b * b),(c * c)] [a,(-a),((((a * a) * q) * q) / (b * b)),((((a * a) * q) * q) / (c * c))] [(((-a) * q) / w),(q^((-(n : ℤ)) : ℤ))] [w,((-a) * (q^(((n : ℤ)+1) : ℤ)))] (q^2) q (((a * w) * (q^(((n : ℤ)+1) : ℤ))) / (((b * b) * c) * c)) (n)) = (((pochList [((-a) * q),(((a * q) * q) / w),(w / (a * q))] q (n)) / (pochList [(-q),((a * q) / w),w] q (n))) * (phi [(a * q),((a * q) * q),((((a * a) * q) * q) / (((b * b) * c) * c)),((((a * a) * q) * q) / (w * w)),(q^((-2*(n : ℤ)) : ℤ))] [((((a * a) * q) * q) / (b * b)),((((a * a) * q) * q) / (c * c)),((a * (q^((2-(n : ℤ)) : ℤ))) / w),((a * (q^((3-(n : ℤ)) : ℤ))) / w)] (q * q) (q * q) (n))) := by
  sorry

end FiniteQBenchmark.Identity104
