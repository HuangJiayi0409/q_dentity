import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex21 — Askey–Wilson 有限卷积恒等式
Original representative source: GR2-8.Ex21
Frozen statement: formulas/test/FQI-SRC-GR2-8.Ex21.md
Source formula:
\sum_{k=0}^{m+n}b^{m-k}\begin{bmatrix}m+n\\k\end{bmatrix}_q\frac{(b^2;q)_n(a^2b^2c^2q^{m+n-1};q)_k(c^2;q)_m}{(c^2,b^2c^2q^{k-1};q)_k(b^2c^2q^{2k};q)_{m+n-k}}{}_4\phi_3^{[\min(k,n)]}(q^{-k},b^2c^2q^{k-1},q^{-n},a^2b^2q^{n-1};b^2,a^2b^2c^2q^{m+n-1},q^{-m-n};q,q)P_k(w_2;bw_1,b/w_1,cs,c/s)P_{m+n-k}(w_1;at,a/t,bcsq^k,bcq^k/s)=P_n(w_1;at,a/t,bw_2,b/w_2)P_m(w_2;abtq^n,abq^n/t,cs,c/s).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity191
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c s t w1 w2 q : K) (m n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [a,b,c,s,t,w1,w2], v ≠ 0)
 (h_domain : ∀ k ∈ Finset.range (m+n+1), (((pochList [(c * c),((((b * b) * c) * c) * (q^(((k : ℤ)-1) : ℤ)))] q (k)) * (pochList [((((b * b) * c) * c) * (q^((2*(k : ℤ)) : ℤ)))] q (m+n-k))) ≠ 0 ∧
    phiDefined [(b * b),((((((a * a) * b) * b) * c) * c) * (q^(((m : ℤ)+(n : ℤ)-1) : ℤ))),(q^((-(m : ℤ)-(n : ℤ)) : ℤ))] q (min k n) ∧
    w1 ≠ 0 ∧
    s ≠ 0 ∧
    w2 ≠ 0 ∧
    phiDefined [((b * w1) * (b / w1)),((b * w1) * (c * s)),((b * w1) * (c / s))] q (k) ∧
    (b * w1) ≠ 0 ∧
    t ≠ 0 ∧
    phiDefined [((a * t) * (a / t)),((a * t) * (((b * c) * s) * (q^(((k : ℤ)) : ℤ)))),((a * t) * (((b * c) * (q^(((k : ℤ)) : ℤ))) / s))] q (m+n-k) ∧
    (a * t) ≠ 0) ∧
    t ≠ 0 ∧
    w2 ≠ 0 ∧
    w1 ≠ 0 ∧
    phiDefined [((a * t) * (a / t)),((a * t) * (b * w2)),((a * t) * (b / w2))] q (n) ∧
    (a * t) ≠ 0 ∧
    s ≠ 0 ∧
    phiDefined [((((a * b) * t) * (q^(((n : ℤ)) : ℤ))) * (((a * b) * (q^(((n : ℤ)) : ℤ))) / t)),((((a * b) * t) * (q^(((n : ℤ)) : ℤ))) * (c * s)),((((a * b) * t) * (q^(((n : ℤ)) : ℤ))) * (c / s))] q (m) ∧
    (((a * b) * t) * (q^(((n : ℤ)) : ℤ))) ≠ 0) :
 (∑ k ∈ Finset.range (m+n+1), (((((((((b^(((m : ℤ)-(k : ℤ)) : ℤ)) * (gaussian q (m+n) k)) * (pochList [(b * b)] q (n))) * (pochList [((((((a * a) * b) * b) * c) * c) * (q^(((m : ℤ)+(n : ℤ)-1) : ℤ)))] q (k))) * (pochList [(c * c)] q (m))) / ((pochList [(c * c),((((b * b) * c) * c) * (q^(((k : ℤ)-1) : ℤ)))] q (k)) * (pochList [((((b * b) * c) * c) * (q^((2*(k : ℤ)) : ℤ)))] q (m+n-k)))) * (phi [(q^((-(k : ℤ)) : ℤ)),((((b * b) * c) * c) * (q^(((k : ℤ)-1) : ℤ))),(q^((-(n : ℤ)) : ℤ)),((((a * a) * b) * b) * (q^(((n : ℤ)-1) : ℤ)))] [(b * b),((((((a * a) * b) * b) * c) * c) * (q^(((m : ℤ)+(n : ℤ)-1) : ℤ))),(q^((-(m : ℤ)-(n : ℤ)) : ℤ))] q q (min k n))) * (askeyWilson (w2) ((b * w1)) ((b / w1)) ((c * s)) ((c / s)) (q) (k))) * (askeyWilson (w1) ((a * t)) ((a / t)) ((((b * c) * s) * (q^(((k : ℤ)) : ℤ)))) ((((b * c) * (q^(((k : ℤ)) : ℤ))) / s)) (q) (m+n-k)))) = ((askeyWilson (w1) ((a * t)) ((a / t)) ((b * w2)) ((b / w2)) (q) (n)) * (askeyWilson (w2) ((((a * b) * t) * (q^(((n : ℤ)) : ℤ)))) ((((a * b) * (q^(((n : ℤ)) : ℤ))) / t)) ((c * s)) ((c / s)) (q) (m))) := by
  sorry

end FiniteQBenchmark.Identity191
