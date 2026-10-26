import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-9.L8 — 分拆筛辅助有限和的递推
Original representative source: AP-9.L8
Frozen statement: formulas/train/FQI-SRC-AP-9.L8.md
Source formula:
f(A,r;X,Y,L)-f(A,r-1;X,Y,L)-f(A-1,r+1;X,Y,L)+f(A-1,r;X,Y,L)=q^{L+2A+2Y+r}\begin{bmatrix}2A+X+r-2\\A+Y\end{bmatrix}_{q}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity295
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (A r X Y L : ℤ)
 (hq : q ≠ 0) (hr : 1 ≤ r) (hAX : 2 ≤ 2*A+X)
 (h_domain : True) :
 ((((sieveSmallF q A r X Y L) - (sieveSmallF q A (r-1) X Y L)) - (sieveSmallF q (A-1) (r+1) X Y L)) + (sieveSmallF q (A-1) r X Y L)) = ((q^(L+2*A+2*Y+r)) * (gaussianInt q (2*A+X+r-2) (A+Y))) := by
  sorry

end FiniteQBenchmark.Identity295
