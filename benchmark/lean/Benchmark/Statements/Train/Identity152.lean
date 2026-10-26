import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.Ex27 — Askey–Wilson 的四个三角多项式特例
Original representative source: GR2-7.Ex27
Frozen statement: formulas/train/FQI-SRC-GR2-7.Ex27.md
Source formula:
P_n(z;q,-q,s,-s)=(q^{n+2};q)_n\frac{z^{n+1}-z^{-n-1}}{z-z^{-1}},\quad P_n(z;1,-1,s,-s)=(q^n;q)_n(z^n+z^{-n})\ (n\ge1),\quad P_n(z;q,-1,s,-s)=(q^{n+1};q)_n\frac{z^{n+1}-z^{-n}}{z-1},\quad P_n(z;1,-q,s,-s)=(q^{n+1};q)_n\frac{z^{n+1}+z^{-n}}{z+1},\quad s^2=q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity152
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z s q : K) (n : ℕ)
 (hbase : regular q) (hs : s^2 = q) (hz : z ≠ 0)
 (h_second : phiDefined [-1,s,-s] q n) (h_domain : z ≠ 0 ∧
    phiDefined [(q * (-q)),(q * s),(q * (-s))] q (n) ∧
    q ≠ 0 ∧
    phiDefined [(q * -1),(q * s),(q * (-s))] q (n) ∧
    phiDefined [(1 * (-q)),(1 * s),(1 * (-s))] q (n) ∧
    1 ≠ 0) :
 (askeyWilson (z) (q) ((-q)) (s) ((-s)) (q) (n)) = ((pochList [(q^(((n : ℤ)+2) : ℤ))] q (n)) * (∑ k ∈ Finset.range (n+1), ((q^((0) : ℤ)) * (z^(((n : ℤ)-2*(k : ℤ)) : ℤ))))) ∧
 (askeyWilson (z) (q) (-1) (s) ((-s)) (q) (n)) = ((pochList [(q^(((n : ℤ)+1) : ℤ))] q (n)) * (∑ k ∈ Finset.range (2*n+1), (z^(((n : ℤ)-(k : ℤ)) : ℤ)))) ∧
 (askeyWilson (z) (1) ((-q)) (s) ((-s)) (q) (n)) = ((pochList [(q^(((n : ℤ)+1) : ℤ))] q (n)) * (∑ k ∈ Finset.range (2*n+1), (((-1:K)^(((k : ℤ)) : ℤ)) * (z^(((n : ℤ)-(k : ℤ)) : ℤ))))) ∧
 (1 ≤ n → (askeyWilson (z) (1) (-1) (s) ((-s)) (q) (n)) = ((pochList [(q^(((n : ℤ)) : ℤ))] q (n)) * ((z^(((n : ℤ)) : ℤ)) + (z^((-(n : ℤ)) : ℤ))))) := by
  sorry

end FiniteQBenchmark.Identity152
