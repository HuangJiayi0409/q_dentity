import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-7.GH — q-移位迭代的有限累积系数
Original representative source: FINE-7.GH
Frozen statement: formulas/train/FQI-SRC-FINE-7.GH.md
Source formula:
H_n=\frac{(b/a;q)_{n+1}}{(bq;q)_{n+1}(b/(at);q)_{n+1}},\qquad G_n=-\frac{b/(at)}{1-b/(at)}\sum_{j=0}^n\frac{(b/a;q)_j q^j}{(bq;q)_j(bq/(at);q)_j}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity345
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b t q : K) (n : ℕ)
 (hat : a*t ≠ 0) (hrec : ∀ j ≤ n, (1-b*q^(j+1))*(b*q^j-a*t) ≠ 0)
 (h_domain : a ≠ 0 ∧
    (a * t) ≠ 0 ∧
    ((pochList [(b * q)] q (n+1)) * (pochList [(b / (a * t))] q (n+1))) ≠ 0 ∧
    (1 - (b / (a * t))) ≠ 0 ∧
    ∀ j ∈ Finset.range (n+1), (a ≠ 0 ∧
    (a * t) ≠ 0 ∧
    ((pochList [(b * q)] q (j)) * (pochList [((b * q) / (a * t))] q (j))) ≠ 0)) :
 ((fineHG a b t q (n+1)).1) = ((pochList [(b / a)] q (n+1)) / ((pochList [(b * q)] q (n+1)) * (pochList [(b / (a * t))] q (n+1)))) ∧
 ((fineHG a b t q (n+1)).2) = (((-(b / (a * t))) / (1 - (b / (a * t)))) * (∑ j ∈ Finset.range (n+1), (((pochList [(b / a)] q (j)) * (q^j)) / ((pochList [(b * q)] q (j)) * (pochList [((b * q) / (a * t))] q (j)))))) := by
  sorry

end FiniteQBenchmark.Identity345
