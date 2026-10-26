import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-22 — 终止 q-Clausen 平方公式
Original representative source: GR2-III-22
Frozen statement: formulas/train/FQI-SRC-GR2-III-22.md
Source formula:
\left[\sum_{k=0}^L\frac{(a,b,abz,ab/z;q)_kq^k}{(q,-ab;q)_k(a^2b^2q;q^2)_k}\right]^2=\sum_{k=0}^R\frac{(a^2,b^2,ab,abz,ab/z;q)_kq^k}{(q,-ab,a^2b^2;q)_k(a^2b^2q;q^2)_k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity265
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b z q : K) (L R : ℕ)
 (hbase : regular q) (hz : z ≠ 0) (hL : terminatesAt [a,b,a*b*z,a*b/z] q L) (hR : terminatesAt [a^2,b^2,a*b,a*b*z,a*b/z] q R)
 (h_domain : ∀ k ∈ Finset.range (L+1), (z ≠ 0 ∧
    ((pochList [q,((-a) * b)] q (k)) * (pochList [(((a^2) * (b^2)) * q)] (q^2) (k))) ≠ 0) ∧
    ∀ k ∈ Finset.range (R+1), (z ≠ 0 ∧
    ((pochList [q,((-a) * b),((a^2) * (b^2))] q (k)) * (pochList [(((a^2) * (b^2)) * q)] (q^2) (k))) ≠ 0)) :
 ((∑ k ∈ Finset.range (L+1), (((pochList [a,b,((a * b) * z),((a * b) / z)] q (k)) * (q^(((k : ℤ)) : ℤ))) / ((pochList [q,((-a) * b)] q (k)) * (pochList [(((a^2) * (b^2)) * q)] (q^2) (k)))))^2) = (∑ k ∈ Finset.range (R+1), (((pochList [(a^2),(b^2),(a * b),((a * b) * z),((a * b) / z)] q (k)) * (q^(((k : ℤ)) : ℤ))) / ((pochList [q,((-a) * b),((a^2) * (b^2))] q (k)) * (pochList [(((a^2) * (b^2)) * q)] (q^2) (k))))) := by
  sorry

end FiniteQBenchmark.Identity265
