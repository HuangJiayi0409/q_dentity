import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.5.20 — Askey–Wilson 正交证明的有限消去式
Original representative source: GR2-7.5.20
Frozen statement: formulas/train/FQI-SRC-GR2-7.5.20.md
Source formula:
\sum_{j=0}^m\frac{(q^{-m},abcdq^{m-1};q)_jq^j}{(q,abcd;q)_j}{}_3\phi_2^{[n]}(q^{-n},abcdq^{n-1},abq^j;abcdq^j,ab;q,q)=\frac{(q,cd;q)_n(1-abcd/q)}{(abcd/q,ab;q)_n(1-abcdq^{2n-1})}(ab)^n\delta_{mn}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity135
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d q : K) (m n : ℕ)
 (hbase : regular q) (hnm : n ≤ m)
 (h_domain : ∀ j ∈ Finset.range (m+1), ((pochList [q,(((a * b) * c) * d)] q (j)) ≠ 0 ∧
    phiDefined [((((a * b) * c) * d) * (q^(((j : ℤ)) : ℤ))),(a * b)] q (n)) ∧
    q ≠ 0 ∧
    ((pochList [((((a * b) * c) * d) / q),(a * b)] q (n)) * (1 - ((((a * b) * c) * d) * (q^((2*(n : ℤ)-1) : ℤ))))) ≠ 0) :
 (∑ j ∈ Finset.range (m+1), ((((pochList [(q^((-(m : ℤ)) : ℤ)),((((a * b) * c) * d) * (q^(((m : ℤ)-1) : ℤ)))] q (j)) * (q^(((j : ℤ)) : ℤ))) / (pochList [q,(((a * b) * c) * d)] q (j))) * (phi [(q^((-(n : ℤ)) : ℤ)),((((a * b) * c) * d) * (q^(((n : ℤ)-1) : ℤ))),((a * b) * (q^(((j : ℤ)) : ℤ)))] [((((a * b) * c) * d) * (q^(((j : ℤ)) : ℤ))),(a * b)] q q (n)))) = (((((pochList [q,(c * d)] q (n)) * (1 - ((((a * b) * c) * d) / q))) / ((pochList [((((a * b) * c) * d) / q),(a * b)] q (n)) * (1 - ((((a * b) * c) * d) * (q^((2*(n : ℤ)-1) : ℤ)))))) * ((a * b)^(((n : ℤ)) : ℤ))) * (if (m) = (n) then (1 : K) else 0)) := by
  sorry

end FiniteQBenchmark.Identity135
