import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-19 — 终止平衡 4φ3 的 very-well-poised 反写
Original representative source: GR2-III-19
Frozen statement: formulas/train/FQI-SRC-GR2-III-19.md
Source formula:
{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},a,b,c\\d,e,f\end{matrix};q,q\right]=\frac{(d/b,d/c;q)_n}{(d,d/(bc);q)_n}W_8^{[n]}(\sigma;f/a,e/a,b,c,q^{-n};q,efq^n/(bc)),\quad\sigma=ef/(aq).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity263
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d ee f sigma q : K) (n : ℕ)
 (hbase : regular q) (hnz : a*b*c*d*ee*f ≠ 0) (hs : sigma = ee*f/(a*q)) (hs1 : sigma ≠ 1) (hbal : d*ee*f = a*b*c*q^(1-(n:ℤ)))
 (h_domain : phiDefined [d,ee,f] q (n) ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    (b * c) ≠ 0 ∧
    (pochList [d,(d / (b * c))] q (n)) ≠ 0 ∧
    a ≠ 0 ∧
    wDefined sigma [(f / a),(ee / a),b,c,(q^((-(n : ℤ)) : ℤ))] q (n)) :
 (phi [(q^((-(n : ℤ)) : ℤ)),a,b,c] [d,ee,f] q q (n)) = (((pochList [(d / b),(d / c)] q (n)) / (pochList [d,(d / (b * c))] q (n))) * (wellPoisedRaw sigma [(f / a),(ee / a),b,c,(q^((-(n : ℤ)) : ℤ))] q (((ee * f) * (q^(((n : ℤ)) : ℤ))) / (b * c)) (n))) := by
  sorry

end FiniteQBenchmark.Identity263
