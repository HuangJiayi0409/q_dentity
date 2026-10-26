import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SCHUR-RR-BUNDLE — Schur 两支有限 Rogers–Ramanujan
Original representative source: AP-3.E10
Frozen statement: formulas/train/FQI-SCHUR-RR-BUNDLE.md
Source formula:
\sum_{j=0}^{\lfloor(n+1-a)/2\rfloor}q^{j^2+aj}\begin{bmatrix}n+1-a-j\\j\end{bmatrix}_{q}=\sum_{h=-n-2}^{n+2}(-1)^hq^{h(5h+1)/2-2ah}\begin{bmatrix}n+1\\\lfloor(n+1-5h)/2\rfloor+a\end{bmatrix}_{q}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity030
variable {K : Type*} [Field K]

theorem statement (q : K) (n : ℕ) (a : ℤ) (ha : a = 0 ∨ a = 1) :
 (∑ j ∈ Finset.Icc (0 : ℤ) (((n : ℤ)+1-a)/2),
 q^(j^2+a*j)*gaussianInt q ((n : ℤ)+1-a-j) j) =
 ∑ h ∈ Finset.Icc (-(n : ℤ)-2) ((n : ℤ)+2),
 (-1)^h*q^(h*(5*h+1)/2-2*a*h)*gaussianInt q ((n : ℤ)+1) ((((n : ℤ)+1-5*h)/2)+a) := by
  sorry

end FiniteQBenchmark.Identity030
