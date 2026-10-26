import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-BAILEY-LEMMA — 有限 Bailey 引理
Original representative source: AQ-REF-BAILEY
Frozen statement: formulas/train/FQI-BAILEY-LEMMA.md
Source formula:
\sum_{r=0}^n\frac{(\rho_1,\rho_2;q)_r(aq/(\rho_1\rho_2))^r(aq/(\rho_1\rho_2);q)_{n-r}}{(aq/\rho_1,aq/\rho_2;q)_n(q;q)_{n-r}}\beta_r=\sum_{r=0}^n\frac{(\rho_1,\rho_2;q)_r(aq/(\rho_1\rho_2))^r\alpha_r}{(aq/\rho_1,aq/\rho_2;q)_r(q;q)_{n-r}(aq;q)_{n+r}}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity019
variable {K : Type*} [Field K]

theorem statement (a q u v : K) (n : ℕ) (alpha beta : ℕ → K)
    (hu : u ≠ 0) (hv : v ≠ 0)
    (hden : baileyDefined a q n)
    (hpair : ∀ j ≤ n, beta j = baileySum a q alpha j)
    (hshift : ∀ j ≤ n, pochList [a*q/u,a*q/v] q j ≠ 0) :
    (∑ r ∈ Finset.range (n+1), pochList [u,v] q r * (a*q/(u*v))^r *
      poch (a*q/(u*v)) q (n-r) /
      (pochList [a*q/u,a*q/v] q n * poch q q (n-r)) * beta r) =
    ∑ r ∈ Finset.range (n+1), pochList [u,v] q r * (a*q/(u*v))^r * alpha r /
      (pochList [a*q/u,a*q/v] q r * poch q q (n-r) * poch (a*q) q (n+r)) := by
  sorry

end FiniteQBenchmark.Identity019
