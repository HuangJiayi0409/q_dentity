import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-II-15 — 偶数终止长度的 q-Dixon 3φ2 求和
Original representative source: GR2-II-15
Frozen statement: formulas/train/FQI-SRC-GR2-II-15.md
Source formula:
{}_3\phi_2^{[2n]}\!\left[\begin{matrix}q^{-2n},b,c\\q^{1-2n}/b,q^{1-2n}/c\end{matrix};q,q^{2-n}/(bc)\right]=\frac{(b,c;q)_n(q,bc;q)_{2n}}{(q,bc;q)_n(b,c;q)_{2n}}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity247
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (b c q : K) (n : ℕ)
 (hbase : regular q) (hbc : b*c ≠ 0)
 (h_domain : b ≠ 0 ∧
    c ≠ 0 ∧
    (b * c) ≠ 0 ∧
    phiDefined [((q^((1-2*(n : ℤ)) : ℤ)) / b),((q^((1-2*(n : ℤ)) : ℤ)) / c)] q (2*n) ∧
    ((pochList [q,(b * c)] q (n)) * (pochList [b,c] q (2*n))) ≠ 0) :
 (phi [(q^((-2*(n : ℤ)) : ℤ)),b,c] [((q^((1-2*(n : ℤ)) : ℤ)) / b),((q^((1-2*(n : ℤ)) : ℤ)) / c)] q ((q^((2-(n : ℤ)) : ℤ)) / (b * c)) (2*n)) = (((pochList [b,c] q (n)) * (pochList [q,(b * c)] q (2*n))) / ((pochList [q,(b * c)] q (n)) * (pochList [b,c] q (2*n)))) := by
  sorry

end FiniteQBenchmark.Identity247
