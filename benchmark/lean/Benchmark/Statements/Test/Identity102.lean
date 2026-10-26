import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.10.8 — 有限双底数求和（四）
Original representative source: GR2-3.10.8
Frozen statement: formulas/test/FQI-SRC-GR2-3.10.8.md
Source formula:
\Phi_n[a^2,aq^2,-aq^2,b^2;a,-a,a^2q^2/b^2\mid-aq^{n-1}/b^2,q^{-n};b^2q^{2-n},-aq^{n+1};q^2,q;q^2]=\frac{(-aq,a/(qb^2);q)_n(aq/b^2,1/(b^2q^2);q^2)_nq^n}{(-q,1/(qb^2);q)_n(a/(qb^2),a^2q^2/b^2;q^2)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity102
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (n : ℕ)
 (hbase : regular q) (ha : a ≠ 0) (hb : b ≠ 0)
 (h_domain : (b * b) ≠ 0 ∧
    phiDefined [a,(-a),((((a * a) * q) * q) / (b * b))] (q^2) (n) ∧
    ∀ k ≤ (n), pochList [((b * b) * (q^((2-(n : ℤ)) : ℤ))),((-a) * (q^(((n : ℤ)+1) : ℤ)))] q k ≠ 0 ∧
    ((q * b) * b) ≠ 0 ∧
    (((b * b) * q) * q) ≠ 0 ∧
    ((pochList [(-q),(1 / ((q * b) * b))] q (n)) * (pochList [(a / ((q * b) * b)),((((a * a) * q) * q) / (b * b))] (q * q) (n))) ≠ 0) :
 (bibasicPhi [(a * a),((a * q) * q),(((-a) * q) * q),(b * b)] [a,(-a),((((a * a) * q) * q) / (b * b))] [(((-a) * (q^(((n : ℤ)-1) : ℤ))) / (b * b)),(q^((-(n : ℤ)) : ℤ))] [((b * b) * (q^((2-(n : ℤ)) : ℤ))),((-a) * (q^(((n : ℤ)+1) : ℤ)))] (q^2) q (q * q) (n)) = ((((pochList [((-a) * q),(a / ((q * b) * b))] q (n)) * (pochList [((a * q) / (b * b)),(1 / (((b * b) * q) * q))] (q * q) (n))) * (q^(((n : ℤ)) : ℤ))) / ((pochList [(-q),(1 / ((q * b) * b))] q (n)) * (pochList [(a / ((q * b) * b)),((((a * a) * q) * q) / (b * b))] (q * q) (n)))) := by
  sorry

end FiniteQBenchmark.Identity102
