import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-3.7 — Bailey 链的有限双和
Original representative source: SILLS-3.7
Frozen statement: formulas/train/FQI-SRC-SILLS-3.7.md
Source formula:
\mathcal B_n[\alpha;x,q]=\sum_{j=0}^nx^jq^{j^2}/((q;q)_j(q;q)_{n-j}),\qquad \alpha_r=(-1)^rx^{2r}q^{r(5r-1)/2}(1-xq^{2r})(x;q)_r/((1-x)(q;q)_r)
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity384
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (n : ℕ)
 
 (h_domain : ∀ r ∈ Finset.range (n+1), (((1 - x) * (pochList [q] q (r))) ≠ 0 ∧
    ((pochList [q] q (n-r)) * (pochList [(x * q)] q (n+r))) ≠ 0) ∧
    ∀ j ∈ Finset.range (n+1), (((pochList [q] q (j)) * (pochList [q] q (n-j))) ≠ 0)) :
 (∑ r ∈ Finset.range (n+1), ((((((((-1:K)^r) * (x^(2*r))) * (q^(r*(5*r-1)/2))) * (1 - (x * (q^(2*r))))) * (pochList [x] q (r))) / ((1 - x) * (pochList [q] q (r)))) / ((pochList [q] q (n-r)) * (pochList [(x * q)] q (n+r))))) = (∑ j ∈ Finset.range (n+1), (((x^j) * (q^(j*j))) / ((pochList [q] q (j)) * (pochList [q] q (n-j))))) := by
  sorry

end FiniteQBenchmark.Identity384
