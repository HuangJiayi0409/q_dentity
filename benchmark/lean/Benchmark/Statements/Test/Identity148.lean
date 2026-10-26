import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.Ex11 — 仿射 q-Krawtchouk 有限正交
Original representative source: GR2-7.Ex11
Frozen statement: formulas/test/FQI-SRC-GR2-7.Ex11.md
Source formula:
\sum_{x=0}^NK_m^{\rm Aff}(q^{-x})K_n^{\rm Aff}(q^{-x})\frac{(aq,q^{-N};q)_x}{(q;q)_x}\left(-\frac{q^{N-1}}a\right)^xq^{-x(x-1)/2}=\delta_{mn}/h_n,\quad h_n=\frac{(aq,q^{-N};q)_n}{(q;q)_n}(-1)^n(aq)^{N-n}q^{Nn-n(n-1)/2}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity148
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (N m n : ℕ)
 (hbase : regular q) (hm : m ≤ N) (hn : n ≤ N) (ha : a ≠ 0)
 (h_domain : ∀ x ∈ Finset.range (N+1), (phiDefined [(a * q),(q^((-(N : ℤ)) : ℤ))] q (m) ∧
    phiDefined [(a * q),(q^((-(N : ℤ)) : ℤ))] q (n) ∧
    (pochList [q] q (x)) ≠ 0 ∧
    a ≠ 0) ∧
    (pochList [q] q (n)) ≠ 0 ∧
    (((((pochList [(a * q),(q^((-(N : ℤ)) : ℤ))] q (n)) / (pochList [q] q (n))) * ((-1:K)^(((n : ℤ)) : ℤ))) * ((a * q)^(((N : ℤ)-(n : ℤ)) : ℤ))) * (q^(((N : ℤ)*(n : ℤ)-(n : ℤ)*((n : ℤ)-1)/2) : ℤ))) ≠ 0) :
 (∑ x ∈ Finset.range (N+1), ((((((phi [(q^((-((m : ℤ))) : ℤ)),(q^((-((x : ℤ))) : ℤ)),0] [(a * q),(q^((-(N : ℤ)) : ℤ))] q q (m)) * (phi [(q^((-((n : ℤ))) : ℤ)),(q^((-((x : ℤ))) : ℤ)),0] [(a * q),(q^((-(N : ℤ)) : ℤ))] q q (n))) * (pochList [(a * q),(q^((-(N : ℤ)) : ℤ))] q (x))) / (pochList [q] q (x))) * (((-(q^(((N : ℤ)-1) : ℤ))) / a)^(((x : ℤ)) : ℤ))) * (q^((-(x : ℤ)*((x : ℤ)-1)/2) : ℤ)))) = ((if (m) = (n) then (1 : K) else 0) / (((((pochList [(a * q),(q^((-(N : ℤ)) : ℤ))] q (n)) / (pochList [q] q (n))) * ((-1:K)^(((n : ℤ)) : ℤ))) * ((a * q)^(((N : ℤ)-(n : ℤ)) : ℤ))) * (q^(((N : ℤ)*(n : ℤ)-(n : ℤ)*((n : ℤ)-1)/2) : ℤ)))) := by
  sorry

end FiniteQBenchmark.Identity148
