import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.9.5 — 终止 6φ5 的奇偶平方和
Original representative source: GR2-8.9.5
Frozen statement: formulas/train/FQI-SRC-GR2-8.9.5.md
Source formula:
{}_6\phi_5^{[n]}(q^{-n},Aq^n,B,-B,h^2z^2,h^2/z^2;B^2,h^2s,-h^2s,-h^2,-h^2;q,q)=\sum_{k=0}^{\lfloor n/2\rfloor}\frac{(q^{-n},Aq^n,h^2,h^2z^2,h^2/z^2;q)_{2k}(q,A/B^2;q^2)_kq^{2k^2+k}B^{2k}}{(q,h^2s,-h^2s,-h^2,Aq^{2k-1};q)_{2k}(A,B^2q;q^2)_k}\left[{}_4\phi_3^{[n-2k]}(q^{2k-n},Aq^{n+2k},hq^kz,hq^k/z;h^2sq^{2k},-h^2sq^{2k},-h^2q^{2k};q,q)\right]^2.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity173
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (A B h u s z q : K) (n : ℕ)
 (hbase : regular q) (hA : A = h^4) (hB : B = u^2) (hs : s^2 = q) (hnz : ∀ v ∈ [A,B,z], v ≠ 0)
 (h_domain : (z * z) ≠ 0 ∧
    phiDefined [(B * B),((h * h) * s),(((-h) * h) * s),((-h) * h),((-h) * h)] q (n) ∧
    ∀ k ∈ Finset.range (n/2+1), ((z * z) ≠ 0 ∧
    (B * B) ≠ 0 ∧
    ((pochList [q,((h * h) * s),(((-h) * h) * s),((-h) * h),(A * (q^((2*(k : ℤ)-1) : ℤ)))] q (2*k)) * (pochList [A,((B * B) * q)] (q * q) (k))) ≠ 0 ∧
    z ≠ 0 ∧
    phiDefined [(((h * h) * s) * (q^((2*(k : ℤ)) : ℤ))),((((-h) * h) * s) * (q^((2*(k : ℤ)) : ℤ))),(((-h) * h) * (q^((2*(k : ℤ)) : ℤ)))] q (n-2*k))) :
 (phi [(q^((-(n : ℤ)) : ℤ)),(A * (q^(((n : ℤ)) : ℤ))),B,(-B),(((h * h) * z) * z),((h * h) / (z * z))] [(B * B),((h * h) * s),(((-h) * h) * s),((-h) * h),((-h) * h)] q q (n)) = (∑ k ∈ Finset.range (n/2+1), ((((((pochList [(q^((-(n : ℤ)) : ℤ)),(A * (q^(((n : ℤ)) : ℤ))),(h * h),(((h * h) * z) * z),((h * h) / (z * z))] q (2*k)) * (pochList [q,(A / (B * B))] (q * q) (k))) * (q^((2*(k : ℤ)*(k : ℤ)+(k : ℤ)) : ℤ))) * (B^((2*(k : ℤ)) : ℤ))) / ((pochList [q,((h * h) * s),(((-h) * h) * s),((-h) * h),(A * (q^((2*(k : ℤ)-1) : ℤ)))] q (2*k)) * (pochList [A,((B * B) * q)] (q * q) (k)))) * ((phi [(q^((2*(k : ℤ)-(n : ℤ)) : ℤ)),(A * (q^(((n : ℤ)+2*(k : ℤ)) : ℤ))),((h * (q^(((k : ℤ)) : ℤ))) * z),((h * (q^(((k : ℤ)) : ℤ))) / z)] [(((h * h) * s) * (q^((2*(k : ℤ)) : ℤ))),((((-h) * h) * s) * (q^((2*(k : ℤ)) : ℤ))),(((-h) * h) * (q^((2*(k : ℤ)) : ℤ)))] q q (n-2*k))^2))) := by
  sorry

end FiniteQBenchmark.Identity173
