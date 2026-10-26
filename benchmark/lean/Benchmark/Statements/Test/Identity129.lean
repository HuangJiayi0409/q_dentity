import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.2.22 — q-Hahn 有限正交
Original representative source: GR2-7.2.22
Frozen statement: formulas/test/FQI-SRC-GR2-7.2.22.md
Source formula:
\sum_{x=0}^NQ_m(x)Q_n(x)\frac{(aq;q)_x(bq;q)_{N-x}}{(q;q)_x(q;q)_{N-x}}(aq)^{-x}=\frac{(abq^2;q)_N(aq)^{-N}}{(q;q)_N}\frac{(q;q)_n(1-abq)(bq,abq^{N+2};q)_n}{(abq;q)_n(1-abq^{2n+1})(aq,q^{-N};q)_n}(-aq)^nq^{n(n-1)/2-Nn}\delta_{mn}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity129
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b q : K) (N m n : ℕ)
 (hbase : regular q) (hm : m ≤ N) (hn : n ≤ N) (ha : a ≠ 0)
 (h_domain : ∀ x ∈ Finset.range (N+1), (phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ))] q (min (m) (x)) ∧
    phiDefined [(a * q),(q^((-((N : ℤ))) : ℤ))] q (min (n) (x)) ∧
    ((pochList [q] q (x)) * (pochList [q] q (N-x))) ≠ 0) ∧
    (pochList [q] q (N)) ≠ 0 ∧
    (((pochList [((a * b) * q)] q (n)) * (1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ))))) * (pochList [(a * q),(q^((-(N : ℤ)) : ℤ))] q (n))) ≠ 0) :
 (∑ x ∈ Finset.range (N+1), ((((((phi [(q^((-((m : ℤ))) : ℤ)),((a * b) * (q^(((m : ℤ)+1) : ℤ))),(q^((-((x : ℤ))) : ℤ))] [(a * q),(q^((-((N : ℤ))) : ℤ))] q q (min (m) (x))) * (phi [(q^((-((n : ℤ))) : ℤ)),((a * b) * (q^(((n : ℤ)+1) : ℤ))),(q^((-((x : ℤ))) : ℤ))] [(a * q),(q^((-((N : ℤ))) : ℤ))] q q (min (n) (x)))) * (pochList [(a * q)] q (x))) * (pochList [(b * q)] q (N-x))) / ((pochList [q] q (x)) * (pochList [q] q (N-x)))) * ((a * q)^((-(x : ℤ)) : ℤ)))) = ((((((((((pochList [(((a * b) * q) * q)] q (N)) * ((a * q)^((-(N : ℤ)) : ℤ))) / (pochList [q] q (N))) * (pochList [q] q (n))) * (1 - ((a * b) * q))) * (pochList [(b * q),((a * b) * (q^(((N : ℤ)+2) : ℤ)))] q (n))) / (((pochList [((a * b) * q)] q (n)) * (1 - ((a * b) * (q^((2*(n : ℤ)+1) : ℤ))))) * (pochList [(a * q),(q^((-(N : ℤ)) : ℤ))] q (n)))) * (((-a) * q)^(((n : ℤ)) : ℤ))) * (q^(((n : ℤ)*((n : ℤ)-1)/2-(N : ℤ)*(n : ℤ)) : ℤ))) * (if (m) = (n) then (1 : K) else 0)) := by
  sorry

end FiniteQBenchmark.Identity129
