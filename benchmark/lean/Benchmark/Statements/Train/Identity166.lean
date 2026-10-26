import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.7.4 — q-Racah乘积双重展开修正式
Original representative source: GR2-8.7.4
Frozen statement: formulas/train/FQI-SRC-GR2-8.7.4.md
Source formula:
W_n(x;a,b,c,N)W_n(y;\alpha,ab/\alpha,\gamma,M)=\frac{(bq,aq/c;q)_nc^n}{(aq,bcq;q)_n}\sum_{r=0}^n\sum_{s=0}^{n-r}\frac{(q^{-n},abq^{n+1};q)_{r+s}(q^{-x},cq^{x-N},q^{-y},\gamma q^{y-M};q)_r}{(q^{-N};q)_{r+s}(q,\alpha q,q^{-M},ab\gamma q/\alpha,cq^{1-s};q)_r}\frac{(q^{x-N},c^{-1}q^{-x};q)_s(1-cq^{r-s})q^{r+s-rs}}{(q,bq,aq/c;q)_s(1-cq^{-s})}A_{r,s}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity166
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c alpha gamma q : K) (N M n x y : ℕ)
 (hbase : regular q) (hn : n ≤ N) (hNM : N ≤ M) (hx : x ≤ N) (hy : y ≤ M) (hnz : ∀ v ∈ [a,b,c,alpha,gamma], v ≠ 0)
 (h_domain : phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q (min (n) (x)) ∧
    alpha ≠ 0 ∧
    phiDefined [(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) / alpha) * gamma) * q)] q (min (n) (y)) ∧
    c ≠ 0 ∧
    (pochList [(a * q),((b * c) * q)] q (n)) ≠ 0 ∧
    ∀ r ∈ Finset.range (min n (min x y)+1), (∀ s ∈ Finset.range (min (n-r) (N-x)+1), ((pochList [(q^((-(N : ℤ)) : ℤ))] q (r+s)) ≠ 0 ∧
    c ≠ 0 ∧
    alpha ≠ 0 ∧
    (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))) ≠ 0 ∧
    ((((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] q (r+s)) / (pochList [(q^((-(N : ℤ)) : ℤ))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))))) * (q^(((r : ℤ)+(s : ℤ)) : ℤ))) ≠ 0 → (alpha ≠ 0) ∧
    ((((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] q (r+s)) / (pochList [(q^((-(N : ℤ)) : ℤ))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))))) * (q^(((r : ℤ)+(s : ℤ)) : ℤ))) ≠ 0 → (phiDefined [(alpha * (q^((((r : ℤ))+1) : ℤ))),(q^((((r : ℤ))-((M : ℤ))) : ℤ)),((((a * b) * gamma) * (q^((((r : ℤ))+1) : ℤ))) / alpha),(c * (q^((1+((r : ℤ))-((s : ℤ))) : ℤ)))] q (s))))) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((x : ℤ))) : ℤ)),(c * (q^(((x : ℤ)-((N : ℤ))) : ℤ)))] [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q q (min (n) (x))) * (phi [(q^((-((n : ℤ))) : ℤ)),((alpha * ((a * b) / alpha)) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^(((y : ℤ)-((M : ℤ))) : ℤ)))] [(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) / alpha) * gamma) * q)] q q (min (n) (y)))) = ((((pochList [(b * q),((a * q) / c)] q (n)) * (c^(((n : ℤ)) : ℤ))) / (pochList [(a * q),((b * c) * q)] q (n))) * (∑ r ∈ Finset.range (min n (min x y)+1), (∑ s ∈ Finset.range (min (n-r) (N-x)+1), (if ((((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] q (r+s)) / (pochList [(q^((-(N : ℤ)) : ℤ))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))))) * (q^(((r : ℤ)+(s : ℤ)) : ℤ))) = 0 then 0 else ((((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ)))] q (r+s)) / (pochList [(q^((-(N : ℤ)) : ℤ))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))))) * (q^(((r : ℤ)+(s : ℤ)) : ℤ)))*(phi [(q^((-((s : ℤ))) : ℤ)),(q^((((r : ℤ))-((y : ℤ))) : ℤ)),(gamma * (q^((((r : ℤ))+((y : ℤ))-((M : ℤ))) : ℤ))),(a * (q^((((r : ℤ))+1) : ℤ))),((b * c) * (q^((((r : ℤ))+1) : ℤ)))] [(alpha * (q^((((r : ℤ))+1) : ℤ))),(q^((((r : ℤ))-((M : ℤ))) : ℤ)),((((a * b) * gamma) * (q^((((r : ℤ))+1) : ℤ))) / alpha),(c * (q^((1+((r : ℤ))-((s : ℤ))) : ℤ)))] q q (s)))))) := by
  sorry

end FiniteQBenchmark.Identity166
