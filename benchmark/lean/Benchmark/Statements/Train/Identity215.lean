import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-11.Ex24ii — 底数 q² 的 12W11 到 10W9 变换
Original representative source: GR2-11.Ex24ii
Frozen statement: formulas/train/FQI-SRC-GR2-11.Ex24ii.md
Source formula:
W_{12}^{[\lfloor n/2\rfloor]}(a;a^2/\lambda^2,b,bq,c,cq,dq^n,dq^{n+1},q^{1-n},q^{-n};q^2,q^2)=\frac{(aq,d/\lambda,\lambda q/b,\lambda q/c;q)_n}{(\lambda q,d/a,aq/b,aq/c;q)_n}W_{10}^{[n]}(\lambda;a/\lambda,\mu,-\mu,b,c,dq^n,q^{-n};q,-q\lambda/a),\quad\lambda=bcd/(aq),\quad\mu^2=\lambda^2q/a.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity215
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d lam mu q : K) (n : ℕ)
 (hbase : regular q) (hl : lam = b*c*d/(a*q)) (hm : mu^2 = lam^2*q/a) (hnz : a*b*c*d ≠ 0)
 (h_domain : (lam^2) ≠ 0 ∧
    wDefined a [((a^2) / (lam^2)),b,(b * q),c,(c * q),(d * (q^(((n : ℤ)) : ℤ))),(d * (q^(((n : ℤ)+1) : ℤ))),(q^((1-(n : ℤ)) : ℤ)),(q^((-(n : ℤ)) : ℤ))] (q^2) (n/2) ∧
    lam ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    a ≠ 0 ∧
    (pochList [(lam * q),(d / a),((a * q) / b),((a * q) / c)] q (n)) ≠ 0 ∧
    wDefined lam [(a / lam),mu,(-mu),b,c,(d * (q^(((n : ℤ)) : ℤ))),(q^((-(n : ℤ)) : ℤ))] q (n)) :
 (wellPoisedRaw a [((a^2) / (lam^2)),b,(b * q),c,(c * q),(d * (q^(((n : ℤ)) : ℤ))),(d * (q^(((n : ℤ)+1) : ℤ))),(q^((1-(n : ℤ)) : ℤ)),(q^((-(n : ℤ)) : ℤ))] (q^2) (q^2) (n/2)) = (((pochList [(a * q),(d / lam),((lam * q) / b),((lam * q) / c)] q (n)) / (pochList [(lam * q),(d / a),((a * q) / b),((a * q) / c)] q (n))) * (wellPoisedRaw lam [(a / lam),mu,(-mu),b,c,(d * (q^(((n : ℤ)) : ℤ))),(q^((-(n : ℤ)) : ℤ))] q (((-q) * lam) / a) (n))) := by
  sorry

end FiniteQBenchmark.Identity215
