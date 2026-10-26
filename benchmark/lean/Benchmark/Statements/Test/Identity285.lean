import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-11.2.9 — 盒内平面分拆行列式
Original representative source: AP-11.2.9
Frozen statement: formulas/test/FQI-SRC-AP-11.2.9.md
Source formula:
\Pi_{k,r}(n;q)=\det\left(q^{(i-j)(i-j-1)/2}\begin{bmatrix}n+r\\r-i+j\end{bmatrix}_{q}\right)_{1\le i,j\le k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity285
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (k r n : ℕ) (hk : 0 < k) (hr : 0 < r) :
 planeBoxPi q k r n = Matrix.det (fun i j : Fin k =>
   q^((((i.val:ℤ)-j.val)*((i.val:ℤ)-j.val-1)/2).toNat) *
   gaussianInt q ((n:ℤ)+r) ((r:ℤ)-i.val+j.val)) := by
  sorry

end FiniteQBenchmark.Identity285
