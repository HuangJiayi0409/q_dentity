import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.9.1 — 终止 5φ4 的有限乘积展开
Original representative source: GR2-8.9.1
Frozen statement: formulas/train/FQI-SRC-GR2-8.9.1.md
Source formula:
{}_5\phi_4^{[n]}(q^{-n},Aq^n,B,Bz^2,B/z^2;B^2,h^2s,-h^2s,-B;q,q)=\sum_{j=0}^n\frac{(q^{-n},Aq^n,Bs,-Bs;q)_j(-1)^jq^{j(j+1)/2}}{(q,h^2s,-h^2s,B^2q^j;q)_j}{}_4\phi_3^{[n-j]}(q^{j-n},Aq^{j+n},Bsq^j,-Bsq^j;B^2q^{2j+1},h^2sq^j,-h^2sq^j;q,q){}_5\phi_4^{[j]}(q^{-j},B^2q^j,B,Bz^2,B/z^2;B^2,Bs,-Bs,-B;q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity171
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (A B h u s z q : K) (n : ℕ)
 (hbase : regular q) (hA : A = h^4) (hB : B = u^2) (hs : s^2 = q) (hnz : ∀ v ∈ [A,B,z], v ≠ 0)
 (h_domain : (z * z) ≠ 0 ∧
    phiDefined [(B * B),((h * h) * s),(((-h) * h) * s),(-B)] q (n) ∧
    ∀ j ∈ Finset.range (n+1), ((pochList [q,((h * h) * s),(((-h) * h) * s),((B * B) * (q^(((j : ℤ)) : ℤ)))] q (j)) ≠ 0 ∧
    phiDefined [((B * B) * (q^((2*(j : ℤ)+1) : ℤ))),(((h * h) * s) * (q^(((j : ℤ)) : ℤ))),((((-h) * h) * s) * (q^(((j : ℤ)) : ℤ)))] q (n-j) ∧
    (z * z) ≠ 0 ∧
    phiDefined [(B * B),(B * s),((-B) * s),(-B)] q (j))) :
 (phi [(q^((-(n : ℤ)) : ℤ)),(A * (q^(((n : ℤ)) : ℤ))),B,((B * z) * z),(B / (z * z))] [(B * B),((h * h) * s),(((-h) * h) * s),(-B)] q q (n)) = (∑ j ∈ Finset.range (n+1), ((((((pochList [(q^((-(n : ℤ)) : ℤ)),(A * (q^(((n : ℤ)) : ℤ))),(B * s),((-B) * s)] q (j)) * ((-1:K)^(((j : ℤ)) : ℤ))) * (q^(((j : ℤ)*((j : ℤ)+1)/2) : ℤ))) / (pochList [q,((h * h) * s),(((-h) * h) * s),((B * B) * (q^(((j : ℤ)) : ℤ)))] q (j))) * (phi [(q^(((j : ℤ)-(n : ℤ)) : ℤ)),(A * (q^(((j : ℤ)+(n : ℤ)) : ℤ))),((B * s) * (q^(((j : ℤ)) : ℤ))),(((-B) * s) * (q^(((j : ℤ)) : ℤ)))] [((B * B) * (q^((2*(j : ℤ)+1) : ℤ))),(((h * h) * s) * (q^(((j : ℤ)) : ℤ))),((((-h) * h) * s) * (q^(((j : ℤ)) : ℤ)))] q q (n-j))) * (phi [(q^((-(j : ℤ)) : ℤ)),((B * B) * (q^(((j : ℤ)) : ℤ))),B,((B * z) * z),(B / (z * z))] [(B * B),(B * s),((-B) * s),(-B)] q q (j)))) := by
  sorry

end FiniteQBenchmark.Identity171
