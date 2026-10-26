import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex2 — 大 q-Jacobi 的有限乘积公式
Original representative source: GR2-8.Ex2
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex2.md
Source formula:
J_n(x)J_n(y)=(-aq)^nq^{\binom n2}\frac{(bq;q)_n}{(aq;q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},cq/x,cq/y;q)_m}{(q,bq,cq,cq;q)_m}(xy/a)^m{}_4\phi_3^{[m]}(q^{-m},b^{-1}q^{-m},x,y;aq,xq^{-m}/c,yq^{-m}/c;q,abq/c^2).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity178
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x y a b c q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [a,b,c,x,y], v ≠ 0)
 (h_domain : phiDefined [(a * q),(c * q)] q (n) ∧
    (pochList [(a * q)] q (n)) ≠ 0 ∧
    ∀ m ∈ Finset.range (n+1), (x ≠ 0 ∧
    y ≠ 0 ∧
    (pochList [q,(b * q),(c * q),(c * q)] q (m)) ≠ 0 ∧
    a ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    (c * c) ≠ 0 ∧
    phiDefined [(a * q),((x * (q^((-(m : ℤ)) : ℤ))) / c),((y * (q^((-(m : ℤ)) : ℤ))) / c)] q (m))) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),x] [(a * q),(c * q)] q q (n)) * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),y] [(a * q),(c * q)] q q (n))) = (((((((-a) * q)^(((n : ℤ)) : ℤ)) * (q^(((n : ℤ)*((n : ℤ)-1)/2) : ℤ))) * (pochList [(b * q)] q (n))) / (pochList [(a * q)] q (n))) * (∑ m ∈ Finset.range (n+1), ((((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),((c * q) / x),((c * q) / y)] q (m)) / (pochList [q,(b * q),(c * q),(c * q)] q (m))) * (((x * y) / a)^(((m : ℤ)) : ℤ))) * (phi [(q^((-(m : ℤ)) : ℤ)),((q^((-(m : ℤ)) : ℤ)) / b),x,y] [(a * q),((x * (q^((-(m : ℤ)) : ℤ))) / c),((y * (q^((-(m : ℤ)) : ℤ))) / c)] q (((a * b) * q) / (c * c)) (m))))) := by
  sorry

end FiniteQBenchmark.Identity178
