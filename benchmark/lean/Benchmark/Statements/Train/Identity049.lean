import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex3ii — 有限 q 多项式定理
Original representative source: GR2-1.Ex3ii
Frozen statement: formulas/train/FQI-SRC-GR2-1.Ex3ii.md
Source formula:
(a_1\cdots a_{m+1};q)_n=\sum_{\substack{k_1,\ldots,k_m\ge0\\K=k_1+\cdots+k_m\le n}}\frac{(q;q)_n\prod_{j=1}^m(a_j;q)_{k_j}(a_{m+1};q)_{n-K}}{\prod_{j=1}^m(q;q)_{k_j}(q;q)_{n-K}}\prod_{j=2}^{m+1}a_j^{k_1+\cdots+k_{j-1}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity049
variable {K : Type*} [Field K]

theorem statement (q : K) (m n : ℕ) (a : Fin (m+1) → K) (hm : 1 ≤ m) (hq : regular q) :
 poch (∏ j, a j) q n =
 ∑ k ∈ (Finset.univ : Finset (Fin m → Fin (n+1))).filter (fun k => (∑ i, (k i).val) ≤ n),
 (poch q q n * (∏ j : Fin m, poch (a j.castSucc) q (k j).val) *
 poch (a (Fin.last m)) q (n-∑ j, (k j).val) /
 ((∏ j : Fin m, poch q q (k j).val)*poch q q (n-∑ j, (k j).val))) *
 ∏ j : Fin (m+1), (a j)^(∑ i : Fin m, if i.val < j.val then (k i).val else 0) := by
  sorry

end FiniteQBenchmark.Identity049
