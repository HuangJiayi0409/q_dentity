import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-OSCILLATION-M-EVEN — 振荡分拆闭式：M-EVEN
Original representative source: AP-9.3.9
Frozen statement: formulas/train/FQI-OSCILLATION-M-EVEN.md
Source formula:
M_{k,i}(a,b;2\mu;q)=q^{\mu((4k+2)\mu+2k-2i+1)}\begin{bmatrix}a+b\\b-(2k+1)\mu\end{bmatrix}_{q}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity032
variable {K : Type*} [Field K]

theorem statement (q : K) (k i a b mu : ℕ) (hi : 1 ≤ i) (hik : i ≤ k)
 (hab : b = a ∨ b+1 = a) :
 oscillationPoly q false k i a b (2*mu) =
 q^((mu : ℤ)*((4*(k : ℤ)+2)*mu+2*k-2*i+1)) *
 gaussianInt q (a+b) ((b : ℤ)-(2*(k : ℤ)+1)*mu) := by
  sorry

end FiniteQBenchmark.Identity032
