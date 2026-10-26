import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.7.9-finite — 终止良配 4φ3 的 2φ1 变换
Original representative source: GR2-8.7.9-finite
Frozen statement: formulas/train/FQI-SRC-GR2-8.7.9-finite.md
Source formula:
\sum_{k=0}^n\frac{1-aq^{2k}}{1-a}\frac{(a,q^{-n};q)_k}{(q,w;q)_k}\left(\frac{w}{aq}\right)^k=\frac{(wq^{-n-1}/a;q)_n}{(w;q)_n}{}_2\phi_1^{[\max(0,n-1)]}(q^{-n},q^{1-n};wq^{-n}/a;q,wq^n).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity168
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a w q : K) (n : ℕ)
 (hbase : regular q) (hnz : ∀ v ∈ [a,w], v ≠ 0)
 (h_domain : ∀ k ∈ Finset.range (n+1), ((1 - a) ≠ 0 ∧
    (pochList [q,w] q (k)) ≠ 0 ∧
    (a * q) ≠ 0) ∧
    a ≠ 0 ∧
    (pochList [w] q (n)) ≠ 0 ∧
    phiDefined [((w * (q^((-(n : ℤ)) : ℤ))) / a)] q (n-1)) :
 (∑ k ∈ Finset.range (n+1), (((((1 - (a * (q^((2*(k : ℤ)) : ℤ)))) / (1 - a)) * (pochList [a,(q^((-(n : ℤ)) : ℤ))] q (k))) / (pochList [q,w] q (k))) * ((w / (a * q))^(((k : ℤ)) : ℤ)))) = (((pochList [((w * (q^((-(n : ℤ)-1) : ℤ))) / a)] q (n)) / (pochList [w] q (n))) * (phi [(q^((-(n : ℤ)) : ℤ)),(q^((1-(n : ℤ)) : ℤ))] [((w * (q^((-(n : ℤ)) : ℤ))) / a)] q (w * (q^(((n : ℤ)) : ℤ))) (n-1))) := by
  sorry

end FiniteQBenchmark.Identity168
