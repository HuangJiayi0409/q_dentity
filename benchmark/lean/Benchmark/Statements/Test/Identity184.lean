import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex12 — Rogers 线性化的逆公式
Original representative source: GR2-8.Ex12
Frozen statement: formulas/test/FQI-SRC-GR2-8.Ex12.md
Source formula:
C_{m+n}(z;\beta)=\sum_{k=0}^{\min(m,n)}\frac{(q;q)_m(q;q)_n(\beta;q)_{m+n}}{(\beta;q)_m(\beta;q)_n(q;q)_{m+n}}\frac{(\beta^{-2}q^{-m-n},\beta^{-1};q)_k(1-\beta^{-2}q^{2k-m-n})}{(q,\beta^{-1}q^{1-m-n};q)_k(1-\beta^{-2}q^{-m-n})}(\beta^2/q)^kC_{m-k}(z;\beta)C_{n-k}(z;\beta).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity184
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z beta q : K) (m n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [beta,z], v ≠ 0)
 (h_domain : z ≠ 0 ∧
    ∀ k ≤ (m+n), poch q q k ≠ 0 ∧
    ∀ k ∈ Finset.range (min m n+1), ((((pochList [beta] q (m)) * (pochList [beta] q (n))) * (pochList [q] q (m+n))) ≠ 0 ∧
    (beta * beta) ≠ 0 ∧
    beta ≠ 0 ∧
    ((pochList [q,((q^((1-(m : ℤ)-(n : ℤ)) : ℤ)) / beta)] q (k)) * (1 - ((q^((-(m : ℤ)-(n : ℤ)) : ℤ)) / (beta * beta)))) ≠ 0 ∧
    q ≠ 0 ∧
    z ≠ 0 ∧
    ∀ k ≤ (m-k), poch q q k ≠ 0 ∧
    ∀ k ≤ (n-k), poch q q k ≠ 0)) :
 (ultraspherical beta z q (m+n)) = (∑ k ∈ Finset.range (min m n+1), ((((((((((pochList [q] q (m)) * (pochList [q] q (n))) * (pochList [beta] q (m+n))) / (((pochList [beta] q (m)) * (pochList [beta] q (n))) * (pochList [q] q (m+n)))) * (pochList [((q^((-(m : ℤ)-(n : ℤ)) : ℤ)) / (beta * beta)),(1 / beta)] q (k))) * (1 - ((q^((2*(k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ)) / (beta * beta)))) / ((pochList [q,((q^((1-(m : ℤ)-(n : ℤ)) : ℤ)) / beta)] q (k)) * (1 - ((q^((-(m : ℤ)-(n : ℤ)) : ℤ)) / (beta * beta))))) * (((beta * beta) / q)^(((k : ℤ)) : ℤ))) * (ultraspherical beta z q (m-k))) * (ultraspherical beta z q (n-k)))) := by
  sorry

end FiniteQBenchmark.Identity184
