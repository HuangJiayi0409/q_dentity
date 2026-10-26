import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.Ex8ii — q-Krawtchouk 有限正交（二）
Original representative source: GR2-7.Ex8ii
Frozen statement: formulas/test/FQI-SRC-GR2-7.Ex8ii.md
Source formula:
\sum_{x=0}^N\widetilde K_m(q^{-x})\widetilde K_n(q^{-x})\frac{(aq;q)_{N-x}(-1)^{N-x}q^{x(x-1)/2}}{(q;q)_x(q;q)_{N-x}}=\frac{(q,aq;q)_n(q;q)_{N-n}}{(q;q)_N^2}(-1)^na^Nq^{(N+n+1)(N+n)/2-n(n+1)}\delta_{mn}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity146
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (N m n : ℕ)
 (hbase : regular q) (hm : m ≤ N) (hn : n ≤ N)
 (h_domain : ∀ x ∈ Finset.range (N+1), (phiDefined [(q^((-(N : ℤ)) : ℤ))] q (m) ∧
    phiDefined [(q^((-(N : ℤ)) : ℤ))] q (n) ∧
    ((pochList [q] q (x)) * (pochList [q] q (N-x))) ≠ 0) ∧
    ((pochList [q] q (N))^2) ≠ 0) :
 (∑ x ∈ Finset.range (N+1), ((((((phi [(q^((-((m : ℤ))) : ℤ)),(q^((-((x : ℤ))) : ℤ))] [(q^((-(N : ℤ)) : ℤ))] q (a * (q^(((m : ℤ)+1) : ℤ))) (m)) * (phi [(q^((-((n : ℤ))) : ℤ)),(q^((-((x : ℤ))) : ℤ))] [(q^((-(N : ℤ)) : ℤ))] q (a * (q^(((n : ℤ)+1) : ℤ))) (n))) * (pochList [(a * q)] q (N-x))) * ((-1:K)^(((N : ℤ)-(x : ℤ)) : ℤ))) * (q^(((x : ℤ)*((x : ℤ)-1)/2) : ℤ))) / ((pochList [q] q (x)) * (pochList [q] q (N-x))))) = (((((((pochList [q,(a * q)] q (n)) * (pochList [q] q (N-n))) / ((pochList [q] q (N))^2)) * ((-1:K)^(((n : ℤ)) : ℤ))) * (a^(((N : ℤ)) : ℤ))) * (q^((((N : ℤ)+(n : ℤ)+1)*((N : ℤ)+(n : ℤ))/2-(n : ℤ)*((n : ℤ)+1)) : ℤ))) * (if (m) = (n) then (1 : K) else 0)) := by
  sorry

end FiniteQBenchmark.Identity146
