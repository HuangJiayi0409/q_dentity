import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.6.2 — Askey–Wilson 有限连接公式
Original representative source: GR2-7.6.2
Frozen statement: formulas/train/FQI-SRC-GR2-7.6.2.md
Source formula:
P_n(z;\alpha,\beta,\gamma,d)=\sum_{k=0}^nc_{k,n}P_k(z;a,b,c,d),\quad c_{k,n}=\frac{(\alpha d,\beta d,\gamma d,q;q)_n(\alpha\beta\gamma dq^{n-1};q)_kq^{k^2-nk}d^{k-n}}{(\alpha d,\beta d,\gamma d,q,abcdq^{k-1};q)_k(q;q)_{n-k}}{}_5\phi_4^{[n-k]}(q^{k-n},\alpha\beta\gamma dq^{n+k-1},adq^k,bdq^k,cdq^k;abcdq^{2k},\alpha dq^k,\beta dq^k,\gamma dq^k;q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity138
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z alpha beta gamma a b c d q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [alpha,a,d,z], v ≠ 0)
 (h_domain : z ≠ 0 ∧
    phiDefined [(alpha * beta),(alpha * gamma),(alpha * d)] q (n) ∧
    alpha ≠ 0 ∧
    ∀ k ∈ Finset.range (n+1), (((pochList [(alpha * d),(beta * d),(gamma * d),q,((((a * b) * c) * d) * (q^(((k : ℤ)-1) : ℤ)))] q (k)) * (pochList [q] q (n-k))) ≠ 0 ∧
    phiDefined [((((a * b) * c) * d) * (q^((2*(k : ℤ)) : ℤ))),((alpha * d) * (q^(((k : ℤ)) : ℤ))),((beta * d) * (q^(((k : ℤ)) : ℤ))),((gamma * d) * (q^(((k : ℤ)) : ℤ)))] q (n-k) ∧
    z ≠ 0 ∧
    phiDefined [(a * b),(a * c),(a * d)] q (k) ∧
    a ≠ 0)) :
 (askeyWilson (z) (alpha) (beta) (gamma) (d) (q) (n)) = (∑ k ∈ Finset.range (n+1), (((((((pochList [(alpha * d),(beta * d),(gamma * d),q] q (n)) * (pochList [((((alpha * beta) * gamma) * d) * (q^(((n : ℤ)-1) : ℤ)))] q (k))) * (q^(((k : ℤ)*(k : ℤ)-(n : ℤ)*(k : ℤ)) : ℤ))) * (d^(((k : ℤ)-(n : ℤ)) : ℤ))) / ((pochList [(alpha * d),(beta * d),(gamma * d),q,((((a * b) * c) * d) * (q^(((k : ℤ)-1) : ℤ)))] q (k)) * (pochList [q] q (n-k)))) * (phi [(q^(((k : ℤ)-(n : ℤ)) : ℤ)),((((alpha * beta) * gamma) * d) * (q^(((n : ℤ)+(k : ℤ)-1) : ℤ))),((a * d) * (q^(((k : ℤ)) : ℤ))),((b * d) * (q^(((k : ℤ)) : ℤ))),((c * d) * (q^(((k : ℤ)) : ℤ)))] [((((a * b) * c) * d) * (q^((2*(k : ℤ)) : ℤ))),((alpha * d) * (q^(((k : ℤ)) : ℤ))),((beta * d) * (q^(((k : ℤ)) : ℤ))),((gamma * d) * (q^(((k : ℤ)) : ℤ)))] q q (n-k))) * (askeyWilson (z) (a) (b) (c) (d) (q) (k)))) := by
  sorry

end FiniteQBenchmark.Identity138
