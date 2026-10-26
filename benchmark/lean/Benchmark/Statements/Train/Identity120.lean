import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-5.Ex18iii — Bailey 有限双边 5ψ5 求和
Original representative source: GR2-5.Ex18iii
Frozen statement: formulas/train/FQI-SRC-GR2-5.Ex18iii.md
Source formula:
\sum_{k=-n}^n\frac{(b,c,d,e,q^{-n};q)_k}{(q/b,q/c,q/d,q/e,q^{n+1};q)_k}q^k=\frac{(q,q/(bc),q/(bd),q/(cd);q)_n}{(q/b,q/c,q/d,q/(bcd);q)_n},\qquad bcde=q^{n+1}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity120
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (b c d e q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ x ∈ [b,c,d,e], x ≠ 0) (hbal : b*c*d*e = q^(n+1))
 (h_domain : ∀ k ∈ Finset.Icc (-(n:ℤ)) ((n:ℤ)), (pochListIntDefined [b,c,d,e,(q^((-(n : ℤ)) : ℤ))] q ((k : ℤ)) ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    e ≠ 0 ∧
    pochListIntDefined [((q^1) / b),((q^1) / c),((q^1) / d),((q^1) / e),(q^(((n : ℤ)+1) : ℤ))] q ((k : ℤ)) ∧
    (pochListInt [((q^1) / b),((q^1) / c),((q^1) / d),((q^1) / e),(q^(((n : ℤ)+1) : ℤ))] q ((k : ℤ))) ≠ 0) ∧
    (b * c) ≠ 0 ∧
    (b * d) ≠ 0 ∧
    (c * d) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    ((b * c) * d) ≠ 0 ∧
    (pochList [((q^1) / b),((q^1) / c),((q^1) / d),((q^1) / ((b * c) * d))] q (n)) ≠ 0) :
 (∑ k ∈ Finset.Icc (-(n:ℤ)) ((n:ℤ)), (((pochListInt [b,c,d,e,(q^((-(n : ℤ)) : ℤ))] q ((k : ℤ))) / (pochListInt [((q^1) / b),((q^1) / c),((q^1) / d),((q^1) / e),(q^(((n : ℤ)+1) : ℤ))] q ((k : ℤ)))) * (q^(((k : ℤ)) : ℤ)))) = ((1 * (pochList [(q^1),((q^1) / (b * c)),((q^1) / (b * d)),((q^1) / (c * d))] q (n))) / (pochList [((q^1) / b),((q^1) / c),((q^1) / d),((q^1) / ((b * c) * d))] q (n))) := by
  sorry

end FiniteQBenchmark.Identity120
