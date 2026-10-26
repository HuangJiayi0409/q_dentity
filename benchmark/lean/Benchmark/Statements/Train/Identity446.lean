import Benchmark.Batch5Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-KAC-CHEUNG-26.23 — 对称q-Taylor基底的正确有限构造
Original representative source: KAC-CHEUNG-26.23
Frozen statement: formulas/train/FQI-SRC-KAC-CHEUNG-26.23.md
Source formula:
T_0(x)=1,\qquad T_n(x)=\frac{x^n}{\langle n\rangle_q!}-\sum_{k=0}^{n-1}\frac{a^{n-k}}{\langle n-k\rangle_q!}T_k(x),\qquad\widetilde D_qT_n=T_{n-1},\quad T_n(a)=0\ (n\ge1).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity446
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q a : ℂ) (n : ℕ) (hq : q ≠ 0) (hq2 : q^2 ≠ 1)
 (hden : ∀ j ∈ Finset.Icc 1 n, symNumber q j ≠ 0) :
 symTaylor q a 0 = 1 ∧ (1 ≤ n →
 symTaylor q a n = Polynomial.C (1/symFactorial q n)*Polynomial.X^n -
 (∑ k ∈ Finset.range n, Polynomial.C (a^(n-k)/symFactorial q (n-k))*symTaylor q a k) ∧
 (∀ x : ℂ, symJackson q (fun y => (symTaylor q a n).eval y) x = (symTaylor q a (n-1)).eval x) ∧
 (symTaylor q a n).eval a=0) := by
  sorry

end FiniteQBenchmark.Identity446
