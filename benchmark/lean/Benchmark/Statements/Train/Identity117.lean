import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.Ex31ii — 有限三次变换（二）
Original representative source: GR2-3.Ex31ii
Frozen statement: formulas/train/FQI-SRC-GR2-3.Ex31ii.md
Source formula:
\sum_{k=0}^n\frac{(1-aq^{4k})(1-bq^{-2k})}{(1-a)(1-b)}\frac{(a,1/(ab);q)_k(abq;q)_{2k}(c,a/(bc);q^3)_kq^{3k}}{(q^3,a^2bq^3;q^3)_k(q/b;q)_{2k}(aq/c,bcq;q)_k}=\frac{(aq,bq;q)_n(cq^3,aq^3/(bc);q^3)_n}{(aq/c,bcq;q)_n(q^3,aq^3/b;q^3)_n}W_{10}^{[n]}(a/b;1/(ab^2),c,a/(bc),aq^{n+1},aq^{n+2},aq^{n+3},q^{-3n};q^3,q^3).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity117
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ x ∈ [a,b,c], x ≠ 0)
 (h_domain : ∀ k ∈ Finset.range (n+1), (((1 - a) * (1 - b)) ≠ 0 ∧
    (a * b) ≠ 0 ∧
    (b * c) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    (((pochList [(q^3),(((a * a) * b) * (q^3))] (q^3) (k)) * (pochList [(q / b)] q (2*k))) * (pochList [((a * q) / c),((b * c) * q)] q (k))) ≠ 0) ∧
    (b * c) ≠ 0 ∧
    c ≠ 0 ∧
    b ≠ 0 ∧
    ((pochList [((a * q) / c),((b * c) * q)] q (n)) * (pochList [(q^3),((a * (q^3)) / b)] (q^3) (n))) ≠ 0 ∧
    ((a * b) * b) ≠ 0 ∧
    wDefined (a / b) [(1 / ((a * b) * b)),c,(a / (b * c)),(a * (q^(((n : ℤ)+1) : ℤ))),(a * (q^(((n : ℤ)+2) : ℤ))),(a * (q^(((n : ℤ)+3) : ℤ))),(q^((-3*(n : ℤ)) : ℤ))] (q^3) (n)) :
 (∑ k ∈ Finset.range (n+1), ((((((((1 - (a * (q^((4*(k : ℤ)) : ℤ)))) * (1 - (b * (q^((-2*(k : ℤ)) : ℤ))))) / ((1 - a) * (1 - b))) * (pochList [a,(1 / (a * b))] q (k))) * (pochList [((a * b) * q)] q (2*k))) * (pochList [c,(a / (b * c))] (q^3) (k))) * (q^((3*(k : ℤ)) : ℤ))) / (((pochList [(q^3),(((a * a) * b) * (q^3))] (q^3) (k)) * (pochList [(q / b)] q (2*k))) * (pochList [((a * q) / c),((b * c) * q)] q (k))))) = ((((pochList [(a * q),(b * q)] q (n)) * (pochList [(c * (q^3)),((a * (q^3)) / (b * c))] (q^3) (n))) / ((pochList [((a * q) / c),((b * c) * q)] q (n)) * (pochList [(q^3),((a * (q^3)) / b)] (q^3) (n)))) * (wellPoisedRaw (a / b) [(1 / ((a * b) * b)),c,(a / (b * c)),(a * (q^(((n : ℤ)+1) : ℤ))),(a * (q^(((n : ℤ)+2) : ℤ))),(a * (q^(((n : ℤ)+3) : ℤ))),(q^((-3*(n : ℤ)) : ℤ))] (q^3) (q^3) (n))) := by
  sorry

end FiniteQBenchmark.Identity117
