import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-5.Ex11 — 双边终止 8ψ8 到 4ψ4
Original representative source: GR2-5.Ex11
Frozen statement: formulas/train/FQI-SRC-GR2-5.Ex11.md
Source formula:
\sum_{k=-n}^n\frac{1-aq^{2k}}{1-a}\frac{(c,d,e,f,aq^{-n},q^{-n};q)_k}{(aq/c,aq/d,aq/e,aq/f,q^{n+1},aq^{n+1};q)_k}\left(\frac{a^2q^{2n+2}}{cdef}\right)^k=\frac{(aq,q/a,aq/(cd),aq/(ef);q)_n}{(q/c,q/d,aq/e,aq/f;q)_n}\sum_{k=-n}^n\frac{(e,f,aq^{n+1}/(cd),q^{-n};q)_k}{(aq/c,aq/d,q^{n+1},ef/(aq^n);q)_k}q^k.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity119
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a c d e f q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ x ∈ [a,c,d,e,f], x ≠ 0)
 (h_domain : ∀ k ∈ Finset.Icc (-(n:ℤ)) ((n:ℤ)), ((1 - a) ≠ 0 ∧
    pochListIntDefined [c,d,e,f,(a * (q^((-(n : ℤ)) : ℤ))),(q^((-(n : ℤ)) : ℤ))] q ((k : ℤ)) ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    e ≠ 0 ∧
    f ≠ 0 ∧
    pochListIntDefined [((a * q) / c),((a * q) / d),((a * q) / e),((a * q) / f),(q^(((n : ℤ)+1) : ℤ)),(a * (q^(((n : ℤ)+1) : ℤ)))] q ((k : ℤ)) ∧
    (pochListInt [((a * q) / c),((a * q) / d),((a * q) / e),((a * q) / f),(q^(((n : ℤ)+1) : ℤ)),(a * (q^(((n : ℤ)+1) : ℤ)))] q ((k : ℤ))) ≠ 0 ∧
    (((c * d) * e) * f) ≠ 0) ∧
    a ≠ 0 ∧
    (c * d) ≠ 0 ∧
    (e * f) ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    e ≠ 0 ∧
    f ≠ 0 ∧
    (pochList [(q / c),(q / d),((a * q) / e),((a * q) / f)] q (n)) ≠ 0 ∧
    ∀ k ∈ Finset.Icc (-(n:ℤ)) ((n:ℤ)), ((c * d) ≠ 0 ∧
    pochListIntDefined [e,f,((a * (q^(((n : ℤ)+1) : ℤ))) / (c * d)),(q^((-(n : ℤ)) : ℤ))] q ((k : ℤ)) ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    (a * (q^(((n : ℤ)) : ℤ))) ≠ 0 ∧
    pochListIntDefined [((a * q) / c),((a * q) / d),(q^(((n : ℤ)+1) : ℤ)),((e * f) / (a * (q^(((n : ℤ)) : ℤ))))] q ((k : ℤ)) ∧
    (pochListInt [((a * q) / c),((a * q) / d),(q^(((n : ℤ)+1) : ℤ)),((e * f) / (a * (q^(((n : ℤ)) : ℤ))))] q ((k : ℤ))) ≠ 0)) :
 (∑ k ∈ Finset.Icc (-(n:ℤ)) ((n:ℤ)), (((((1 - (a * (q^((2*(k : ℤ)) : ℤ)))) / (1 - a)) * (pochListInt [c,d,e,f,(a * (q^((-(n : ℤ)) : ℤ))),(q^((-(n : ℤ)) : ℤ))] q ((k : ℤ)))) / (pochListInt [((a * q) / c),((a * q) / d),((a * q) / e),((a * q) / f),(q^(((n : ℤ)+1) : ℤ)),(a * (q^(((n : ℤ)+1) : ℤ)))] q ((k : ℤ)))) * ((((a * a) * (q^((2*(n : ℤ)+2) : ℤ))) / (((c * d) * e) * f))^(((k : ℤ)) : ℤ)))) = (((pochList [(a * q),(q / a),((a * q) / (c * d)),((a * q) / (e * f))] q (n)) / (pochList [(q / c),(q / d),((a * q) / e),((a * q) / f)] q (n))) * (∑ k ∈ Finset.Icc (-(n:ℤ)) ((n:ℤ)), (((pochListInt [e,f,((a * (q^(((n : ℤ)+1) : ℤ))) / (c * d)),(q^((-(n : ℤ)) : ℤ))] q ((k : ℤ))) / (pochListInt [((a * q) / c),((a * q) / d),(q^(((n : ℤ)+1) : ℤ)),((e * f) / (a * (q^(((n : ℤ)) : ℤ))))] q ((k : ℤ)))) * (q^(((k : ℤ)) : ℤ))))) := by
  sorry

end FiniteQBenchmark.Identity119
