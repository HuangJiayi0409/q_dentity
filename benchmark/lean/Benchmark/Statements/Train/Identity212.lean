import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-11.Ex21-p0 — 有限二次求和的两个基本超几何分支
Original representative source: GR2-11.Ex21-p0
Frozen statement: formulas/train/FQI-SRC-GR2-11.Ex21-p0.md
Source formula:
\sum_{k=0}^n\frac{1-aq^{3k}}{1-a}\frac{(b,c,d;q)_k(e,f,q^{-2n};q^2)_kq^k}{(aq^2/b,aq^2/c,aq^2/d;q^2)_k(aq/e,aq/f,aq^{2n+1};q)_k}=\frac{(aq^2,a^2q^2/(bce),a^2q^2/(bde),aq^2/(cd);q^2)_n}{(a^2q^2/(be),aq^2/c,aq^2/d,a^2q^2/(bcde);q^2)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity212
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d ee f q : K) (n : ℕ)
 (hbase : regular q) (hnz : a*b*c*d*ee*f ≠ 0) (hbal1 : b*c*d = a*q) (hbal2 : ee*f = a^2*q^(2*n+1)) (hbranch : b = a ∨ ee = a)
 (h_domain : ∀ k ∈ Finset.range (n+1), ((1 - a) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    ee ≠ 0 ∧
    f ≠ 0 ∧
    ((pochList [((a * (q^2)) / b),((a * (q^2)) / c),((a * (q^2)) / d)] (q^2) (k)) * (pochList [((a * q) / ee),((a * q) / f),(a * (q^((2*(n : ℤ)+1) : ℤ)))] q (k))) ≠ 0) ∧
    ((b * c) * ee) ≠ 0 ∧
    ((b * d) * ee) ≠ 0 ∧
    (c * d) ≠ 0 ∧
    (b * ee) ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    (((b * c) * d) * ee) ≠ 0 ∧
    (pochList [(((a^2) * (q^2)) / (b * ee)),((a * (q^2)) / c),((a * (q^2)) / d),(((a^2) * (q^2)) / (((b * c) * d) * ee))] (q^2) (n)) ≠ 0) :
 (∑ k ∈ Finset.range (n+1), ((((((1 - (a * (q^((3*(k : ℤ)) : ℤ)))) / (1 - a)) * (pochList [b,c,d] q (k))) * (pochList [ee,f,(q^((-2*(n : ℤ)) : ℤ))] (q^2) (k))) * (q^(((k : ℤ)) : ℤ))) / ((pochList [((a * (q^2)) / b),((a * (q^2)) / c),((a * (q^2)) / d)] (q^2) (k)) * (pochList [((a * q) / ee),((a * q) / f),(a * (q^((2*(n : ℤ)+1) : ℤ)))] q (k))))) = ((pochList [(a * (q^2)),(((a^2) * (q^2)) / ((b * c) * ee)),(((a^2) * (q^2)) / ((b * d) * ee)),((a * (q^2)) / (c * d))] (q^2) (n)) / (pochList [(((a^2) * (q^2)) / (b * ee)),((a * (q^2)) / c),((a * (q^2)) / d),(((a^2) * (q^2)) / (((b * c) * d) * ee))] (q^2) (n))) := by
  sorry

end FiniteQBenchmark.Identity212
