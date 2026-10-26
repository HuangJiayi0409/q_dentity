import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex4ii — q-Hahn 乘积的有限三重和
Original representative source: GR2-8.Ex4ii
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex4ii.md
Source formula:
Q_n(x)Q_n(y)=\frac{(bq,abq^{N+2};q)_n(bq^{N+1})^{-n}}{(aq,q^{-N};q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},bq^{N+1-x-y};q)_mq^{(x+1)m}}{(q,bq,abq^{N+2};q)_m}\sum_{k=0}^{\min(m,x,y)}\frac{(q^{-m},abq^{m+1},q^{-x},q^{-y};q)_k(bq^{N-x+2})^k}{(q,aq,q^{-N},bq^{N+1-x-y};q)_k}{}_3\phi_2^{[\min(m-k,x-k)]}(q^{k-m},q^{k-x},bq^{N+1-x};0,bq^{N+1-x-y+k};q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity180
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (N n x y : ℕ)
 (hbase : regular q) (hn : n ≤ N) (hx : x ≤ N) (hy : y ≤ N) (hnz : ∀ v ∈ [a,b], v ≠ 0)
 (h_domain : phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ))] q (min (n) (x)) ∧
    phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ))] q (min (n) (y)) ∧
    (pochList [(a * q),(q^((-(N : ℤ)) : ℤ))] q (n)) ≠ 0 ∧
    ∀ m ∈ Finset.range (n+1), ((pochList [q,(b * q),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (m)) ≠ 0 ∧
    ∀ k ∈ Finset.range (min m (min x y)+1), ((pochList [q,(a * q),(q^((-(N : ℤ)) : ℤ)),(b * (q^(((N : ℤ)+1-(x : ℤ)-(y : ℤ)) : ℤ)))] q (k)) ≠ 0 ∧
    phiDefined [0,(b * (q^(((N : ℤ)+1-(x : ℤ)-(y : ℤ)+(k : ℤ)) : ℤ)))] q (min (m-k) (x-k))))) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((x : ℤ))) : ℤ))] [(a * q),(q^((-((N : ℤ))) : ℤ))] q q (min (n) (x))) * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((y : ℤ))) : ℤ))] [(a * q),(q^((-((N : ℤ))) : ℤ))] q q (min (n) (y)))) = ((((pochList [(b * q),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (n)) * ((b * (q^(((N : ℤ)+1) : ℤ)))^((-(n : ℤ)) : ℤ))) / (pochList [(a * q),(q^((-(N : ℤ)) : ℤ))] q (n))) * (∑ m ∈ Finset.range (n+1), ((((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(b * (q^(((N : ℤ)+1-(x : ℤ)-(y : ℤ)) : ℤ)))] q (m)) * (q^((((x : ℤ)+1)*(m : ℤ)) : ℤ))) / (pochList [q,(b * q),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (m))) * (∑ k ∈ Finset.range (min m (min x y)+1), ((((pochList [(q^((-(m : ℤ)) : ℤ)),((a * b) * (q^(((m : ℤ)+1) : ℤ))),(q^((-(x : ℤ)) : ℤ)),(q^((-(y : ℤ)) : ℤ))] q (k)) * ((b * (q^(((N : ℤ)-(x : ℤ)+2) : ℤ)))^(((k : ℤ)) : ℤ))) / (pochList [q,(a * q),(q^((-(N : ℤ)) : ℤ)),(b * (q^(((N : ℤ)+1-(x : ℤ)-(y : ℤ)) : ℤ)))] q (k))) * (phi [(q^(((k : ℤ)-(m : ℤ)) : ℤ)),(q^(((k : ℤ)-(x : ℤ)) : ℤ)),(b * (q^(((N : ℤ)+1-(x : ℤ)) : ℤ)))] [0,(b * (q^(((N : ℤ)+1-(x : ℤ)-(y : ℤ)+(k : ℤ)) : ℤ)))] q q (min (m-k) (x-k)))))))) := by
  sorry

end FiniteQBenchmark.Identity180
