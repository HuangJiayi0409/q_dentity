import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-13 — 终止 3φ2 变换（三）
Original representative source: GR2-III-13
Frozen statement: formulas/train/FQI-SRC-GR2-III-13.md
Source formula:
{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},b,c\\d,e\end{matrix};q,deq^n/(bc)\right]=\frac{(e/c;q)_n}{(e;q)_n}{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},c,d/b\\d,cq^{1-n}/e\end{matrix};q,q\right]
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity260
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (b c d ee q : K) (n : ℕ)
 (hbase : regular q) (hnz : b*c*ee ≠ 0)
 (h_domain : (b * c) ≠ 0 ∧
    phiDefined [d,ee] q (n) ∧
    c ≠ 0 ∧
    (pochList [ee] q (n)) ≠ 0 ∧
    b ≠ 0 ∧
    ee ≠ 0 ∧
    phiDefined [d,((c * (q^((1-(n : ℤ)) : ℤ))) / ee)] q (n)) :
 (phi [(q^((-(n : ℤ)) : ℤ)),b,c] [d,ee] q (((d * ee) * (q^(((n : ℤ)) : ℤ))) / (b * c)) (n)) = (((pochList [(ee / c)] q (n)) / (pochList [ee] q (n))) * (phi [(q^((-(n : ℤ)) : ℤ)),c,(d / b)] [d,((c * (q^((1-(n : ℤ)) : ℤ))) / ee)] q q (n))) := by
  sorry

end FiniteQBenchmark.Identity260
