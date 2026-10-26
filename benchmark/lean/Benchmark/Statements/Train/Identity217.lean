import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-11.Ex39-p0 — D 型 Jackson 的有限单纯形变式（已注明修订）
Original representative source: GR2-11.Ex39-p0
Frozen statement: formulas/train/FQI-SRC-GR2-11.Ex39-p0.md
Source formula:
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|\le N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{s=1}^d\frac{1-az_sq^{k_s+|k|}}{1-az_s}\prod_{r<s}\frac1{(z_rz_s;q)_{k_r+k_s}}\prod_{r,s=1}^d\frac{(z_sb_r,z_s/b_r;q)_{k_s}}{(qz_s/z_r;q)_{k_s}}\prod_{r=1}^d\frac{(az_r;q)_{|k|}(aq/z_r;q)_{|k|-k_r}}{(aqb_r,aq/b_r;q)_{|k|}}\frac{(q^{-N},c,a^2q^{N+1}/c;q)_{|k|}q^{|k|}}{\prod_{s=1}^d(aqz_s/c,cz_s/(aq^N),az_sq^{N+1};q)_{k_s}}=\prod_{s=1}^d\frac{(aqz_s,aq/z_s,aqb_s/c,aq/(b_sc);q)_N}{(aqz_s/c,aq/(z_sc),aqb_s,aq/b_s;q)_N}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity217
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q a c : K) (d N : ℕ) (bs z : Fin d → K)
 (hbase : regular q) (hd : 0 < d) (hz : ∀ i, z i ≠ 0) (hzd : Function.Injective z) (ha : a ≠ 0) (hc : c ≠ 0) (hb : ∀ i, bs i ≠ 0)
 (h_domain : ∀ k ∈ (subCompositions d N), ((vandermonde z) ≠ 0 ∧
    ∀ s ∈ (Finset.univ : Finset (Fin d)), ((1 - (a * (z s))) ≠ 0) ∧
    ∀ r ∈ (Finset.univ : Finset (Fin d)), (∀ s ∈ (Finset.univ : Finset (Fin d)).filter (fun s => r < s), ((pochList [((z r) * (z s))] q ((k r).val+(k s).val)) ≠ 0)) ∧
    ∀ r ∈ (Finset.univ : Finset (Fin d)), (∀ s ∈ (Finset.univ : Finset (Fin d)), ((bs r) ≠ 0 ∧
    (z r) ≠ 0 ∧
    (pochList [((q * (z s)) / (z r))] q ((k s).val)) ≠ 0)) ∧
    ∀ r ∈ (Finset.univ : Finset (Fin d)), ((z r) ≠ 0 ∧
    (bs r) ≠ 0 ∧
    (pochList [((a * q) * (bs r)),((a * q) / (bs r))] q (∑ i, (k i).val)) ≠ 0) ∧
    c ≠ 0 ∧
    ∀ s ∈ (Finset.univ : Finset (Fin d)), (c ≠ 0 ∧
    (a * (q^(((N : ℤ)) : ℤ))) ≠ 0) ∧
    (∏ s ∈ (Finset.univ : Finset (Fin d)), (pochList [(((a * q) * (z s)) / c),((c * (z s)) / (a * (q^(((N : ℤ)) : ℤ)))),((a * (z s)) * (q^(((N : ℤ)+1) : ℤ)))] q ((k s).val))) ≠ 0) ∧
    ∀ s ∈ (Finset.univ : Finset (Fin d)), ((z s) ≠ 0 ∧
    c ≠ 0 ∧
    ((bs s) * c) ≠ 0 ∧
    ((z s) * c) ≠ 0 ∧
    (bs s) ≠ 0 ∧
    (pochList [(((a * q) * (z s)) / c),((a * q) / ((z s) * c)),((a * q) * (bs s)),((a * q) / (bs s))] q (N)) ≠ 0)) :
 (∑ k ∈ (subCompositions d N), (((((((((vandermonde (fun i => z i*q^((k i).val))) / (vandermonde z)) * (∏ s ∈ (Finset.univ : Finset (Fin d)), ((1 - ((a * (z s)) * (q^((k s).val + ∑ i, (k i).val)))) / (1 - (a * (z s)))))) * (∏ r ∈ (Finset.univ : Finset (Fin d)), (∏ s ∈ (Finset.univ : Finset (Fin d)).filter (fun s => r < s), (1 / (pochList [((z r) * (z s))] q ((k r).val+(k s).val)))))) * (∏ r ∈ (Finset.univ : Finset (Fin d)), (∏ s ∈ (Finset.univ : Finset (Fin d)), ((pochList [((z s) * (bs r)),((z s) / (bs r))] q ((k s).val)) / (pochList [((q * (z s)) / (z r))] q ((k s).val)))))) * (∏ r ∈ (Finset.univ : Finset (Fin d)), (((pochList [(a * (z r))] q (∑ i, (k i).val)) * (pochList [((a * q) / (z r))] q ((∑ i, (k i).val)-(k r).val))) / (pochList [((a * q) * (bs r)),((a * q) / (bs r))] q (∑ i, (k i).val))))) * (pochList [(q^((-(N : ℤ)) : ℤ)),c,(((a^2) * (q^(((N : ℤ)+1) : ℤ))) / c)] q (∑ i, (k i).val))) * (q^(∑ i, (k i).val))) / (∏ s ∈ (Finset.univ : Finset (Fin d)), (pochList [(((a * q) * (z s)) / c),((c * (z s)) / (a * (q^(((N : ℤ)) : ℤ)))),((a * (z s)) * (q^(((N : ℤ)+1) : ℤ)))] q ((k s).val))))) = (∏ s ∈ (Finset.univ : Finset (Fin d)), ((pochList [((a * q) * (z s)),((a * q) / (z s)),(((a * q) * (bs s)) / c),((a * q) / ((bs s) * c))] q (N)) / (pochList [(((a * q) * (z s)) / c),((a * q) / ((z s) * c)),((a * q) * (bs s)),((a * q) / (bs s))] q (N)))) := by
  sorry

end FiniteQBenchmark.Identity217
