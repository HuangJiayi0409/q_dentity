import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.2.47 — q 数阶乘与有限乘积转换
Original representative source: GR2-1.2.47
Frozen statement: formulas/train/FQI-SRC-GR2-1.2.47.md
Source formula:
[\alpha]_{q;n}=(1-q)^{-n}(q^\alpha;q)_n.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity040
variable {K : Type*} [Field K]

theorem statement (q L alpha : ℂ) (n : ℕ) (hlog : Complex.exp L = q) (hq : regular q) :
 (∏ j ∈ Finset.range n, (1-Complex.exp ((alpha+j)*L))/(1-q)) =
 (1-q)^(-(n : ℤ))*poch (Complex.exp (alpha*L)) q n := by
  sorry

end FiniteQBenchmark.Identity040
