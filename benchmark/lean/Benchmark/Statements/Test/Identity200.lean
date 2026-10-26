import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-9.Ex5i — 对偶 q-Hahn 有限生成函数（一，定义核正）
Original representative source: GR2-9.Ex5i
Frozen statement: formulas/test/FQI-SRC-GR2-9.Ex5i.md
Source formula:
\sum_{n=0}^N\frac{(q^{-N};q)_n}{(q;q)_n}D_n(x;b,c,N)t^n={}_2\phi_1^{[x]}(q^{-x},c^{-1}q^{-x};bq;q,bctq^{x+1})(tq^{-N};q)_{N-x}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity200
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (b c t q : K) (N x : ℕ)
 (hbase : regular q) (hx : x ≤ N) (hc : c ≠ 0)
 (h_domain : ∀ n ∈ Finset.range (N+1), ((pochList [q] q (n)) ≠ 0 ∧
    phiDefined [(q^((-(N : ℤ)) : ℤ)),(b * q)] q (min n x)) ∧
    c ≠ 0 ∧
    phiDefined [(b * q)] q (x)) :
 (∑ n ∈ Finset.range (N+1), ((((pochList [(q^((-(N : ℤ)) : ℤ))] q (n)) / (pochList [q] q (n))) * (phi [(q^((-(n : ℤ)) : ℤ)),(q^((-(x : ℤ)) : ℤ)),((b * c) * (q^(((x : ℤ)+1) : ℤ)))] [(q^((-(N : ℤ)) : ℤ)),(b * q)] q q (min n x))) * (t^(((n : ℤ)) : ℤ)))) = ((phi [(q^((-(x : ℤ)) : ℤ)),((q^((-(x : ℤ)) : ℤ)) / c)] [(b * q)] q (((b * c) * t) * (q^(((x : ℤ)+1) : ℤ))) (x)) * (pochList [(t * (q^((-(N : ℤ)) : ℤ)))] q (N-x))) := by
  sorry

end FiniteQBenchmark.Identity200
