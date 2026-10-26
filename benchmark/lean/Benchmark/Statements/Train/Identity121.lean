import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-5.Ex18iv — Bailey 非对称长度的双边 5ψ5 求和
Original representative source: GR2-5.Ex18iv
Frozen statement: formulas/train/FQI-SRC-GR2-5.Ex18iv.md
Source formula:
\sum_{k=-n-1}^n\frac{(b,c,d,e,q^{-n};q)_k}{(q^2/b,q^2/c,q^2/d,q^2/e,q^{n+2};q)_k}q^k=\frac{(1-q)(q^2,q^2/(bc),q^2/(bd),q^2/(cd);q)_n}{(q^2/b,q^2/c,q^2/d,q^2/(bcd);q)_n},\qquad bcde=q^{n+3}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity121
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (b c d e q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ x ∈ [b,c,d,e], x ≠ 0) (hbal : b*c*d*e = q^(n+3))
 (h_domain : ∀ k ∈ Finset.Icc (-(n:ℤ)-1) ((n:ℤ)), (pochListIntDefined [b,c,d,e,(q^((-(n : ℤ)) : ℤ))] q ((k : ℤ)) ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    e ≠ 0 ∧
    pochListIntDefined [((q^2) / b),((q^2) / c),((q^2) / d),((q^2) / e),(q^(((n : ℤ)+2) : ℤ))] q ((k : ℤ)) ∧
    (pochListInt [((q^2) / b),((q^2) / c),((q^2) / d),((q^2) / e),(q^(((n : ℤ)+2) : ℤ))] q ((k : ℤ))) ≠ 0) ∧
    (b * c) ≠ 0 ∧
    (b * d) ≠ 0 ∧
    (c * d) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    ((b * c) * d) ≠ 0 ∧
    (pochList [((q^2) / b),((q^2) / c),((q^2) / d),((q^2) / ((b * c) * d))] q (n)) ≠ 0) :
 (∑ k ∈ Finset.Icc (-(n:ℤ)-1) ((n:ℤ)), (((pochListInt [b,c,d,e,(q^((-(n : ℤ)) : ℤ))] q ((k : ℤ))) / (pochListInt [((q^2) / b),((q^2) / c),((q^2) / d),((q^2) / e),(q^(((n : ℤ)+2) : ℤ))] q ((k : ℤ)))) * (q^(((k : ℤ)) : ℤ)))) = (((1 - q) * (pochList [(q^2),((q^2) / (b * c)),((q^2) / (b * d)),((q^2) / (c * d))] q (n))) / (pochList [((q^2) / b),((q^2) / c),((q^2) / d),((q^2) / ((b * c) * d))] q (n))) := by
  sorry

end FiniteQBenchmark.Identity121
