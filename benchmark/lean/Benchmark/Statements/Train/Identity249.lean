import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-II-19 — 终止 q-Whipple 的有限乘积形式
Original representative source: GR2-II-19
Frozen statement: formulas/train/FQI-SRC-GR2-II-19.md
Source formula:
{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},q^{n+1},c,-c\\e,c^2q/e,-q\end{matrix};q,q\right]=q^{n(n+1)/2}\frac{(eq^{-n},c^2q^{1-n}/e;q^2)_\ell}{(eq^\epsilon,c^2q^{1+\epsilon}/e;q^2)_\ell},\quad\ell=\lceil n/2\rceil,\quad\epsilon=1-(n\bmod2).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity249
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (ee c q : K) (n : ℕ)
 (hbase : regular q) (he : ee ≠ 0)
 (h_domain : ee ≠ 0 ∧
    phiDefined [ee,(((c^2) * q) / ee),(-q)] q (n) ∧
    (pochList [(ee * (q^((1-((n : ℤ)%2)) : ℤ))),(((c^2) * (q^((2-((n : ℤ)%2)) : ℤ))) / ee)] (q^2) ((n+1)/2)) ≠ 0) :
 (phi [(q^((-(n : ℤ)) : ℤ)),(q^(((n : ℤ)+1) : ℤ)),c,(-c)] [ee,(((c^2) * q) / ee),(-q)] q q (n)) = (((q^(((n : ℤ)*((n : ℤ)+1)/2) : ℤ)) * (pochList [(ee * (q^((-(n : ℤ)) : ℤ))),(((c^2) * (q^((1-(n : ℤ)) : ℤ))) / ee)] (q^2) ((n+1)/2))) / (pochList [(ee * (q^((1-((n : ℤ)%2)) : ℤ))),(((c^2) * (q^((2-((n : ℤ)%2)) : ℤ))) / ee)] (q^2) ((n+1)/2))) := by
  sorry

end FiniteQBenchmark.Identity249
