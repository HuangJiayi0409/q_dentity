import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-9.5.3-finite — 有限支撑权序列的 Askey–Wilson 双线性变换
Original representative source: GR2-9.5.3-finite
Frozen statement: formulas/test/FQI-SRC-GR2-9.5.3-finite.md
Source formula:
\sum_{n=0}^N\nu_nk_nr_n(z)r_n(v)=\sum_{n=0}^N\frac{(dz,d/z,dv,d/v;q)_nw_n}{(q,bd,cd,d/a;q)_n}W_{10}^{[n]}(aq^{-n}/d;q^{1-n}/(bd),q^{1-n}/(cd),q^{-n},az,a/z,av,a/v;q,bcq/(ad)),\quad\nu_n=\frac{(bc,ad;q)_n(-ad)^nq^{\binom n2}}{(abcd;q)_{2n}}\sum_{j=0}^{N-n}\frac{(adq^n,adq^n;q)_j}{(q,abcdq^{2n};q)_j}w_{n+j},\quad k_n=\frac{1-abcdq^{2n-1}}{1-abcd/q}\frac{(abcd/q,ab,ac,ad;q)_n}{(q,bc,bd,cd;q)_n}a^{-2n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity197
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z v a b c d q : K) (N : ℕ) (weights : ℕ → K)
 (hbase : regular q) (h_support : ∀ j, N < j → weights j = 0) (hnz : ∀ v ∈ [a,b,c,d,z,v], v ≠ 0)
 (h_domain : ∀ n ∈ Finset.range (N+1), ((pochList [(((a * b) * c) * d)] q (2*n)) ≠ 0 ∧
    ∀ j ∈ Finset.range (N-n+1), ((pochList [q,((((a * b) * c) * d) * (q^((2*(n : ℤ)) : ℤ)))] q (j)) ≠ 0) ∧
    q ≠ 0 ∧
    (1 - ((((a * b) * c) * d) / q)) ≠ 0 ∧
    (pochList [q,(b * c),(b * d),(c * d)] q (n)) ≠ 0 ∧
    z ≠ 0 ∧
    phiDefined [(a * b),(a * c),(a * d)] q (n) ∧
    v ≠ 0) ∧
    ∀ n ∈ Finset.range (N+1), (z ≠ 0 ∧
    v ≠ 0 ∧
    a ≠ 0 ∧
    (pochList [q,(b * d),(c * d),(d / a)] q (n)) ≠ 0 ∧
    d ≠ 0 ∧
    (a * d) ≠ 0 ∧
    (b * d) ≠ 0 ∧
    (c * d) ≠ 0 ∧
    wDefined ((a * (q^((-(n : ℤ)) : ℤ))) / d) [((q^((1-(n : ℤ)) : ℤ)) / (b * d)),((q^((1-(n : ℤ)) : ℤ)) / (c * d)),(q^((-(n : ℤ)) : ℤ)),(a * z),(a / z),(a * v),(a / v)] q (n))) :
 (∑ n ∈ Finset.range (N+1), ((((((((pochList [(b * c),(a * d)] q (n)) * (((-a) * d)^(((n : ℤ)) : ℤ))) * (q^(((n : ℤ)*((n : ℤ)-1)/2) : ℤ))) / (pochList [(((a * b) * c) * d)] q (2*n))) * (∑ j ∈ Finset.range (N-n+1), (((pochList [((a * d) * (q^(((n : ℤ)) : ℤ))),((a * d) * (q^(((n : ℤ)) : ℤ)))] q (j)) / (pochList [q,((((a * b) * c) * d) * (q^((2*(n : ℤ)) : ℤ)))] q (j))) * (weights (n+j))))) * (((((1 - ((((a * b) * c) * d) * (q^((2*(n : ℤ)-1) : ℤ)))) / (1 - ((((a * b) * c) * d) / q))) * (pochList [((((a * b) * c) * d) / q),(a * b),(a * c),(a * d)] q (n))) / (pochList [q,(b * c),(b * d),(c * d)] q (n))) * (a^((-2*(n : ℤ)) : ℤ)))) * (phi [(q^((-((n : ℤ))) : ℤ)),((((a * b) * c) * d) * (q^((((n : ℤ))-1) : ℤ))),(a * z),(a / z)] [(a * b),(a * c),(a * d)] q q (n))) * (phi [(q^((-((n : ℤ))) : ℤ)),((((a * b) * c) * d) * (q^((((n : ℤ))-1) : ℤ))),(a * v),(a / v)] [(a * b),(a * c),(a * d)] q q (n)))) = (∑ n ∈ Finset.range (N+1), ((((pochList [(d * z),(d / z),(d * v),(d / v)] q (n)) * (weights n)) / (pochList [q,(b * d),(c * d),(d / a)] q (n))) * (wellPoisedRaw ((a * (q^((-(n : ℤ)) : ℤ))) / d) [((q^((1-(n : ℤ)) : ℤ)) / (b * d)),((q^((1-(n : ℤ)) : ℤ)) / (c * d)),(q^((-(n : ℤ)) : ℤ)),(a * z),(a / z),(a * v),(a / v)] q (((b * c) * q) / (a * d)) (n)))) := by
  sorry

end FiniteQBenchmark.Identity197
