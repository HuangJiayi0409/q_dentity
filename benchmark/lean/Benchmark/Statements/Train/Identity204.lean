import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-9.Ex17i — 终止 Askey–Wilson 双线性展开（修订）
Original representative source: GR2-9.Ex17i
Frozen statement: formulas/train/FQI-SRC-GR2-9.Ex17i.md
Source formula:
\sum_{n=0}^N\frac{(q^{-N},UVq^{N-1};q)_n(1-abcdq^{2n-1})(abcd/q,ab,ac,-ab;q)_nq^{n(n+1)/2}(d/a)^n}{(U,-V;q)_n(1-abcd/q)(q,bd;q)_n(abcd;q)_{2n}}{}_4\phi_3^{[N-n]}(q^{n-N},UVq^{n+N-1},abq^n,-cdq^n;abcdq^{2n},Uq^n,-Vq^n;q,q)r_n(z)r_n(v)=(-1)^N\frac{(-U,V;q)_N}{(U,-V;q)_N}\sum_{m=0}^N\frac{(q^{-N},UVq^{N-1},-ab,dz,d/z,dv,d/v;q)_mq^m}{(q,ad,ad,bd,-U,V,d/a;q)_m}W_{10}^{[m]}(aq^{-m}/d;q^{1-m}/(bd),q^{1-m}/(cd),q^{-m},az,a/z,av,a/v;q,bcq/(ad)).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity204
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d U V z v q : K) (N : ℕ)
 (hbase : regular q) (hnz : U*V ≠ 0)
 (h_domain : ∀ n ∈ Finset.range (N+1), (q ≠ 0 ∧
    a ≠ 0 ∧
    ((((pochList [U,(-V)] q (n)) * (1 - ((((a * b) * c) * d) / q))) * (pochList [q,(b * d)] q (n))) * (pochList [(((a * b) * c) * d)] q (2*n))) ≠ 0 ∧
    phiDefined [((((a * b) * c) * d) * (q^((2*(n : ℤ)) : ℤ))),(U * (q^(((n : ℤ)) : ℤ))),((-V) * (q^(((n : ℤ)) : ℤ)))] q (N-n) ∧
    z ≠ 0 ∧
    phiDefined [(a * b),(a * c),(a * d)] q (n) ∧
    v ≠ 0) ∧
    (pochList [U,(-V)] q (N)) ≠ 0 ∧
    ∀ m ∈ Finset.range (N+1), (z ≠ 0 ∧
    v ≠ 0 ∧
    a ≠ 0 ∧
    (pochList [q,(a * d),(a * d),(b * d),(-U),V,(d / a)] q (m)) ≠ 0 ∧
    d ≠ 0 ∧
    (a * d) ≠ 0 ∧
    (b * d) ≠ 0 ∧
    (c * d) ≠ 0 ∧
    wDefined ((a * (q^((-(m : ℤ)) : ℤ))) / d) [((q^((1-(m : ℤ)) : ℤ)) / (b * d)),((q^((1-(m : ℤ)) : ℤ)) / (c * d)),(q^((-(m : ℤ)) : ℤ)),(a * z),(a / z),(a * v),(a / v)] q (m))) :
 (∑ n ∈ Finset.range (N+1), (((((((((pochList [(q^((-(N : ℤ)) : ℤ)),((U * V) * (q^(((N : ℤ)-1) : ℤ)))] q (n)) * (1 - ((((a * b) * c) * d) * (q^((2*(n : ℤ)-1) : ℤ))))) * (pochList [((((a * b) * c) * d) / q),(a * b),(a * c),((-a) * b)] q (n))) * (q^(((n : ℤ)*((n : ℤ)+1)/2) : ℤ))) * ((d / a)^n)) / ((((pochList [U,(-V)] q (n)) * (1 - ((((a * b) * c) * d) / q))) * (pochList [q,(b * d)] q (n))) * (pochList [(((a * b) * c) * d)] q (2*n)))) * (phi [(q^(((n : ℤ)-(N : ℤ)) : ℤ)),((U * V) * (q^(((n : ℤ)+(N : ℤ)-1) : ℤ))),((a * b) * (q^(((n : ℤ)) : ℤ))),(((-c) * d) * (q^(((n : ℤ)) : ℤ)))] [((((a * b) * c) * d) * (q^((2*(n : ℤ)) : ℤ))),(U * (q^(((n : ℤ)) : ℤ))),((-V) * (q^(((n : ℤ)) : ℤ)))] q q (N-n))) * (phi [(q^((-((n : ℤ))) : ℤ)),((((a * b) * c) * d) * (q^(((n : ℤ)-1) : ℤ))),(a * z),(a / z)] [(a * b),(a * c),(a * d)] q q (n))) * (phi [(q^((-((n : ℤ))) : ℤ)),((((a * b) * c) * d) * (q^(((n : ℤ)-1) : ℤ))),(a * v),(a / v)] [(a * b),(a * c),(a * d)] q q (n)))) = (((((-1:K)^N) * (pochList [(-U),V] q (N))) / (pochList [U,(-V)] q (N))) * (∑ m ∈ Finset.range (N+1), ((((pochList [(q^((-(N : ℤ)) : ℤ)),((U * V) * (q^(((N : ℤ)-1) : ℤ))),((-a) * b),(d * z),(d / z),(d * v),(d / v)] q (m)) * (q^(((m : ℤ)) : ℤ))) / (pochList [q,(a * d),(a * d),(b * d),(-U),V,(d / a)] q (m))) * (wellPoisedRaw ((a * (q^((-(m : ℤ)) : ℤ))) / d) [((q^((1-(m : ℤ)) : ℤ)) / (b * d)),((q^((1-(m : ℤ)) : ℤ)) / (c * d)),(q^((-(m : ℤ)) : ℤ)),(a * z),(a / z),(a * v),(a / v)] q (((b * c) * q) / (a * d)) (m))))) := by
  sorry

end FiniteQBenchmark.Identity204
