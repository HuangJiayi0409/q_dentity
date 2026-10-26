import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-1.94-corrected — Andrews 有限 Heine 变换
Original representative source: SILLS-1.94-corrected
Frozen statement: formulas/train/FQI-SRC-SILLS-1.94-corrected.md
Source formula:
{}_3\phi_2^{[n]}\!\left[\begin{matrix}a,b,q^{-n}\\c,q^{1-n}/t\end{matrix};q,q\right]=\frac{(b,at;q)_n}{(c,t;q)_n}{}_3\phi_2^{[n]}\!\left[\begin{matrix}c/b,t,q^{-n}\\at,q^{1-n}/b\end{matrix};q,q\right].
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity364
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c t q : K) (n : ℕ)
 (hbt : b*t ≠ 0) (hq : q ≠ 0)
 (h_domain : t ≠ 0 ∧
    phiDefined [c,((q^((1-((n : ℤ))) : ℤ)) / t)] q (n) ∧
    (pochList [c,t] q (n)) ≠ 0 ∧
    b ≠ 0 ∧
    phiDefined [(a * t),((q^((1-(n : ℤ)) : ℤ)) / b)] q (n)) :
 (phi [a,b,(q^((-((n : ℤ))) : ℤ))] [c,((q^((1-((n : ℤ))) : ℤ)) / t)] q q (n)) = (((pochList [b,(a * t)] q (n)) / (pochList [c,t] q (n))) * (phi [(c / b),t,(q^((-(n : ℤ)) : ℤ))] [(a * t),((q^((1-(n : ℤ)) : ℤ)) / b)] q q (n))) := by
  sorry

end FiniteQBenchmark.Identity364
