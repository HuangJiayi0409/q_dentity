import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-25 — 近良配 5φ4 到 12φ11 变换
Original representative source: GR2-III-25
Frozen statement: formulas/train/FQI-SRC-GR2-III-25.md
Source formula:
{}_5\phi_4^{[n]}\!\left[\begin{matrix}a,b,c,d,q^{-n}\\aq/b,aq/c,aq/d,a^2q^{-n}/\lambda^2\end{matrix};q,q\right]=\frac{(\lambda q/a,\lambda^2q/a;q)_n}{(\lambda q,\lambda^2q/a^2;q)_n}\mathcal V_n(\lambda;b\lambda/a,c\lambda/a,d\lambda/a;a,aq;\lambda^2q^{n+1}/a,q^{-n}),\quad\lambda=qa^2/(bcd).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity266
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d lam q : K) (n : ℕ)
 (hbase : regular q) (hl : lam = q*a^2/(b*c*d)) (hnz : a*b*c*d*lam ≠ 0) (hl1 : lam ≠ 1)
 (h_domain : b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    (lam^2) ≠ 0 ∧
    phiDefined [((a * q) / b),((a * q) / c),((a * q) / d),(((a^2) * (q^((-(n : ℤ)) : ℤ))) / (lam^2))] q (n) ∧
    a ≠ 0 ∧
    (a^2) ≠ 0 ∧
    (pochList [(lam * q),(((lam^2) * q) / (a^2))] q (n)) ≠ 0 ∧
    ∀ k ∈ Finset.range (n+1), ((1 - lam) ≠ 0 ∧
    a ≠ 0 ∧
    ((b * lam) / a) ≠ 0 ∧
    ((c * lam) / a) ≠ 0 ∧
    ((d * lam) / a) ≠ 0 ∧
    (((lam^2) * (q^(((n : ℤ)+1) : ℤ))) / a) ≠ 0 ∧
    (q^((-(n : ℤ)) : ℤ)) ≠ 0 ∧
    (pochList [q,((lam * q) / ((b * lam) / a)),((lam * q) / ((c * lam) / a)),((lam * q) / ((d * lam) / a)),((lam * q) / (((lam^2) * (q^(((n : ℤ)+1) : ℤ))) / a)),((lam * q) / (q^((-(n : ℤ)) : ℤ)))] q (k)) ≠ 0 ∧
    (a * q) ≠ 0 ∧
    (pochList [(((lam^2) * (q^2)) / a),(((lam^2) * (q^2)) / (a * q))] (q^2) (k)) ≠ 0)) :
 (phi [a,b,c,d,(q^((-(n : ℤ)) : ℤ))] [((a * q) / b),((a * q) / c),((a * q) / d),(((a^2) * (q^((-(n : ℤ)) : ℤ))) / (lam^2))] q q (n)) = (((pochList [((lam * q) / a),(((lam^2) * q) / a)] q (n)) / (pochList [(lam * q),(((lam^2) * q) / (a^2))] q (n))) * (∑ k ∈ Finset.range (n+1), (((((((1 - (lam * (q^((2*(k : ℤ)) : ℤ)))) / (1 - lam)) * (pochList [lam,((b * lam) / a),((c * lam) / a),((d * lam) / a),(((lam^2) * (q^(((n : ℤ)+1) : ℤ))) / a),(q^((-(n : ℤ)) : ℤ))] q (k))) / (pochList [q,((lam * q) / ((b * lam) / a)),((lam * q) / ((c * lam) / a)),((lam * q) / ((d * lam) / a)),((lam * q) / (((lam^2) * (q^(((n : ℤ)+1) : ℤ))) / a)),((lam * q) / (q^((-(n : ℤ)) : ℤ)))] q (k))) * (pochList [a,(a * q)] (q^2) (k))) / (pochList [(((lam^2) * (q^2)) / a),(((lam^2) * (q^2)) / (a * q))] (q^2) (k))) * (q^(((k : ℤ)) : ℤ))))) := by
  sorry

end FiniteQBenchmark.Identity266
