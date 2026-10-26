import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-11.Ex38-p0 — D 型多变量有限 Jackson 求和
Original representative source: GR2-11.Ex38-p0
Frozen statement: formulas/test/FQI-SRC-GR2-11.Ex38-p0.md
Source formula:
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|=N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{r<s}\frac1{(z_rz_s;q)_{k_r+k_s}}\prod_{s=1}^d\frac{z_s^{k_s}q^{\binom{k_s}2}\prod_{r=1}^{d-1}(z_sa_r,z_s/a_r;q)_{k_s}}{(bz_s,z_sq^{1-N}/b;q)_{k_s}\prod_{r=1}^d(qz_s/z_r;q)_{k_s}}=(-bq^{N-1})^N\frac{\prod_{s=1}^{d-1}(ba_s,b/a_s;q)_N}{(q;q)_N\prod_{s=1}^d(bz_s,b/z_s;q)_N}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity216
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q b : K) (d N : ℕ) (aa : Fin (d-1) → K) (z : Fin d → K)
 (hbase : regular q) (hd : 0 < d) (hz : ∀ i, z i ≠ 0) (hzd : Function.Injective z) (ha : ∀ i, aa i ≠ 0) (hb : b ≠ 0)
 (h_domain : ∀ k ∈ (compositions d N), ((vandermonde z) ≠ 0 ∧
    ∀ r ∈ (Finset.univ : Finset (Fin d)), (∀ s ∈ (Finset.univ : Finset (Fin d)).filter (fun s => r < s), ((pochList [((z r) * (z s))] q ((k r).val+(k s).val)) ≠ 0)) ∧
    ∀ s ∈ (Finset.univ : Finset (Fin d)), (∀ r ∈ (Finset.univ : Finset (Fin (d-1))), ((aa r) ≠ 0) ∧
    b ≠ 0 ∧
    ∀ r ∈ (Finset.univ : Finset (Fin d)), ((z r) ≠ 0) ∧
    ((pochList [(b * (z s)),(((z s) * (q^((1-(N : ℤ)) : ℤ))) / b)] q ((k s).val)) * (∏ r ∈ (Finset.univ : Finset (Fin d)), (pochList [((q * (z s)) / (z r))] q ((k s).val)))) ≠ 0)) ∧
    ∀ s ∈ (Finset.univ : Finset (Fin (d-1))), ((aa s) ≠ 0) ∧
    ∀ s ∈ (Finset.univ : Finset (Fin d)), ((z s) ≠ 0) ∧
    ((pochList [q] q (N)) * (∏ s ∈ (Finset.univ : Finset (Fin d)), (pochList [(b * (z s)),(b / (z s))] q (N)))) ≠ 0) :
 (∑ k ∈ (compositions d N), ((((vandermonde (fun i => z i*q^((k i).val))) / (vandermonde z)) * (∏ r ∈ (Finset.univ : Finset (Fin d)), (∏ s ∈ (Finset.univ : Finset (Fin d)).filter (fun s => r < s), (1 / (pochList [((z r) * (z s))] q ((k r).val+(k s).val)))))) * (∏ s ∈ (Finset.univ : Finset (Fin d)), (((((z s)^((k s).val)) * (q^((k s).val*((k s).val-1)/2))) * (∏ r ∈ (Finset.univ : Finset (Fin (d-1))), (pochList [((z s) * (aa r)),((z s) / (aa r))] q ((k s).val)))) / ((pochList [(b * (z s)),(((z s) * (q^((1-(N : ℤ)) : ℤ))) / b)] q ((k s).val)) * (∏ r ∈ (Finset.univ : Finset (Fin d)), (pochList [((q * (z s)) / (z r))] q ((k s).val)))))))) = (((((-b) * (q^(((N : ℤ)-1) : ℤ)))^N) * (∏ s ∈ (Finset.univ : Finset (Fin (d-1))), (pochList [(b * (aa s)),(b / (aa s))] q (N)))) / ((pochList [q] q (N)) * (∏ s ∈ (Finset.univ : Finset (Fin d)), (pochList [(b * (z s)),(b / (z s))] q (N))))) := by
  sorry

end FiniteQBenchmark.Identity216
