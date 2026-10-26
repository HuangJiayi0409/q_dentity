import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-II-37 — 双底数有限差分消去
Original representative source: GR2-II-37
Frozen statement: formulas/train/FQI-SRC-GR2-II-37.md
Source formula:
(1-a/q)(1-b/q)\sum_{k=0}^n\frac{(ap^k,bp^{-k};q)_{n-1}(1-ap^{2k}/b)}{(p;p)_k(p;p)_{n-k}(ap^k/b;p)_{n+1}}(-1)^kp^{k(k-1)/2}=\delta_{n,0}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity254
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b p q : K) (n : ℕ)
 (hbase : regular q) (hp : regular p) (hab : a*b ≠ 0)
 (h_domain : q ≠ 0 ∧
    ∀ k ∈ Finset.range (n+1), (pochListIntDefined [(a * (p^(((k : ℤ)) : ℤ))),(b * (p^((-(k : ℤ)) : ℤ)))] q ((n : ℤ)-1) ∧
    b ≠ 0 ∧
    (((pochList [p] p (k)) * (pochList [p] p (n-k))) * (pochList [((a * (p^(((k : ℤ)) : ℤ))) / b)] p (n+1))) ≠ 0)) :
 (((1 - (a / q)) * (1 - (b / q))) * (∑ k ∈ Finset.range (n+1), (((((pochListInt [(a * (p^(((k : ℤ)) : ℤ))),(b * (p^((-(k : ℤ)) : ℤ)))] q ((n : ℤ)-1)) * (1 - ((a * (p^((2*(k : ℤ)) : ℤ))) / b))) / (((pochList [p] p (k)) * (pochList [p] p (n-k))) * (pochList [((a * (p^(((k : ℤ)) : ℤ))) / b)] p (n+1)))) * ((-1 : K)^k)) * (p^(((k : ℤ)*((k : ℤ)-1)/2) : ℤ))))) = (if (n) = (0) then (1 : K) else 0) := by
  sorry

end FiniteQBenchmark.Identity254
