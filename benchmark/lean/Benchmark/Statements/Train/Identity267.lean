import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-26 — 终止近良配 5φ4 的半长度变换
Original representative source: GR2-III-26
Frozen statement: formulas/train/FQI-SRC-GR2-III-26.md
Source formula:
{}_5\phi_4^{[n]}\!\left[\begin{matrix}q^{-n},b,c,d,e\\q^{1-n}/b,q^{1-n}/c,q^{1-n}/d,eq^{-2n}/\mu^2\end{matrix};q,q\right]=\frac{(\mu^2q^{n+1},\mu q/e;q)_n}{(\mu^2q^{n+1}/e,\mu q;q)_n}\mathcal V_{\lfloor n/2\rfloor}(\mu;\mu bq^n,\mu cq^n,\mu dq^n;q^{-n},q^{1-n};e,\mu^2q^{n+1}/e),\quad\mu=q^{1-2n}/(bcd).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity267
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (b c d ee mu q : K) (n : ℕ)
 (hbase : regular q) (hm : mu = q^(1-2*(n:ℤ))/(b*c*d)) (hnz : b*c*d*ee*mu ≠ 0) (hm1 : mu ≠ 1)
 (h_domain : b ≠ 0 ∧
    c ≠ 0 ∧
    d ≠ 0 ∧
    (mu^2) ≠ 0 ∧
    phiDefined [((q^((1-(n : ℤ)) : ℤ)) / b),((q^((1-(n : ℤ)) : ℤ)) / c),((q^((1-(n : ℤ)) : ℤ)) / d),((ee * (q^((-2*(n : ℤ)) : ℤ))) / (mu^2))] q (n) ∧
    ee ≠ 0 ∧
    (pochList [(((mu^2) * (q^(((n : ℤ)+1) : ℤ))) / ee),(mu * q)] q (n)) ≠ 0 ∧
    ∀ k ∈ Finset.range (n/2+1), ((1 - mu) ≠ 0 ∧
    ee ≠ 0 ∧
    ((mu * b) * (q^(((n : ℤ)) : ℤ))) ≠ 0 ∧
    ((mu * c) * (q^(((n : ℤ)) : ℤ))) ≠ 0 ∧
    ((mu * d) * (q^(((n : ℤ)) : ℤ))) ≠ 0 ∧
    (((mu^2) * (q^(((n : ℤ)+1) : ℤ))) / ee) ≠ 0 ∧
    (pochList [q,((mu * q) / ((mu * b) * (q^(((n : ℤ)) : ℤ)))),((mu * q) / ((mu * c) * (q^(((n : ℤ)) : ℤ)))),((mu * q) / ((mu * d) * (q^(((n : ℤ)) : ℤ)))),((mu * q) / ee),((mu * q) / (((mu^2) * (q^(((n : ℤ)+1) : ℤ))) / ee))] q (k)) ≠ 0 ∧
    (q^((-(n : ℤ)) : ℤ)) ≠ 0 ∧
    (q^((1-(n : ℤ)) : ℤ)) ≠ 0 ∧
    (pochList [(((mu^2) * (q^2)) / (q^((-(n : ℤ)) : ℤ))),(((mu^2) * (q^2)) / (q^((1-(n : ℤ)) : ℤ)))] (q^2) (k)) ≠ 0)) :
 (phi [(q^((-(n : ℤ)) : ℤ)),b,c,d,ee] [((q^((1-(n : ℤ)) : ℤ)) / b),((q^((1-(n : ℤ)) : ℤ)) / c),((q^((1-(n : ℤ)) : ℤ)) / d),((ee * (q^((-2*(n : ℤ)) : ℤ))) / (mu^2))] q q (n)) = (((pochList [((mu^2) * (q^(((n : ℤ)+1) : ℤ))),((mu * q) / ee)] q (n)) / (pochList [(((mu^2) * (q^(((n : ℤ)+1) : ℤ))) / ee),(mu * q)] q (n))) * (∑ k ∈ Finset.range (n/2+1), (((((((1 - (mu * (q^((2*(k : ℤ)) : ℤ)))) / (1 - mu)) * (pochList [mu,((mu * b) * (q^(((n : ℤ)) : ℤ))),((mu * c) * (q^(((n : ℤ)) : ℤ))),((mu * d) * (q^(((n : ℤ)) : ℤ))),ee,(((mu^2) * (q^(((n : ℤ)+1) : ℤ))) / ee)] q (k))) / (pochList [q,((mu * q) / ((mu * b) * (q^(((n : ℤ)) : ℤ)))),((mu * q) / ((mu * c) * (q^(((n : ℤ)) : ℤ)))),((mu * q) / ((mu * d) * (q^(((n : ℤ)) : ℤ)))),((mu * q) / ee),((mu * q) / (((mu^2) * (q^(((n : ℤ)+1) : ℤ))) / ee))] q (k))) * (pochList [(q^((-(n : ℤ)) : ℤ)),(q^((1-(n : ℤ)) : ℤ))] (q^2) (k))) / (pochList [(((mu^2) * (q^2)) / (q^((-(n : ℤ)) : ℤ))),(((mu^2) * (q^2)) / (q^((1-(n : ℤ)) : ℤ)))] (q^2) (k))) * (q^(((k : ℤ)) : ℤ))))) := by
  sorry

end FiniteQBenchmark.Identity267
