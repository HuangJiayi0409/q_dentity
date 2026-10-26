import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.9.8 — 双连续 q-超球平方展开（修订）
Original representative source: GR2-8.9.8
Frozen statement: formulas/train/FQI-SRC-GR2-8.9.8.md
Source formula:
{}_7\phi_6^{[n]}(q^{-n},q^{n+\alpha+2},q^{(\alpha+1)/2},q^{(\alpha+1)/2}z^2,q^{(\alpha+1)/2}/z^2,q^{(\alpha+2)/2}w^2,q^{(\alpha+2)/2}/w^2;q^{\alpha+1},q^{(\alpha+3)/2},-q^{(\alpha+3)/2},-q^{(\alpha+2)/2},-q^{(\alpha+2)/2},-q^{(\alpha+1)/2};q,q)=\sum_{j=0}^n\frac{(q^{-n},q^{n+\alpha+2},q^{(\alpha+2)/2},q^{(\alpha+2)/2}w^2,q^{(\alpha+2)/2}/w^2;q)_j(-1)^jq^{j+\binom j2}}{(q,q^{(\alpha+3)/2},-q^{(\alpha+3)/2},-q^{(\alpha+2)/2},q^{j+\alpha+1};q)_j}\left[\frac{(q;q)_j(q;q)_{n-j}q^{[n(\alpha+2)+2j(n-j)-j]/4}}{(q^{\alpha+1};q)_j(q^{2j+\alpha+2};q)_{n-j}}C_j(z;q^{(\alpha+1)/2})C_{n-j}(w;q^{j+(\alpha+2)/2})\right]^2.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity174
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (alpha L z w q : ℂ) (n : ℕ)
 (hbase : regular q) (hL : Complex.exp L = q) (hz : z ≠ 0) (hw : w ≠ 0)
 (h_domain : (z * z) ≠ 0 ∧
    (w * w) ≠ 0 ∧
    phiDefined [(Complex.exp (L*(alpha+1))),(Complex.exp (L*((alpha+3)/2))),(-(Complex.exp (L*((alpha+3)/2)))),(-(Complex.exp (L*((alpha+2)/2)))),(-(Complex.exp (L*((alpha+2)/2)))),(-(Complex.exp (L*((alpha+1)/2))))] q (n) ∧
    ∀ j ∈ Finset.range (n+1), ((w * w) ≠ 0 ∧
    (pochList [q,(Complex.exp (L*((alpha+3)/2))),(-(Complex.exp (L*((alpha+3)/2)))),(-(Complex.exp (L*((alpha+2)/2)))),(Complex.exp (L*((j:ℂ)+alpha+1)))] q (j)) ≠ 0 ∧
    ((pochList [(Complex.exp (L*(alpha+1)))] q (j)) * (pochList [(Complex.exp (L*(2*(j:ℂ)+alpha+2)))] q (n-j))) ≠ 0 ∧
    z ≠ 0 ∧
    ∀ k ≤ (j), poch q q k ≠ 0 ∧
    w ≠ 0 ∧
    ∀ k ≤ (n-j), poch q q k ≠ 0)) :
 (phi [(q^((-(n : ℤ)) : ℤ)),(Complex.exp (L*((n:ℂ)+alpha+2))),(Complex.exp (L*((alpha+1)/2))),(((Complex.exp (L*((alpha+1)/2))) * z) * z),((Complex.exp (L*((alpha+1)/2))) / (z * z)),(((Complex.exp (L*((alpha+2)/2))) * w) * w),((Complex.exp (L*((alpha+2)/2))) / (w * w))] [(Complex.exp (L*(alpha+1))),(Complex.exp (L*((alpha+3)/2))),(-(Complex.exp (L*((alpha+3)/2)))),(-(Complex.exp (L*((alpha+2)/2)))),(-(Complex.exp (L*((alpha+2)/2)))),(-(Complex.exp (L*((alpha+1)/2))))] q q (n)) = (∑ j ∈ Finset.range (n+1), (((((pochList [(q^((-(n : ℤ)) : ℤ)),(Complex.exp (L*((n:ℂ)+alpha+2))),(Complex.exp (L*((alpha+2)/2))),(((Complex.exp (L*((alpha+2)/2))) * w) * w),((Complex.exp (L*((alpha+2)/2))) / (w * w))] q (j)) * ((-1:ℂ)^(((j : ℤ)) : ℤ))) * (q^(((j : ℤ)+(j : ℤ)*((j : ℤ)-1)/2) : ℤ))) / (pochList [q,(Complex.exp (L*((alpha+3)/2))),(-(Complex.exp (L*((alpha+3)/2)))),(-(Complex.exp (L*((alpha+2)/2)))),(Complex.exp (L*((j:ℂ)+alpha+1)))] q (j))) * (((((((pochList [q] q (j)) * (pochList [q] q (n-j))) * (Complex.exp (L*(((n:ℂ)*(alpha+2)+2*(j:ℂ)*((n:ℂ)-j)-j)/4)))) / ((pochList [(Complex.exp (L*(alpha+1)))] q (j)) * (pochList [(Complex.exp (L*(2*(j:ℂ)+alpha+2)))] q (n-j)))) * (ultraspherical (Complex.exp (L*((alpha+1)/2))) z q (j))) * (ultraspherical (Complex.exp (L*((j:ℂ)+(alpha+2)/2))) w q (n-j)))^2))) := by
  sorry

end FiniteQBenchmark.Identity174
