import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex8 — 任意有限权序列的 q-Racah 双线性变换
Original representative source: GR2-8.Ex8
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex8.md
Source formula:
\sum_{n=0}^z\frac{(aq,abq,bcq;q)_n(-c)^{-n}\lambda_nq^{\binom n2}}{(q,bq,aq/c;q)_n(abq;q)_{2n}}W_n(x;a,b,c,N)W_n(y;\alpha,ab/\alpha,\gamma,M)=\sum_{r=0}^z\sum_{s=0}^{z-r}\frac{(q^{-z};q)_{r+s}}{(q^{-N};q)_{r+s}}H_{r,s}A_{r,s}\mu_{r+s},\quad\lambda_n=\sum_{k=0}^{z-n}\frac{(q^{-z};q)_{n+k}\mu_{n+k}}{(q,abq^{2n+2};q)_k},\quad H_{r,s}=\frac{(q^{-x},cq^{x-N},q^{-y},\gamma q^{y-M};q)_r(q^{x-N},c^{-1}q^{-x};q)_s(1-cq^{r-s})q^{-rs}}{(q,\alpha q,q^{-M},ab\gamma q/\alpha,cq^{1-s};q)_r(q,bq,aq/c;q)_s(1-cq^{-s})},\quad A_{r,s}={}_5\phi_4^{[s]}(q^{-s},q^{r-y},\gamma q^{r+y-M},aq^{r+1},bcq^{r+1};\alpha q^{r+1},q^{r-M},ab\gamma q^{r+1}/\alpha,cq^{1+r-s};q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity182
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c alpha gamma q : K) (N M z x y : ℕ) (mu : ℕ → K)
 (hbase : regular q) (hzN : z ≤ N) (hNM : N ≤ M) (hx : x ≤ N) (hy : y ≤ M) (hnz : ∀ v ∈ [a,b,c,alpha,gamma], v ≠ 0)
 (h_domain : ∀ n ∈ Finset.range (z+1), (∀ k ∈ Finset.range (z-n+1), ((pochList [q,((a * b) * (q^((2*(n : ℤ)+2) : ℤ)))] q (k)) ≠ 0) ∧
    c ≠ 0 ∧
    ((pochList [q,(b * q),((a * q) / c)] q (n)) * (pochList [((a * b) * q)] q (2*n))) ≠ 0 ∧
    phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q (min (n) (x)) ∧
    alpha ≠ 0 ∧
    phiDefined [(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) / alpha) * gamma) * q)] q (min (n) (y))) ∧
    ∀ r ∈ Finset.range (min z (min x y)+1), (∀ s ∈ Finset.range (min (z-r) (N-x)+1), ((pochList [(q^((-(N : ℤ)) : ℤ))] q (r+s)) ≠ 0 ∧
    c ≠ 0 ∧
    alpha ≠ 0 ∧
    (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))) ≠ 0 ∧
    ((((pochList [(q^((-(z : ℤ)) : ℤ))] q (r+s)) / (pochList [(q^((-(N : ℤ)) : ℤ))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))))) * (mu (r+s))) ≠ 0 → (alpha ≠ 0) ∧
    ((((pochList [(q^((-(z : ℤ)) : ℤ))] q (r+s)) / (pochList [(q^((-(N : ℤ)) : ℤ))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))))) * (mu (r+s))) ≠ 0 → (phiDefined [(alpha * (q^((((r : ℤ))+1) : ℤ))),(q^((((r : ℤ))-((M : ℤ))) : ℤ)),((((a * b) * gamma) * (q^((((r : ℤ))+1) : ℤ))) / alpha),(c * (q^((1+((r : ℤ))-((s : ℤ))) : ℤ)))] q (s))))) :
 (∑ n ∈ Finset.range (z+1), (((((((pochList [(a * q),((a * b) * q),((b * c) * q)] q (n)) * ((-c)^((-(n : ℤ)) : ℤ))) * (∑ k ∈ Finset.range (z-n+1), (((pochList [(q^((-(z : ℤ)) : ℤ))] q (n+k)) * (mu (n+k))) / (pochList [q,((a * b) * (q^((2*(n : ℤ)+2) : ℤ)))] q (k))))) * (q^(((n : ℤ)*((n : ℤ)-1)/2) : ℤ))) / ((pochList [q,(b * q),((a * q) / c)] q (n)) * (pochList [((a * b) * q)] q (2*n)))) * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((x : ℤ))) : ℤ)),(c * (q^(((x : ℤ)-((N : ℤ))) : ℤ)))] [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q q (min (n) (x)))) * (phi [(q^((-((n : ℤ))) : ℤ)),((alpha * ((a * b) / alpha)) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^(((y : ℤ)-((M : ℤ))) : ℤ)))] [(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) / alpha) * gamma) * q)] q q (min (n) (y))))) = (∑ r ∈ Finset.range (min z (min x y)+1), (∑ s ∈ Finset.range (min (z-r) (N-x)+1), (if ((((pochList [(q^((-(z : ℤ)) : ℤ))] q (r+s)) / (pochList [(q^((-(N : ℤ)) : ℤ))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))))) * (mu (r+s))) = 0 then 0 else ((((pochList [(q^((-(z : ℤ)) : ℤ))] q (r+s)) / (pochList [(q^((-(N : ℤ)) : ℤ))] q (r+s))) * (((((pochList [(q^((-((x : ℤ))) : ℤ)),(c * (q^((((x : ℤ))-((N : ℤ))) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(gamma * (q^((((y : ℤ))-((M : ℤ))) : ℤ)))] q (r)) * (pochList [(q^((((x : ℤ))-((N : ℤ))) : ℤ)),((q^((-((x : ℤ))) : ℤ)) / c)] q (s))) * (1 - (c * (q^((((r : ℤ))-((s : ℤ))) : ℤ))))) * (q^((-((r : ℤ))*((s : ℤ))) : ℤ))) / (((pochList [q,(alpha * q),(q^((-((M : ℤ))) : ℤ)),((((a * b) * gamma) * q) / alpha),(c * (q^((1-((s : ℤ))) : ℤ)))] q (r)) * (pochList [q,(b * q),((a * q) / c)] q (s))) * (1 - (c * (q^((-((s : ℤ))) : ℤ))))))) * (mu (r+s)))*(phi [(q^((-((s : ℤ))) : ℤ)),(q^((((r : ℤ))-((y : ℤ))) : ℤ)),(gamma * (q^((((r : ℤ))+((y : ℤ))-((M : ℤ))) : ℤ))),(a * (q^((((r : ℤ))+1) : ℤ))),((b * c) * (q^((((r : ℤ))+1) : ℤ)))] [(alpha * (q^((((r : ℤ))+1) : ℤ))),(q^((((r : ℤ))-((M : ℤ))) : ℤ)),((((a * b) * gamma) * (q^((((r : ℤ))+1) : ℤ))) / alpha),(c * (q^((1+((r : ℤ))-((s : ℤ))) : ℤ)))] q q (s))))) := by
  sorry

end FiniteQBenchmark.Identity182
