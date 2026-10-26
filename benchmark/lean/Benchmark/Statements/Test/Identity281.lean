import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-7.E11 — 有最大部分限制的 Göllnitz 型有限公式
Original representative source: AP-7.E11
Frozen statement: formulas/test/FQI-SRC-AP-7.E11.md
Source formula:
d_{6n-1}(q)=\sum_{j=0}^{\lfloor n/2\rfloor}q^{6nj-3j^2+2j}\begin{bmatrix}n-j\\j\end{bmatrix}_{q^6}\Lambda_{n-2j}(q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity281
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ)
 (hn : 1 ≤ n)
 (h_domain : True) :
 (apGollnitz q (6*n-1)) = (∑ j ∈ Finset.range (n/2+1), (((q^(6*n*j-3*j*j+2*j)) * (gaussian (q^6) (n-j) (j))) * (apLambda q (n-2*j)))) := by
  sorry

end FiniteQBenchmark.Identity281
