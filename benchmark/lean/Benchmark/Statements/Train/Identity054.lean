import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex12iv — 高阶 q-Leibniz 公式
Original representative source: GR2-1.Ex12iv
Frozen statement: formulas/train/FQI-SRC-GR2-1.Ex12iv.md
Source formula:
D_q^n(fg)(z)=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_q(D_q^{n-k}f)(zq^k)(D_q^kg)(z).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity054
variable {K : Type*} [Field K]

theorem statement (q z : ℂ) (f g : ℂ → ℂ) (n : ℕ) (hq : regular q) (hz : z ≠ 0) :
 ((jackson q)^[n] (fun x => f x*g x)) z =
 ∑ k ∈ Finset.range (n+1), gaussian q n k *
 ((jackson q)^[n-k] f) (z*q^k) * ((jackson q)^[k] g) z := by
  sorry

end FiniteQBenchmark.Identity054
