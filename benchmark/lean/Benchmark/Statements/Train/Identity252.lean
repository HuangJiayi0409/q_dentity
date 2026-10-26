import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-II-35 — Gosper 双底数求和扩展
Original representative source: GR2-II-35
Frozen statement: formulas/train/FQI-SRC-GR2-II-35.md
Source formula:
\sum_{k=0}^n\frac{(1-ap^kq^k)(1-bp^kq^{-k})}{(1-a)(1-b)}\frac{(a,b;p)_k(c,a/(bc);q)_k}{(q,aq/b;q)_k(ap/c,bcp;p)_k}q^k=\frac{(ap,bp;p)_n(cq,aq/(bc);q)_n}{(q,aq/b;q)_n(ap/c,bcp;p)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity252
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c p q : K) (n : ℕ)
 (hbase : regular q) (hp : regular p) (hnz : a*b*c ≠ 0)
 (h_domain : ∀ k ∈ Finset.range (n+1), (((1 - a) * (1 - b)) ≠ 0 ∧
    (b * c) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    ((pochList [q,((a * q) / b)] q (k)) * (pochList [((a * p) / c),((b * c) * p)] p (k))) ≠ 0) ∧
    (b * c) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    ((pochList [q,((a * q) / b)] q (n)) * (pochList [((a * p) / c),((b * c) * p)] p (n))) ≠ 0) :
 (∑ k ∈ Finset.range (n+1), (((((((1 - ((a * (p^(((k : ℤ)) : ℤ))) * (q^(((k : ℤ)) : ℤ)))) * (1 - ((b * (p^(((k : ℤ)) : ℤ))) * (q^((-(k : ℤ)) : ℤ))))) / ((1 - a) * (1 - b))) * (pochList [a,b] p (k))) * (pochList [c,(a / (b * c))] q (k))) * (q^(((k : ℤ)) : ℤ))) / ((pochList [q,((a * q) / b)] q (k)) * (pochList [((a * p) / c),((b * c) * p)] p (k))))) = (((pochList [(a * p),(b * p)] p (n)) * (pochList [(c * q),((a * q) / (b * c))] q (n))) / ((pochList [q,((a * q) / b)] q (n)) * (pochList [((a * p) / c),((b * c) * p)] p (n)))) := by
  sorry

end FiniteQBenchmark.Identity252
