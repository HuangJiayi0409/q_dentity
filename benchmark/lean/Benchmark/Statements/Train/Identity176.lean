import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex1i — 小 q-Jacobi 乘积的有限双和（一）
Original representative source: GR2-8.Ex1i
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex1i.md
Source formula:
\ell_n(x)\ell_n(y)=(-aq)^nq^{\binom n2}\frac{(bq;q)_n}{(aq;q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},x^{-1},y^{-1};q)_m}{(q,bq;q)_m}\left(\frac{xyq^{1-m}}a\right)^m\sum_{k=0}^m\frac{(q^{-m},b^{-1}q^{-m};q)_k(abxy)^kq^{k^2+2k}}{(q,aq,xq^{1-m},yq^{1-m};q)_k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity176
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x y a b q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [a,b,x,y], v ≠ 0)
 (h_domain : phiDefined [(a * q)] q (n) ∧
    (pochList [(a * q)] q (n)) ≠ 0 ∧
    ∀ m ∈ Finset.range (n+1), (x ≠ 0 ∧
    y ≠ 0 ∧
    (pochList [q,(b * q)] q (m)) ≠ 0 ∧
    a ≠ 0 ∧
    ∀ k ∈ Finset.range (m+1), (b ≠ 0 ∧
    (pochList [q,(a * q),(x * (q^((1-(m : ℤ)) : ℤ))),(y * (q^((1-(m : ℤ)) : ℤ)))] q (k)) ≠ 0))) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] [(a * q)] q (q * x) (n)) * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] [(a * q)] q (q * y) (n))) = (((((((-a) * q)^(((n : ℤ)) : ℤ)) * (q^(((n : ℤ)*((n : ℤ)-1)/2) : ℤ))) * (pochList [(b * q)] q (n))) / (pochList [(a * q)] q (n))) * (∑ m ∈ Finset.range (n+1), ((((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(1 / x),(1 / y)] q (m)) / (pochList [q,(b * q)] q (m))) * ((((x * y) * (q^((1-(m : ℤ)) : ℤ))) / a)^(((m : ℤ)) : ℤ))) * (∑ k ∈ Finset.range (m+1), ((((pochList [(q^((-(m : ℤ)) : ℤ)),((q^((-(m : ℤ)) : ℤ)) / b)] q (k)) * ((((a * b) * x) * y)^(((k : ℤ)) : ℤ))) * (q^(((k : ℤ)*(k : ℤ)+2*(k : ℤ)) : ℤ))) / (pochList [q,(a * q),(x * (q^((1-(m : ℤ)) : ℤ))),(y * (q^((1-(m : ℤ)) : ℤ)))] q (k))))))) := by
  sorry

end FiniteQBenchmark.Identity176
