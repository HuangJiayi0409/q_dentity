import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-07 — 终止 2φ1 到 3φ2 变换（二）
Original representative source: GR2-III-07
Frozen statement: formulas/train/FQI-SRC-GR2-III-07.md
Source formula:
{}_2\phi_1^{[n]}\!\left[\begin{matrix}q^{-n},b\\c\end{matrix};q,z\right]=\frac{(c/b;q)_n}{(c;q)_n}{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},b,bzq^{-n}/c\\bq^{1-n}/c,0\end{matrix};q,q\right]
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity256
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (b c z q : K) (n : ℕ)
 (hbase : regular q) (hnz : b*c ≠ 0)
 (h_domain : phiDefined [c] q (n) ∧
    b ≠ 0 ∧
    (pochList [c] q (n)) ≠ 0 ∧
    c ≠ 0 ∧
    phiDefined [((b * (q^((1-(n : ℤ)) : ℤ))) / c),0] q (n)) :
 (phi [(q^((-(n : ℤ)) : ℤ)),b] [c] q z (n)) = (((pochList [(c / b)] q (n)) / (pochList [c] q (n))) * (phi [(q^((-(n : ℤ)) : ℤ)),b,(((b * z) * (q^((-(n : ℤ)) : ℤ))) / c)] [((b * (q^((1-(n : ℤ)) : ℤ))) / c),0] q q (n))) := by
  sorry

end FiniteQBenchmark.Identity256
