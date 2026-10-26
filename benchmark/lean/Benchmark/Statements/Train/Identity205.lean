import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-9.Ex17ii — 连续 q-Jacobi 的有限连接公式（归一化核正）
Original representative source: GR2-9.Ex17ii
Frozen statement: formulas/train/FQI-SRC-GR2-9.Ex17ii.md
Source formula:
\mathscr J_m(z;A,B)=\sum_{n=0}^mg(n,m)\mathscr J_n(z;U,V),\quad g(n,m)=\frac{(Aq,-Bq;q)_m(UVq,-q;q)_n(ABq^{m+1};q)_nq^{n(n-m)}}{(-q;q)_m(UVq;q)_{2n}(q;q)_{m-n}(Aq,-Bq;q)_n}{}_4\phi_3^{[m-n]}(q^{n-m},ABq^{n+m+1},Uq^{n+1},-Vq^{n+1};UVq^{2n+2},Aq^{n+1},-Bq^{n+1};q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity205
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (A B U V s z q : K) (m : ℕ)
 (hbase : regular q) (hs : s^2 = q) (hz : z ≠ 0) (hnz : A*B*U*V ≠ 0)
 (h_domain : (pochList [q,(-q)] q (m)) ≠ 0 ∧
    z ≠ 0 ∧
    phiDefined [(A * q),((-B) * q),(-q)] q (m) ∧
    ∀ n ∈ Finset.range (m+1), (((((pochList [(-q)] q (m)) * (pochList [((U * V) * q)] q (2*n))) * (pochList [q] q (m-n))) * (pochList [(A * q),((-B) * q)] q (n))) ≠ 0 ∧
    phiDefined [((U * V) * (q^((2*(n : ℤ)+2) : ℤ))),(A * (q^(((n : ℤ)+1) : ℤ))),((-B) * (q^(((n : ℤ)+1) : ℤ)))] q (m-n) ∧
    (pochList [q,(-q)] q (n)) ≠ 0 ∧
    z ≠ 0 ∧
    phiDefined [(U * q),((-V) * q),(-q)] q (n))) :
 (((pochList [(A * q),((-B) * q)] q (m)) / (pochList [q,(-q)] q (m))) * (phi [(q^((-((m : ℤ))) : ℤ)),((A * B) * (q^(((m : ℤ)+1) : ℤ))),(s * z),(s / z)] [(A * q),((-B) * q),(-q)] q q (m))) = (∑ n ∈ Finset.range (m+1), (((((((pochList [(A * q),((-B) * q)] q (m)) * (pochList [((U * V) * q),(-q)] q (n))) * (pochList [((A * B) * (q^(((m : ℤ)+1) : ℤ)))] q (n))) * (q^(((n : ℤ)*((n : ℤ)-(m : ℤ))) : ℤ))) / ((((pochList [(-q)] q (m)) * (pochList [((U * V) * q)] q (2*n))) * (pochList [q] q (m-n))) * (pochList [(A * q),((-B) * q)] q (n)))) * (phi [(q^(((n : ℤ)-(m : ℤ)) : ℤ)),((A * B) * (q^(((n : ℤ)+(m : ℤ)+1) : ℤ))),(U * (q^(((n : ℤ)+1) : ℤ))),((-V) * (q^(((n : ℤ)+1) : ℤ)))] [((U * V) * (q^((2*(n : ℤ)+2) : ℤ))),(A * (q^(((n : ℤ)+1) : ℤ))),((-B) * (q^(((n : ℤ)+1) : ℤ)))] q q (m-n))) * (((pochList [(U * q),((-V) * q)] q (n)) / (pochList [q,(-q)] q (n))) * (phi [(q^((-((n : ℤ))) : ℤ)),((U * V) * (q^(((n : ℤ)+1) : ℤ))),(s * z),(s / z)] [(U * q),((-V) * q),(-q)] q q (n))))) := by
  sorry

end FiniteQBenchmark.Identity205
