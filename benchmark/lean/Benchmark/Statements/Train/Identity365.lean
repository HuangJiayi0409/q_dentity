import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-1.95 — 有限 Heine 和的二阶递推
Original representative source: SILLS-1.95
Frozen statement: formulas/train/FQI-SRC-SILLS-1.95.md
Source formula:
f_n+\frac{-abtq^{2n}+atq^{n+1}+btq^{n+1}-ctq^{2n}+cq^{n+1}+q^{n+2}-q^3-q^2}{q^2(1-cq^{n-1})(1-tq^{n-1})}f_{n-1}+\frac{q(1-q^{n-1})(1-atq^{n-2})(1-btq^{n-2})}{(1-cq^{n-1})(1-tq^{n-2})(1-tq^{n-1})}f_{n-2}=0.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity365
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c t q : K) (n : ℕ)
 (hn : 2 ≤ n) (hq : q ≠ 0) (ht : t ≠ 0)
 (h_domain : t ≠ 0 ∧
    phiDefined [c,((q^((1-((n : ℤ))) : ℤ)) / t)] q (n) ∧
    (((q^2) * (1 - (c * (q^(((n : ℤ)-1) : ℤ))))) * (1 - (t * (q^(((n : ℤ)-1) : ℤ))))) ≠ 0 ∧
    phiDefined [c,((q^((1-((n : ℤ)-1)) : ℤ)) / t)] q (n-1) ∧
    (((1 - (c * (q^(((n : ℤ)-1) : ℤ)))) * (1 - (t * (q^(((n : ℤ)-2) : ℤ))))) * (1 - (t * (q^(((n : ℤ)-1) : ℤ))))) ≠ 0 ∧
    phiDefined [c,((q^((1-((n : ℤ)-2)) : ℤ)) / t)] q (n-2)) :
 (((phi [a,b,(q^((-((n : ℤ))) : ℤ))] [c,((q^((1-((n : ℤ))) : ℤ)) / t)] q q (n)) + (((((((((((((-a) * b) * t) * (q^((2*(n : ℤ)) : ℤ))) + ((a * t) * (q^(((n : ℤ)+1) : ℤ)))) + ((b * t) * (q^(((n : ℤ)+1) : ℤ)))) - ((c * t) * (q^((2*(n : ℤ)) : ℤ)))) + (c * (q^(((n : ℤ)+1) : ℤ)))) + (q^(((n : ℤ)+2) : ℤ))) - (q^3)) - (q^2)) / (((q^2) * (1 - (c * (q^(((n : ℤ)-1) : ℤ))))) * (1 - (t * (q^(((n : ℤ)-1) : ℤ)))))) * (phi [a,b,(q^((-((n : ℤ)-1)) : ℤ))] [c,((q^((1-((n : ℤ)-1)) : ℤ)) / t)] q q (n-1)))) + (((((q * (1 - (q^(((n : ℤ)-1) : ℤ)))) * (1 - ((a * t) * (q^(((n : ℤ)-2) : ℤ))))) * (1 - ((b * t) * (q^(((n : ℤ)-2) : ℤ))))) / (((1 - (c * (q^(((n : ℤ)-1) : ℤ)))) * (1 - (t * (q^(((n : ℤ)-2) : ℤ))))) * (1 - (t * (q^(((n : ℤ)-1) : ℤ)))))) * (phi [a,b,(q^((-((n : ℤ)-2)) : ℤ))] [c,((q^((1-((n : ℤ)-2)) : ℤ)) / t)] q q (n-2)))) = 0 := by
  sorry

end FiniteQBenchmark.Identity365
