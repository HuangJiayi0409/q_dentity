import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-15 — Sears 平衡终止 4φ3 变换
Original representative source: GR2-III-15
Frozen statement: formulas/train/FQI-SRC-GR2-III-15.md
Source formula:
{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},a,b,c\\d,e,f\end{matrix};q,q\right]=a^n\frac{(e/a,f/a;q)_n}{(e,f;q)_n}{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},a,d/b,d/c\\d,aq^{1-n}/e,aq^{1-n}/f\end{matrix};q,q\right]
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity262
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d ee f q : K) (n : ℕ)
 (hbase : regular q) (hnz : a*b*c*ee*f ≠ 0) (hbal : d*ee*f = a*b*c*q^(1-(n:ℤ)))
 (h_domain : phiDefined [d,ee,f] q (n) ∧
    a ≠ 0 ∧
    (pochList [ee,f] q (n)) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    ee ≠ 0 ∧
    f ≠ 0 ∧
    phiDefined [d,((a * (q^((1-(n : ℤ)) : ℤ))) / ee),((a * (q^((1-(n : ℤ)) : ℤ))) / f)] q (n)) :
 (phi [(q^((-(n : ℤ)) : ℤ)),a,b,c] [d,ee,f] q q (n)) = ((((a^n) * (pochList [(ee / a),(f / a)] q (n))) / (pochList [ee,f] q (n))) * (phi [(q^((-(n : ℤ)) : ℤ)),a,(d / b),(d / c)] [d,((a * (q^((1-(n : ℤ)) : ℤ))) / ee),((a * (q^((1-(n : ℤ)) : ℤ))) / f)] q q (n))) := by
  sorry

end FiniteQBenchmark.Identity262
