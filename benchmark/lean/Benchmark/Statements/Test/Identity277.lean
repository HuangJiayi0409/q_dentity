import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-3.E1 — 有限 Jacobi 三重积
Original representative source: AP-3.E1
Frozen statement: formulas/test/FQI-SRC-AP-3.E1.md
Source formula:
\sum_{j=-n}^n q^{j^2}x^j\begin{bmatrix}2n\\n+j\end{bmatrix}_{q^2}=(-x^{-1}q;q^2)_n(-xq;q^2)_n.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity277
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x : K) (n : ℕ)
 (hx : x ≠ 0)
 (h_domain : x ≠ 0) :
 (∑ j ∈ Finset.Icc (-(n:ℤ)) (n:ℤ), q^(j*j).toNat*x^j*gaussianInt (q^2) (2*(n:ℤ)) ((n:ℤ)+j)) = (pochList [((-1 / x) * q),((-x) * q)] (q^2) (n)) := by
  sorry

end FiniteQBenchmark.Identity277
