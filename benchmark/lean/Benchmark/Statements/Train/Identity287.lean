import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-13.E3 — 三变量 q-下降乘积卷积
Original representative source: AP-13.E3
Frozen statement: formulas/train/FQI-SRC-AP-13.E3.md
Source formula:
\prod_{i=0}^{n-1}(X-Zq^i)=\sum_{k=0}^n \begin{bmatrix}n\\k\end{bmatrix}_{q}\prod_{j=0}^{k-1}(Y-Zq^j)\prod_{h=0}^{n-k-1}(X-Yq^h).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity287
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (X Y Z q : K) (n : ℕ) :
 (∏ i ∈ Finset.range n, (X-Z*q^i)) =
 ∑ k ∈ Finset.range (n+1), gaussian q n k *
   (∏ j ∈ Finset.range k, (Y-Z*q^j)) *
   (∏ h ∈ Finset.range (n-k), (X-Y*q^h)) := by
  sorry

end FiniteQBenchmark.Identity287
