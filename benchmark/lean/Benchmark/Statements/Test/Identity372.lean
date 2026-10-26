import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-2.Lem2.31 — 关于1的双边 Bailey 有限和
Original representative source: SILLS-2.Lem2.31
Frozen statement: formulas/test/FQI-SRC-SILLS-2.Lem2.31.md
Source formula:
\sum_{r=-n}^n\begin{bmatrix}2n\\n+r\end{bmatrix}_q a^rq^{r^2/2}=(-a\sqrt q,-\sqrt q/a;q)_n.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity372
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a t q : K) (n : ℕ)
 (ha : a ≠ 0) (ht : t^2 = q)
 (h_domain : a ≠ 0) :
 (∑ r ∈ Finset.Icc (-(n:ℤ) : ℤ) (n : ℤ), ((gaussianInt q (2*(n:ℤ)) ((n:ℤ)+r)) * (a^r*t^(r*r).toNat))) = (pochList [((-a) * t),((-t) / a)] q (n)) := by
  sorry

end FiniteQBenchmark.Identity372
