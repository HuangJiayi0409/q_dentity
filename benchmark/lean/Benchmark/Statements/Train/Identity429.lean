import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-7.rank — 有限域定秩矩阵计数
Original representative source: KAC-CHEUNG-7.rank
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-7.rank.md
Source formula:
\#\{A\in\mathbb F_q^{m\times n}:\operatorname{rank}A=j\}=\begin{bmatrix}n\\j\end{bmatrix}_q\begin{bmatrix}m\\j\end{bmatrix}_q\prod_{i=0}^{j-1}(q^j-q^i)=\begin{bmatrix}n\\j\end{bmatrix}_q\prod_{i=0}^{j-1}(q^m-q^i).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity429
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement {F : Type*} [Field F] [Fintype F] (m n j : ℕ) (hj : j ≤ min m n) :
 ((rankMatrices F m n j).card : ℤ) =
 gaussian (Fintype.card F : ℤ) n j*gaussian (Fintype.card F : ℤ) m j*
 (∏ i ∈ Finset.range j, ((Fintype.card F : ℤ)^j-(Fintype.card F : ℤ)^i)) ∧
 gaussian (Fintype.card F : ℤ) n j*gaussian (Fintype.card F : ℤ) m j*
 (∏ i ∈ Finset.range j, ((Fintype.card F : ℤ)^j-(Fintype.card F : ℤ)^i)) =
 gaussian (Fintype.card F : ℤ) n j*(∏ i ∈ Finset.range j, ((Fintype.card F : ℤ)^m-(Fintype.card F : ℤ)^i)) := by
  sorry

end FiniteQBenchmark.Identity429
