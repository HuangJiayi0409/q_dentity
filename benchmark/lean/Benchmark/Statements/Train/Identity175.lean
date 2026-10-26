import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.9.9 — 一般终止 6φ5 的有限平方展开
Original representative source: GR2-8.9.9
Frozen statement: formulas/train/FQI-SRC-GR2-8.9.9.md
Source formula:
{}_6\phi_5^{[n]}(q^{-n},Aq^n,h^2,B,h^2z^2,h^2/z^2;h^2s,D,AB/D,-h^2s,-h^2;q,q)=\sum_{j=0}^n\frac{(q^{-n},Aq^n,h^2,A/D,D/B,h^2z^2,h^2/z^2;q)_j(-1)^jB^jq^{j(j+1)/2}}{(q,h^2s,-h^2s,-h^2,Aq^{j-1},D,AB/D;q)_j}\left[{}_4\phi_3^{[n-j]}(q^{j-n},Aq^{j+n},hs^jz,hs^j/z;h^2sq^j,-h^2sq^j,-h^2q^j;q,q)\right]^2.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity175
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (A B D h u s z q : K) (n : ℕ)
 (hbase : regular q) (hA : A = h^4) (hB : B = u^2) (hs : s^2 = q) (hnz : ∀ v ∈ [A,B,z], v ≠ 0) (hD : D ≠ 0)
 (h_domain : (z * z) ≠ 0 ∧
    D ≠ 0 ∧
    phiDefined [((h * h) * s),D,((A * B) / D),(((-h) * h) * s),((-h) * h)] q (n) ∧
    ∀ j ∈ Finset.range (n+1), (D ≠ 0 ∧
    B ≠ 0 ∧
    (z * z) ≠ 0 ∧
    (pochList [q,((h * h) * s),(((-h) * h) * s),((-h) * h),(A * (q^(((j : ℤ)-1) : ℤ))),D,((A * B) / D)] q (j)) ≠ 0 ∧
    z ≠ 0 ∧
    phiDefined [(((h * h) * s) * (q^(((j : ℤ)) : ℤ))),((((-h) * h) * s) * (q^(((j : ℤ)) : ℤ))),(((-h) * h) * (q^(((j : ℤ)) : ℤ)))] q (n-j))) :
 (phi [(q^((-(n : ℤ)) : ℤ)),(A * (q^(((n : ℤ)) : ℤ))),(h * h),B,(((h * h) * z) * z),((h * h) / (z * z))] [((h * h) * s),D,((A * B) / D),(((-h) * h) * s),((-h) * h)] q q (n)) = (∑ j ∈ Finset.range (n+1), ((((((pochList [(q^((-(n : ℤ)) : ℤ)),(A * (q^(((n : ℤ)) : ℤ))),(h * h),(A / D),(D / B),(((h * h) * z) * z),((h * h) / (z * z))] q (j)) * ((-1:K)^(((j : ℤ)) : ℤ))) * (B^(((j : ℤ)) : ℤ))) * (q^(((j : ℤ)*((j : ℤ)+1)/2) : ℤ))) / (pochList [q,((h * h) * s),(((-h) * h) * s),((-h) * h),(A * (q^(((j : ℤ)-1) : ℤ))),D,((A * B) / D)] q (j))) * ((phi [(q^(((j : ℤ)-(n : ℤ)) : ℤ)),(A * (q^(((j : ℤ)+(n : ℤ)) : ℤ))),((h * (s^(((j : ℤ)) : ℤ))) * z),((h * (s^(((j : ℤ)) : ℤ))) / z)] [(((h * h) * s) * (q^(((j : ℤ)) : ℤ))),((((-h) * h) * s) * (q^(((j : ℤ)) : ℤ))),(((-h) * h) * (q^(((j : ℤ)) : ℤ)))] q q (n-j))^2))) := by
  sorry

end FiniteQBenchmark.Identity175
