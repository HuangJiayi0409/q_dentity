import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-2.Ex2c — 三步长 Bailey 有限和
Original representative source: SILLS-2.Ex2c
Frozen statement: formulas/train/FQI-SRC-SILLS-2.Ex2c.md
Source formula:
\mathcal B_n[\alpha;x^3,q^3]=(xq;q)_{3n}/((q^3;q^3)_n(x^3q^3;q^3)_{2n}),\qquad \alpha_r=\alpha_r^{(1,3,2)}(x^3,q^3)
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity374
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (n : ℕ)
 
 (h_domain : ∀ r ∈ Finset.range (n+1), (1 ∣ r → (1-x)*poch (q^1) (q^1) (r/1) ≠ 0 ∧
    ((pochList [(q^3)] (q^3) (n-r)) * (pochList [((x^3) * (q^3))] (q^3) (n+r))) ≠ 0) ∧
    ((pochList [(q^3)] (q^3) (n)) * (pochList [((x^3) * (q^3))] (q^3) (2*n))) ≠ 0) :
 (∑ r ∈ Finset.range (n+1), ((sillsAlpha x q 1 2 r) / ((pochList [(q^3)] (q^3) (n-r)) * (pochList [((x^3) * (q^3))] (q^3) (n+r))))) = ((pochList [(x * q)] q (3*n)) / ((pochList [(q^3)] (q^3) (n)) * (pochList [((x^3) * (q^3))] (q^3) (2*n)))) := by
  sorry

end FiniteQBenchmark.Identity374
