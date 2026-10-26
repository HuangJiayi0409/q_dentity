import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-2.Pair112 — 基本 Bailey 有限和
Original representative source: SILLS-2.Pair112
Frozen statement: formulas/test/FQI-SRC-SILLS-2.Pair112.md
Source formula:
\mathcal B_n[\alpha;x,q]=1/(q;q)_n,\qquad \alpha_r=\alpha_r^{(1,1,2)}(x^1,q^1)
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity370
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (n : ℕ)
 
 (h_domain : ∀ r ∈ Finset.range (n+1), (1 ∣ r → (1-x)*poch (q^1) (q^1) (r/1) ≠ 0 ∧
    ((pochList [(q^1)] (q^1) (n-r)) * (pochList [((x^1) * (q^1))] (q^1) (n+r))) ≠ 0) ∧
    (pochList [q] q (n)) ≠ 0) :
 (∑ r ∈ Finset.range (n+1), ((sillsAlpha x q 1 2 r) / ((pochList [(q^1)] (q^1) (n-r)) * (pochList [((x^1) * (q^1))] (q^1) (n+r))))) = (1 / (pochList [q] q (n))) := by
  sorry

end FiniteQBenchmark.Identity370
