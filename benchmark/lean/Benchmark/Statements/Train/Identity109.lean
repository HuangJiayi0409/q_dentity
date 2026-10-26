import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.Ex4-transform — 终止 4φ3(q²) 到 4φ2(q)
Original representative source: GR2-3.Ex4-transform
Frozen statement: formulas/train/FQI-SRC-GR2-3.Ex4-transform.md
Source formula:
{}_4\phi_3^{[\lfloor n/2\rfloor]}(q^{-n},q^{1-n},a,aq;qb^2,d,dq;q^2,q^2)=\frac{(d/a;q)_n}{(d;q)_n}a^n{}_4\phi_2^{[n]}(q^{-n},a,b,-b;b^2,aq^{1-n}/d;q,-q/d).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity109
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b d q : K) (n : ℕ)
 (hbase : regular q) (ha : a ≠ 0) (hd : d ≠ 0)
 (h_domain : phiDefined [((q * b) * b),d,(d * q)] (q * q) (n/2) ∧
    a ≠ 0 ∧
    (pochList [d] q (n)) ≠ 0 ∧
    d ≠ 0 ∧
    phiDefined [(b * b),((a * (q^((1-(n : ℤ)) : ℤ))) / d)] q (n)) :
 (phi [(q^((-(n : ℤ)) : ℤ)),(q^((1-(n : ℤ)) : ℤ)),a,(a * q)] [((q * b) * b),d,(d * q)] (q * q) (q * q) (n/2)) = ((((pochList [(d / a)] q (n)) / (pochList [d] q (n))) * (a^n)) * (phi [(q^((-(n : ℤ)) : ℤ)),a,b,(-b)] [(b * b),((a * (q^((1-(n : ℤ)) : ℤ))) / d)] q ((-q) / d) (n))) := by
  sorry

end FiniteQBenchmark.Identity109
