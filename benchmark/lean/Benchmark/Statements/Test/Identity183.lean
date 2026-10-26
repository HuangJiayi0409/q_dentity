import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex11 — Askey–Wilson 的有限加法公式
Original representative source: GR2-8.Ex11
Frozen statement: formulas/test/FQI-SRC-GR2-8.Ex11.md
Source formula:
P_n(v;a,as,-a,-as)=\sum_{k=0}^nA_{k,n}(z,w)P_k(v;azw,a/(zw),az/w,aw/z),\quad A_{k,n}=\frac{(q;q)_n(a^4q^n,a^4/q,a^2s,-a^2s,-a^2;q)_ka^{n-k}}{(q;q)_k(q;q)_{n-k}(a^4/q;q)_{2k}(a^2s,-a^2s,-a^2;q)_n}P_{n-k}(z;as^k,as^{k+1},-as^k,-as^{k+1})P_{n-k}(w;as^k,as^{k+1},-as^k,-as^{k+1}),\quad s^2=q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity183
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a z w v s q : K) (n : ℕ)
 (hbase : regular q) (hs : s^2 = q) (hnz : ∀ v ∈ [a,z,w,v], v ≠ 0)
 (h_domain : v ≠ 0 ∧
    phiDefined [(a * (a * s)),(a * (-a)),(a * ((-a) * s))] q (n) ∧
    a ≠ 0 ∧
    ∀ k ∈ Finset.range (n+1), (q ≠ 0 ∧
    ((((pochList [q] q (k)) * (pochList [q] q (n-k))) * (pochList [((a^4) / q)] q (2*k))) * (pochList [((a * a) * s),(((-a) * a) * s),((-a) * a)] q (n))) ≠ 0 ∧
    z ≠ 0 ∧
    phiDefined [((a * (s^(((k : ℤ)) : ℤ))) * (a * (s^(((k : ℤ)+1) : ℤ)))),((a * (s^(((k : ℤ)) : ℤ))) * ((-a) * (s^(((k : ℤ)) : ℤ)))),((a * (s^(((k : ℤ)) : ℤ))) * ((-a) * (s^(((k : ℤ)+1) : ℤ))))] q (n-k) ∧
    (a * (s^(((k : ℤ)) : ℤ))) ≠ 0 ∧
    w ≠ 0 ∧
    (z * w) ≠ 0 ∧
    v ≠ 0 ∧
    phiDefined [(((a * z) * w) * (a / (z * w))),(((a * z) * w) * ((a * z) / w)),(((a * z) * w) * ((a * w) / z))] q (k) ∧
    ((a * z) * w) ≠ 0)) :
 (askeyWilson (v) (a) ((a * s)) ((-a)) (((-a) * s)) (q) (n)) = (∑ k ∈ Finset.range (n+1), (((((((pochList [q] q (n)) * (pochList [((a^4) * (q^(((n : ℤ)) : ℤ))),((a^4) / q),((a * a) * s),(((-a) * a) * s),((-a) * a)] q (k))) * (a^(((n : ℤ)-(k : ℤ)) : ℤ))) / ((((pochList [q] q (k)) * (pochList [q] q (n-k))) * (pochList [((a^4) / q)] q (2*k))) * (pochList [((a * a) * s),(((-a) * a) * s),((-a) * a)] q (n)))) * (askeyWilson (z) ((a * (s^(((k : ℤ)) : ℤ)))) ((a * (s^(((k : ℤ)+1) : ℤ)))) (((-a) * (s^(((k : ℤ)) : ℤ)))) (((-a) * (s^(((k : ℤ)+1) : ℤ)))) (q) (n-k))) * (askeyWilson (w) ((a * (s^(((k : ℤ)) : ℤ)))) ((a * (s^(((k : ℤ)+1) : ℤ)))) (((-a) * (s^(((k : ℤ)) : ℤ)))) (((-a) * (s^(((k : ℤ)+1) : ℤ)))) (q) (n-k))) * (askeyWilson (v) (((a * z) * w)) ((a / (z * w))) (((a * z) / w)) (((a * w) / z)) (q) (k)))) := by
  sorry

end FiniteQBenchmark.Identity183
