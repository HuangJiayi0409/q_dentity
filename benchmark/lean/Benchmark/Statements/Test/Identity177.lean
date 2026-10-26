import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex1ii — 小 q-Jacobi 乘积的有限三重和
Original representative source: GR2-8.Ex1ii
Frozen statement: formulas/test/FQI-SRC-GR2-8.Ex1ii.md
Source formula:
\ell_n(x)\ell_n(y)=(-bq)^{-n}q^{-\binom n2}\frac{(bq;q)_n}{(aq;q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1};q)_m}{(q,bq;q)_m}(-byq^2)^mq^{\binom m2}\sum_{k=0}^m\frac{(q^{-m},abq^{m+1};q)_k(xq)^k}{(q,aq;q)_k}{}_2\phi_1^{[m-k]}(q^{k-m},bxq;0;q,(by)^{-1}).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity177
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x y a b q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [b,y], v ≠ 0)
 (h_domain : phiDefined [(a * q)] q (n) ∧
    (pochList [(a * q)] q (n)) ≠ 0 ∧
    ∀ m ∈ Finset.range (n+1), ((pochList [q,(b * q)] q (m)) ≠ 0 ∧
    ∀ k ∈ Finset.range (m+1), ((pochList [q,(a * q)] q (k)) ≠ 0 ∧
    (b * y) ≠ 0 ∧
    phiDefined [0] q (m-k)))) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] [(a * q)] q (q * x) (n)) * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] [(a * q)] q (q * y) (n))) = (((((((-b) * q)^((-(n : ℤ)) : ℤ)) * (q^((-(n : ℤ)*((n : ℤ)-1)/2) : ℤ))) * (pochList [(b * q)] q (n))) / (pochList [(a * q)] q (n))) * (∑ m ∈ Finset.range (n+1), (((((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] q (m)) / (pochList [q,(b * q)] q (m))) * (((((-b) * y) * q) * q)^(((m : ℤ)) : ℤ))) * (q^(((m : ℤ)*((m : ℤ)-1)/2) : ℤ))) * (∑ k ∈ Finset.range (m+1), ((((pochList [(q^((-(m : ℤ)) : ℤ)),((a * b) * (q^(((m : ℤ)+1) : ℤ)))] q (k)) * ((x * q)^(((k : ℤ)) : ℤ))) / (pochList [q,(a * q)] q (k))) * (phi [(q^(((k : ℤ)-(m : ℤ)) : ℤ)),((b * x) * q)] [0] q (1 / (b * y)) (m-k))))))) := by
  sorry

end FiniteQBenchmark.Identity177
