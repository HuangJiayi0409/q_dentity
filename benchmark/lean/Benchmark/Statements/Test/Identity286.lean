import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-11.2.10 — MacMahon 盒内平面分拆有限乘积
Original representative source: AP-11.2.10
Frozen statement: formulas/test/FQI-SRC-AP-11.2.10.md
Source formula:
\Pi_{k,r}(n;q)=\prod_{j=0}^{k-1}\frac{(q;q)_j(q;q)_{n+r+j}}{(q;q)_{r+j}(q;q)_{n+j}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity286
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (k r n : ℕ) (hk : 0 < k) (hr : 0 < r)
 (hden : ∀ j ∈ Finset.range k, poch q q (r+j)*poch q q (n+j) ≠ 0) :
 planeBoxPi q k r n = ∏ j ∈ Finset.range k,
   (poch q q j * poch q q (n+r+j)) / (poch q q (r+j)*poch q q (n+j)) := by
  sorry

end FiniteQBenchmark.Identity286
