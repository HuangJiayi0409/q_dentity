import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.Ex14 — 连续 q-超球的 Chebyshev 边界
Original representative source: GR2-7.Ex14
Frozen statement: formulas/train/FQI-SRC-GR2-7.Ex14.md
Source formula:
C_n(z;q)=\sum_{k=0}^nz^{n-2k}=\frac{z^{n+1}-z^{-n-1}}{z-z^{-1}},\qquad\lim_{\beta\to1}\frac{1-q^n}{2(1-\beta)}C_n(z;\beta)=\frac{z^n+z^{-n}}2\quad(n\ge1).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity149
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z q : ℂ) (n : ℕ) (hq : regular q) (hz : z ≠ 0) :
 ultraspherical q z q n = (∑ k ∈ Finset.range (n+1), z^((n:ℤ)-2*k)) ∧
 (z-z⁻¹ ≠ 0 → ultraspherical q z q n = (z^(n+1)-z^(-(n:ℤ)-1))/(z-z⁻¹)) ∧
 (1 ≤ n → Filter.Tendsto (fun beta : ℂ => (1-q^n)/(2*(1-beta))*ultraspherical beta z q n)
    (nhdsWithin 1 ({1}ᶜ)) (nhds ((z^n+z^(-(n:ℤ)))/2))) := by
  sorry

end FiniteQBenchmark.Identity149
