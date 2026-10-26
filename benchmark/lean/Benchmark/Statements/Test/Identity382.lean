import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-2.108 — Mock theta 相关的有限 Bailey 对
Original representative source: SILLS-2.108
Frozen statement: formulas/test/FQI-SRC-SILLS-2.108.md
Source formula:
\mathcal B_n[\alpha;1,q]=1/(-q;q)_n,\qquad \alpha_0=1,\quad\alpha_r=q^{r(3r+1)/2}\sum_{j=-r}^{r}(-1)^jq^{-j^2}-q^{r(3r-1)/2}\sum_{j=-r+1}^{r-1}(-1)^jq^{-j^2}\ (r\ge1)
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity382
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n : ℕ)
 (hq : q ≠ 0)
 (h_domain : ∀ r ∈ Finset.range (n+1), (((pochList [q] q (n-r)) * (pochList [(1 * q)] q (n+r))) ≠ 0) ∧
    (pochList [(-q)] q (n)) ≠ 0) :
 (∑ r ∈ Finset.range (n+1), ((if r = 0 then 1 else (((q^(r*(3*r+1)/2)) * (∑ j ∈ Finset.Icc (-(r:ℤ) : ℤ) (r : ℤ), ((-1:K)^j*q^(-j*j)))) - ((q^(r*(3*r-1)/2)) * (∑ j ∈ Finset.Icc (-(r:ℤ)+1 : ℤ) ((r:ℤ)-1 : ℤ), ((-1:K)^j*q^(-j*j)))))) / ((pochList [q] q (n-r)) * (pochList [(1 * q)] q (n+r))))) = (1 / (pochList [(-q)] q (n))) := by
  sorry

end FiniteQBenchmark.Identity382
