import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex20 — 特殊 Askey–Wilson 的有限线性化
Original representative source: GR2-8.Ex20
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex20.md
Source formula:
P_m(z;a,q/a,-b,-q/b)P_n(z;a,q/a,-b,-q/b)=\sum_{k=0}^{2\min(m,n)}L_kP_{m+n-k}(z;a,q/a,-b,-q/b),\quad L_k=\frac{(q;q)_{2m}(q;q)_{2n}(q;q)_{m+n}}{(q;q)_m(q;q)_n(q;q)_{2m+2n}}b^{-k}q^{(3m+3n+1)k-3\binom k2}\frac{1-q^{2m+2n+1-2k}}{1-q^{2m+2n+1-k}}\frac{(q^{-2m-2n},-bq^{-m-n}/a,-abq^{-m-n-1};q)_k}{(q,q^{-2m},q^{-2n},q^{-m-n};q)_k}T_k(-bq^{m+n+1-k}/a,-bq^{-m-n}/a)T_k(-abq^{m+n-k},-abq^{-m-n-1}),\quad T_k(U,V)=\sum_{j=\max(0,k-m,k-n)}^{\min(k,m,n)}\frac{(q^{-k},q^{-m},q^{-n},U;q)_j(q^{-m},q^{-n};q)_{k-j}}{(q,V;q)_j}q^{(2k-m-n)j-j^2}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity190
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b z q : ℝ) (m n : ℕ)
 (hbase : regular q) (ha : 0 < a) (hb : 0 < b) (hz : z ≠ 0)
 (h_domain : a ≠ 0 ∧
    b ≠ 0 ∧
    z ≠ 0 ∧
    phiDefined [(a * (q / a)),(a * (-b)),(a * ((-q) / b))] q (m) ∧
    phiDefined [(a * (q / a)),(a * (-b)),(a * ((-q) / b))] q (n) ∧
    ∀ k ∈ Finset.range (2*min m n+1), ((((pochList [q] q (m)) * (pochList [q] q (n))) * (pochList [q] q (2*m+2*n))) ≠ 0 ∧
    (1 - (q^((2*(m : ℤ)+2*(n : ℤ)+1-(k : ℤ)) : ℤ))) ≠ 0 ∧
    a ≠ 0 ∧
    (pochList [q,(q^((-2*(m : ℤ)) : ℤ)),(q^((-2*(n : ℤ)) : ℤ)),(q^((-(m : ℤ)-(n : ℤ)) : ℤ))] q (k)) ≠ 0 ∧
    ∀ j ∈ Finset.Icc (max (k-m) (k-n)) (min k (min m n)), (a ≠ 0 ∧
    (pochList [q,(((-b) * (q^((-(m : ℤ)-(n : ℤ)) : ℤ))) / a)] q (j)) ≠ 0) ∧
    ∀ j ∈ Finset.Icc (max (k-m) (k-n)) (min k (min m n)), ((pochList [q,(((-a) * b) * (q^((-(m : ℤ)-(n : ℤ)-1) : ℤ)))] q (j)) ≠ 0) ∧
    b ≠ 0 ∧
    z ≠ 0 ∧
    phiDefined [(a * (q / a)),(a * (-b)),(a * ((-q) / b))] q (m+n-k))) :
 ((askeyWilson (z) (a) ((q / a)) ((-b)) (((-q) / b)) (q) (m)) * (askeyWilson (z) (a) ((q / a)) ((-b)) (((-q) / b)) (q) (n))) = (∑ k ∈ Finset.range (2*min m n+1), (((((((((((((pochList [q] q (2*m)) * (pochList [q] q (2*n))) * (pochList [q] q (m+n))) / (((pochList [q] q (m)) * (pochList [q] q (n))) * (pochList [q] q (2*m+2*n)))) * (b^((-(k : ℤ)) : ℤ))) * (q^(((3*(m : ℤ)+3*(n : ℤ)+1)*(k : ℤ)-3*((k : ℤ)*((k : ℤ)-1)/2)) : ℤ))) * (1 - (q^((2*(m : ℤ)+2*(n : ℤ)+1-2*(k : ℤ)) : ℤ)))) / (1 - (q^((2*(m : ℤ)+2*(n : ℤ)+1-(k : ℤ)) : ℤ)))) * (pochList [(q^((-2*(m : ℤ)-2*(n : ℤ)) : ℤ)),(((-b) * (q^((-(m : ℤ)-(n : ℤ)) : ℤ))) / a),(((-a) * b) * (q^((-(m : ℤ)-(n : ℤ)-1) : ℤ)))] q (k))) / (pochList [q,(q^((-2*(m : ℤ)) : ℤ)),(q^((-2*(n : ℤ)) : ℤ)),(q^((-(m : ℤ)-(n : ℤ)) : ℤ))] q (k))) * (∑ j ∈ Finset.Icc (max (k-m) (k-n)) (min k (min m n)), ((((pochList [(q^((-(k : ℤ)) : ℤ)),(q^((-(m : ℤ)) : ℤ)),(q^((-(n : ℤ)) : ℤ)),(((-b) * (q^(((m : ℤ)+(n : ℤ)+1-(k : ℤ)) : ℤ))) / a)] q (j)) * (pochList [(q^((-(m : ℤ)) : ℤ)),(q^((-(n : ℤ)) : ℤ))] q (k-j))) / (pochList [q,(((-b) * (q^((-(m : ℤ)-(n : ℤ)) : ℤ))) / a)] q (j))) * (q^(((2*(k : ℤ)-(m : ℤ)-(n : ℤ))*(j : ℤ)-(j : ℤ)*(j : ℤ)) : ℤ))))) * (∑ j ∈ Finset.Icc (max (k-m) (k-n)) (min k (min m n)), ((((pochList [(q^((-(k : ℤ)) : ℤ)),(q^((-(m : ℤ)) : ℤ)),(q^((-(n : ℤ)) : ℤ)),(((-a) * b) * (q^(((m : ℤ)+(n : ℤ)-(k : ℤ)) : ℤ)))] q (j)) * (pochList [(q^((-(m : ℤ)) : ℤ)),(q^((-(n : ℤ)) : ℤ))] q (k-j))) / (pochList [q,(((-a) * b) * (q^((-(m : ℤ)-(n : ℤ)-1) : ℤ)))] q (j))) * (q^(((2*(k : ℤ)-(m : ℤ)-(n : ℤ))*(j : ℤ)-(j : ℤ)*(j : ℤ)) : ℤ))))) * (askeyWilson (z) (a) ((q / a)) ((-b)) (((-q) / b)) (q) (m+n-k)))) := by
  sorry

end FiniteQBenchmark.Identity190
