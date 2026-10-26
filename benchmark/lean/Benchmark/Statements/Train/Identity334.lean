import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-10.12 — Bailey 对逐项反求递推
Original representative source: AQ-10.12
Frozen statement: formulas/train/FQI-SRC-AQ-10.12.md
Source formula:
\alpha_0=\beta_0,\quad \alpha_n=(aq;q)_{2n}\beta_n-\sum_{r=0}^{n-1}\frac{(aq^{n+r+1};q)_{n-r}}{(q;q)_{n-r}}\alpha_r.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity334
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (alpha : ℕ → K) (n : ℕ)
 (hn : 1 ≤ n) (hq : q ≠ 0)
 (h_domain : baileyDefined a q (0) ∧
    baileyDefined a q (n) ∧
    ∀ r ∈ Finset.range (n-1+1), ((pochList [q] q (n-r)) ≠ 0)) :
 (alpha 0) = (baileySum a q alpha (0)) ∧
 (alpha n) = (((pochList [(a * q)] q (2*n)) * (baileySum a q alpha (n))) - (∑ r ∈ Finset.range (n-1+1), (((pochList [(a * (q^(((n : ℤ)+(r : ℤ)+1) : ℤ)))] q (n-r)) / (pochList [q] q (n-r))) * (alpha r)))) := by
  sorry

end FiniteQBenchmark.Identity334
