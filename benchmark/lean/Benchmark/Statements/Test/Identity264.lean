import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-21 — Singh 有限二次变换
Original representative source: GR2-III-21
Frozen statement: formulas/test/FQI-SRC-GR2-III-21.md
Source formula:
\sum_{k=0}^L\frac{(A,B,c,d;q)_kq^k}{(q,-cd;q)_k(ABq;q^2)_k}=\sum_{k=0}^R\frac{(A,B,c^2,d^2;q^2)_kq^{2k}}{(q^2,ABq,-cd,-cdq;q^2)_k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity264
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (A B c d q : K) (L R : ℕ)
 (hbase : regular q) (hL : terminatesAt [A,B,c,d] q L) (hR : terminatesAt [A,B,c^2,d^2] (q^2) R)
 (h_domain : ∀ k ∈ Finset.range (L+1), (((pochList [q,((-c) * d)] q (k)) * (pochList [((A * B) * q)] (q^2) (k))) ≠ 0) ∧
    ∀ k ∈ Finset.range (R+1), ((pochList [(q^2),((A * B) * q),((-c) * d),(((-c) * d) * q)] (q^2) (k)) ≠ 0)) :
 (∑ k ∈ Finset.range (L+1), (((pochList [A,B,c,d] q (k)) * (q^(((k : ℤ)) : ℤ))) / ((pochList [q,((-c) * d)] q (k)) * (pochList [((A * B) * q)] (q^2) (k))))) = (∑ k ∈ Finset.range (R+1), (((pochList [A,B,(c^2),(d^2)] (q^2) (k)) * (q^((2*(k : ℤ)) : ℤ))) / (pochList [(q^2),((A * B) * q),((-c) * d),(((-c) * d) * q)] (q^2) (k)))) := by
  sorry

end FiniteQBenchmark.Identity264
