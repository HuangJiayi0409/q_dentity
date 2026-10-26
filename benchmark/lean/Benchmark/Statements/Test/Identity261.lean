import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-14 — Sears–Carlitz 终止变换
Original representative source: GR2-III-14
Frozen statement: formulas/test/FQI-SRC-GR2-III-14.md
Source formula:
{}_3\phi_2^{[n]}\!\left[\begin{matrix}a,b,c\\aq/b,aq/c\end{matrix};q,aqz/(bc)\right]=(az;q)_n\sum_{k=0}^{\lfloor n/2\rfloor}\frac{(a;q)_{2k}(aq/(bc);q)_k}{(q,aq/b,aq/c,az,q/z;q)_k}q^k,\qquad a=q^{-n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity261
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c z q : K) (n : ℕ)
 (hbase : regular q) (ha : a = q^(-(n:ℤ))) (hnz : b*c*z ≠ 0)
 (h_domain : b ≠ 0 ∧
    c ≠ 0 ∧
    (b * c) ≠ 0 ∧
    phiDefined [((a * q) / b),((a * q) / c)] q (n) ∧
    ∀ k ∈ Finset.range (n/2+1), ((b * c) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    z ≠ 0 ∧
    (pochList [q,((a * q) / b),((a * q) / c),(a * z),(q / z)] q (k)) ≠ 0)) :
 (phi [a,b,c] [((a * q) / b),((a * q) / c)] q (((a * q) * z) / (b * c)) (n)) = ((pochList [(a * z)] q (n)) * (∑ k ∈ Finset.range (n/2+1), ((((pochList [a] q (2*k)) * (pochList [((a * q) / (b * c))] q (k))) / (pochList [q,((a * q) / b),((a * q) / c),(a * z),(q / z)] q (k))) * (q^(((k : ℤ)) : ℤ))))) := by
  sorry

end FiniteQBenchmark.Identity261
