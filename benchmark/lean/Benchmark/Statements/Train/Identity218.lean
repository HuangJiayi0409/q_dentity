import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-11.Ex40-p0 — 多变量终止 Bailey 变换
Original representative source: GR2-11.Ex40-p0
Frozen statement: formulas/train/FQI-SRC-GR2-11.Ex40-p0.md
Source formula:
\mathcal S(a;b,c,d;e,f,g)=\left(\frac a\lambda\right)^{|m|}\frac{(\lambda q/f,\lambda q/g;q)_{|m|}}{(aq/f,aq/g;q)_{|m|}}\prod_{s=1}^{\ell}\frac{(aqz_s,\lambda qz_s/d;q)_{m_s}}{(\lambda qz_s,aqz_s/d;q)_{m_s}}\mathcal S(\lambda;\lambda b/a,\lambda c/a,d;\lambda e/a,f,g),\quad\lambda=a^2q/(bce),\quad a^3q^{2+|m|}=bcdefg,\quad\mathcal S(A;B,C,D;E,F,G)=\sum_{0\le k_s\le m_s}\frac{\Delta(zq^k)}{\Delta(z)}q^{|k|}\prod_{s=1}^{\ell}\frac{1-Az_sq^{k_s+|k|}}{1-Az_s}\frac{(B,C,D;q)_{|k|}}{(Aq/E,Aq/F,Aq/G;q)_{|k|}}\prod_{r=1}^{\ell}\frac{(Az_r;q)_{|k|}}{(Az_rq^{m_r+1};q)_{|k|}}\prod_{s=1}^{\ell}\frac{(Ez_s,Fz_s,Gz_s;q)_{k_s}}{(Aqz_s/B,Aqz_s/C,Aqz_s/D;q)_{k_s}}\prod_{r,s=1}^{\ell}\frac{(q^{-m_r}z_s/z_r;q)_{k_s}}{(qz_s/z_r;q)_{k_s}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity218
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q a b c d ee f g lam : K) (ell : ℕ) (m : Fin ell → ℕ) (z : Fin ell → K)
 (hbase : regular q) (hell : 0 < ell) (hzd : Function.Injective z) (hl : lam = a^2*q/(b*c*ee)) (hbal : a^3*q^(2+∑ i, m i) = b*c*d*ee*f*g)
 (h_domain : ∀ k ∈ (Finset.univ : Finset ((i : Fin ell) → Fin (m i+1))), ((vandermonde z) ≠ 0 ∧
    ∀ s ∈ (Finset.univ : Finset (Fin ell)), ((1 - (a * (z s))) ≠ 0) ∧
    ee ≠ 0 ∧
    f ≠ 0 ∧
    g ≠ 0 ∧
    (pochList [((a * q) / ee),((a * q) / f),((a * q) / g)] q (∑ i, (k i).val)) ≠ 0 ∧
    ∀ r ∈ (Finset.univ : Finset (Fin ell)), ((pochList [((a * (z r)) * (q^(m r+1)))] q (∑ i, (k i).val)) ≠ 0) ∧
    ∀ s ∈ (Finset.univ : Finset (Fin ell)), (b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    (pochList [(((a * q) * (z s)) / b),(((a * q) * (z s)) / c),(((a * q) * (z s)) / d)] q ((k s).val)) ≠ 0) ∧
    ∀ r ∈ (Finset.univ : Finset (Fin ell)), (∀ s ∈ (Finset.univ : Finset (Fin ell)), ((z r) ≠ 0 ∧
    (pochList [((q * (z s)) / (z r))] q ((k s).val)) ≠ 0))) ∧
    lam ≠ 0 ∧
    f ≠ 0 ∧
    g ≠ 0 ∧
    (pochList [((a * q) / f),((a * q) / g)] q (∑ i, m i)) ≠ 0 ∧
    ∀ s ∈ (Finset.univ : Finset (Fin ell)), (d ≠ 0 ∧
    (pochList [((lam * q) * (z s)),(((a * q) * (z s)) / d)] q (m s)) ≠ 0) ∧
    ∀ k ∈ (Finset.univ : Finset ((i : Fin ell) → Fin (m i+1))), ((vandermonde z) ≠ 0 ∧
    ∀ s ∈ (Finset.univ : Finset (Fin ell)), ((1 - (lam * (z s))) ≠ 0) ∧
    a ≠ 0 ∧
    ((lam * ee) / a) ≠ 0 ∧
    f ≠ 0 ∧
    g ≠ 0 ∧
    (pochList [((lam * q) / ((lam * ee) / a)),((lam * q) / f),((lam * q) / g)] q (∑ i, (k i).val)) ≠ 0 ∧
    ∀ r ∈ (Finset.univ : Finset (Fin ell)), ((pochList [((lam * (z r)) * (q^(m r+1)))] q (∑ i, (k i).val)) ≠ 0) ∧
    ∀ s ∈ (Finset.univ : Finset (Fin ell)), (a ≠ 0 ∧
    ((lam * b) / a) ≠ 0 ∧
    ((lam * c) / a) ≠ 0 ∧
    d ≠ 0 ∧
    (pochList [(((lam * q) * (z s)) / ((lam * b) / a)),(((lam * q) * (z s)) / ((lam * c) / a)),(((lam * q) * (z s)) / d)] q ((k s).val)) ≠ 0) ∧
    ∀ r ∈ (Finset.univ : Finset (Fin ell)), (∀ s ∈ (Finset.univ : Finset (Fin ell)), ((z r) ≠ 0 ∧
    (pochList [((q * (z s)) / (z r))] q ((k s).val)) ≠ 0)))) :
 (∑ k ∈ (Finset.univ : Finset ((i : Fin ell) → Fin (m i+1))), (((((((((vandermonde (fun i => z i*q^((k i).val))) / (vandermonde z)) * (q^(∑ i, (k i).val))) * (∏ s ∈ (Finset.univ : Finset (Fin ell)), ((1 - ((a * (z s)) * (q^((k s).val + ∑ i, (k i).val)))) / (1 - (a * (z s)))))) * (pochList [b,c,d] q (∑ i, (k i).val))) / (pochList [((a * q) / ee),((a * q) / f),((a * q) / g)] q (∑ i, (k i).val))) * (∏ r ∈ (Finset.univ : Finset (Fin ell)), ((pochList [(a * (z r))] q (∑ i, (k i).val)) / (pochList [((a * (z r)) * (q^(m r+1)))] q (∑ i, (k i).val))))) * (∏ s ∈ (Finset.univ : Finset (Fin ell)), ((pochList [(ee * (z s)),(f * (z s)),(g * (z s))] q ((k s).val)) / (pochList [(((a * q) * (z s)) / b),(((a * q) * (z s)) / c),(((a * q) * (z s)) / d)] q ((k s).val))))) * (∏ r ∈ (Finset.univ : Finset (Fin ell)), (∏ s ∈ (Finset.univ : Finset (Fin ell)), ((pochList [(((q^(-(m r:ℤ))) * (z s)) / (z r))] q ((k s).val)) / (pochList [((q * (z s)) / (z r))] q ((k s).val))))))) = ((((((a / lam)^(∑ i, m i)) * (pochList [((lam * q) / f),((lam * q) / g)] q (∑ i, m i))) / (pochList [((a * q) / f),((a * q) / g)] q (∑ i, m i))) * (∏ s ∈ (Finset.univ : Finset (Fin ell)), ((pochList [((a * q) * (z s)),(((lam * q) * (z s)) / d)] q (m s)) / (pochList [((lam * q) * (z s)),(((a * q) * (z s)) / d)] q (m s))))) * (∑ k ∈ (Finset.univ : Finset ((i : Fin ell) → Fin (m i+1))), (((((((((vandermonde (fun i => z i*q^((k i).val))) / (vandermonde z)) * (q^(∑ i, (k i).val))) * (∏ s ∈ (Finset.univ : Finset (Fin ell)), ((1 - ((lam * (z s)) * (q^((k s).val + ∑ i, (k i).val)))) / (1 - (lam * (z s)))))) * (pochList [((lam * b) / a),((lam * c) / a),d] q (∑ i, (k i).val))) / (pochList [((lam * q) / ((lam * ee) / a)),((lam * q) / f),((lam * q) / g)] q (∑ i, (k i).val))) * (∏ r ∈ (Finset.univ : Finset (Fin ell)), ((pochList [(lam * (z r))] q (∑ i, (k i).val)) / (pochList [((lam * (z r)) * (q^(m r+1)))] q (∑ i, (k i).val))))) * (∏ s ∈ (Finset.univ : Finset (Fin ell)), ((pochList [(((lam * ee) / a) * (z s)),(f * (z s)),(g * (z s))] q ((k s).val)) / (pochList [(((lam * q) * (z s)) / ((lam * b) / a)),(((lam * q) * (z s)) / ((lam * c) / a)),(((lam * q) * (z s)) / d)] q ((k s).val))))) * (∏ r ∈ (Finset.univ : Finset (Fin ell)), (∏ s ∈ (Finset.univ : Finset (Fin ell)), ((pochList [(((q^(-(m r:ℤ))) * (z s)) / (z r))] q ((k s).val)) / (pochList [((q * (z s)) / (z r))] q ((k s).val)))))))) := by
  sorry

end FiniteQBenchmark.Identity218
