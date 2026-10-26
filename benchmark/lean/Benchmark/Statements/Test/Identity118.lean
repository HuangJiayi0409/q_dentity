import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.Ex34 — 二次底数的终止 4φ3 求和
Original representative source: GR2-3.Ex34
Frozen statement: formulas/test/FQI-SRC-GR2-3.Ex34.md
Source formula:
{}_4\phi_3^{[n]}(q^{-2n},c^2,a,qa;q^2a^2,cq^{-n},cq^{1-n};q^2,q^2)=\frac{(-q,qa/c;q)_n}{(-aq,q/c;q)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity118
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a c q : K) (n : ℕ)
 (hbase : regular q) (hc : c ≠ 0)
 (h_domain : phiDefined [(((q * q) * a) * a),(c * (q^((-(n : ℤ)) : ℤ))),(c * (q^((1-(n : ℤ)) : ℤ)))] (q * q) (n) ∧
    c ≠ 0 ∧
    (pochList [((-a) * q),(q / c)] q (n)) ≠ 0) :
 (phi [(q^((-2*(n : ℤ)) : ℤ)),(c * c),a,(q * a)] [(((q * q) * a) * a),(c * (q^((-(n : ℤ)) : ℤ))),(c * (q^((1-(n : ℤ)) : ℤ)))] (q * q) (q * q) (n)) = ((pochList [(-q),((q * a) / c)] q (n)) / (pochList [((-a) * q),(q / c)] q (n))) := by
  sorry

end FiniteQBenchmark.Identity118
