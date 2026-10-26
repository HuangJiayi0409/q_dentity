import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.5.36 — 连续 q-超球奇数次数的二次变换
Original representative source: GR2-7.5.36
Frozen statement: formulas/train/FQI-SRC-GR2-7.5.36.md
Source formula:
C_{2n+1}(z;\beta)=\frac{z+z^{-1}}2\frac{(\beta,-1;q)_{n+1}}{(s,-s;q)_{n+1}}s^{-n}\frac{(\beta s,-qs;q)_n}{(q,-q;q)_n}{}_4\phi_3^{[n]}(q^{-n},\beta q^{n+1},sz^2,s/z^2;\beta s,-qs,-q;q,q),\quad s^2=q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity137
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z beta s q : K) [CharZero K] (n : ℕ)
 (hbase : regular q) (hs : s^2 = q) (hnz : ∀ v ∈ [beta,z], v ≠ 0)
 (h_domain : z ≠ 0 ∧
    ∀ k ≤ (2*n+1), poch q q k ≠ 0 ∧
    2 ≠ 0 ∧
    (pochList [s,(-s)] q (n+1)) ≠ 0 ∧
    (pochList [q,(-q)] q (n)) ≠ 0 ∧
    (z * z) ≠ 0 ∧
    phiDefined [(beta * s),((-q) * s),(-q)] q (n)) :
 (ultraspherical beta z q (2*n+1)) = ((((((((z + (1 / z)) / 2) * (pochList [beta,-1] q (n+1))) / (pochList [s,(-s)] q (n+1))) * (s^((-(n : ℤ)) : ℤ))) * (pochList [(beta * s),((-q) * s)] q (n))) / (pochList [q,(-q)] q (n))) * (phi [(q^((-(n : ℤ)) : ℤ)),(beta * (q^(((n : ℤ)+1) : ℤ))),((s * z) * z),(s / (z * z))] [(beta * s),((-q) * s),(-q)] q q (n))) := by
  sorry

end FiniteQBenchmark.Identity137
