import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex26 — 相伴 Askey–Wilson 的有限 10W9 展开
Original representative source: GR2-8.Ex26
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex26.md
Source formula:
r_n^{\rho}(z)=\sum_{k=0}^n\frac{(q^{-n},abcd\rho^2q^{n-1},abcd\rho^2/q,az,a/z;q)_kq^k}{(q,ab\rho,ac\rho,ad\rho,abcd\rho/q;q)_k}W_{10}^{[n-k]}(abcd\rho^2q^{k-2};\rho,bc\rho/q,bd\rho/q,cd\rho/q,q^{k+1},abcd\rho^2q^{n+k-1},q^{k-n};q,a^2).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity193
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z a b c d rho q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [a,b,c,d,rho,z], v ≠ 0)
 (h_domain : ∀ j < n, (1-a*b*c*d*((rho * (q^(((j : ℤ)) : ℤ))))^2/q)*(1-a*b*c*d*((rho * (q^(((j : ℤ)) : ℤ))))^2) ≠ 0 ∧
    ∀ j < n, (1-a*b*c*d*((rho * (q^(((j : ℤ)) : ℤ))))^2/q^2)*(1-a*b*c*d*((rho * (q^(((j : ℤ)) : ℤ))))^2/q) ≠ 0 ∧
    ∀ j < n, awAssocA a b c d q ((rho * (q^(((j : ℤ)) : ℤ)))) ≠ 0 ∧
    ∀ k ∈ Finset.range (n+1), (q ≠ 0 ∧
    z ≠ 0 ∧
    (pochList [q,((a * b) * rho),((a * c) * rho),((a * d) * rho),(((((a * b) * c) * d) * rho) / q)] q (k)) ≠ 0 ∧
    wDefined ((((((a * b) * c) * d) * rho) * rho) * (q^(((k : ℤ)-2) : ℤ))) [rho,(((b * c) * rho) / q),(((b * d) * rho) / q),(((c * d) * rho) / q),(q^(((k : ℤ)+1) : ℤ)),((((((a * b) * c) * d) * rho) * rho) * (q^(((n : ℤ)+(k : ℤ)-1) : ℤ))),(q^(((k : ℤ)-(n : ℤ)) : ℤ))] q (n-k))) :
 (associatedAW z a b c d rho q n) = (∑ k ∈ Finset.range (n+1), ((((pochList [(q^((-(n : ℤ)) : ℤ)),((((((a * b) * c) * d) * rho) * rho) * (q^(((n : ℤ)-1) : ℤ))),((((((a * b) * c) * d) * rho) * rho) / q),(a * z),(a / z)] q (k)) * (q^(((k : ℤ)) : ℤ))) / (pochList [q,((a * b) * rho),((a * c) * rho),((a * d) * rho),(((((a * b) * c) * d) * rho) / q)] q (k))) * (wellPoisedRaw ((((((a * b) * c) * d) * rho) * rho) * (q^(((k : ℤ)-2) : ℤ))) [rho,(((b * c) * rho) / q),(((b * d) * rho) / q),(((c * d) * rho) / q),(q^(((k : ℤ)+1) : ℤ)),((((((a * b) * c) * d) * rho) * rho) * (q^(((n : ℤ)+(k : ℤ)-1) : ℤ))),(q^(((k : ℤ)-(n : ℤ)) : ℤ))] q (a * a) (n-k)))) := by
  sorry

end FiniteQBenchmark.Identity193
