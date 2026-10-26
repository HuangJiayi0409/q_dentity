import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-11.6.5-p0 — Macdonald 有限乘积望远镜求和
Original representative source: GR2-11.6.5-p0
Frozen statement: formulas/train/FQI-SRC-GR2-11.6.5-p0.md
Source formula:
\sum_{k=0}^nV_k\prod_{j=0}^{k-1}U_j=1-\prod_{j=0}^nU_j,\quad U_j=\frac{(1-b_j)(1-c_j)(1-d_j)(1-a_j^2/(b_jc_jd_j))}{(1-a_j/b_j)(1-a_j/c_j)(1-a_j/d_j)(1-b_jc_jd_j/a_j)},\quad V_j=\frac{(1-a_j)(1-a_j/(b_jc_j))(1-a_j/(b_jd_j))(1-a_j/(c_jd_j))}{(1-a_j/(b_jc_jd_j))(1-a_j/d_j)(1-a_j/c_j)(1-a_j/b_j)}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity207
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d : ℕ → K) (n : ℕ)
 (hnz : ∀ j ≤ n, a j*b j*c j*d j ≠ 0)
 (h_domain : ∀ k ∈ Finset.range (n+1), (((b k) * (c k)) ≠ 0 ∧
    ((b k) * (d k)) ≠ 0 ∧
    ((c k) * (d k)) ≠ 0 ∧
    (((b k) * (c k)) * (d k)) ≠ 0 ∧
    (d k) ≠ 0 ∧
    (c k) ≠ 0 ∧
    (b k) ≠ 0 ∧
    ((((1 - ((a k) / (((b k) * (c k)) * (d k)))) * (1 - ((a k) / (d k)))) * (1 - ((a k) / (c k)))) * (1 - ((a k) / (b k)))) ≠ 0 ∧
    ∀ j ∈ Finset.range (k), ((((b j) * (c j)) * (d j)) ≠ 0 ∧
    (b j) ≠ 0 ∧
    (c j) ≠ 0 ∧
    (d j) ≠ 0 ∧
    (a j) ≠ 0 ∧
    ((((1 - ((a j) / (b j))) * (1 - ((a j) / (c j)))) * (1 - ((a j) / (d j)))) * (1 - ((((b j) * (c j)) * (d j)) / (a j)))) ≠ 0)) ∧
    ∀ j ∈ Finset.range (n+1), ((((b j) * (c j)) * (d j)) ≠ 0 ∧
    (b j) ≠ 0 ∧
    (c j) ≠ 0 ∧
    (d j) ≠ 0 ∧
    (a j) ≠ 0 ∧
    ((((1 - ((a j) / (b j))) * (1 - ((a j) / (c j)))) * (1 - ((a j) / (d j)))) * (1 - ((((b j) * (c j)) * (d j)) / (a j)))) ≠ 0)) :
 (∑ k ∈ Finset.range (n+1), ((((((1 - (a k)) * (1 - ((a k) / ((b k) * (c k))))) * (1 - ((a k) / ((b k) * (d k))))) * (1 - ((a k) / ((c k) * (d k))))) / ((((1 - ((a k) / (((b k) * (c k)) * (d k)))) * (1 - ((a k) / (d k)))) * (1 - ((a k) / (c k)))) * (1 - ((a k) / (b k))))) * (∏ j ∈ Finset.range (k), (((((1 - (b j)) * (1 - (c j))) * (1 - (d j))) * (1 - (((a j)^2) / (((b j) * (c j)) * (d j))))) / ((((1 - ((a j) / (b j))) * (1 - ((a j) / (c j)))) * (1 - ((a j) / (d j)))) * (1 - ((((b j) * (c j)) * (d j)) / (a j)))))))) = (1 - (∏ j ∈ Finset.range (n+1), (((((1 - (b j)) * (1 - (c j))) * (1 - (d j))) * (1 - (((a j)^2) / (((b j) * (c j)) * (d j))))) / ((((1 - ((a j) / (b j))) * (1 - ((a j) / (c j)))) * (1 - ((a j) / (d j)))) * (1 - ((((b j) * (c j)) * (d j)) / (a j))))))) := by
  sorry

end FiniteQBenchmark.Identity207
