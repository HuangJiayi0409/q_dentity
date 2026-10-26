import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-11.2.4 — Carlitz 固定首列行列式
Original representative source: AP-11.2.4
Frozen statement: formulas/train/FQI-SRC-AP-11.2.4.md
Source formula:
\pi_r(n_1,\ldots,n_k;q)=q^{n_1+\cdots+n_k}\det\left(q^{(i-j)(i-j-1)/2}\begin{bmatrix}n_j+r-1\\r-i+j-1\end{bmatrix}_{q}\right)_{1\le i,j\le k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity284
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (k r : ℕ) (n : Fin k → ℕ)
 (hk : 0 < k) (hr : 0 < r) (hn : Antitone n) :
 planePi q r n = q^(∑ j, n j) * Matrix.det (fun i j : Fin k =>
   q^((((i.val:ℤ)-j.val)*((i.val:ℤ)-j.val-1)/2).toNat) *
   gaussianInt q ((n j:ℤ)+r-1) ((r:ℤ)-i.val+j.val-1)) := by
  sorry

end FiniteQBenchmark.Identity284
