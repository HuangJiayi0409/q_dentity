import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.5.1 — Rogers 连续 q-超球线性化公式
Original representative source: GR2-8.5.1
Frozen statement: formulas/train/FQI-SRC-GR2-8.5.1.md
Source formula:
C_m(z;\beta)C_n(z;\beta)=\sum_{k=0}^{\min(m,n)}\frac{(q;q)_{m+n-2k}(\beta;q)_{m-k}(\beta;q)_{n-k}(\beta;q)_k(\beta^2;q)_{m+n-k}(1-\beta q^{m+n-2k})}{(\beta^2;q)_{m+n-2k}(q;q)_{m-k}(q;q)_{n-k}(q;q)_k(\beta q;q)_{m+n-k}(1-\beta)}C_{m+n-2k}(z;\beta).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity165
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z beta q : K) (m n : ℕ)
 (hbase : regular q) 
 (h_domain : z ≠ 0 ∧
    ∀ k ≤ (m), poch q q k ≠ 0 ∧
    ∀ k ≤ (n), poch q q k ≠ 0 ∧
    ∀ k ∈ Finset.range (min m n+1), (((((((pochList [(beta * beta)] q (m+n-2*k)) * (pochList [q] q (m-k))) * (pochList [q] q (n-k))) * (pochList [q] q (k))) * (pochList [(beta * q)] q (m+n-k))) * (1 - beta)) ≠ 0 ∧
    z ≠ 0 ∧
    ∀ k ≤ (m+n-2*k), poch q q k ≠ 0)) :
 ((ultraspherical beta z q (m)) * (ultraspherical beta z q (n))) = (∑ k ∈ Finset.range (min m n+1), ((((((((pochList [q] q (m+n-2*k)) * (pochList [beta] q (m-k))) * (pochList [beta] q (n-k))) * (pochList [beta] q (k))) * (pochList [(beta * beta)] q (m+n-k))) * (1 - (beta * (q^(((m : ℤ)+(n : ℤ)-2*(k : ℤ)) : ℤ))))) / ((((((pochList [(beta * beta)] q (m+n-2*k)) * (pochList [q] q (m-k))) * (pochList [q] q (n-k))) * (pochList [q] q (k))) * (pochList [(beta * q)] q (m+n-k))) * (1 - beta))) * (ultraspherical beta z q (m+n-2*k)))) := by
  sorry

end FiniteQBenchmark.Identity165
