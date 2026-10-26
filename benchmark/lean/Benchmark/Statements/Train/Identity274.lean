import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-3.3.14 — Saalschütz 的系数卷积形式
Original representative source: AP-3.3.14
Frozen statement: formulas/train/FQI-SRC-AP-3.3.14.md
Source formula:
\sum_{j=0}^N\frac{(a;q)_j(b;q)_j(c/(ab);q)_{N-j}}{(q;q)_j(c;q)_j(q;q)_{N-j}}\left(\frac{ab}{c}\right)^{N-j}=\frac{(c/a;q)_N(c/b;q)_N}{(q;q)_N(c;q)_N}\left(\frac{ab}{c}\right)^N.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity274
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c q : K) (N : ℕ)
 (hnz : a*b*c ≠ 0)
 (h_domain : ∀ j ∈ Finset.range (N+1), ((a * b) ≠ 0 ∧
    ((pochList [q,c] q (j)) * (pochList [q] q (N-j))) ≠ 0 ∧
    c ≠ 0) ∧
    a ≠ 0 ∧
    b ≠ 0 ∧
    (pochList [q,c] q (N)) ≠ 0 ∧
    c ≠ 0) :
 (∑ j ∈ Finset.range (N+1), ((((pochList [a,b] q (j)) * (pochList [(c / (a * b))] q (N-j))) / ((pochList [q,c] q (j)) * (pochList [q] q (N-j)))) * (((a * b) / c)^(N-j)))) = (((pochList [(c / a),(c / b)] q (N)) / (pochList [q,c] q (N))) * (((a * b) / c)^N)) := by
  sorry

end FiniteQBenchmark.Identity274
