import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.4.7 — 连续 q-超球多项式的有限双和乘积
Original representative source: GR2-8.4.7
Frozen statement: formulas/train/FQI-SRC-GR2-8.4.7.md
Source formula:
r_n(z)r_n(w)=\frac{1+a^2q^n}{1+a^2}(-q^{-1/2})^n\sum_{m=0}^n\frac{(q^{-n},a^4q^n,-sz/w,-a^2sw/z;q)_mq^m}{(q,a^2s,-a^2s,-a^2q;q)_m}{}_4\phi_3^{[m]}(q^{-m},a^2,a^2w^2,a^2/z^2;a^4,-a^2sw/z,-sq^{-m}w/z;q,q),\quad s^2=q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity164
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a z w s q : K) (n : ℕ)
 (hbase : regular q) (hs : s^2 = q) (hnz : ∀ v ∈ [a,z,w], v ≠ 0)
 (h_domain : z ≠ 0 ∧
    phiDefined [((a * a) * s),((-a) * a),(((-a) * a) * s)] q (n) ∧
    w ≠ 0 ∧
    (1 + (a * a)) ≠ 0 ∧
    s ≠ 0 ∧
    ∀ m ∈ Finset.range (n+1), (w ≠ 0 ∧
    z ≠ 0 ∧
    (pochList [q,((a * a) * s),(((-a) * a) * s),(((-a) * a) * q)] q (m)) ≠ 0 ∧
    (z * z) ≠ 0 ∧
    phiDefined [(a^4),(((((-a) * a) * s) * w) / z),((((-s) * (q^((-(m : ℤ)) : ℤ))) * w) / z)] q (m))) :
 ((phi [(q^((-(n : ℤ)) : ℤ)),((a^4) * (q^(((n : ℤ)) : ℤ))),(a * z),(a / z)] [((a * a) * s),((-a) * a),(((-a) * a) * s)] q q (n)) * (phi [(q^((-(n : ℤ)) : ℤ)),((a^4) * (q^(((n : ℤ)) : ℤ))),(a * w),(a / w)] [((a * a) * s),((-a) * a),(((-a) * a) * s)] q q (n))) = ((((1 + ((a * a) * (q^(((n : ℤ)) : ℤ)))) / (1 + (a * a))) * ((-1 / s)^(((n : ℤ)) : ℤ))) * (∑ m ∈ Finset.range (n+1), ((((pochList [(q^((-(n : ℤ)) : ℤ)),((a^4) * (q^(((n : ℤ)) : ℤ))),(((-s) * z) / w),(((((-a) * a) * s) * w) / z)] q (m)) * (q^(((m : ℤ)) : ℤ))) / (pochList [q,((a * a) * s),(((-a) * a) * s),(((-a) * a) * q)] q (m))) * (phi [(q^((-(m : ℤ)) : ℤ)),(a * a),(((a * a) * w) * w),((a * a) / (z * z))] [(a^4),(((((-a) * a) * s) * w) / z),((((-s) * (q^((-(m : ℤ)) : ℤ))) * w) / z)] q q (m))))) := by
  sorry

end FiniteQBenchmark.Identity164
