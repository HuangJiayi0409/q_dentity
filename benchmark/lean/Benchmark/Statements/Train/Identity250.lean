import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-II-22 — Jackson 终止平衡 8φ7 求和
Original representative source: GR2-II-22
Frozen statement: formulas/train/FQI-SRC-GR2-II-22.md
Source formula:
W_8^{[n]}(a;b,c,d,e,q^{-n};q,q)=\frac{(aq,aq/(bc),aq/(bd),aq/(cd);q)_n}{(aq/b,aq/c,aq/d,aq/(bcd);q)_n}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity250
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d ee q : K) (n : ℕ)
 (hbase : regular q) (hnz : a*b*c*d*ee ≠ 0) (hbal : b*c*d*ee = a^2*q^((n:ℤ)+1))
 (h_domain : wDefined a [b,c,d,ee,(q^((-(n : ℤ)) : ℤ))] q (n) ∧
    (b * c) ≠ 0 ∧
    (b * d) ≠ 0 ∧
    (c * d) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    ((b * c) * d) ≠ 0 ∧
    (pochList [((a * q) / b),((a * q) / c),((a * q) / d),((a * q) / ((b * c) * d))] q (n)) ≠ 0) :
 (wellPoisedRaw a [b,c,d,ee,(q^((-(n : ℤ)) : ℤ))] q q (n)) = ((pochList [(a * q),((a * q) / (b * c)),((a * q) / (b * d)),((a * q) / (c * d))] q (n)) / (pochList [((a * q) / b),((a * q) / c),((a * q) / d),((a * q) / ((b * c) * d))] q (n))) := by
  sorry

end FiniteQBenchmark.Identity250
