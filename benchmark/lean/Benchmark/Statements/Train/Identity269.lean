import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-III-28 — Bailey 终止 10φ9 变换
Original representative source: GR2-III-28
Frozen statement: formulas/train/FQI-SRC-GR2-III-28.md
Source formula:
W_{10}^{[n]}(a;b,c,d,e,f,\lambda aq^{n+1}/(ef),q^{-n};q,q)=\frac{(aq,aq/(ef),\lambda q/e,\lambda q/f;q)_n}{(aq/e,aq/f,\lambda q/(ef),\lambda q;q)_n}W_{10}^{[n]}(\lambda;\lambda b/a,\lambda c/a,\lambda d/a,e,f,\lambda aq^{n+1}/(ef),q^{-n};q,q),\quad\lambda=qa^2/(bcd).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity269
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d ee f lam q : K) (n : ℕ)
 (hbase : regular q) (hl : lam = q*a^2/(b*c*d)) (hnz : a*b*c*d*ee*f*lam ≠ 0) (ha1 : a ≠ 1) (hl1 : lam ≠ 1)
 (h_domain : (ee * f) ≠ 0 ∧
    wDefined a [b,c,d,ee,f,(((lam * a) * (q^(((n : ℤ)+1) : ℤ))) / (ee * f)),(q^((-(n : ℤ)) : ℤ))] q (n) ∧
    ee ≠ 0 ∧
    f ≠ 0 ∧
    (pochList [((a * q) / ee),((a * q) / f),((lam * q) / (ee * f)),(lam * q)] q (n)) ≠ 0 ∧
    a ≠ 0 ∧
    wDefined lam [((lam * b) / a),((lam * c) / a),((lam * d) / a),ee,f,(((lam * a) * (q^(((n : ℤ)+1) : ℤ))) / (ee * f)),(q^((-(n : ℤ)) : ℤ))] q (n)) :
 (wellPoisedRaw a [b,c,d,ee,f,(((lam * a) * (q^(((n : ℤ)+1) : ℤ))) / (ee * f)),(q^((-(n : ℤ)) : ℤ))] q q (n)) = (((pochList [(a * q),((a * q) / (ee * f)),((lam * q) / ee),((lam * q) / f)] q (n)) / (pochList [((a * q) / ee),((a * q) / f),((lam * q) / (ee * f)),(lam * q)] q (n))) * (wellPoisedRaw lam [((lam * b) / a),((lam * c) / a),((lam * d) / a),ee,f,(((lam * a) * (q^(((n : ℤ)+1) : ℤ))) / (ee * f)),(q^((-(n : ℤ)) : ℤ))] q q (n))) := by
  sorry

end FiniteQBenchmark.Identity269
