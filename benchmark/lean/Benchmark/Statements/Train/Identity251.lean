import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-II-34 — Gosper 不定双底数有限求和
Original representative source: GR2-II-34
Frozen statement: formulas/train/FQI-SRC-GR2-II-34.md
Source formula:
\sum_{k=0}^n\frac{1-ap^kq^k}{1-a}\frac{(a;p)_k(c;q)_k}{(q;q)_k(ap/c;p)_k}c^{-k}=\frac{(ap;p)_n(cq;q)_n}{(q;q)_n(ap/c;p)_n}c^{-n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity251
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a c p q : K) (n : ℕ)
 (hbase : regular q) (hp : regular p) (hc : c ≠ 0)
 (h_domain : ∀ k ∈ Finset.range (n+1), ((1 - a) ≠ 0 ∧
    c ≠ 0 ∧
    ((pochList [q] q (k)) * (pochList [((a * p) / c)] p (k))) ≠ 0) ∧
    c ≠ 0 ∧
    ((pochList [q] q (n)) * (pochList [((a * p) / c)] p (n))) ≠ 0) :
 (∑ k ∈ Finset.range (n+1), ((((((1 - ((a * (p^(((k : ℤ)) : ℤ))) * (q^(((k : ℤ)) : ℤ)))) / (1 - a)) * (pochList [a] p (k))) * (pochList [c] q (k))) / ((pochList [q] q (k)) * (pochList [((a * p) / c)] p (k)))) * (c^((-(k : ℤ)) : ℤ)))) = ((((pochList [(a * p)] p (n)) * (pochList [(c * q)] q (n))) / ((pochList [q] q (n)) * (pochList [((a * p) / c)] p (n)))) * (c^((-(n : ℤ)) : ℤ))) := by
  sorry

end FiniteQBenchmark.Identity251
