import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.2.18 — q-Racah 有限正交及对偶正交
Original representative source: GR2-7.2.18
Frozen statement: formulas/train/FQI-SRC-GR2-7.2.18.md
Source formula:
\sum_{x=0}^N\rho_x W_m(x)W_n(x)=\delta_{mn}/h_n,\qquad\sum_{n=0}^Nh_nW_n(x)W_n(y)=\delta_{xy}/\rho_x,\quad\rho_x=\frac{(cq^{-N},aq,bcq,q^{-N};q)_x(1-cq^{2x-N})}{(q,cq^{-N}/a,q^{-N}/b,cq;q)_x(1-cq^{-N})}(abq)^{-x},\quad h_n=\frac{(bq,aq/c;q)_N}{(abq^2,1/c;q)_N}\frac{(abq,aq,bcq,q^{-N};q)_n(1-abq^{2n+1})q^{Nn}c^{-n}}{(q,bq,aq/c,abq^{N+2};q)_n(1-abq)}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity128
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c q : K) (N m n x y : ℕ)
 (hbase : regular q) (hm : m ≤ N) (hn : n ≤ N) (hx : x ≤ N) (hy : y ≤ N) (hnz : ∀ v ∈ [a,b,c], v ≠ 0)
 (h_domain : ∀ j ∈ Finset.range (N+1), (a ≠ 0 ∧
    b ≠ 0 ∧
    ((pochList [q,((c * (q^((-((N : ℤ))) : ℤ))) / a),((q^((-((N : ℤ))) : ℤ)) / b),(c * q)] q (j)) * (1 - (c * (q^((-((N : ℤ))) : ℤ))))) ≠ 0 ∧
    phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q (min (m) (j)) ∧
    phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q (min (n) (j))) ∧
    c ≠ 0 ∧
    (pochList [(((a * b) * q) * q),(1 / c)] q (N)) ≠ 0 ∧
    ((pochList [q,(b * q),((a * q) / c),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (n)) * (1 - ((a * b) * q))) ≠ 0 ∧
    (((((((pochList [(b * q),((a * q) / c)] q (N)) / (pochList [(((a * b) * q) * q),(1 / c)] q (N))) * (pochList [((a * b) * q),(a * q),((b * c) * q),(q^((-((N : ℤ))) : ℤ))] q (n))) * (1 - ((a * b) * (q^((2*((n : ℤ))+1) : ℤ))))) * (q^((((N : ℤ))*((n : ℤ))) : ℤ))) * (c^((-((n : ℤ))) : ℤ))) / ((pochList [q,(b * q),((a * q) / c),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (n)) * (1 - ((a * b) * q)))) ≠ 0 ∧
    ∀ j ∈ Finset.range (N+1), (c ≠ 0 ∧
    (pochList [(((a * b) * q) * q),(1 / c)] q (N)) ≠ 0 ∧
    ((pochList [q,(b * q),((a * q) / c),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (j)) * (1 - ((a * b) * q))) ≠ 0 ∧
    phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q (min (j) (x)) ∧
    phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q (min (j) (y))) ∧
    a ≠ 0 ∧
    b ≠ 0 ∧
    ((pochList [q,((c * (q^((-((N : ℤ))) : ℤ))) / a),((q^((-((N : ℤ))) : ℤ)) / b),(c * q)] q (x)) * (1 - (c * (q^((-((N : ℤ))) : ℤ))))) ≠ 0 ∧
    ((((pochList [(c * (q^((-((N : ℤ))) : ℤ))),(a * q),((b * c) * q),(q^((-((N : ℤ))) : ℤ))] q (x)) * (1 - (c * (q^((2*((x : ℤ))-((N : ℤ))) : ℤ))))) / ((pochList [q,((c * (q^((-((N : ℤ))) : ℤ))) / a),((q^((-((N : ℤ))) : ℤ)) / b),(c * q)] q (x)) * (1 - (c * (q^((-((N : ℤ))) : ℤ)))))) * (((a * b) * q)^((-((x : ℤ))) : ℤ))) ≠ 0) :
 (∑ j ∈ Finset.range (N+1), ((((((pochList [(c * (q^((-((N : ℤ))) : ℤ))),(a * q),((b * c) * q),(q^((-((N : ℤ))) : ℤ))] q (j)) * (1 - (c * (q^((2*((j : ℤ))-((N : ℤ))) : ℤ))))) / ((pochList [q,((c * (q^((-((N : ℤ))) : ℤ))) / a),((q^((-((N : ℤ))) : ℤ)) / b),(c * q)] q (j)) * (1 - (c * (q^((-((N : ℤ))) : ℤ)))))) * (((a * b) * q)^((-((j : ℤ))) : ℤ))) * (phi [(q^((-((m : ℤ))) : ℤ)),((a * b) * (q^(((m : ℤ)+1) : ℤ))),(q^((-((j : ℤ))) : ℤ)),(c * (q^(((j : ℤ)-((N : ℤ))) : ℤ)))] [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q q (min (m) (j)))) * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((j : ℤ))) : ℤ)),(c * (q^(((j : ℤ)-((N : ℤ))) : ℤ)))] [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q q (min (n) (j))))) = ((if (m) = (n) then (1 : K) else 0) / (((((((pochList [(b * q),((a * q) / c)] q (N)) / (pochList [(((a * b) * q) * q),(1 / c)] q (N))) * (pochList [((a * b) * q),(a * q),((b * c) * q),(q^((-((N : ℤ))) : ℤ))] q (n))) * (1 - ((a * b) * (q^((2*((n : ℤ))+1) : ℤ))))) * (q^((((N : ℤ))*((n : ℤ))) : ℤ))) * (c^((-((n : ℤ))) : ℤ))) / ((pochList [q,(b * q),((a * q) / c),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (n)) * (1 - ((a * b) * q))))) ∧
 (∑ j ∈ Finset.range (N+1), (((((((((pochList [(b * q),((a * q) / c)] q (N)) / (pochList [(((a * b) * q) * q),(1 / c)] q (N))) * (pochList [((a * b) * q),(a * q),((b * c) * q),(q^((-((N : ℤ))) : ℤ))] q (j))) * (1 - ((a * b) * (q^((2*((j : ℤ))+1) : ℤ))))) * (q^((((N : ℤ))*((j : ℤ))) : ℤ))) * (c^((-((j : ℤ))) : ℤ))) / ((pochList [q,(b * q),((a * q) / c),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (j)) * (1 - ((a * b) * q)))) * (phi [(q^((-((j : ℤ))) : ℤ)),((a * b) * (q^(((j : ℤ)+1) : ℤ))),(q^((-((x : ℤ))) : ℤ)),(c * (q^(((x : ℤ)-((N : ℤ))) : ℤ)))] [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q q (min (j) (x)))) * (phi [(q^((-((j : ℤ))) : ℤ)),((a * b) * (q^(((j : ℤ)+1) : ℤ))),(q^((-((y : ℤ))) : ℤ)),(c * (q^(((y : ℤ)-((N : ℤ))) : ℤ)))] [(a * q),(q^((-((N : ℤ))) : ℤ)),((b * c) * q)] q q (min (j) (y))))) = ((if (x) = (y) then (1 : K) else 0) / ((((pochList [(c * (q^((-((N : ℤ))) : ℤ))),(a * q),((b * c) * q),(q^((-((N : ℤ))) : ℤ))] q (x)) * (1 - (c * (q^((2*((x : ℤ))-((N : ℤ))) : ℤ))))) / ((pochList [q,((c * (q^((-((N : ℤ))) : ℤ))) / a),((q^((-((N : ℤ))) : ℤ)) / b),(c * q)] q (x)) * (1 - (c * (q^((-((N : ℤ))) : ℤ)))))) * (((a * b) * q)^((-((x : ℤ))) : ℤ)))) := by
  sorry

end FiniteQBenchmark.Identity128
