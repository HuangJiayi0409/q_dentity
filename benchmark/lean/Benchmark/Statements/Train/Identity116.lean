import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.Ex31i — 有限三次变换（一）
Original representative source: GR2-3.Ex31i
Frozen statement: formulas/train/FQI-SRC-GR2-3.Ex31i.md
Source formula:
\sum_{k=0}^n\frac{1-acq^{4k}}{1-ac}\frac{(a,b;q)_k(cq/b;q)_{2k}(a^2bcq^{3n},q^{-3n};q^3)_kq^k}{(cq^3,acq^3/b;q^3)_k(ab;q)_{2k}(q^{1-3n}/(ab),acq^{3n+1};q)_k}=\frac{(1-acq^2)(1-ab/q^2)(1-abq^{3n})(1-acq^{3n})}{(1-acq^{3n+2})(1-abq^{3n-2})(1-ab)(1-ac)}\sum_{k=0}^n\frac{1-acq^{6k+2}}{1-acq^2}\frac{(aq^2,bq^2,cq^2/b,cq^3/b,a^2bcq^{3n},q^{-3n};q^3)_kq^{3k}}{(cq^3,acq^3/b,abq^3,abq^2,q^{5-3n}/(ab),acq^{3n+5};q^3)_k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity116
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c q : K) (n : ℕ)
 (hbase : regular q) (ha : a ≠ 0) (hb : b ≠ 0)
 (h_domain : ∀ k ∈ Finset.range (n+1), ((1 - (a * c)) ≠ 0 ∧
    b ≠ 0 ∧
    (a * b) ≠ 0 ∧
    (((pochList [(c * (q^3)),(((a * c) * (q^3)) / b)] (q^3) (k)) * (pochList [(a * b)] q (2*k))) * (pochList [((q^((1-3*(n : ℤ)) : ℤ)) / (a * b)),((a * c) * (q^((3*(n : ℤ)+1) : ℤ)))] q (k))) ≠ 0) ∧
    (q * q) ≠ 0 ∧
    ((((1 - ((a * c) * (q^((3*(n : ℤ)+2) : ℤ)))) * (1 - ((a * b) * (q^((3*(n : ℤ)-2) : ℤ))))) * (1 - (a * b))) * (1 - (a * c))) ≠ 0 ∧
    ∀ k ∈ Finset.range (n+1), ((1 - (((a * c) * q) * q)) ≠ 0 ∧
    b ≠ 0 ∧
    (a * b) ≠ 0 ∧
    (pochList [(c * (q^3)),(((a * c) * (q^3)) / b),((a * b) * (q^3)),(((a * b) * q) * q),((q^((5-3*(n : ℤ)) : ℤ)) / (a * b)),((a * c) * (q^((3*(n : ℤ)+5) : ℤ)))] (q^3) (k)) ≠ 0)) :
 (∑ k ∈ Finset.range (n+1), (((((((1 - ((a * c) * (q^((4*(k : ℤ)) : ℤ)))) / (1 - (a * c))) * (pochList [a,b] q (k))) * (pochList [((c * q) / b)] q (2*k))) * (pochList [((((a * a) * b) * c) * (q^((3*(n : ℤ)) : ℤ))),(q^((-3*(n : ℤ)) : ℤ))] (q^3) (k))) * (q^(((k : ℤ)) : ℤ))) / (((pochList [(c * (q^3)),(((a * c) * (q^3)) / b)] (q^3) (k)) * (pochList [(a * b)] q (2*k))) * (pochList [((q^((1-3*(n : ℤ)) : ℤ)) / (a * b)),((a * c) * (q^((3*(n : ℤ)+1) : ℤ)))] q (k))))) = ((((((1 - (((a * c) * q) * q)) * (1 - ((a * b) / (q * q)))) * (1 - ((a * b) * (q^((3*(n : ℤ)) : ℤ))))) * (1 - ((a * c) * (q^((3*(n : ℤ)) : ℤ))))) / ((((1 - ((a * c) * (q^((3*(n : ℤ)+2) : ℤ)))) * (1 - ((a * b) * (q^((3*(n : ℤ)-2) : ℤ))))) * (1 - (a * b))) * (1 - (a * c)))) * (∑ k ∈ Finset.range (n+1), (((((1 - ((a * c) * (q^((6*(k : ℤ)+2) : ℤ)))) / (1 - (((a * c) * q) * q))) * (pochList [((a * q) * q),((b * q) * q),(((c * q) * q) / b),((c * (q^3)) / b),((((a * a) * b) * c) * (q^((3*(n : ℤ)) : ℤ))),(q^((-3*(n : ℤ)) : ℤ))] (q^3) (k))) * (q^((3*(k : ℤ)) : ℤ))) / (pochList [(c * (q^3)),(((a * c) * (q^3)) / b),((a * b) * (q^3)),(((a * b) * q) * q),((q^((5-3*(n : ℤ)) : ℤ)) / (a * b)),((a * c) * (q^((3*(n : ℤ)+5) : ℤ)))] (q^3) (k))))) := by
  sorry

end FiniteQBenchmark.Identity116
