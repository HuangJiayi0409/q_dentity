import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-11.Ex22-p0 — 有限三次求和的基本超几何分支
Original representative source: GR2-11.Ex22-p0
Frozen statement: formulas/test/FQI-SRC-GR2-11.Ex22-p0.md
Source formula:
\sum_{k=0}^n\frac{1-aq^{4k}}{1-a}\frac{(b,c;q)_k(d;q)_{2k}(e,q^{-3n};q^3)_kq^k}{(aq^3/b,aq^3/c;q^3)_k(aq/d;q)_{2k}(aq/e,aq^{3n+1};q)_k}=\frac{(aq^3,a^2q^3/(bce),a^2q^3/(bde),aq^3/(cd);q^3)_n}{(a^2q^3/(be),aq^3/c,aq^3/d,a^2q^3/(bcde);q^3)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity213
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d ee q : K) (n : ℕ)
 (hbase : regular q) (hnz : a*b*c*d*ee ≠ 0) (hbal1 : b*c*d = a*q) (hbal2 : d*ee = a^2*q^(3*n+1)) (hb : b = a)
 (h_domain : ∀ k ∈ Finset.range (n+1), ((1 - a) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    ee ≠ 0 ∧
    (((pochList [((a * (q^3)) / b),((a * (q^3)) / c)] (q^3) (k)) * (pochList [((a * q) / d)] q (2*k))) * (pochList [((a * q) / ee),(a * (q^((3*(n : ℤ)+1) : ℤ)))] q (k))) ≠ 0) ∧
    ((b * c) * ee) ≠ 0 ∧
    ((b * d) * ee) ≠ 0 ∧
    (c * d) ≠ 0 ∧
    (b * ee) ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    (((b * c) * d) * ee) ≠ 0 ∧
    (pochList [(((a^2) * (q^3)) / (b * ee)),((a * (q^3)) / c),((a * (q^3)) / d),(((a^2) * (q^3)) / (((b * c) * d) * ee))] (q^3) (n)) ≠ 0) :
 (∑ k ∈ Finset.range (n+1), (((((((1 - (a * (q^((4*(k : ℤ)) : ℤ)))) / (1 - a)) * (pochList [b,c] q (k))) * (pochList [d] q (2*k))) * (pochList [ee,(q^((-3*(n : ℤ)) : ℤ))] (q^3) (k))) * (q^(((k : ℤ)) : ℤ))) / (((pochList [((a * (q^3)) / b),((a * (q^3)) / c)] (q^3) (k)) * (pochList [((a * q) / d)] q (2*k))) * (pochList [((a * q) / ee),(a * (q^((3*(n : ℤ)+1) : ℤ)))] q (k))))) = ((pochList [(a * (q^3)),(((a^2) * (q^3)) / ((b * c) * ee)),(((a^2) * (q^3)) / ((b * d) * ee)),((a * (q^3)) / (c * d))] (q^3) (n)) / (pochList [(((a^2) * (q^3)) / (b * ee)),((a * (q^3)) / c),((a * (q^3)) / d),(((a^2) * (q^3)) / (((b * c) * d) * ee))] (q^3) (n))) := by
  sorry

end FiniteQBenchmark.Identity213
