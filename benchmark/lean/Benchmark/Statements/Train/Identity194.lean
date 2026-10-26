import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex27 — 相伴 Askey–Wilson 的双重有限和
Original representative source: GR2-8.Ex27
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex27.md
Source formula:
r_n^{\rho}(z)=\frac{(abcd\rho^2/q,\rho q;q)_n\rho^{-n}}{(q,abcd\rho/q;q)_n}\sum_{k=0}^n\frac{(q^{-n},abcd\rho^2q^{n-1},a\rho z,a\rho/z;q)_kq^k}{(\rho q,ab\rho,ac\rho,ad\rho;q)_k}\sum_{j=0}^k\frac{(\rho,ab\rho/q,ac\rho/q,ad\rho/q;q)_jq^j}{(q,abcd\rho^2/q^2,a\rho z,a\rho/z;q)_j}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity194
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z a b c d rho q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [a,b,c,d,rho,z], v ≠ 0)
 (h_domain : ∀ j < n, (1-a*b*c*d*((rho * (q^(((j : ℤ)) : ℤ))))^2/q)*(1-a*b*c*d*((rho * (q^(((j : ℤ)) : ℤ))))^2) ≠ 0 ∧
    ∀ j < n, (1-a*b*c*d*((rho * (q^(((j : ℤ)) : ℤ))))^2/q^2)*(1-a*b*c*d*((rho * (q^(((j : ℤ)) : ℤ))))^2/q) ≠ 0 ∧
    ∀ j < n, awAssocA a b c d q ((rho * (q^(((j : ℤ)) : ℤ)))) ≠ 0 ∧
    q ≠ 0 ∧
    (pochList [q,(((((a * b) * c) * d) * rho) / q)] q (n)) ≠ 0 ∧
    ∀ k ∈ Finset.range (n+1), (z ≠ 0 ∧
    (pochList [(rho * q),((a * b) * rho),((a * c) * rho),((a * d) * rho)] q (k)) ≠ 0 ∧
    ∀ j ∈ Finset.range (k+1), (q ≠ 0 ∧
    (q * q) ≠ 0 ∧
    z ≠ 0 ∧
    (pochList [q,((((((a * b) * c) * d) * rho) * rho) / (q * q)),((a * rho) * z),((a * rho) / z)] q (j)) ≠ 0))) :
 (associatedAW z a b c d rho q n) = ((((pochList [((((((a * b) * c) * d) * rho) * rho) / q),(rho * q)] q (n)) * (rho^((-(n : ℤ)) : ℤ))) / (pochList [q,(((((a * b) * c) * d) * rho) / q)] q (n))) * (∑ k ∈ Finset.range (n+1), ((((pochList [(q^((-(n : ℤ)) : ℤ)),((((((a * b) * c) * d) * rho) * rho) * (q^(((n : ℤ)-1) : ℤ))),((a * rho) * z),((a * rho) / z)] q (k)) * (q^(((k : ℤ)) : ℤ))) / (pochList [(rho * q),((a * b) * rho),((a * c) * rho),((a * d) * rho)] q (k))) * (∑ j ∈ Finset.range (k+1), (((pochList [rho,(((a * b) * rho) / q),(((a * c) * rho) / q),(((a * d) * rho) / q)] q (j)) * (q^(((j : ℤ)) : ℤ))) / (pochList [q,((((((a * b) * c) * d) * rho) * rho) / (q * q)),((a * rho) * z),((a * rho) / z)] q (j))))))) := by
  sorry

end FiniteQBenchmark.Identity194
