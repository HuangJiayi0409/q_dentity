import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.Ex3 — 终止 3φ2 的二次变换
Original representative source: GR2-3.Ex3
Frozen statement: formulas/train/FQI-SRC-GR2-3.Ex3.md
Source formula:
{}_3\phi_2^{[n]}(a,q/a,q^{-n};c,-q;q,q)=\frac{(-q^{1-n}/c;q)_n}{(-q^{-n};q)_n}{}_3\phi_2^{[n]}(c/a,ac/q,q^{-2n};c^2,0;q^2,q^2).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity107
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a c q : K) (n : ℕ)
 (hbase : regular q) (ha : a ≠ 0) (hc : c ≠ 0)
 (h_domain : a ≠ 0 ∧
    phiDefined [c,(-q)] q (n) ∧
    c ≠ 0 ∧
    (pochList [(-(q^((-(n : ℤ)) : ℤ)))] q (n)) ≠ 0 ∧
    q ≠ 0 ∧
    phiDefined [(c * c),0] (q * q) (n)) :
 (phi [a,(q / a),(q^((-(n : ℤ)) : ℤ))] [c,(-q)] q q (n)) = (((pochList [((-(q^((1-(n : ℤ)) : ℤ))) / c)] q (n)) / (pochList [(-(q^((-(n : ℤ)) : ℤ)))] q (n))) * (phi [(c / a),((a * c) / q),(q^((-2*(n : ℤ)) : ℤ))] [(c * c),0] (q * q) (q * q) (n))) := by
  sorry

end FiniteQBenchmark.Identity107
