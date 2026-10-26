import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex7i — q-Hahn 有限离散双线性核
Original representative source: GR2-8.Ex7i
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex7i.md
Source formula:
\sum_{n=0}^z\frac{(abq,aq,q^{-z};q)_n(1-abq^{2n+1})(-aq)^{-n}q^{Nn-\binom n2}}{(q,bq,abq^{N+2};q)_n(1-abq)}Q_n(x;a,b,N)Q_n(y;a,b,M)=\sum_{r=0}^z\sum_{s=0}^{z-r}\frac{(q^{-z};q)_{r+s}(abq^2;q)_{2r+2s}(q^{-x},q^{-y};q)_r(q^{x-N},q^{y-M};q)_s(q^{N-z};q)_{z-r-s}(-1)^{r+s}a^{-s}q^{(r+s)(2N-r-s+1)/2-(x+y+1)s}}{(q^{-M},q^{-N},abq^{N+2};q)_{r+s}(q,aq;q)_r(q,bq;q)_s(abq^{N+r+s+2};q)_{z-r-s}}{}_2\phi_1^{[\max(0,z-r-s-1)]}(q^{r+s-z},q^{1+r+s-z};q^{1+N-z};q,abq^{N+z+2}).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity181
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (N M z x y : ℕ)
 (hbase : regular q) (hzN : z ≤ N) (hNM : N ≤ M) (hx : x ≤ N) (hy : y ≤ M) (ha : a ≠ 0)
 (h_domain : ∀ n ∈ Finset.range (z+1), (((pochList [q,(b * q),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (n)) * (1 - ((a * b) * q))) ≠ 0 ∧
    phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ))] q (min (n) (x)) ∧
    phiDefined [(a * q),(q^((-((M : ℤ))) : ℤ))] q (min (n) (y))) ∧
    ∀ r ∈ Finset.range (min z (min x y)+1), (∀ s ∈ Finset.range (min (z-r) (min (N-x) (M-y))+1), (((((pochList [(q^((-(M : ℤ)) : ℤ)),(q^((-(N : ℤ)) : ℤ)),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (r+s)) * (pochList [q,(a * q)] q (r))) * (pochList [q,(b * q)] q (s))) * (pochList [((a * b) * (q^(((N : ℤ)+(r : ℤ)+(s : ℤ)+2) : ℤ)))] q (z-r-s))) ≠ 0 ∧
    (((((((((pochList [(q^((-(z : ℤ)) : ℤ))] q (r+s)) * (pochList [(((a * b) * q) * q)] q (2*r+2*s))) * (pochList [(q^((-(x : ℤ)) : ℤ)),(q^((-(y : ℤ)) : ℤ))] q (r))) * (pochList [(q^(((x : ℤ)-(N : ℤ)) : ℤ)),(q^(((y : ℤ)-(M : ℤ)) : ℤ))] q (s))) * (pochList [(q^(((N : ℤ)-(z : ℤ)) : ℤ))] q (z-r-s))) * ((-1:K)^(((r : ℤ)+(s : ℤ)) : ℤ))) * (a^((-(s : ℤ)) : ℤ))) * (q^((((r : ℤ)+(s : ℤ))*(2*(N : ℤ)-(r : ℤ)-(s : ℤ)+1)/2-((x : ℤ)+(y : ℤ)+1)*(s : ℤ)) : ℤ))) / ((((pochList [(q^((-(M : ℤ)) : ℤ)),(q^((-(N : ℤ)) : ℤ)),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (r+s)) * (pochList [q,(a * q)] q (r))) * (pochList [q,(b * q)] q (s))) * (pochList [((a * b) * (q^(((N : ℤ)+(r : ℤ)+(s : ℤ)+2) : ℤ)))] q (z-r-s)))) ≠ 0 → (phiDefined [(q^((1+(N : ℤ)-(z : ℤ)) : ℤ))] q (z-r-s-1))))) :
 (∑ n ∈ Finset.range (z+1), (((((((pochList [((a * b) * q),(a * q),(q^((-(z : ℤ)) : ℤ))] q (n)) * (1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ))))) * (((-a) * q)^((-(n : ℤ)) : ℤ))) * (q^(((N : ℤ)*(n : ℤ)-(n : ℤ)*((n : ℤ)-1)/2) : ℤ))) / ((pochList [q,(b * q),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (n)) * (1 - ((a * b) * q)))) * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((x : ℤ))) : ℤ))] [(a * q),(q^((-((N : ℤ))) : ℤ))] q q (min (n) (x)))) * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((y : ℤ))) : ℤ))] [(a * q),(q^((-((M : ℤ))) : ℤ))] q q (min (n) (y))))) = (∑ r ∈ Finset.range (min z (min x y)+1), (∑ s ∈ Finset.range (min (z-r) (min (N-x) (M-y))+1), (if (((((((((pochList [(q^((-(z : ℤ)) : ℤ))] q (r+s)) * (pochList [(((a * b) * q) * q)] q (2*r+2*s))) * (pochList [(q^((-(x : ℤ)) : ℤ)),(q^((-(y : ℤ)) : ℤ))] q (r))) * (pochList [(q^(((x : ℤ)-(N : ℤ)) : ℤ)),(q^(((y : ℤ)-(M : ℤ)) : ℤ))] q (s))) * (pochList [(q^(((N : ℤ)-(z : ℤ)) : ℤ))] q (z-r-s))) * ((-1:K)^(((r : ℤ)+(s : ℤ)) : ℤ))) * (a^((-(s : ℤ)) : ℤ))) * (q^((((r : ℤ)+(s : ℤ))*(2*(N : ℤ)-(r : ℤ)-(s : ℤ)+1)/2-((x : ℤ)+(y : ℤ)+1)*(s : ℤ)) : ℤ))) / ((((pochList [(q^((-(M : ℤ)) : ℤ)),(q^((-(N : ℤ)) : ℤ)),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (r+s)) * (pochList [q,(a * q)] q (r))) * (pochList [q,(b * q)] q (s))) * (pochList [((a * b) * (q^(((N : ℤ)+(r : ℤ)+(s : ℤ)+2) : ℤ)))] q (z-r-s)))) = 0 then 0 else (((((((((pochList [(q^((-(z : ℤ)) : ℤ))] q (r+s)) * (pochList [(((a * b) * q) * q)] q (2*r+2*s))) * (pochList [(q^((-(x : ℤ)) : ℤ)),(q^((-(y : ℤ)) : ℤ))] q (r))) * (pochList [(q^(((x : ℤ)-(N : ℤ)) : ℤ)),(q^(((y : ℤ)-(M : ℤ)) : ℤ))] q (s))) * (pochList [(q^(((N : ℤ)-(z : ℤ)) : ℤ))] q (z-r-s))) * ((-1:K)^(((r : ℤ)+(s : ℤ)) : ℤ))) * (a^((-(s : ℤ)) : ℤ))) * (q^((((r : ℤ)+(s : ℤ))*(2*(N : ℤ)-(r : ℤ)-(s : ℤ)+1)/2-((x : ℤ)+(y : ℤ)+1)*(s : ℤ)) : ℤ))) / ((((pochList [(q^((-(M : ℤ)) : ℤ)),(q^((-(N : ℤ)) : ℤ)),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (r+s)) * (pochList [q,(a * q)] q (r))) * (pochList [q,(b * q)] q (s))) * (pochList [((a * b) * (q^(((N : ℤ)+(r : ℤ)+(s : ℤ)+2) : ℤ)))] q (z-r-s))))*(phi [(q^(((r : ℤ)+(s : ℤ)-(z : ℤ)) : ℤ)),(q^((1+(r : ℤ)+(s : ℤ)-(z : ℤ)) : ℤ))] [(q^((1+(N : ℤ)-(z : ℤ)) : ℤ))] q ((a * b) * (q^(((N : ℤ)+(z : ℤ)+2) : ℤ))) (z-r-s-1))))) := by
  sorry

end FiniteQBenchmark.Identity181
