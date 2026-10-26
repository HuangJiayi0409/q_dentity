import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-21.23 — basic multinomial 的整除筛选
Original representative source: FINE-21.23
Frozen statement: formulas/train/FQI-SRC-FINE-21.23.md
Source formula:
Q_m=0\ (m\not\equiv0\pmod k),\qquad Q_{nk}=\frac{(q;q)_{nk}}{(q^{k/p};q^{k/p})_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity355
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q s zeta : ℂ) (k p n m : ℕ) (hk : 0 < k) (hp : 0 < p)
 (hs : s^p = q) (hz : IsPrimitiveRoot zeta k)
 (hden : ∀ j ≤ max m (n*k), poch q q j ≠ 0) (hout : poch (s^k) (s^k) n ≠ 0) :
 (¬ k ∣ m → fineQ q (fun i : Fin p × Fin k => s^i.1.val*zeta^i.2.val) m = 0) ∧
 fineQ q (fun i : Fin p × Fin k => s^i.1.val*zeta^i.2.val) (n*k) = poch q q (n*k)/poch (s^k) (s^k) n := by
  sorry

end FiniteQBenchmark.Identity355
