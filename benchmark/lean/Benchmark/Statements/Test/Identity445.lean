import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-26.rootsum — 相同平移参数的根和有限解
Original representative source: KAC-CHEUNG-26.rootsum
Frozen statement: formulas/test/FQI-SRC-KAC-CHEUNG-26.rootsum.md
Source formula:
s_n=(a-h)[n]_{q,r}+h[n]_{q,r}\sum_{j=1}^n\frac{j}{[j]_{q,r}},\qquad s_1=a.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity445
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q r h a : ℂ) (n : ℕ) (T : ℕ → Polynomial ℂ)
 (hq : q ≠ 0) (hq1 : q ≠ 1) (hqr : q ≠ r) (hn : 1 ≤ n)
 (hnum : ∀ j ∈ Finset.Icc 1 n, pairNumber q r j ≠ 0)
 (hT : quantumTaylorFamily q r h h a T n) :
 quantumRootSum T n = (a-h)*pairNumber q r n +
 h*pairNumber q r n*(∑ j ∈ Finset.Icc 1 n, (j:ℂ)/pairNumber q r j) ∧ quantumRootSum T 1=a := by
  sorry

end FiniteQBenchmark.Identity445
