import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-2.Lem2.53 — 半整数幂 Bailey 有限和
Original representative source: SILLS-2.Lem2.53
Frozen statement: formulas/train/FQI-SRC-SILLS-2.Lem2.53.md
Source formula:
\mathcal B_n[\alpha;q,q]=1/((q^{3/2};q)_n(q;q)_n),\qquad \alpha_r=q^{r^2+r/2}(1+q^{r+1/2})/(1+\sqrt q)
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity381
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q t : K) (n : ℕ)
 (ht : t^2 = q)
 (h_domain : ∀ r ∈ Finset.range (n+1), ((1 + t) ≠ 0 ∧
    ((pochList [q] q (n-r)) * (pochList [(q * q)] q (n+r))) ≠ 0) ∧
    ((pochList [(t^3)] q (n)) * (pochList [q] q (n))) ≠ 0) :
 (∑ r ∈ Finset.range (n+1), ((((t^(2*r*r+r)) * (1 + (t^(2*r+1)))) / (1 + t)) / ((pochList [q] q (n-r)) * (pochList [(q * q)] q (n+r))))) = (1 / ((pochList [(t^3)] q (n)) * (pochList [q] q (n)))) := by
  sorry

end FiniteQBenchmark.Identity381
