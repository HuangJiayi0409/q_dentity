import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-BAILEY-INVERSION — 有限 Bailey 反演
Original representative source: AQ-3.40
Frozen statement: formulas/train/FQI-BAILEY-INVERSION.md
Source formula:
\alpha_0=\beta_0,\qquad \alpha_n=(1-aq^{2n})\sum_{j=0}^n\frac{(aq;q)_{n+j-1}(-1)^{n-j}q^{(n-j)(n-j-1)/2}}{(q;q)_{n-j}}\beta_j\quad(n\ge1).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity018
variable {K : Type*} [Field K]

theorem statement (a q : K) (n : ℕ) (alpha beta : ℕ → K)
    (hden : baileyDefined a q n)
    (hpair : ∀ j ≤ n, beta j = baileySum a q alpha j) :
    alpha 0 = beta 0 ∧ (0 < n →
      alpha n = (1-a*q^(2*n)) * ∑ j ∈ Finset.range (n+1),
        poch (a*q) q (n+j-1) * (-1)^(n-j) * q^((n-j)*(n-j-1)/2) /
          poch q q (n-j) * beta j) := by
  sorry

end FiniteQBenchmark.Identity018
