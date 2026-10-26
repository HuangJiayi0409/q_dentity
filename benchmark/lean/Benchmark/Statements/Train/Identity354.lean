import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-21.21 — basic multinomial 的分数幂特化
Original representative source: FINE-21.21
Frozen statement: formulas/train/FQI-SRC-FINE-21.21.md
Source formula:
Q_n(1,q^{1/p},q^{2/p},\ldots,q^{(p-1)/p})=\frac{(q;q)_n}{(q^{1/p};q^{1/p})_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity354
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q s : K) (p n : ℕ) (hp : 0 < p) (hs : s^p = q)
 (hden : ∀ j ≤ n, poch q q j ≠ 0) (hout : poch s s n ≠ 0) :
 fineQ q (fun i : Fin p => s^i.val) n = poch q q n/poch s s n := by
  sorry

end FiniteQBenchmark.Identity354
