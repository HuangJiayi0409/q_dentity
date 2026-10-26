import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-II-17 — 终止 q-Watson 求和及奇偶消失
Original representative source: GR2-II-17
Frozen statement: formulas/train/FQI-SRC-GR2-II-17.md
Source formula:
{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},aq^n,c,-c\\s,-s,c^2\end{matrix};q,q\right]=\begin{cases}c^n\dfrac{(q,aq/c^2;q^2)_{n/2}}{(aq,c^2q;q^2)_{n/2}},&n\text{ 为偶数},\\0,&n\text{ 为奇数}.\end{cases}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity248
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a s c q : K) (n : ℕ)
 (hbase : regular q) (hsc : s*c ≠ 0) (ha : s^2 = a*q)
 (h_domain : phiDefined [s,(-s),(c^2)] q (n) ∧
    n % 2 = 0 → ((c^2) ≠ 0) ∧
    n % 2 = 0 → ((pochList [(a * q),((c^2) * q)] (q^2) (n/2)) ≠ 0)) :
 (phi [(q^((-(n : ℤ)) : ℤ)),(a * (q^(((n : ℤ)) : ℤ))),c,(-c)] [s,(-s),(c^2)] q q (n)) = (if n % 2 = 0 then (((c^n) * (pochList [q,((a * q) / (c^2))] (q^2) (n/2))) / (pochList [(a * q),((c^2) * q)] (q^2) (n/2))) else 0) := by
  sorry

end FiniteQBenchmark.Identity248
