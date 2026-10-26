import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.Ex21-mixed — 双底数与普通超几何的混合有限变换
Original representative source: GR2-3.Ex21-mixed
Frozen statement: formulas/train/FQI-SRC-GR2-3.Ex21-mixed.md
Source formula:
\sum_{k=0}^nK_k(a,b,c;p,q)\frac{(C-A-n)_k(-B-C-n)_k(\mu B-\mu A-n)_k(-n)_k}{(-\mu C-n)_k(\mu B+\mu C-\mu A-n)_k(-A-n)_k(-B-n)_k}=T_n(a,b,c;p,q)\frac{n!(\mu A+1-\mu B)_n(A+1-C)_n(B+C+1)_n}{(A+1)_n(B+1)_n(\mu C+1)_n(\mu A+1-\mu B-\mu C)_n}\sum_{k=0}^n\frac{(A+k+k/\mu)(B+k-k/\mu)}{AB}\frac{(A)_k(B)_k(\mu C)_k(\mu A-\mu B-\mu C)_k}{k!(\mu A+1-\mu B)_k(A+1-C)_k(B+C+1)_k}R_{n,k}(a,b,c;p,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity113
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c p q A B C mu : K) [CharZero K] (n : ℕ)
 (hbase : regular q) (hp : regular p) (hnz : ∀ x ∈ [A,B,mu,a,b,c], x ≠ 0)
 (h_domain : ∀ k ∈ Finset.range (n+1), (((1 - a) * (1 - b)) ≠ 0 ∧
    (b * c) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    ((pochList [q,((a * q) / b)] q (k)) * (pochList [((a * p) / c),((b * c) * p)] p (k))) ≠ 0 ∧
    (risingList [(((-mu) * C) - (n:K)),((((mu * B) + (mu * C)) - (mu * A)) - (n:K)),((-A) - (n:K)),((-B) - (n:K))] (k)) ≠ 0) ∧
    (b * c) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    ((pochList [q,((a * q) / b)] q (n)) * (pochList [((a * p) / c),((b * c) * p)] p (n))) ≠ 0 ∧
    (risingList [(A + 1),(B + 1),((mu * C) + 1),((((mu * A) + 1) - (mu * B)) - (mu * C))] (n)) ≠ 0 ∧
    ∀ k ∈ Finset.range (n+1), (mu ≠ 0 ∧
    (A * B) ≠ 0 ∧
    ((Nat.factorial k:K) * (risingList [(((mu * A) + 1) - (mu * B)),((A + 1) - C),((B + C) + 1)] (k))) ≠ 0 ∧
    a ≠ 0 ∧
    (b * c) ≠ 0 ∧
    c ≠ 0 ∧
    b ≠ 0 ∧
    ((pochList [((q^((-(n : ℤ)) : ℤ)) / c),(((b * c) * (q^((-(n : ℤ)) : ℤ))) / a)] q (k)) * (pochList [((p^((-(n : ℤ)) : ℤ)) / a),((p^((-(n : ℤ)) : ℤ)) / b)] p (k))) ≠ 0)) :
 (∑ k ∈ Finset.range (n+1), (((((((((1 - ((a * (p^(((k : ℤ)) : ℤ))) * (q^(((k : ℤ)) : ℤ)))) * (1 - ((b * (p^(((k : ℤ)) : ℤ))) * (q^((-(k : ℤ)) : ℤ))))) / ((1 - a) * (1 - b))) * (pochList [a,b] p (k))) * (pochList [c,(a / (b * c))] q (k))) * (q^(((k : ℤ)) : ℤ))) / ((pochList [q,((a * q) / b)] q (k)) * (pochList [((a * p) / c),((b * c) * p)] p (k)))) * (risingList [((C - A) - (n:K)),(((-B) - C) - (n:K)),(((mu * B) - (mu * A)) - (n:K)),(-(n:K))] (k))) / (risingList [(((-mu) * C) - (n:K)),((((mu * B) + (mu * C)) - (mu * A)) - (n:K)),((-A) - (n:K)),((-B) - (n:K))] (k)))) = (((((((pochList [(a * p),(b * p)] p (n)) * (pochList [(c * q),((a * q) / (b * c))] q (n))) / ((pochList [q,((a * q) / b)] q (n)) * (pochList [((a * p) / c),((b * c) * p)] p (n)))) * (Nat.factorial n : K)) * (risingList [(((mu * A) + 1) - (mu * B)),((A + 1) - C),((B + C) + 1)] (n))) / (risingList [(A + 1),(B + 1),((mu * C) + 1),((((mu * A) + 1) - (mu * B)) - (mu * C))] (n))) * (∑ k ∈ Finset.range (n+1), (((((((A + (k:K)) + ((k:K) / mu)) * ((B + (k:K)) - ((k:K) / mu))) / (A * B)) * (risingList [A,B,(mu * C),(((mu * A) - (mu * B)) - (mu * C))] (k))) / ((Nat.factorial k:K) * (risingList [(((mu * A) + 1) - (mu * B)),((A + 1) - C),((B + C) + 1)] (k)))) * (((pochList [((c * (p^((-(n : ℤ)) : ℤ))) / a),((p^((-(n : ℤ)) : ℤ)) / (b * c))] p (k)) * (pochList [(q^((-(n : ℤ)) : ℤ)),((b * (q^((-(n : ℤ)) : ℤ))) / a)] q (k))) / ((pochList [((q^((-(n : ℤ)) : ℤ)) / c),(((b * c) * (q^((-(n : ℤ)) : ℤ))) / a)] q (k)) * (pochList [((p^((-(n : ℤ)) : ℤ)) / a),((p^((-(n : ℤ)) : ℤ)) / b)] p (k))))))) := by
  sorry

end FiniteQBenchmark.Identity113
