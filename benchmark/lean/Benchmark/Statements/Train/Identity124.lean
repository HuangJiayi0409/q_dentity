import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-6.6.10 — 终止 8φ7 与有限部分和的变换
Original representative source: GR2-6.6.10
Frozen statement: formulas/train/FQI-SRC-GR2-6.6.10.md
Source formula:
W_8^{[m]}(a^2bc;abcd,ab,ac,a^2q^{m+1},q^{-m};q,q/(ad))=\frac{(a^2bcq,q,aq/b,aq/c;q)_m}{(qa^2,abq,acq,q/(bc);q)_m}\sum_{k=0}^m\frac{(1-a^2q^{2k})(a^2,ab,ac,ad;q)_k}{(1-a^2)(q,aq/b,aq/c,aq/d;q)_k}\left(\frac q{abcd}\right)^k.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity124
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d q : K) (m : ℕ)
 (hbase : regular q) (hnz : ∀ x ∈ [a,b,c,d], x ≠ 0)
 (h_domain : (a * d) ≠ 0 ∧
    wDefined (((a * a) * b) * c) [(((a * b) * c) * d),(a * b),(a * c),((a * a) * (q^(((m : ℤ)+1) : ℤ))),(q^((-(m : ℤ)) : ℤ))] q (m) ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    (b * c) ≠ 0 ∧
    (pochList [((q * a) * a),((a * b) * q),((a * c) * q),(q / (b * c))] q (m)) ≠ 0 ∧
    ∀ k ∈ Finset.range (m+1), (b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    ((1 - (a * a)) * (pochList [q,((a * q) / b),((a * q) / c),((a * q) / d)] q (k))) ≠ 0 ∧
    (((a * b) * c) * d) ≠ 0)) :
 (wellPoisedRaw (((a * a) * b) * c) [(((a * b) * c) * d),(a * b),(a * c),((a * a) * (q^(((m : ℤ)+1) : ℤ))),(q^((-(m : ℤ)) : ℤ))] q (q / (a * d)) (m)) = (((pochList [((((a * a) * b) * c) * q),q,((a * q) / b),((a * q) / c)] q (m)) / (pochList [((q * a) * a),((a * b) * q),((a * c) * q),(q / (b * c))] q (m))) * (∑ k ∈ Finset.range (m+1), ((((1 - ((a * a) * (q^((2*(k : ℤ)) : ℤ)))) * (pochList [(a * a),(a * b),(a * c),(a * d)] q (k))) / ((1 - (a * a)) * (pochList [q,((a * q) / b),((a * q) / c),((a * q) / d)] q (k)))) * ((q / (((a * b) * c) * d))^(((k : ℤ)) : ℤ))))) := by
  sorry

end FiniteQBenchmark.Identity124
