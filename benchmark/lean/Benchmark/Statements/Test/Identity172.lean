import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.9.2 — 终止 5φ4 的有限平方和
Original representative source: GR2-8.9.2
Frozen statement: formulas/test/FQI-SRC-GR2-8.9.2.md
Source formula:
{}_5\phi_4^{[n]}(q^{-n},Aq^n,B,Bz^2,B/z^2;B^2,h^2s,-h^2s,-B;q,q)=\sum_{k=0}^{\lfloor n/2\rfloor}\frac{(-1)^n(q^{-n},Aq^n,Bs,-Bs;q)_j(q,A/B^2;q^2)_k B^{2k}q^{2kj+k+j(j+1)/2}}{(q,h^2s,-h^2s,B^2q^j;q)_j(Aq^{2j+1},B^2q^{2j+2};q^2)_k}\left[{}_4\phi_3^{[j]}(q^{-j},B^2q^j,uz,u/z;Bs,-Bs,-B;q,q)\right]^2,\quad j=n-2k.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity172
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (A B h u s z q : K) (n : ℕ)
 (hbase : regular q) (hA : A = h^4) (hB : B = u^2) (hs : s^2 = q) (hnz : ∀ v ∈ [A,B,z], v ≠ 0)
 (h_domain : (z * z) ≠ 0 ∧
    phiDefined [(B * B),((h * h) * s),(((-h) * h) * s),(-B)] q (n) ∧
    ∀ k ∈ Finset.range (n/2+1), ((B * B) ≠ 0 ∧
    ((pochList [q,((h * h) * s),(((-h) * h) * s),((B * B) * (q^((((n : ℤ)-2*(k : ℤ))) : ℤ)))] q ((n-2*k))) * (pochList [(A * (q^((2*((n : ℤ)-2*(k : ℤ))+1) : ℤ))),((B * B) * (q^((2*((n : ℤ)-2*(k : ℤ))+2) : ℤ)))] (q * q) (k))) ≠ 0 ∧
    z ≠ 0 ∧
    phiDefined [(B * s),((-B) * s),(-B)] q ((n-2*k)))) :
 (phi [(q^((-(n : ℤ)) : ℤ)),(A * (q^(((n : ℤ)) : ℤ))),B,((B * z) * z),(B / (z * z))] [(B * B),((h * h) * s),(((-h) * h) * s),(-B)] q q (n)) = (∑ k ∈ Finset.range (n/2+1), ((((((((-1:K)^(((n : ℤ)) : ℤ)) * (pochList [(q^((-(n : ℤ)) : ℤ)),(A * (q^(((n : ℤ)) : ℤ))),(B * s),((-B) * s)] q ((n-2*k)))) * (pochList [q,(A / (B * B))] (q * q) (k))) * (B^((2*(k : ℤ)) : ℤ))) * (q^((2*(k : ℤ)*((n : ℤ)-2*(k : ℤ))+(k : ℤ)+((n : ℤ)-2*(k : ℤ))*((n : ℤ)-2*(k : ℤ)+1)/2) : ℤ))) / ((pochList [q,((h * h) * s),(((-h) * h) * s),((B * B) * (q^((((n : ℤ)-2*(k : ℤ))) : ℤ)))] q ((n-2*k))) * (pochList [(A * (q^((2*((n : ℤ)-2*(k : ℤ))+1) : ℤ))),((B * B) * (q^((2*((n : ℤ)-2*(k : ℤ))+2) : ℤ)))] (q * q) (k)))) * ((phi [(q^((-((n : ℤ)-2*(k : ℤ))) : ℤ)),((B * B) * (q^((((n : ℤ)-2*(k : ℤ))) : ℤ))),(u * z),(u / z)] [(B * s),((-B) * s),(-B)] q q ((n-2*k)))^2))) := by
  sorry

end FiniteQBenchmark.Identity172
