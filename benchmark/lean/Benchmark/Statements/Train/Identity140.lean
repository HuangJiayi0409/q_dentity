import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.6.14 — Rogers 连续 q-超球连接公式
Original representative source: GR2-7.6.14
Frozen statement: formulas/train/FQI-SRC-GR2-7.6.14.md
Source formula:
C_n(z;\gamma)=\sum_{k=0}^{\lfloor n/2\rfloor}\frac{\beta^k(\gamma/\beta;q)_k(\gamma;q)_{n-k}(1-\beta q^{n-2k})}{(q;q)_k(\beta q;q)_{n-k}(1-\beta)}C_{n-2k}(z;\beta).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity140
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z beta gamma q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [beta,z], v ≠ 0)
 (h_domain : z ≠ 0 ∧
    ∀ k ≤ (n), poch q q k ≠ 0 ∧
    ∀ k ∈ Finset.range (n/2+1), (beta ≠ 0 ∧
    (((pochList [q] q (k)) * (pochList [(beta * q)] q (n-k))) * (1 - beta)) ≠ 0 ∧
    z ≠ 0 ∧
    ∀ k ≤ (n-2*k), poch q q k ≠ 0)) :
 (ultraspherical gamma z q (n)) = (∑ k ∈ Finset.range (n/2+1), ((((((beta^(((k : ℤ)) : ℤ)) * (pochList [(gamma / beta)] q (k))) * (pochList [gamma] q (n-k))) * (1 - (beta * (q^(((n : ℤ)-2*(k : ℤ)) : ℤ))))) / (((pochList [q] q (k)) * (pochList [(beta * q)] q (n-k))) * (1 - beta))) * (ultraspherical beta z q (n-2*k)))) := by
  sorry

end FiniteQBenchmark.Identity140
