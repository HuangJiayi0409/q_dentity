import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-CAYLEY — Cayley 有限有理分解
Original representative source: AP-5.CAYLEY
Frozen statement: formulas/test/FQI-CAYLEY.md
Source formula:
\frac1{(q;q)_n}=\sum_{\substack{p_1,\ldots,p_n\ge0\\\sum_{j=1}^n jp_j=n}}\prod_{j=1}^n\frac1{j^{p_j}p_j!(1-q^j)^{p_j}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity031
variable {K : Type*} [Field K]

theorem statement [CharZero K] (q : K) (n : ℕ) (hden : ∀ j ∈ Finset.Icc 1 n, 1-q^j ≠ 0) :
 (poch q q n)⁻¹ = ∑ p ∈ cayleyVectors n,
 ∏ j : Fin n, ((j.val+1 : K)^(p j).val * (Nat.factorial (p j).val : K) * (1-q^(j.val+1))^(p j).val)⁻¹ := by
  sorry

end FiniteQBenchmark.Identity031
