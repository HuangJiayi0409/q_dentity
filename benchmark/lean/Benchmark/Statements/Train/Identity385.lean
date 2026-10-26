import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-3.Lem3.3 — 偶模数 Bailey 有限和
Original representative source: SILLS-3.Lem3.3
Frozen statement: formulas/train/FQI-SRC-SILLS-3.Lem3.3.md
Source formula:
\mathcal B_n[\alpha;x,q]=1/(q^2;q^2)_n,\qquad \alpha_r=(-1)^rq^{r^2}(1-xq^{2r})(x^2;q^2)_r/((1-x)(q^2;q^2)_r)
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity385
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (n : ℕ)
 
 (h_domain : ∀ r ∈ Finset.range (n+1), (((1 - x) * (pochList [(q^2)] (q^2) (r))) ≠ 0 ∧
    ((pochList [q] q (n-r)) * (pochList [(x * q)] q (n+r))) ≠ 0) ∧
    (pochList [(q^2)] (q^2) (n)) ≠ 0) :
 (∑ r ∈ Finset.range (n+1), (((((((-1:K)^r) * (q^(r*r))) * (1 - (x * (q^(2*r))))) * (pochList [(x^2)] (q^2) (r))) / ((1 - x) * (pochList [(q^2)] (q^2) (r)))) / ((pochList [q] q (n-r)) * (pochList [(x * q)] q (n+r))))) = (1 / (pochList [(q^2)] (q^2) (n))) := by
  sorry

end FiniteQBenchmark.Identity385
