import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-GAUSSIAN-VANDERMONDE — Gaussian q-Vandermonde 卷积
Original representative source: AP-3.3.10
Frozen statement: formulas/train/FQI-GAUSSIAN-VANDERMONDE.md
Source formula:
\sum_{k=\max(0,h-m)}^{\min(h,n)} \begin{bmatrix}n\\k\end{bmatrix}_{q}\begin{bmatrix}m\\h-k\end{bmatrix}_{q}q^{(n-k)(h-k)}=\begin{bmatrix}m+n\\h\end{bmatrix}_{q}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity008
variable {K : Type*} [Field K]

theorem statement (q : K) (m n h : ℕ) (hh : h ≤ m+n) :
 (∑ k ∈ Finset.Icc (h-m) (min h n), gaussian q n k * gaussian q m (h-k) * q^((n-k)*(h-k))) = gaussian q (m+n) h := by
  sorry

end FiniteQBenchmark.Identity008
