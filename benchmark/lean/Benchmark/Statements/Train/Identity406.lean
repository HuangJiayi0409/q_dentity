import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-4.54 — Borwein A 多项式的正向有限和
Original representative source: SILLS-4.54
Frozen statement: formulas/train/FQI-SRC-SILLS-4.54.md
Source formula:
\mathsf A_n(q)=\sum_{j=0}^{\lfloor n/3\rfloor}\frac{(q^3;q^3)_{n-j-1}(1-q^{2n})(q;q)_{3j}q^{3j^2}}{(q;q)_{n-3j}(q^3;q^3)_{2j}(q^3;q^3)_j}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity406
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ)
 (hn : 1 ≤ n)
 (h_domain : ∀ j ∈ Finset.range (n/3+1), ((((pochList [q] q (n-3*j)) * (pochList [(q^3)] (q^3) (2*j))) * (pochList [(q^3)] (q^3) (j))) ≠ 0)) :
 (borweinA q n) = (∑ j ∈ Finset.range (n/3+1), (((((pochList [(q^3)] (q^3) (n-j-1)) * (1 - (q^(2*n)))) * (pochList [q] q (3*j))) * (q^(3*j*j))) / (((pochList [q] q (n-3*j)) * (pochList [(q^3)] (q^3) (2*j))) * (pochList [(q^3)] (q^3) (j))))) ∧
 (borweinA q 0) = 1 := by
  sorry

end FiniteQBenchmark.Identity406
