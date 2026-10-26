import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex24 — 连续 q-Jacobi 特例的有限线性化
Original representative source: GR2-8.Ex24
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex24.md
Source formula:
r_n(z)r_{n-m}(z)=\sum_{k=0}^{2(n-m)}c_kr_{m+k}(z),\quad c_k=\frac{(ab;q)_{2m}(ab;q)_{2n-2m}(q,-as,bs,-ab;q)_n}{(abq;q)_{2n}(q,-as,bs,-ab;q)_m(-q,as,-bs,ab;q)_{n-m}}\frac{(1-abq^{2m+2k})(abq^{2m},-q^{m+1},-bsq^m,a/b,a^2b^2q^{2n},q^{2m-2n};q)_kq^{n-m}s^ka^{-k}}{(1-ab)(q,-abq^m,-asq^m,b^2q^{2m+1},q^{2m-2n+1}/(ab),abq^{2n+1};q)_k}W_{10}^{[\lfloor k/2\rfloor]}(b^2q^{2m};b^2,b^2q^{2n+1},q^{2m-2n+1}/a^2,abq^{2m+k},abq^{2m+k+1},q^{1-k},q^{-k};q^2,q^2),\quad s^2=q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity192
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b s z q : K) (m n : ℕ)
 (hbase : regular q) (hmn : m ≤ n) (hs : s^2 = q) (hnz : ∀ v ∈ [a,b,z], v ≠ 0)
 (h_domain : z ≠ 0 ∧
    phiDefined [(a * s),((-b) * s),(-q)] q (n) ∧
    phiDefined [(a * s),((-b) * s),(-q)] q (n-m) ∧
    ∀ k ∈ Finset.range (2*(n-m)+1), ((((pochList [((a * b) * q)] q (2*n)) * (pochList [q,((-a) * s),(b * s),((-a) * b)] q (m))) * (pochList [(-q),(a * s),((-b) * s),(a * b)] q (n-m))) ≠ 0 ∧
    b ≠ 0 ∧
    (a * b) ≠ 0 ∧
    ((1 - (a * b)) * (pochList [q,(((-a) * b) * (q^(((m : ℤ)) : ℤ))),(((-a) * s) * (q^(((m : ℤ)) : ℤ))),((b * b) * (q^((2*(m : ℤ)+1) : ℤ))),((q^((2*(m : ℤ)-2*(n : ℤ)+1) : ℤ)) / (a * b)),((a * b) * (q^((2*(n : ℤ)+1) : ℤ)))] q (k))) ≠ 0 ∧
    (a * a) ≠ 0 ∧
    wDefined ((b * b) * (q^((2*(m : ℤ)) : ℤ))) [(b * b),((b * b) * (q^((2*(n : ℤ)+1) : ℤ))),((q^((2*(m : ℤ)-2*(n : ℤ)+1) : ℤ)) / (a * a)),((a * b) * (q^((2*(m : ℤ)+(k : ℤ)) : ℤ))),((a * b) * (q^((2*(m : ℤ)+(k : ℤ)+1) : ℤ))),(q^((1-(k : ℤ)) : ℤ)),(q^((-(k : ℤ)) : ℤ))] (q * q) (k/2) ∧
    z ≠ 0 ∧
    phiDefined [(a * s),((-b) * s),(-q)] q (m+k))) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)) : ℤ))),(s * z),(s / z)] [(a * s),((-b) * s),(-q)] q q (n)) * (phi [(q^((-((n : ℤ)-(m : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)-(m : ℤ)) : ℤ))),(s * z),(s / z)] [(a * s),((-b) * s),(-q)] q q (n-m))) = (∑ k ∈ Finset.range (2*(n-m)+1), ((((((((((((pochList [(a * b)] q (2*m)) * (pochList [(a * b)] q (2*n-2*m))) * (pochList [q,((-a) * s),(b * s),((-a) * b)] q (n))) / (((pochList [((a * b) * q)] q (2*n)) * (pochList [q,((-a) * s),(b * s),((-a) * b)] q (m))) * (pochList [(-q),(a * s),((-b) * s),(a * b)] q (n-m)))) * (1 - ((a * b) * (q^((2*(m : ℤ)+2*(k : ℤ)) : ℤ))))) * (pochList [((a * b) * (q^((2*(m : ℤ)) : ℤ))),(-(q^(((m : ℤ)+1) : ℤ))),(((-b) * s) * (q^(((m : ℤ)) : ℤ))),(a / b),((((a * a) * b) * b) * (q^((2*(n : ℤ)) : ℤ))),(q^((2*(m : ℤ)-2*(n : ℤ)) : ℤ))] q (k))) * (q^(((n : ℤ)-(m : ℤ)) : ℤ))) * (s^(((k : ℤ)) : ℤ))) * (a^((-(k : ℤ)) : ℤ))) / ((1 - (a * b)) * (pochList [q,(((-a) * b) * (q^(((m : ℤ)) : ℤ))),(((-a) * s) * (q^(((m : ℤ)) : ℤ))),((b * b) * (q^((2*(m : ℤ)+1) : ℤ))),((q^((2*(m : ℤ)-2*(n : ℤ)+1) : ℤ)) / (a * b)),((a * b) * (q^((2*(n : ℤ)+1) : ℤ)))] q (k)))) * (wellPoisedRaw ((b * b) * (q^((2*(m : ℤ)) : ℤ))) [(b * b),((b * b) * (q^((2*(n : ℤ)+1) : ℤ))),((q^((2*(m : ℤ)-2*(n : ℤ)+1) : ℤ)) / (a * a)),((a * b) * (q^((2*(m : ℤ)+(k : ℤ)) : ℤ))),((a * b) * (q^((2*(m : ℤ)+(k : ℤ)+1) : ℤ))),(q^((1-(k : ℤ)) : ℤ)),(q^((-(k : ℤ)) : ℤ))] (q * q) (q * q) (k/2))) * (phi [(q^((-((m : ℤ)+(k : ℤ))) : ℤ)),((a * b) * (q^(((m : ℤ)+(k : ℤ)) : ℤ))),(s * z),(s / z)] [(a * s),((-b) * s),(-q)] q q (m+k)))) := by
  sorry

end FiniteQBenchmark.Identity192
