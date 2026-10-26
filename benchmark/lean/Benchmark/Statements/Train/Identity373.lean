import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-2.Ex2b — 二步长带符号 Bailey 有限和
Original representative source: SILLS-2.Ex2b
Frozen statement: formulas/train/FQI-SRC-SILLS-2.Ex2b.md
Source formula:
\mathcal B_n[\alpha;x^2,q^2]=(-1)^nq^{n^2}/((q^2;q^2)_n(-xq;q)_{2n}),\qquad \alpha_r=\alpha_r^{(1,2,1)}(x^2,q^2)
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity373
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (n : ℕ)
 
 (h_domain : ∀ r ∈ Finset.range (n+1), (1 ∣ r → (1-x)*poch (q^1) (q^1) (r/1) ≠ 0 ∧
    ((pochList [(q^2)] (q^2) (n-r)) * (pochList [((x^2) * (q^2))] (q^2) (n+r))) ≠ 0) ∧
    ((pochList [(q^2)] (q^2) (n)) * (pochList [((-x) * q)] q (2*n))) ≠ 0) :
 (∑ r ∈ Finset.range (n+1), ((sillsAlpha x q 1 1 r) / ((pochList [(q^2)] (q^2) (n-r)) * (pochList [((x^2) * (q^2))] (q^2) (n+r))))) = ((((-1:K)^n) * (q^(n*n))) / ((pochList [(q^2)] (q^2) (n)) * (pochList [((-x) * q)] q (2*n)))) := by
  sorry

end FiniteQBenchmark.Identity373
