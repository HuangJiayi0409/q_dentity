import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.2.2 — Bailey 的有限序列双和展开
Original representative source: GR2-2.2.2
Frozen statement: formulas/train/FQI-SRC-GR2-2.2.2.md
Source formula:
\sum_{k=0}^n\frac{(b,c,q^{-n};q)_k}{(q,aq/b,aq/c;q)_k}A_k=\sum_{j=0}^n\frac{(aq/(bc),aq^j,q^{-n};q)_j}{(q,aq/b,aq/c;q)_j}(-1)^jq^{-j(j-1)/2}\sum_{i=0}^{n-j}\frac{(q^{j-n},aq^{2j};q)_i}{(q,aq^j;q)_i}q^{-ij}\left(\frac{bc}{aq}\right)^{i+j}A_{i+j}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity062
variable {K : Type*} [Field K]

theorem statement (a b c q : K) (A : ℕ → K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c], x ≠ 0)
 (ho : phiDefined [a*q/b,a*q/c] q n)
 (hi : ∀ j ≤ n, phiDefined [a*q^j] q (n-j)) :
 (∑ k ∈ Finset.range (n+1), pochList [b,c,q^(-(n : ℤ))] q k /
 pochList [q,a*q/b,a*q/c] q k*A k) =
 ∑ j ∈ Finset.range (n+1),
 pochList [a*q/(b*c),a*q^j,q^(-(n : ℤ))] q j/pochList [q,a*q/b,a*q/c] q j *
 (-1)^j*q^(-((j : ℤ)*(j-1)/2)) *
 ∑ i ∈ Finset.range (n-j+1),
 pochList [q^((j : ℤ)-n),a*q^(2*j)] q i/pochList [q,a*q^j] q i *
 q^(-((i : ℤ)*j))*(b*c/(a*q))^(i+j)*A (i+j) := by
  sorry

end FiniteQBenchmark.Identity062
