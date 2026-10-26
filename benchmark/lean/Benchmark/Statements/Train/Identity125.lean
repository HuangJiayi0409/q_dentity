import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-6.Ex14 — Askey 单变量有限常数项恒等式
Original representative source: GR2-6.Ex14
Frozen statement: formulas/train/FQI-SRC-GR2-6.Ex14.md
Source formula:
\operatorname{CT}_x(qx,x^{-1};q)_j(qx^2,qx^{-2};q^2)_k=\frac{(q;q)_{2j}(q^2;q^2)_{2k}(q^{2j+1};q^2)_k}{(q;q)_j(q^2;q^2)_k(q;q)_{j+2k}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity125
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (j k : ℕ)
 (hbase : regular q) 
 (h_domain : (((pochList [q] q (j)) * (pochList [(q * q)] (q * q) (k))) * (pochList [q] q (j+2*k))) ≠ 0) :
 ((pochList [laurentMono 1 q,laurentMono (-1) 1] (laurentMono 0 q) j * pochList [laurentMono 2 q,laurentMono (-2) q] (laurentMono 0 (q^2)) k).coeff 0) = ((((pochList [q] q (2*j)) * (pochList [(q * q)] (q * q) (2*k))) * (pochList [(q^((2*(j : ℤ)+1) : ℤ))] (q * q) (k))) / (((pochList [q] q (j)) * (pochList [(q * q)] (q * q) (k))) * (pochList [q] q (j+2*k)))) := by
  sorry

end FiniteQBenchmark.Identity125
