import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-15.2 — Fine 系数的有限卷积
Original representative source: FINE-15.2
Frozen statement: formulas/train/FQI-SRC-FINE-15.2.md
Source formula:
A_N=\sum_{k=0}^N\frac{(-1)^k(aq;q)_{N-k}q^{k(k-1)/2}}{(bq;q)_{N-k}(q;q)_k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity346
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (N : ℕ)
 
 (h_domain : ∀ j ≤ (N), poch q q j ≠ 0 ∧ poch (b*q) q j ≠ 0 ∧
    ∀ k ∈ Finset.range (N+1), (((pochList [(b * q)] q (N-k)) * (pochList [q] q (k))) ≠ 0)) :
 (fineA a b q (N)) = (∑ k ∈ Finset.range (N+1), (((((-1:K)^k) * (pochList [(a * q)] q (N-k))) * (q^(k*(k-1)/2))) / ((pochList [(b * q)] q (N-k)) * (pochList [q] q (k))))) := by
  sorry

end FiniteQBenchmark.Identity346
