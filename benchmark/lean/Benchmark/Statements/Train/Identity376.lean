import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-2.Ex2e — 偶指标 Bailey 有限和 II
Original representative source: SILLS-2.Ex2e
Frozen statement: formulas/train/FQI-SRC-SILLS-2.Ex2e.md
Source formula:
\mathcal B_n[\alpha;x,q]=1/((q;q)_n(xq;q^2)_n),\qquad \alpha_r=\alpha_r^{(2,1,3)}(x^1,q^1)
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity376
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (n : ℕ)
 
 (h_domain : ∀ r ∈ Finset.range (n+1), (2 ∣ r → (1-x)*poch (q^2) (q^2) (r/2) ≠ 0 ∧
    ((pochList [(q^1)] (q^1) (n-r)) * (pochList [((x^1) * (q^1))] (q^1) (n+r))) ≠ 0) ∧
    ((pochList [q] q (n)) * (pochList [(x * q)] (q^2) (n))) ≠ 0) :
 (∑ r ∈ Finset.range (n+1), ((sillsAlpha x q 2 3 r) / ((pochList [(q^1)] (q^1) (n-r)) * (pochList [((x^1) * (q^1))] (q^1) (n+r))))) = (1 / ((pochList [q] q (n)) * (pochList [(x * q)] (q^2) (n)))) := by
  sorry

end FiniteQBenchmark.Identity376
