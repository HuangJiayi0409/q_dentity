import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-21.2 — basic multinomial 的根单位筛选
Original representative source: FINE-21.2
Frozen statement: formulas/train/FQI-SRC-FINE-21.2.md
Source formula:
Q_n(1,\zeta,\ldots,\zeta^{k-1})=\begin{cases}0,&n\not\equiv0\pmod k,\\\dfrac{(q;q)_n}{(q^k;q^k)_{n/k}},&n\equiv0\pmod k,\end{cases}\quad \zeta=e^{2\pi i/k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity353
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q zeta : ℂ) (k n : ℕ) (hk : 0 < k) (hz : IsPrimitiveRoot zeta k)
 (hden : ∀ j ≤ n, poch q q j ≠ 0)
 (hout : k ∣ n → poch (q^k) (q^k) (n/k) ≠ 0) :
 fineQ q (fun i : Fin k => zeta^i.val) n =
 if k ∣ n then poch q q n/poch (q^k) (q^k) (n/k) else 0 := by
  sorry

end FiniteQBenchmark.Identity353
