import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-3.E7 — Rogers–Szegő 线性化公式
Original representative source: AP-3.E7
Frozen statement: formulas/train/FQI-SRC-AP-3.E7.md
Source formula:
H_m(t;q)H_n(t;q)=\sum_{r=0}^{\min(m,n)}\begin{bmatrix}m\\r\end{bmatrix}_{q}\begin{bmatrix}n\\r\end{bmatrix}_{q}(q;q)_r t^r H_{m+n-2r}(t;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity278
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q t : K) (m n : ℕ)
 
 (h_domain : True) :
 ((rogersSzego t q m) * (rogersSzego t q n)) = (∑ r ∈ Finset.range (min m n+1), (((((gaussian q (m) (r)) * (gaussian q (n) (r))) * (pochList [q] q (r))) * (t^r)) * (rogersSzego t q (m+n-2*r)))) := by
  sorry

end FiniteQBenchmark.Identity278
