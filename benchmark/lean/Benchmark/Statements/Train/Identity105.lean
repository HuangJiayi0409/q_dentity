import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.10.15 — 有限双底数到 10φ9 的变换（一）
Original representative source: GR2-3.10.15
Frozen statement: formulas/train/FQI-SRC-GR2-3.10.15.md
Source formula:
\Phi_n[a^2,-aq^2,b^2,c^2,d^2;-a,a^2q^2/b^2,a^2q^2/c^2,a^2q^2/d^2\mid-\lambda q^{n+1}/a,q^{-n};a^2q^{-n}/\lambda,-aq^{n+1};q^2,q;q]=\frac{(-aq,\lambda q/a;q)_n(\lambda q^2/a^2;q^2)_n}{(-q,\lambda q/a^2;q)_n(\lambda q^2;q^2)_n}W_{10}^{[n]}(\lambda;a,aq,\lambda b^2/a^2,\lambda c^2/a^2,\lambda d^2/a^2,\lambda^2q^{2n+2}/a^2,q^{-2n};q^2,qa^2/\lambda),\quad\lambda=(qa^2/(bcd))^2.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity105
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d lam q : K) (n : ℕ)
 (hbase : regular q) (hp : ∀ x ∈ [a,b,c,d,lam], x ≠ 0) (hlam : lam = a^4*q^2/(b^2*c^2*d^2))
 (h_domain : (b * b) ≠ 0 ∧
    (c * c) ≠ 0 ∧
    (d * d) ≠ 0 ∧
    a ≠ 0 ∧
    lam ≠ 0 ∧
    phiDefined [(-a),((((a * a) * q) * q) / (b * b)),((((a * a) * q) * q) / (c * c)),((((a * a) * q) * q) / (d * d))] (q^2) (n) ∧
    ∀ k ≤ (n), pochList [(((a * a) * (q^((-(n : ℤ)) : ℤ))) / lam),((-a) * (q^(((n : ℤ)+1) : ℤ)))] q k ≠ 0 ∧
    (a * a) ≠ 0 ∧
    ((pochList [(-q),((lam * q) / (a * a))] q (n)) * (pochList [((lam * q) * q)] (q * q) (n))) ≠ 0 ∧
    wDefined lam [a,(a * q),(((lam * b) * b) / (a * a)),(((lam * c) * c) / (a * a)),(((lam * d) * d) / (a * a)),(((lam * lam) * (q^((2*(n : ℤ)+2) : ℤ))) / (a * a)),(q^((-2*(n : ℤ)) : ℤ))] (q * q) (n)) :
 (bibasicPhi [(a * a),(((-a) * q) * q),(b * b),(c * c),(d * d)] [(-a),((((a * a) * q) * q) / (b * b)),((((a * a) * q) * q) / (c * c)),((((a * a) * q) * q) / (d * d))] [(((-lam) * (q^(((n : ℤ)+1) : ℤ))) / a),(q^((-(n : ℤ)) : ℤ))] [(((a * a) * (q^((-(n : ℤ)) : ℤ))) / lam),((-a) * (q^(((n : ℤ)+1) : ℤ)))] (q^2) q q (n)) = ((((pochList [((-a) * q),((lam * q) / a)] q (n)) * (pochList [(((lam * q) * q) / (a * a))] (q * q) (n))) / ((pochList [(-q),((lam * q) / (a * a))] q (n)) * (pochList [((lam * q) * q)] (q * q) (n)))) * (wellPoisedRaw lam [a,(a * q),(((lam * b) * b) / (a * a)),(((lam * c) * c) / (a * a)),(((lam * d) * d) / (a * a)),(((lam * lam) * (q^((2*(n : ℤ)+2) : ℤ))) / (a * a)),(q^((-2*(n : ℤ)) : ℤ))] (q * q) (((a * a) * (q^((1) : ℤ))) / lam) (n))) := by
  sorry

end FiniteQBenchmark.Identity105
