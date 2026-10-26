import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.5.35 — 连续 q-超球偶数次数的二次变换
Original representative source: GR2-7.5.35
Frozen statement: formulas/train/FQI-SRC-GR2-7.5.35.md
Source formula:
C_{2n}(z;\beta)=\frac{(\beta,\beta s;q)_n}{(q,s;q)_n}s^{-n}{}_4\phi_3^{[n]}(q^{-n},\beta q^n,sz^2,s/z^2;\beta s,-s,-q;q,q),\quad s^2=q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity136
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z beta s q : K) (n : ℕ)
 (hbase : regular q) (hs : s^2 = q) (hnz : ∀ v ∈ [beta,z], v ≠ 0)
 (h_domain : z ≠ 0 ∧
    ∀ k ≤ (2*n), poch q q k ≠ 0 ∧
    (pochList [q,s] q (n)) ≠ 0 ∧
    (z * z) ≠ 0 ∧
    phiDefined [(beta * s),(-s),(-q)] q (n)) :
 (ultraspherical beta z q (2*n)) = ((((pochList [beta,(beta * s)] q (n)) / (pochList [q,s] q (n))) * (s^((-(n : ℤ)) : ℤ))) * (phi [(q^((-(n : ℤ)) : ℤ)),(beta * (q^(((n : ℤ)) : ℤ))),((s * z) * z),(s / (z * z))] [(beta * s),(-s),(-q)] q q (n))) := by
  sorry

end FiniteQBenchmark.Identity136
