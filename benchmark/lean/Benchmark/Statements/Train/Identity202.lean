import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-9.Ex7 — 相伴连续 q-超球的有限卷积
Original representative source: GR2-9.Ex7
Frozen statement: formulas/train/FQI-SRC-GR2-9.Ex7.md
Source formula:
C_n^\alpha(z;\beta)=\sum_{k=0}^n\frac{1-\alpha}{1-\alpha q^k}\beta^kC_k(z;q/\beta)C_{n-k}(z;\beta).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity202
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (alpha beta z q : K) (n : ℕ)
 (hbase : regular q) (hnz : alpha*beta*z ≠ 0) (hrec : ∀ j < n, 1-alpha*q^(j+1) ≠ 0 ∧ 1-alpha*beta*q^j ≠ 0)
 (h_domain : ∀ k ∈ Finset.range (n+1), ((1 - (alpha * (q^(((k : ℤ)) : ℤ)))) ≠ 0 ∧
    beta ≠ 0 ∧
    z ≠ 0 ∧
    ∀ k ≤ (k), poch q q k ≠ 0 ∧
    ∀ k ≤ (n-k), poch q q k ≠ 0)) :
 (associatedUltra z alpha beta q n) = (∑ k ∈ Finset.range (n+1), (((((1 - alpha) / (1 - (alpha * (q^(((k : ℤ)) : ℤ))))) * (beta^k)) * (ultraspherical (q / beta) z q (k))) * (ultraspherical beta z q (n-k)))) := by
  sorry

end FiniteQBenchmark.Identity202
