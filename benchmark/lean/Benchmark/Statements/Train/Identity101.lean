import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.10.7 — 有限双底数求和（三）
Original representative source: GR2-3.10.7
Frozen statement: formulas/train/FQI-SRC-GR2-3.10.7.md
Source formula:
\Phi_n[a^2,aq^2,-aq^2,b^2;a,-a,a^2q^2/b^2\mid-aq^n/b^2,q^{-n};b^2q^{1-n},-aq^{n+1};q^2,q;q]=\frac{(-aq,a/b^2;q)_nq^n(1/b^2;q^2)_n}{(-q,1/b^2;q)_n(a^2q^2/b^2;q^2)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity101
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (n : ℕ)
 (hbase : regular q) (ha : a ≠ 0) (hb : b ≠ 0)
 (h_domain : (b * b) ≠ 0 ∧
    phiDefined [a,(-a),((((a * a) * q) * q) / (b * b))] (q^2) (n) ∧
    ∀ k ≤ (n), pochList [((b * b) * (q^((1-(n : ℤ)) : ℤ))),((-a) * (q^(((n : ℤ)+1) : ℤ)))] q k ≠ 0 ∧
    ((pochList [(-q),(1 / (b * b))] q (n)) * (pochList [((((a * a) * q) * q) / (b * b))] (q * q) (n))) ≠ 0) :
 (bibasicPhi [(a * a),((a * q) * q),(((-a) * q) * q),(b * b)] [a,(-a),((((a * a) * q) * q) / (b * b))] [(((-a) * (q^(((n : ℤ)) : ℤ))) / (b * b)),(q^((-(n : ℤ)) : ℤ))] [((b * b) * (q^((1-(n : ℤ)) : ℤ))),((-a) * (q^(((n : ℤ)+1) : ℤ)))] (q^2) q q (n)) = ((((pochList [((-a) * q),(a / (b * b))] q (n)) * (q^(((n : ℤ)) : ℤ))) * (pochList [(1 / (b * b))] (q * q) (n))) / ((pochList [(-q),(1 / (b * b))] q (n)) * (pochList [((((a * a) * q) * q) / (b * b))] (q * q) (n)))) := by
  sorry

end FiniteQBenchmark.Identity101
