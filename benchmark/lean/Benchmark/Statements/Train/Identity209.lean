import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-11.6.21-p0 — 有限支撑的多底数序列展开（修订）
Original representative source: GR2-11.6.21-p0
Frozen statement: formulas/train/FQI-SRC-GR2-11.6.21-p0.md
Source formula:
\sum_{j=0}^N\frac{A_jB_j(xw)^j}{(q;q)_j}=\sum_{n=0}^N\frac{(1-\gamma(rst/q)^n)(1-\sigma(r/q)^n)(-x)^nq^{n+\binom n2}}{(q;q)_n}\sum_{k=0}^{N-n}\frac{(1-\gamma\sigma^{-1}(st)^{n+k})B_{n+k}x^k(s/q)^{\binom{k+1}2}}{(s;s)_k(\gamma rs^{n+k}t/q;rt/q)_n(\sigma rs^{1-n-k}/q;rs/q)_n}\sum_{j=0}^n\frac{(1-\gamma\sigma^{-1}s^{n+k}t^nq^{j-n})(1-s^{-k}q^{j-n})(q^{-n};q)_j}{(1-s^{j-n-k})(q;q)_j}(\gamma\sigma^{-1}(st)^{n+1}q^{j-n-1};st/q)_{k-1}(\gamma\sigma^{-1}s^{n+k}t^{j+1};t)_{n-j-1}(\gamma rs^jt/q;rt/q)_j(\gamma(rst)^{j+1}q^{-j-2};rst/q^2)_{n-j-1}(\sigma rs^{1-j}/q;rs/q)_j(\sigma r^{j+1}q^{-j};r)_{n-j-1}A_jC_{j,n+k-j}w^jq^{n(j-n-k)}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity209
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q r s t gamma sigma x w : K) (N : ℕ) (A B : ℕ → K) (C : ℕ → ℕ → K)
 (hnz : r*s*t*q*gamma*sigma ≠ 0) (hB : ∀ j, N < j → B j = 0) (hC : ∀ j, C j 0 = 1)
 (h_domain : ∀ j ∈ Finset.range (N+1), ((pochList [q] q (j)) ≠ 0) ∧
    ∀ n ∈ Finset.range (N+1), (q ≠ 0 ∧
    (pochList [q] q (n)) ≠ 0 ∧
    ∀ k ∈ Finset.range (N-n+1), (sigma ≠ 0 ∧
    q ≠ 0 ∧
    (((pochList [s] s (k)) * (pochList [((((gamma * r) * (s^(((n : ℤ)+(k : ℤ)) : ℤ))) * t) / q)] ((r * t) / q) (n))) * (pochList [(((sigma * r) * (s^((1-(n : ℤ)-(k : ℤ)) : ℤ))) / q)] ((r * s) / q) (n))) ≠ 0 ∧
    ∀ j ∈ Finset.range (n+1), (sigma ≠ 0 ∧
    ¬ ((j = n ∧ k = 0) ∨ s = q) → (1 - (s^(((j : ℤ)-(n : ℤ)-(k : ℤ)) : ℤ))) ≠ 0 ∧
    (pochList [q] q (j)) ≠ 0 ∧
    q ≠ 0 ∧
    pochListIntDefined [(((gamma / sigma) * ((s * t)^(((n : ℤ)+1) : ℤ))) * (q^(((j : ℤ)-(n : ℤ)-1) : ℤ)))] ((s * t) / q) ((k : ℤ)-1) ∧
    pochListIntDefined [(((gamma / sigma) * (s^(((n : ℤ)+(k : ℤ)) : ℤ))) * (t^(((j : ℤ)+1) : ℤ)))] t ((n : ℤ)-(j : ℤ)-1) ∧
    (q^2) ≠ 0 ∧
    pochListIntDefined [((gamma * (((r * s) * t)^(((j : ℤ)+1) : ℤ))) * (q^((-(j : ℤ)-2) : ℤ)))] (((r * s) * t) / (q^2)) ((n : ℤ)-(j : ℤ)-1) ∧
    pochListIntDefined [((sigma * (r^(((j : ℤ)+1) : ℤ))) * (q^((-(j : ℤ)) : ℤ)))] r ((n : ℤ)-(j : ℤ)-1))))) :
 (∑ j ∈ Finset.range (N+1), ((((A j) * (B j)) * ((x * w)^j)) / (pochList [q] q (j)))) = (∑ n ∈ Finset.range (N+1), ((((((1 - (gamma * ((((r * s) * t) / q)^(((n : ℤ)) : ℤ)))) * (1 - (sigma * ((r / q)^(((n : ℤ)) : ℤ))))) * ((-x)^n)) * (q^(((n : ℤ)+(n : ℤ)*((n : ℤ)-1)/2) : ℤ))) / (pochList [q] q (n))) * (∑ k ∈ Finset.range (N-n+1), ((((((1 - ((gamma / sigma) * ((s * t)^(((n : ℤ)+(k : ℤ)) : ℤ)))) * (B (n+k))) * (x^k)) * ((s / q)^(((k : ℤ)*((k : ℤ)+1)/2) : ℤ))) / (((pochList [s] s (k)) * (pochList [((((gamma * r) * (s^(((n : ℤ)+(k : ℤ)) : ℤ))) * t) / q)] ((r * t) / q) (n))) * (pochList [(((sigma * r) * (s^((1-(n : ℤ)-(k : ℤ)) : ℤ))) / q)] ((r * s) / q) (n)))) * (∑ j ∈ Finset.range (n+1), ((((((((((((((1 - ((((gamma / sigma) * (s^(((n : ℤ)+(k : ℤ)) : ℤ))) * (t^(((n : ℤ)) : ℤ))) * (q^(((j : ℤ)-(n : ℤ)) : ℤ)))) * (if (j = n ∧ k = 0) ∨ s = q then (1 : K) else (1 - ((s^((-(k : ℤ)) : ℤ)) * (q^(((j : ℤ)-(n : ℤ)) : ℤ))))/(1 - (s^(((j : ℤ)-(n : ℤ)-(k : ℤ)) : ℤ))))) * (pochList [(q^((-(n : ℤ)) : ℤ))] q (j))) / (pochList [q] q (j))) * (pochListInt [(((gamma / sigma) * ((s * t)^(((n : ℤ)+1) : ℤ))) * (q^(((j : ℤ)-(n : ℤ)-1) : ℤ)))] ((s * t) / q) ((k : ℤ)-1))) * (pochListInt [(((gamma / sigma) * (s^(((n : ℤ)+(k : ℤ)) : ℤ))) * (t^(((j : ℤ)+1) : ℤ)))] t ((n : ℤ)-(j : ℤ)-1))) * (pochList [((((gamma * r) * (s^(((j : ℤ)) : ℤ))) * t) / q)] ((r * t) / q) (j))) * (pochListInt [((gamma * (((r * s) * t)^(((j : ℤ)+1) : ℤ))) * (q^((-(j : ℤ)-2) : ℤ)))] (((r * s) * t) / (q^2)) ((n : ℤ)-(j : ℤ)-1))) * (pochList [(((sigma * r) * (s^((1-(j : ℤ)) : ℤ))) / q)] ((r * s) / q) (j))) * (pochListInt [((sigma * (r^(((j : ℤ)+1) : ℤ))) * (q^((-(j : ℤ)) : ℤ)))] r ((n : ℤ)-(j : ℤ)-1))) * (A j)) * (C j (n+k-j))) * (w^j)) * (q^(((n : ℤ)*((j : ℤ)-(n : ℤ)-(k : ℤ))) : ℤ)))))))) := by
  sorry

end FiniteQBenchmark.Identity209
