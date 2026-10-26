import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.2.12 — q-Racah 一阶差分
Original representative source: GR2-7.2.12
Frozen statement: formulas/train/FQI-SRC-GR2-7.2.12.md
Source formula:
R_n(t)-R_{n-1}(t)=-\frac{q^{1-n}(1-abq^{2n})(1-t)(1-cdq/t)}{(1-aq)(1-cq)(1-bdq)}{}_4\phi_3^{[n-1]}(q^{1-n},abq^{n+1},qt,cdq^2/t;aq^2,cq^2,bdq^2;q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity127
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (t a b c d q : K) (n : ℕ)
 (hbase : regular q) (hn : 1 ≤ n) (hnz : ∀ v ∈ [t,c,d], v ≠ 0)
 (h_domain : t ≠ 0 ∧
    phiDefined [(a * q),(c * q),((b * d) * q)] q (n) ∧
    phiDefined [(a * q),(c * q),((b * d) * q)] q (n-1) ∧
    (((1 - (a * q)) * (1 - (c * q))) * (1 - ((b * d) * q))) ≠ 0 ∧
    phiDefined [((a * q) * q),((c * q) * q),(((b * d) * q) * q)] q (n-1)) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),t,(((c * d) * q) / t)] [(a * q),(c * q),((b * d) * q)] q q (n)) - (phi [(q^((-((n : ℤ)-1)) : ℤ)),((a * b) * (q^(((n : ℤ)-1+1) : ℤ))),t,(((c * d) * q) / t)] [(a * q),(c * q),((b * d) * q)] q q (n-1))) = ((((((-(q^((1-(n : ℤ)) : ℤ))) * (1 - ((a * b) * (q^((2*(n : ℤ)) : ℤ))))) * (1 - t)) * (1 - (((c * d) * q) / t))) / (((1 - (a * q)) * (1 - (c * q))) * (1 - ((b * d) * q)))) * (phi [(q^((1-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q * t),((((c * d) * q) * q) / t)] [((a * q) * q),((c * q) * q),(((b * d) * q) * q)] q q (n-1))) := by
  sorry

end FiniteQBenchmark.Identity127
