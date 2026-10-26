import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex9 — q-Racah 有限双线性求值
Original representative source: GR2-8.Ex9
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex9.md
Source formula:
\sum_{n=0}^z\frac{1-abq^{2n+1}}{1-abq}\frac{(abq,aq,d,e,bcq,q^{-z};q)_n}{(q,bq,abq^2/d,abq^2/e,aq/c,abq^{z+2};q)_n}\left(\frac{abq^{z+2}}{cde}\right)^nW_n(x;a,b,c,N)W_n(y;\alpha,ab/\alpha,\gamma,M)=\frac{(abq^2,abq^2/(de);q)_z}{(abq^2/d,abq^2/e;q)_z}\sum_{r=0}^z\sum_{s=0}^{z-r}\frac{(q^{-z},d,e;q)_{r+s}q^{r+s}}{(q^{-N},deq^{-z-1}/(ab);q)_{r+s}}H_{r,s}A_{r,s}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity185
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d ee alpha gamma q : K) (N M z x y : ℕ)
 (hbase : regular q) (hzN : z ≤ N) (hNM : N ≤ M) (hx : x ≤ N) (hy : y ≤ M) (hnz : ∀ v ∈ [a,b,c,d,ee,alpha,gamma], v ≠ 0)
 (h_domain : ∀ n ∈ Finset.range (z+1), ((1 - ((a * b) * q)) ≠ 0 ∧
    d ≠ 0 ∧
    ee ≠ 0 ∧
    c ≠ 0 ∧
    (pochList [q,(b * q),((((a * b) * q) * q) / d),((((a * b) * q) * q) / ee),((a * q) / c),((a * b) * (q^(((z : ℤ)+2) : ℤ)))] q (n)) ≠ 0 ∧
    ((c * d) * ee) ≠ 0 ∧
    phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q (min (n) (x)) ∧
    alpha ≠ 0 ∧
    phiDefined [(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) / alpha) * gamma) * q)] q (min (n) (y))) ∧
    (d * ee) ≠ 0 ∧
    d ≠ 0 ∧
    ee ≠ 0 ∧
    (pochList [((((a * b) * q) * q) / d),((((a * b) * q) * q) / ee)] q (z)) ≠ 0 ∧
    ∀ r ∈ Finset.range (min z (min x y)+1), (∀ s ∈ Finset.range (min (z-r) (N-x)+1), ((a * b) ≠ 0 ∧
    (pochList [(q^((-(N : ℤ)) : ℤ)),(((d * ee) * (q^((-(z : ℤ)-1) : ℤ))) / (a * b))] q (r+s)) ≠ 0 ∧
    c ≠ 0 ∧
    alpha ≠ 0 ∧
    (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))) ≠ 0 ∧
    ((((pochList [(q^((-(z : ℤ)) : ℤ)),d,ee] q (r+s)) * (q^(((r : ℤ)+(s : ℤ)) : ℤ))) / (pochList [(q^((-(N : ℤ)) : ℤ)),(((d * ee) * (q^((-(z : ℤ)-1) : ℤ))) / (a * b))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))))) ≠ 0 → (alpha ≠ 0) ∧
    ((((pochList [(q^((-(z : ℤ)) : ℤ)),d,ee] q (r+s)) * (q^(((r : ℤ)+(s : ℤ)) : ℤ))) / (pochList [(q^((-(N : ℤ)) : ℤ)),(((d * ee) * (q^((-(z : ℤ)-1) : ℤ))) / (a * b))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))))) ≠ 0 → (phiDefined [(alpha * (q^((((r : ℤ))+1) : ℤ))),(q^((((r : ℤ))-((M : ℤ))) : ℤ)),((((a * b) * gamma) * (q^((((r : ℤ))+1) : ℤ))) / alpha),(c * (q^((1+((r : ℤ))-((s : ℤ))) : ℤ)))] q (s))))) :
 (∑ n ∈ Finset.range (z+1), (((((((1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ)))) / (1 - ((a * b) * q))) * (pochList [((a * b) * q),(a * q),d,ee,((b * c) * q),(q^((-(z : ℤ)) : ℤ))] q (n))) / (pochList [q,(b * q),((((a * b) * q) * q) / d),((((a * b) * q) * q) / ee),((a * q) / c),((a * b) * (q^(((z : ℤ)+2) : ℤ)))] q (n))) * ((((a * b) * (q^(((z : ℤ)+2) : ℤ))) / ((c * d) * ee))^(((n : ℤ)) : ℤ))) * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((x : ℤ))) : ℤ)),(c * (q^(((x : ℤ)-((N : ℤ))) : ℤ)))] [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q q (min (n) (x)))) * (phi [(q^((-((n : ℤ))) : ℤ)),((alpha * ((a * b) / alpha)) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^(((y : ℤ)-((M : ℤ))) : ℤ)))] [(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) / alpha) * gamma) * q)] q q (min (n) (y))))) = (((pochList [(((a * b) * q) * q),((((a * b) * q) * q) / (d * ee))] q (z)) / (pochList [((((a * b) * q) * q) / d),((((a * b) * q) * q) / ee)] q (z))) * (∑ r ∈ Finset.range (min z (min x y)+1), (∑ s ∈ Finset.range (min (z-r) (N-x)+1), (if ((((pochList [(q^((-(z : ℤ)) : ℤ)),d,ee] q (r+s)) * (q^(((r : ℤ)+(s : ℤ)) : ℤ))) / (pochList [(q^((-(N : ℤ)) : ℤ)),(((d * ee) * (q^((-(z : ℤ)-1) : ℤ))) / (a * b))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))))) = 0 then 0 else ((((pochList [(q^((-(z : ℤ)) : ℤ)),d,ee] q (r+s)) * (q^(((r : ℤ)+(s : ℤ)) : ℤ))) / (pochList [(q^((-(N : ℤ)) : ℤ)),(((d * ee) * (q^((-(z : ℤ)-1) : ℤ))) / (a * b))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ)))))))*(phi [(q^((-((s : ℤ))) : ℤ)),(q^((((r : ℤ))-((y : ℤ))) : ℤ)),(gamma * (q^((((r : ℤ))+((y : ℤ))-((M : ℤ))) : ℤ))),(a * (q^((((r : ℤ))+1) : ℤ))),((b * c) * (q^((((r : ℤ))+1) : ℤ)))] [(alpha * (q^((((r : ℤ))+1) : ℤ))),(q^((((r : ℤ))-((M : ℤ))) : ℤ)),((((a * b) * gamma) * (q^((((r : ℤ))+1) : ℤ))) / alpha),(c * (q^((1+((r : ℤ))-((s : ℤ))) : ℤ)))] q q (s)))))) := by
  sorry

end FiniteQBenchmark.Identity185
