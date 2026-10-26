import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-21.product — 根单位与分数底数的有限乘积重组
Original representative source: FINE-21.product
Frozen statement: formulas/train/FQI-SRC-FINE-21.product.md
Source formula:
\prod_{r=1}^p\prod_{j=0}^{k-1}(aq\zeta^j s^{r-1};q)_n=((aq)^k;s^k)_{np},\quad q=s^p,\quad\zeta=e^{2\pi i/k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity356
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q s zeta : ℂ) (n k p : ℕ) (hk : 0 < k) (hp : 0 < p)
 (hs : s^p = q) (hz : IsPrimitiveRoot zeta k) :
 (∏ r : Fin p, ∏ j : Fin k, poch (a*q*zeta^j.val*s^r.val) q n) =
 poch ((a*q)^k) (s^k) (n*p) := by
  sorry

end FiniteQBenchmark.Identity356
