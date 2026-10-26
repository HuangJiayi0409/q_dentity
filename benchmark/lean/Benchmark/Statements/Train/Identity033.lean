import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-OSCILLATION-M-ODD — 振荡分拆闭式：M-ODD
Original representative source: AP-9.3.10
Frozen statement: formulas/train/FQI-OSCILLATION-M-ODD.md
Source formula:
M_{k,i}(a,b;2\mu-1;q)=q^{(2\mu-1)((2k+1)\mu-2k+i-1)}\begin{bmatrix}a+b\\b-(2k+1)\mu+2k-i+1\end{bmatrix}_{q}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity033
variable {K : Type*} [Field K]

theorem statement (q : K) (k i a b mu : ℕ) (hi : 1 ≤ i) (hik : i ≤ k)
 (hab : b = a ∨ b+1 = a) (hmu : 1 ≤ mu) :
 oscillationPoly q false k i a b (2*mu-1) =
 q^((2*(mu : ℤ)-1)*((2*(k : ℤ)+1)*mu-2*k+i-1)) *
 gaussianInt q (a+b) ((b : ℤ)-(2*(k : ℤ)+1)*mu+2*k-i+1) := by
  sorry

end FiniteQBenchmark.Identity033
