import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex28 — 相伴连续 q-超球线性化公式
Original representative source: GR2-8.Ex28
Frozen statement: formulas/train/FQI-SRC-GR2-8.Ex28.md
Source formula:
C_m^\alpha(z;\beta)C_n^\alpha(z;\beta)=\sum_{k=0}^{\min(m,n)}L_kC_{m+n-2k}^\alpha(z;\beta),\quad L_k=\frac{(q;q)_m(q;q)_n(\alpha q;q)_{m+n-2k}(\alpha\beta;q)_{m-k}(\alpha\beta;q)_{n-k}(\alpha\beta;q)_k}{(\alpha q;q)_m(\alpha q;q)_n(\alpha\beta^2;q)_{m+n-2k}(q;q)_{m-k}(q;q)_{n-k}(q;q)_k}\frac{(\alpha\beta^2;q)_{m+n-k}(q^{k-m-n}/\alpha;q)_k\alpha^k(1-\alpha\beta q^{m+n-2k})}{(\alpha\beta q;q)_{m+n-k}(q^{k-m-n};q)_k(1-\alpha\beta)}W_{10}^{[k]}(q^{k-m-n-1};q^{k-m-n}/(\alpha\beta),q^{k-m-n}/(\alpha\beta),\alpha,\alpha\beta^2/q,q^{k-m},q^{k-n},q^{-k};q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity195
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z alpha beta q : K) (m n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [alpha,beta,z], v ≠ 0)
 (h_domain : ∀ j < (m), 1-alpha*beta*q^j ≠ 0 ∧
    ∀ j < (m), 1-alpha*q^(j+1) ≠ 0 ∧
    ∀ j < (n), 1-alpha*beta*q^j ≠ 0 ∧
    ∀ j < (n), 1-alpha*q^(j+1) ≠ 0 ∧
    ∀ k ∈ Finset.range (min m n+1), (((((((pochList [(alpha * q)] q (m)) * (pochList [(alpha * q)] q (n))) * (pochList [((alpha * beta) * beta)] q (m+n-2*k))) * (pochList [q] q (m-k))) * (pochList [q] q (n-k))) * (pochList [q] q (k))) ≠ 0 ∧
    alpha ≠ 0 ∧
    (((pochList [((alpha * beta) * q)] q (m+n-k)) * (pochList [(q^(((k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ))] q (k))) * (1 - (alpha * beta))) ≠ 0 ∧
    (alpha * beta) ≠ 0 ∧
    q ≠ 0 ∧
    wDefined (q^(((k : ℤ)-(m : ℤ)-(n : ℤ)-1) : ℤ)) [((q^(((k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ)) / (alpha * beta)),((q^(((k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ)) / (alpha * beta)),alpha,(((alpha * beta) * beta) / q),(q^(((k : ℤ)-(m : ℤ)) : ℤ)),(q^(((k : ℤ)-(n : ℤ)) : ℤ)),(q^((-(k : ℤ)) : ℤ))] q (firstTermination [(q^(((k : ℤ)-(m : ℤ)-(n : ℤ)-1) : ℤ)),((q^(((k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ)) / (alpha * beta)),((q^(((k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ)) / (alpha * beta)),alpha,(((alpha * beta) * beta) / q),(q^(((k : ℤ)-(m : ℤ)) : ℤ)),(q^(((k : ℤ)-(n : ℤ)) : ℤ)),(q^((-(k : ℤ)) : ℤ))] q (k)) ∧
    ∀ j < (m+n-2*k), 1-alpha*beta*q^j ≠ 0 ∧
    ∀ j < (m+n-2*k), 1-alpha*q^(j+1) ≠ 0)) :
 ((associatedUltra z alpha beta q (m)) * (associatedUltra z alpha beta q (n))) = (∑ k ∈ Finset.range (min m n+1), ((((((((((((((pochList [q] q (m)) * (pochList [q] q (n))) * (pochList [(alpha * q)] q (m+n-2*k))) * (pochList [(alpha * beta)] q (m-k))) * (pochList [(alpha * beta)] q (n-k))) * (pochList [(alpha * beta)] q (k))) / ((((((pochList [(alpha * q)] q (m)) * (pochList [(alpha * q)] q (n))) * (pochList [((alpha * beta) * beta)] q (m+n-2*k))) * (pochList [q] q (m-k))) * (pochList [q] q (n-k))) * (pochList [q] q (k)))) * (pochList [((alpha * beta) * beta)] q (m+n-k))) * (pochList [((q^(((k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ)) / alpha)] q (k))) * (alpha^(((k : ℤ)) : ℤ))) * (1 - ((alpha * beta) * (q^(((m : ℤ)+(n : ℤ)-2*(k : ℤ)) : ℤ))))) / (((pochList [((alpha * beta) * q)] q (m+n-k)) * (pochList [(q^(((k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ))] q (k))) * (1 - (alpha * beta)))) * (wellPoisedRaw (q^(((k : ℤ)-(m : ℤ)-(n : ℤ)-1) : ℤ)) [((q^(((k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ)) / (alpha * beta)),((q^(((k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ)) / (alpha * beta)),alpha,(((alpha * beta) * beta) / q),(q^(((k : ℤ)-(m : ℤ)) : ℤ)),(q^(((k : ℤ)-(n : ℤ)) : ℤ)),(q^((-(k : ℤ)) : ℤ))] q q (firstTermination [(q^(((k : ℤ)-(m : ℤ)-(n : ℤ)-1) : ℤ)),((q^(((k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ)) / (alpha * beta)),((q^(((k : ℤ)-(m : ℤ)-(n : ℤ)) : ℤ)) / (alpha * beta)),alpha,(((alpha * beta) * beta) / q),(q^(((k : ℤ)-(m : ℤ)) : ℤ)),(q^(((k : ℤ)-(n : ℤ)) : ℤ)),(q^((-(k : ℤ)) : ℤ))] q (k)))) * (associatedUltra z alpha beta q (m+n-2*k)))) := by
  sorry

end FiniteQBenchmark.Identity195
