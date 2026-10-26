import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-OSCILLATION-P-ODD — 振荡分拆闭式：P-ODD
Original representative source: AP-9.3.12
Frozen statement: formulas/train/FQI-OSCILLATION-P-ODD.md
Source formula:
P_{k,i}(a,b;2\mu-1;q)=q^{(2\mu-1)((2k+1)\mu-i)}\begin{bmatrix}a+b\\a-(2k+1)\mu+i\end{bmatrix}_{q}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity035
variable {K : Type*} [Field K]

theorem statement (q : K) (k i a b mu : ℕ) (hi : 1 ≤ i) (hik : i ≤ k)
 (hab : b = a ∨ b+1 = a) (hmu : 1 ≤ mu) :
 oscillationPoly q true k i a b (2*mu-1) =
 q^((2*(mu : ℤ)-1)*((2*(k : ℤ)+1)*mu-i)) *
 gaussianInt q (a+b) ((a : ℤ)-(2*(k : ℤ)+1)*mu+i) := by
  sorry

end FiniteQBenchmark.Identity035
