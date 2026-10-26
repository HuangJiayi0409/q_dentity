import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-7.2 — 有序线性无关向量组计数
Original representative source: KAC-CHEUNG-7.2
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-7.2.md
Source formula:
\#\{(v_1,\ldots,v_j)\in(\mathbb F_q^n)^j:\operatorname{rank}(v_1,\ldots,v_j)=j\}=\prod_{i=0}^{j-1}(q^n-q^i).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity428
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement {F : Type*} [Field F] [Fintype F] (n j : ℕ) (hj : j ≤ n) :
 (independentTuples F n j).card = ∏ i ∈ Finset.range j, ((Fintype.card F)^n-(Fintype.card F)^i) := by
  sorry

end FiniteQBenchmark.Identity428
