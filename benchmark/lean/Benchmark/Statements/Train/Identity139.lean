import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.6.8 — Askey–Wilson 单参数连接系数求值
Original representative source: GR2-7.6.8
Frozen statement: formulas/train/FQI-SRC-GR2-7.6.8.md
Source formula:
P_n(z;\alpha,b,c,d)=\sum_{k=0}^n\frac{(\alpha/a;q)_{n-k}(\alpha bcdq^{n-1};q)_k(q,bc,bd,cd;q)_na^{n-k}}{(q,bc,bd,cd;q)_k(abcdq^{k-1};q)_k(q,abcdq^{2k};q)_{n-k}}P_k(z;a,b,c,d).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity139
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z alpha a b c d q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [a,alpha,z], v ≠ 0)
 (h_domain : z ≠ 0 ∧
    phiDefined [(alpha * b),(alpha * c),(alpha * d)] q (n) ∧
    alpha ≠ 0 ∧
    ∀ k ∈ Finset.range (n+1), (a ≠ 0 ∧
    (((pochList [q,(b * c),(b * d),(c * d)] q (k)) * (pochList [((((a * b) * c) * d) * (q^(((k : ℤ)-1) : ℤ)))] q (k))) * (pochList [q,((((a * b) * c) * d) * (q^((2*(k : ℤ)) : ℤ)))] q (n-k))) ≠ 0 ∧
    z ≠ 0 ∧
    phiDefined [(a * b),(a * c),(a * d)] q (k))) :
 (askeyWilson (z) (alpha) (b) (c) (d) (q) (n)) = (∑ k ∈ Finset.range (n+1), ((((((pochList [(alpha / a)] q (n-k)) * (pochList [((((alpha * b) * c) * d) * (q^(((n : ℤ)-1) : ℤ)))] q (k))) * (pochList [q,(b * c),(b * d),(c * d)] q (n))) * (a^(((n : ℤ)-(k : ℤ)) : ℤ))) / (((pochList [q,(b * c),(b * d),(c * d)] q (k)) * (pochList [((((a * b) * c) * d) * (q^(((k : ℤ)-1) : ℤ)))] q (k))) * (pochList [q,((((a * b) * c) * d) * (q^((2*(k : ℤ)) : ℤ)))] q (n-k)))) * (askeyWilson (z) (a) (b) (c) (d) (q) (k)))) := by
  sorry

end FiniteQBenchmark.Identity139
