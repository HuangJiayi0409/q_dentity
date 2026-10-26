import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.Ex8i — q-Krawtchouk 有限正交（一）
Original representative source: GR2-7.Ex8i
Frozen statement: formulas/test/FQI-SRC-GR2-7.Ex8i.md
Source formula:
\sum_{x=0}^NK_m(q^{-x})K_n(q^{-x})\frac{(q^{-N};q)_x}{(q;q)_x}(-a)^x=(-q/a;q)_Na^Nq^{-N(N+1)/2}\frac{(q;q)_n(1+1/a)(-q^{N+1}/a;q)_n}{(-1/a;q)_n(1+q^{2n}/a)(q^{-N};q)_n}(-aq^{N+1})^{-n}q^{n(n+1)}\delta_{mn}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity145
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (N m n : ℕ)
 (hbase : regular q) (hm : m ≤ N) (hn : n ≤ N) (ha : a ≠ 0)
 (h_domain : ∀ x ∈ Finset.range (N+1), (a ≠ 0 ∧
    phiDefined [(q^((-(N : ℤ)) : ℤ)),0] q (m) ∧
    phiDefined [(q^((-(N : ℤ)) : ℤ)),0] q (n) ∧
    (pochList [q] q (x)) ≠ 0) ∧
    a ≠ 0 ∧
    (((pochList [(-1 / a)] q (n)) * (1 + ((q^((2*(n : ℤ)) : ℤ)) / a))) * (pochList [(q^((-(N : ℤ)) : ℤ))] q (n))) ≠ 0) :
 (∑ x ∈ Finset.range (N+1), (((((phi [(q^((-((m : ℤ))) : ℤ)),(q^((-((x : ℤ))) : ℤ)),((-(q^(((m : ℤ)) : ℤ))) / a)] [(q^((-(N : ℤ)) : ℤ)),0] q q (m)) * (phi [(q^((-((n : ℤ))) : ℤ)),(q^((-((x : ℤ))) : ℤ)),((-(q^(((n : ℤ)) : ℤ))) / a)] [(q^((-(N : ℤ)) : ℤ)),0] q q (n))) * (pochList [(q^((-(N : ℤ)) : ℤ))] q (x))) / (pochList [q] q (x))) * ((-a)^(((x : ℤ)) : ℤ)))) = ((((((((((pochList [((-q) / a)] q (N)) * (a^(((N : ℤ)) : ℤ))) * (q^((-(N : ℤ)*((N : ℤ)+1)/2) : ℤ))) * (pochList [q] q (n))) * (1 + (1 / a))) * (pochList [((-(q^(((N : ℤ)+1) : ℤ))) / a)] q (n))) / (((pochList [(-1 / a)] q (n)) * (1 + ((q^((2*(n : ℤ)) : ℤ)) / a))) * (pochList [(q^((-(N : ℤ)) : ℤ))] q (n)))) * (((-a) * (q^(((N : ℤ)+1) : ℤ)))^((-(n : ℤ)) : ℤ))) * (q^(((n : ℤ)*((n : ℤ)+1)) : ℤ))) * (if (m) = (n) then (1 : K) else 0)) := by
  sorry

end FiniteQBenchmark.Identity145
