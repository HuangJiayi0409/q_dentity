import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-13.10 — 倒底数有限乘积转换
Original representative source: KAC-CHEUNG-13.10
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-13.10.md
Source formula:
\prod_{j=0}^{n-1}(a-q^{-j})=(-1)^nq^{-n(n-1)/2}(a;q)_n.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity432
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q a : K) (n : ℕ)
 (hq : q ≠ 0) (hq1 : q ≠ 1)
 (h_domain : True) :
 (∏ j ∈ Finset.range n, (a-q^(-(j:ℤ)))) = ((((-1:K)^n) * (q^(-((n:ℤ)*(n-1)/2)))) * (pochList [a] q (n))) := by
  sorry

end FiniteQBenchmark.Identity432
