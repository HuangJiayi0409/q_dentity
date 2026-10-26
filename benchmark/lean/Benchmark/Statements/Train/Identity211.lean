import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-11.7.8-p0 — Milne 的 A 型多变量 Jackson 求和
Original representative source: GR2-11.7.8-p0
Frozen statement: formulas/train/FQI-SRC-GR2-11.7.8-p0.md
Source formula:
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|=N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{r=1}^d\frac{\prod_{s=1}^{d+1}(a_sz_r;q)_{k_r}}{(bz_r;q)_{k_r}\prod_{s=1}^d(qz_r/z_s;q)_{k_r}}=\frac{(b/a_1,\ldots,b/a_{d+1};q)_N}{(q,bz_1,\ldots,bz_d;q)_N},\quad b=\prod_{s=1}^{d+1}a_s\prod_{r=1}^dz_r.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity211
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q b : K) (d N : ℕ) (aa : Fin (d+1) → K) (z : Fin d → K)
 (hbase : regular q) (hd : 0 < d) (hz : ∀ i, z i ≠ 0) (hzd : Function.Injective z) (ha : ∀ i, aa i ≠ 0) (hb : b = (∏ i, aa i)*(∏ i, z i))
 (h_domain : ∀ k ∈ (compositions d N), ((vandermonde z) ≠ 0 ∧
    ∀ r ∈ (Finset.univ : Finset (Fin d)), (∀ s ∈ (Finset.univ : Finset (Fin d)), ((z s) ≠ 0) ∧
    ((pochList [(b * (z r))] q ((k r).val)) * (∏ s ∈ (Finset.univ : Finset (Fin d)), (pochList [((q * (z r)) / (z s))] q ((k r).val)))) ≠ 0)) ∧
    ∀ s ∈ (Finset.univ : Finset (Fin (d+1))), ((aa s) ≠ 0) ∧
    ((pochList [q] q (N)) * (∏ r ∈ (Finset.univ : Finset (Fin d)), (pochList [(b * (z r))] q (N)))) ≠ 0) :
 (∑ k ∈ (compositions d N), (((vandermonde (fun i => z i*q^((k i).val))) / (vandermonde z)) * (∏ r ∈ (Finset.univ : Finset (Fin d)), ((∏ s ∈ (Finset.univ : Finset (Fin (d+1))), (pochList [((aa s) * (z r))] q ((k r).val))) / ((pochList [(b * (z r))] q ((k r).val)) * (∏ s ∈ (Finset.univ : Finset (Fin d)), (pochList [((q * (z r)) / (z s))] q ((k r).val)))))))) = ((∏ s ∈ (Finset.univ : Finset (Fin (d+1))), (pochList [(b / (aa s))] q (N))) / ((pochList [q] q (N)) * (∏ r ∈ (Finset.univ : Finset (Fin d)), (pochList [(b * (z r))] q (N))))) := by
  sorry

end FiniteQBenchmark.Identity211
