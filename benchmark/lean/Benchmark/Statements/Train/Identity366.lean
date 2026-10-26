import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-1.99 — Watson 终止和二阶递推
Original representative source: SILLS-1.99
Frozen statement: formulas/train/FQI-SRC-SILLS-1.99.md
Source formula:
f_n=\frac{(aq^n-1)(q^n-q)(aq^n-q)(bcde-a^2q^n)}{q(b-aq^n)(c-aq^n)(d-aq^n)(e-aq^n)}f_{n-2}+\frac{aq^n-1}{q(b-aq^n)(c-aq^n)(d-aq^n)(e-aq^n)}\bigl[a^3(q+1)q^{3n}+q^{n+1}(a^2q+a(bec+bed+bcd+cde)+bcde)-aq^{2n}(aq(a+b+c+d+e)+bcde)-bcde(q+1)q\bigr]f_{n-1}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity366
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d ee q : K) (n : ℕ)
 (hn : 2 ≤ n) (hq : q ≠ 0)
 (h_domain : (((b * c) * d) * ee) ≠ 0 ∧
    wDefined a [b,c,d,ee,(q^((-((n : ℤ))) : ℤ))] q (n) ∧
    ((((q * (b - (a * (q^(((n : ℤ)) : ℤ))))) * (c - (a * (q^(((n : ℤ)) : ℤ))))) * (d - (a * (q^(((n : ℤ)) : ℤ))))) * (ee - (a * (q^(((n : ℤ)) : ℤ))))) ≠ 0 ∧
    wDefined a [b,c,d,ee,(q^((-((n : ℤ)-2)) : ℤ))] q (n-2) ∧
    wDefined a [b,c,d,ee,(q^((-((n : ℤ)-1)) : ℤ))] q (n-1)) :
 (wellPoisedRaw a [b,c,d,ee,(q^((-((n : ℤ))) : ℤ))] q (((a^2) * (q^(((n : ℤ)+2) : ℤ))) / (((b * c) * d) * ee)) (n)) = ((((((((a * (q^(((n : ℤ)) : ℤ))) - 1) * ((q^(((n : ℤ)) : ℤ)) - q)) * ((a * (q^(((n : ℤ)) : ℤ))) - q)) * ((((b * c) * d) * ee) - ((a^2) * (q^(((n : ℤ)) : ℤ))))) / ((((q * (b - (a * (q^(((n : ℤ)) : ℤ))))) * (c - (a * (q^(((n : ℤ)) : ℤ))))) * (d - (a * (q^(((n : ℤ)) : ℤ))))) * (ee - (a * (q^(((n : ℤ)) : ℤ)))))) * (wellPoisedRaw a [b,c,d,ee,(q^((-((n : ℤ)-2)) : ℤ))] q (((a^2) * (q^(((n : ℤ)-2+2) : ℤ))) / (((b * c) * d) * ee)) (n-2))) + (((((a * (q^(((n : ℤ)) : ℤ))) - 1) / ((((q * (b - (a * (q^(((n : ℤ)) : ℤ))))) * (c - (a * (q^(((n : ℤ)) : ℤ))))) * (d - (a * (q^(((n : ℤ)) : ℤ))))) * (ee - (a * (q^(((n : ℤ)) : ℤ)))))) * ((((((a^3) * (q + 1)) * (q^((3*(n : ℤ)) : ℤ))) + ((q^(((n : ℤ)+1) : ℤ)) * ((((a^2) * q) + (a * (((((b * ee) * c) + ((b * ee) * d)) + ((b * c) * d)) + ((c * d) * ee)))) + (((b * c) * d) * ee)))) - ((a * (q^((2*(n : ℤ)) : ℤ))) * (((a * q) * ((((a + b) + c) + d) + ee)) + (((b * c) * d) * ee)))) - (((((b * c) * d) * ee) * (q + 1)) * q))) * (wellPoisedRaw a [b,c,d,ee,(q^((-((n : ℤ)-1)) : ℤ))] q (((a^2) * (q^(((n : ℤ)-1+2) : ℤ))) / (((b * c) * d) * ee)) (n-1)))) := by
  sorry

end FiniteQBenchmark.Identity366
