import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-3.5-6 — Bailey 链第二步有限变换
Original representative source: SILLS-3.5-6
Frozen statement: formulas/test/FQI-SRC-SILLS-3.5-6.md
Source formula:
\mathcal B_n[\alpha;x,q]=\frac1{(xq/\rho_1,xq/\rho_2;q)_n}\sum_{j=0}^n\frac{(\rho_1,\rho_2;q)_j(xq/(\rho_1\rho_2);q)_{n-j}(xq/(\rho_1\rho_2))^j}{(q;q)_j(q;q)_{n-j}},\qquad \alpha_r=\frac{(\rho_1,\rho_2;q)_r(xq/(\rho_1\rho_2))^r}{(xq/\rho_1,xq/\rho_2;q)_r}\alpha_r^{(1,1,2)}(x,q)
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity383
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x rho1 rho2 q : K) (n : ℕ)
 (hrho : rho1*rho2 ≠ 0)
 (h_domain : ∀ r ∈ Finset.range (n+1), ((rho1 * rho2) ≠ 0 ∧
    rho1 ≠ 0 ∧
    rho2 ≠ 0 ∧
    (pochList [((x * q) / rho1),((x * q) / rho2)] q (r)) ≠ 0 ∧
    1 ∣ r → (1-x)*poch (q^1) (q^1) (r/1) ≠ 0 ∧
    ((pochList [q] q (n-r)) * (pochList [(x * q)] q (n+r))) ≠ 0) ∧
    rho1 ≠ 0 ∧
    rho2 ≠ 0 ∧
    (pochList [((x * q) / rho1),((x * q) / rho2)] q (n)) ≠ 0 ∧
    ∀ j ∈ Finset.range (n+1), ((rho1 * rho2) ≠ 0 ∧
    ((pochList [q] q (j)) * (pochList [q] q (n-j))) ≠ 0)) :
 (∑ r ∈ Finset.range (n+1), (((((pochList [rho1,rho2] q (r)) * (((x * q) / (rho1 * rho2))^r)) / (pochList [((x * q) / rho1),((x * q) / rho2)] q (r))) * (sillsAlpha x q 1 2 r)) / ((pochList [q] q (n-r)) * (pochList [(x * q)] q (n+r))))) = ((1 / (pochList [((x * q) / rho1),((x * q) / rho2)] q (n))) * (∑ j ∈ Finset.range (n+1), ((((pochList [rho1,rho2] q (j)) * (pochList [((x * q) / (rho1 * rho2))] q (n-j))) * (((x * q) / (rho1 * rho2))^j)) / ((pochList [q] q (j)) * (pochList [q] q (n-j)))))) := by
  sorry

end FiniteQBenchmark.Identity383
