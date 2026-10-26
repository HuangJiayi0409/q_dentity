import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.3.17 — 双重有限和的正交消去
Original representative source: GR2-7.3.17
Frozen statement: formulas/train/FQI-SRC-GR2-7.3.17.md
Source formula:
\sum_{j=0}^m\sum_{k=0}^n\frac{(q^{-m},abq^{m+1};q)_j(q^{-n},abq^{n+1};q)_kq^{j+k}}{(q;q)_j(q;q)_k(abq^2;q)_{j+k}}=\frac{(q^{-n},abq^{n+1};q)_n}{(abq^2;q)_{2n}}(abq^{n+2})^n\delta_{mn}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity132
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (m n : ℕ)
 (hbase : regular q) (hmn : m ≤ n)
 (h_domain : ∀ j ∈ Finset.range (m+1), (∀ k ∈ Finset.range (n+1), ((((pochList [q] q (j)) * (pochList [q] q (k))) * (pochList [(((a * b) * q) * q)] q (j+k))) ≠ 0)) ∧
    (pochList [(((a * b) * q) * q)] q (2*n)) ≠ 0) :
 (∑ j ∈ Finset.range (m+1), (∑ k ∈ Finset.range (n+1), ((((pochList [(q^((-(m : ℤ)) : ℤ)),((a * b) * (q^(((m : ℤ)+1) : ℤ)))] q (j)) * (pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] q (k))) * (q^(((j : ℤ)+(k : ℤ)) : ℤ))) / (((pochList [q] q (j)) * (pochList [q] q (k))) * (pochList [(((a * b) * q) * q)] q (j+k)))))) = ((((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] q (n)) / (pochList [(((a * b) * q) * q)] q (2*n))) * (((a * b) * (q^(((n : ℤ)+2) : ℤ)))^(((n : ℤ)) : ℤ))) * (if (m) = (n) then (1 : K) else 0)) := by
  sorry

end FiniteQBenchmark.Identity132
