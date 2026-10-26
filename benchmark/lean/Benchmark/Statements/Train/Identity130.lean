import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.2.24 — 对偶 q-Hahn 有限正交
Original representative source: GR2-7.2.24
Frozen statement: formulas/train/FQI-SRC-GR2-7.2.24.md
Source formula:
\sum_{x=0}^ND_m(x)D_n(x)\frac{(cq^{-N},bcq,q^{-N};q)_x(1-cq^{2x-N})}{(q,q^{-N}/b,cq;q)_x(1-cq^{-N})}q^{Nx-x(x-1)/2}(-bcq)^{-x}=\frac{(1/c;q)_N(q,bq;q)_n}{(bq;q)_N(bcq,q^{-N};q)_n}(cq^{-N})^n\delta_{mn}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity130
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (b c q : K) (N m n : ℕ)
 (hbase : regular q) (hm : m ≤ N) (hn : n ≤ N) (hnz : ∀ v ∈ [b,c], v ≠ 0)
 (h_domain : ∀ x ∈ Finset.range (N+1), (phiDefined [(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q (min (m) (x)) ∧
    phiDefined [(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q (min (n) (x)) ∧
    b ≠ 0 ∧
    ((pochList [q,((q^((-(N : ℤ)) : ℤ)) / b),(c * q)] q (x)) * (1 - (c * (q^((-(N : ℤ)) : ℤ))))) ≠ 0) ∧
    c ≠ 0 ∧
    ((pochList [(b * q)] q (N)) * (pochList [((b * c) * q),(q^((-(N : ℤ)) : ℤ))] q (n))) ≠ 0) :
 (∑ x ∈ Finset.range (N+1), (((((((phi [(q^((-((m : ℤ))) : ℤ)),(q^((-((x : ℤ))) : ℤ)),(c * (q^(((x : ℤ)-((N : ℤ))) : ℤ)))] [(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q q (min (m) (x))) * (phi [(q^((-((n : ℤ))) : ℤ)),(q^((-((x : ℤ))) : ℤ)),(c * (q^(((x : ℤ)-((N : ℤ))) : ℤ)))] [(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q q (min (n) (x)))) * (pochList [(c * (q^((-(N : ℤ)) : ℤ))),((b * c) * q),(q^((-(N : ℤ)) : ℤ))] q (x))) * (1 - (c * (q^((2*(x : ℤ)-(N : ℤ)) : ℤ))))) / ((pochList [q,((q^((-(N : ℤ)) : ℤ)) / b),(c * q)] q (x)) * (1 - (c * (q^((-(N : ℤ)) : ℤ)))))) * (q^(((N : ℤ)*(x : ℤ)-(x : ℤ)*((x : ℤ)-1)/2) : ℤ))) * ((((-b) * c) * q)^((-(x : ℤ)) : ℤ)))) = (((((pochList [(1 / c)] q (N)) * (pochList [q,(b * q)] q (n))) / ((pochList [(b * q)] q (N)) * (pochList [((b * c) * q),(q^((-(N : ℤ)) : ℤ))] q (n)))) * ((c * (q^((-(N : ℤ)) : ℤ)))^(((n : ℤ)) : ℤ))) * (if (m) = (n) then (1 : K) else 0)) := by
  sorry

end FiniteQBenchmark.Identity130
