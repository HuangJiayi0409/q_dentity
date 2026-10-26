import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-11.7.1 — Milne 的多变量有限 q 求和
Original representative source: GR2-11.7.1
Frozen statement: formulas/test/FQI-SRC-GR2-11.7.1.md
Source formula:
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|=N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{r,s=1}^d\frac{(a_rz_s/z_r;q)_{k_s}}{(qz_s/z_r;q)_{k_s}}=\frac{(a_1\cdots a_d;q)_N}{(q;q)_N},\quad\Delta(z)=\prod_{r<s}(z_r-z_s).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity210
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (d N : ℕ) (aa z : Fin d → K)
 (hbase : regular q) (hd : 0 < d) (hz : ∀ i, z i ≠ 0) (hzd : Function.Injective z)
 (h_domain : ∀ k ∈ (compositions d N), ((vandermonde z) ≠ 0 ∧
    ∀ r ∈ (Finset.univ : Finset (Fin d)), (∀ s ∈ (Finset.univ : Finset (Fin d)), ((z r) ≠ 0 ∧
    (pochList [((q * (z s)) / (z r))] q ((k s).val)) ≠ 0))) ∧
    (pochList [q] q (N)) ≠ 0) :
 (∑ k ∈ (compositions d N), (((vandermonde (fun i => z i*q^((k i).val))) / (vandermonde z)) * (∏ r ∈ (Finset.univ : Finset (Fin d)), (∏ s ∈ (Finset.univ : Finset (Fin d)), ((pochList [(((aa r) * (z s)) / (z r))] q ((k s).val)) / (pochList [((q * (z s)) / (z r))] q ((k s).val))))))) = ((pochList [(∏ i, aa i)] q (N)) / (pochList [q] q (N))) := by
  sorry

end FiniteQBenchmark.Identity210
