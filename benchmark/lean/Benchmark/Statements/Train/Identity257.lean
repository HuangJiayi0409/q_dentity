import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-08 — 终止 2φ1 到 3φ1 变换（第二版原印）
Original representative source: GR2-III-08
Frozen statement: formulas/train/FQI-SRC-GR2-III-08.md
Source formula:
{}_2\phi_1^{[n]}\!\left[\begin{matrix}q^{-n},b\\c\end{matrix};q,z\right]=b^n\frac{(c/b;q)_n}{(c;q)_n}{}_3\phi_1^{[n]}\!\left[\begin{matrix}q^{-n},b,q/z\\bq^{1-n}/c\end{matrix};q,z/c\right]
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity257
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (b c z q : K) (n : ℕ)
 (hbase : regular q) (hnz : b*c*z ≠ 0)
 (h_domain : phiDefined [c] q (n) ∧
    b ≠ 0 ∧
    (pochList [c] q (n)) ≠ 0 ∧
    z ≠ 0 ∧
    c ≠ 0 ∧
    phiDefined [((b * (q^((1-(n : ℤ)) : ℤ))) / c)] q (n)) :
 (phi [(q^((-(n : ℤ)) : ℤ)),b] [c] q z (n)) = ((((b^n) * (pochList [(c / b)] q (n))) / (pochList [c] q (n))) * (phi [(q^((-(n : ℤ)) : ℤ)),b,(q / z)] [((b * (q^((1-(n : ℤ)) : ℤ))) / c)] q (z / c) (n))) := by
  sorry

end FiniteQBenchmark.Identity257
