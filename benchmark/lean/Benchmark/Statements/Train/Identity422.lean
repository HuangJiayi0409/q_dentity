import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-4.3 — 单项式的高阶 q 导数
Original representative source: KAC-CHEUNG-4.3
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-4.3.md
Source formula:
D_q^jx^n=\begin{cases}\dfrac{[n]_q!}{[n-j]_q!}x^{n-j},&0\le j\le n,\\0,&j>n.\end{cases}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity422
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q x : ℂ) (n j : ℕ) (hq : q ≠ 0) (hq1 : q ≠ 1) (hden : j ≤ n → qFactorial q (n-j) ≠ 0) :
 ((jackson q)^[j]) (fun y => y^n) x =
 if j ≤ n then qFactorial q n/qFactorial q (n-j)*x^(n-j) else 0 := by
  sorry

end FiniteQBenchmark.Identity422
