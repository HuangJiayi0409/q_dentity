import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.3.6 — 小 q-Jacobi 三项递推
Original representative source: GR2-7.3.6
Frozen statement: formulas/test/FQI-SRC-GR2-7.3.6.md
Source formula:
x\ell_n(x)=A_n(\ell_{n+1}(x)-\ell_n(x))-C_n(\ell_n(x)-\ell_{n-1}(x)),\quad A_n=-\frac{q^n(1-abq^{n+1})(1-aq^{n+1})}{(1-abq^{2n+1})(1-abq^{2n+2})},\quad C_n=-\frac{aq^n(1-q^n)(1-bq^n)}{(1-abq^{2n})(1-abq^{2n+1})}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity131
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x a b q : K) (n : ℕ)
 (hbase : regular q) 
 (h_domain : phiDefined [(a * q)] q (n) ∧
    ((1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ)))) * (1 - ((a * b) * (q^((2*(n : ℤ)+2) : ℤ))))) ≠ 0 ∧
    ((((-(q^(((n : ℤ)) : ℤ))) * (1 - ((a * b) * (q^(((n : ℤ)+1) : ℤ))))) * (1 - (a * (q^(((n : ℤ)+1) : ℤ))))) / ((1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ)))) * (1 - ((a * b) * (q^((2*(n : ℤ)+2) : ℤ)))))) ≠ 0 → (phiDefined [(a * q)] q (n+1)) ∧
    ((((-(q^(((n : ℤ)) : ℤ))) * (1 - ((a * b) * (q^(((n : ℤ)+1) : ℤ))))) * (1 - (a * (q^(((n : ℤ)+1) : ℤ))))) / ((1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ)))) * (1 - ((a * b) * (q^((2*(n : ℤ)+2) : ℤ)))))) ≠ 0 → (phiDefined [(a * q)] q (n)) ∧
    ((1 - ((a * b) * (q^((2*(n : ℤ)) : ℤ)))) * (1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ))))) ≠ 0 ∧
    (((((-a) * (q^(((n : ℤ)) : ℤ))) * (1 - (q^(((n : ℤ)) : ℤ)))) * (1 - (b * (q^(((n : ℤ)) : ℤ))))) / ((1 - ((a * b) * (q^((2*(n : ℤ)) : ℤ)))) * (1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ)))))) ≠ 0 → (phiDefined [(a * q)] q (n)) ∧
    (((((-a) * (q^(((n : ℤ)) : ℤ))) * (1 - (q^(((n : ℤ)) : ℤ)))) * (1 - (b * (q^(((n : ℤ)) : ℤ))))) / ((1 - ((a * b) * (q^((2*(n : ℤ)) : ℤ)))) * (1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ)))))) ≠ 0 → (¬ (n = 0) → (phiDefined [(a * q)] q (n-1)))) :
 (x * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] [(a * q)] q (q * x) (n))) = ((if ((((-(q^(((n : ℤ)) : ℤ))) * (1 - ((a * b) * (q^(((n : ℤ)+1) : ℤ))))) * (1 - (a * (q^(((n : ℤ)+1) : ℤ))))) / ((1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ)))) * (1 - ((a * b) * (q^((2*(n : ℤ)+2) : ℤ)))))) = 0 then 0 else ((((-(q^(((n : ℤ)) : ℤ))) * (1 - ((a * b) * (q^(((n : ℤ)+1) : ℤ))))) * (1 - (a * (q^(((n : ℤ)+1) : ℤ))))) / ((1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ)))) * (1 - ((a * b) * (q^((2*(n : ℤ)+2) : ℤ))))))*((phi [(q^((-((n : ℤ)+1)) : ℤ)),((a * b) * (q^(((n : ℤ)+1+1) : ℤ)))] [(a * q)] q (q * x) (n+1)) - (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] [(a * q)] q (q * x) (n)))) - (if (((((-a) * (q^(((n : ℤ)) : ℤ))) * (1 - (q^(((n : ℤ)) : ℤ)))) * (1 - (b * (q^(((n : ℤ)) : ℤ))))) / ((1 - ((a * b) * (q^((2*(n : ℤ)) : ℤ)))) * (1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ)))))) = 0 then 0 else (((((-a) * (q^(((n : ℤ)) : ℤ))) * (1 - (q^(((n : ℤ)) : ℤ)))) * (1 - (b * (q^(((n : ℤ)) : ℤ))))) / ((1 - ((a * b) * (q^((2*(n : ℤ)) : ℤ)))) * (1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ))))))*((phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] [(a * q)] q (q * x) (n)) - (if n = 0 then 0 else (phi [(q^((-((n : ℤ)-1)) : ℤ)),((a * b) * (q^(((n : ℤ)-1+1) : ℤ)))] [(a * q)] q (q * x) (n-1)))))) := by
  sorry

end FiniteQBenchmark.Identity131
