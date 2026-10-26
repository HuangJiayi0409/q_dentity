import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.3.3 — q-Hahn 多项式的 Watson 型乘积
Original representative source: GR2-8.3.3
Frozen statement: formulas/train/FQI-SRC-GR2-8.3.3.md
Source formula:
Q_n(x)Q_n(y)=(-aq)^nq^{\binom n2}\frac{(bq;q)_n}{(aq;q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},q^{x-N},q^{y-N};q)_m(aq^{x+y})^{-m}}{(q,bq,q^{-N},q^{-N};q)_m}{}_4\phi_3^{[m]}(q^{-x},q^{-y},b^{-1}q^{-m},q^{-m};aq,q^{N-x+1-m},q^{N-y+1-m};q,abq^{2N+3}).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity163
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (N n x y : ℕ)
 (hbase : regular q) (hn : n ≤ N) (hx : x ≤ N) (hy : y ≤ N) (hnz : ∀ v ∈ [a,b], v ≠ 0)
 (h_domain : phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ))] q (min (n) (x)) ∧
    phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ))] q (min (n) (y)) ∧
    (pochList [(a * q)] q (n)) ≠ 0 ∧
    ∀ m ∈ Finset.range (n+1), ((pochList [q,(b * q),(q^((-(N : ℤ)) : ℤ)),(q^((-(N : ℤ)) : ℤ))] q (m)) ≠ 0 ∧
    (((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^(((x : ℤ)-(N : ℤ)) : ℤ)),(q^(((y : ℤ)-(N : ℤ)) : ℤ))] q (m)) * ((a * (q^(((x : ℤ)+(y : ℤ)) : ℤ)))^((-(m : ℤ)) : ℤ))) / (pochList [q,(b * q),(q^((-(N : ℤ)) : ℤ)),(q^((-(N : ℤ)) : ℤ))] q (m))) ≠ 0 → (b ≠ 0) ∧
    (((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^(((x : ℤ)-(N : ℤ)) : ℤ)),(q^(((y : ℤ)-(N : ℤ)) : ℤ))] q (m)) * ((a * (q^(((x : ℤ)+(y : ℤ)) : ℤ)))^((-(m : ℤ)) : ℤ))) / (pochList [q,(b * q),(q^((-(N : ℤ)) : ℤ)),(q^((-(N : ℤ)) : ℤ))] q (m))) ≠ 0 → (phiDefined [(a * q),(q^(((N : ℤ)-(x : ℤ)+1-(m : ℤ)) : ℤ)),(q^(((N : ℤ)-(y : ℤ)+1-(m : ℤ)) : ℤ))] q (m)))) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((x : ℤ))) : ℤ))] [(a * q),(q^((-((N : ℤ))) : ℤ))] q q (min (n) (x))) * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((y : ℤ))) : ℤ))] [(a * q),(q^((-((N : ℤ))) : ℤ))] q q (min (n) (y)))) = (((((((-a) * q)^(((n : ℤ)) : ℤ)) * (q^(((n : ℤ)*((n : ℤ)-1)/2) : ℤ))) * (pochList [(b * q)] q (n))) / (pochList [(a * q)] q (n))) * (∑ m ∈ Finset.range (n+1), (if (((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^(((x : ℤ)-(N : ℤ)) : ℤ)),(q^(((y : ℤ)-(N : ℤ)) : ℤ))] q (m)) * ((a * (q^(((x : ℤ)+(y : ℤ)) : ℤ)))^((-(m : ℤ)) : ℤ))) / (pochList [q,(b * q),(q^((-(N : ℤ)) : ℤ)),(q^((-(N : ℤ)) : ℤ))] q (m))) = 0 then 0 else (((pochList [(q^((-(n : ℤ)) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^(((x : ℤ)-(N : ℤ)) : ℤ)),(q^(((y : ℤ)-(N : ℤ)) : ℤ))] q (m)) * ((a * (q^(((x : ℤ)+(y : ℤ)) : ℤ)))^((-(m : ℤ)) : ℤ))) / (pochList [q,(b * q),(q^((-(N : ℤ)) : ℤ)),(q^((-(N : ℤ)) : ℤ))] q (m)))*(phi [(q^((-(x : ℤ)) : ℤ)),(q^((-(y : ℤ)) : ℤ)),((q^((-(m : ℤ)) : ℤ)) / b),(q^((-(m : ℤ)) : ℤ))] [(a * q),(q^(((N : ℤ)-(x : ℤ)+1-(m : ℤ)) : ℤ)),(q^(((N : ℤ)-(y : ℤ)+1-(m : ℤ)) : ℤ))] q ((a * b) * (q^((2*(N : ℤ)+3) : ℤ))) (m))))) := by
  sorry

end FiniteQBenchmark.Identity163
