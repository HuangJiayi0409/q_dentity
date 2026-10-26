import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-27 — 近良配 7φ6 到 12φ11 变换
Original representative source: GR2-III-27
Frozen statement: formulas/train/FQI-SRC-GR2-III-27.md
Source formula:
\sum_{k=0}^n\frac{1-aq^{2k}}{1-a}\frac{(a,b,c,d,q^{-n};q)_k}{(q,aq/b,aq/c,aq/d,a^2q^{2-n}/\lambda^2;q)_k}q^k=\frac{(\lambda/(aq),\lambda^2/(aq);q)_n}{(\lambda q,\lambda^2/(a^2q);q)_n}\frac{1-\lambda^2q^{2n-1}/a}{1-\lambda^2/(aq)}\mathcal V_n(\lambda;b\lambda/a,c\lambda/a,d\lambda/a;aq,aq^2;\lambda^2q^{n-1}/a,q^{-n}),\quad\lambda=qa^2/(bcd).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity268
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d lam q : K) (n : ℕ)
 (hbase : regular q) (hl : lam = q*a^2/(b*c*d)) (hnz : a*b*c*d*lam ≠ 0) (ha1 : a ≠ 1) (hl1 : lam ≠ 1)
 (h_domain : ∀ k ∈ Finset.range (n+1), ((1 - a) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    (lam^2) ≠ 0 ∧
    (pochList [q,((a * q) / b),((a * q) / c),((a * q) / d),(((a^2) * (q^((2-(n : ℤ)) : ℤ))) / (lam^2))] q (k)) ≠ 0) ∧
    (a * q) ≠ 0 ∧
    ((a^2) * q) ≠ 0 ∧
    (pochList [(lam * q),((lam^2) / ((a^2) * q))] q (n)) ≠ 0 ∧
    a ≠ 0 ∧
    (1 - ((lam^2) / (a * q))) ≠ 0 ∧
    ∀ k ∈ Finset.range (n+1), ((1 - lam) ≠ 0 ∧
    a ≠ 0 ∧
    ((b * lam) / a) ≠ 0 ∧
    ((c * lam) / a) ≠ 0 ∧
    ((d * lam) / a) ≠ 0 ∧
    (((lam^2) * (q^(((n : ℤ)-1) : ℤ))) / a) ≠ 0 ∧
    (q^((-(n : ℤ)) : ℤ)) ≠ 0 ∧
    (pochList [q,((lam * q) / ((b * lam) / a)),((lam * q) / ((c * lam) / a)),((lam * q) / ((d * lam) / a)),((lam * q) / (((lam^2) * (q^(((n : ℤ)-1) : ℤ))) / a)),((lam * q) / (q^((-(n : ℤ)) : ℤ)))] q (k)) ≠ 0 ∧
    (a * q) ≠ 0 ∧
    (a * (q^2)) ≠ 0 ∧
    (pochList [(((lam^2) * (q^2)) / (a * q)),(((lam^2) * (q^2)) / (a * (q^2)))] (q^2) (k)) ≠ 0)) :
 (∑ k ∈ Finset.range (n+1), (((((1 - (a * (q^((2*(k : ℤ)) : ℤ)))) / (1 - a)) * (pochList [a,b,c,d,(q^((-(n : ℤ)) : ℤ))] q (k))) / (pochList [q,((a * q) / b),((a * q) / c),((a * q) / d),(((a^2) * (q^((2-(n : ℤ)) : ℤ))) / (lam^2))] q (k))) * (q^(((k : ℤ)) : ℤ)))) = (((((pochList [(lam / (a * q)),((lam^2) / (a * q))] q (n)) / (pochList [(lam * q),((lam^2) / ((a^2) * q))] q (n))) * (1 - (((lam^2) * (q^((2*(n : ℤ)-1) : ℤ))) / a))) / (1 - ((lam^2) / (a * q)))) * (∑ k ∈ Finset.range (n+1), (((((((1 - (lam * (q^((2*(k : ℤ)) : ℤ)))) / (1 - lam)) * (pochList [lam,((b * lam) / a),((c * lam) / a),((d * lam) / a),(((lam^2) * (q^(((n : ℤ)-1) : ℤ))) / a),(q^((-(n : ℤ)) : ℤ))] q (k))) / (pochList [q,((lam * q) / ((b * lam) / a)),((lam * q) / ((c * lam) / a)),((lam * q) / ((d * lam) / a)),((lam * q) / (((lam^2) * (q^(((n : ℤ)-1) : ℤ))) / a)),((lam * q) / (q^((-(n : ℤ)) : ℤ)))] q (k))) * (pochList [(a * q),(a * (q^2))] (q^2) (k))) / (pochList [(((lam^2) * (q^2)) / (a * q)),(((lam^2) * (q^2)) / (a * (q^2)))] (q^2) (k))) * (q^(((k : ℤ)) : ℤ))))) := by
  sorry

end FiniteQBenchmark.Identity268
