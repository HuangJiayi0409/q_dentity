import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.Ex40 — Rogers–Szegő 的有限 Turán 恒等式
Original representative source: GR2-7.Ex40
Frozen statement: formulas/train/FQI-SRC-GR2-7.Ex40.md
Source formula:
h_n(x)^2-h_{n+1}(x)h_{n-1}(x)=(1-q)(q;q)_{n-1}\sum_{k=1}^{n}\frac{q^{n-k}x^k}{(q;q)_{n-k}}h_{n-k}(x)^2,\quad h_n(x)=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_qx^k.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity156
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (n : ℕ)
 (hbase : regular q) (hn : 1 ≤ n)
 (h_domain : ∀ k ∈ Finset.Icc (1) (n), ((pochList [q] q (n-k)) ≠ 0)) :
 (((rogersSzego x q (n))^2) - ((rogersSzego x q (n+1)) * (rogersSzego x q (n-1)))) = (((1 - q) * (pochList [q] q (n-1))) * (∑ k ∈ Finset.Icc (1) (n), ((((q^(((n : ℤ)-(k : ℤ)) : ℤ)) * (x^k)) / (pochList [q] q (n-k))) * ((rogersSzego x q (n-k))^2)))) := by
  sorry

end FiniteQBenchmark.Identity156
