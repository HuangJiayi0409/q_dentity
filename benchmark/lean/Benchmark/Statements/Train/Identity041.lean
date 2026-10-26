import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.2.55 — 对称 q 数阶乘转换
Original representative source: GR2-1.2.55
Frozen statement: formulas/train/FQI-SRC-GR2-1.2.55.md
Source formula:
\prod_{j=0}^{n-1}\frac{q^{(\alpha+j)/2}-q^{-(\alpha+j)/2}}{q^{1/2}-q^{-1/2}}=\frac{(q^\alpha;q)_n}{(1-q)^n}q^{n(1-\alpha)/2-n(n-1)/4}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity041
variable {K : Type*} [Field K]

theorem statement (q L alpha : ℂ) (n : ℕ) (hlog : Complex.exp L = q) (hq : regular q)
 (hroot : Complex.exp (L/2)-Complex.exp (-L/2) ≠ 0) :
 (∏ j ∈ Finset.range n,
 (Complex.exp ((alpha+j)*L/2)-Complex.exp (-(alpha+j)*L/2)) /
 (Complex.exp (L/2)-Complex.exp (-L/2))) =
 poch (Complex.exp (alpha*L)) q n / (1-q)^n *
 Complex.exp (((n : ℂ)*(1-alpha)/2-(n : ℂ)*(n-1)/4)*L) := by
  sorry

end FiniteQBenchmark.Identity041
