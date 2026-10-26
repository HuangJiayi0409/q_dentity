import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-20.64b — Rogers–Szegő q-移位递推
Original representative source: FINE-20.64b
Frozen statement: formulas/train/FQI-SRC-FINE-20.64b.md
Source formula:
f_n(uq)-f_n(u)+u(1-q^n)f_{n-1}(u)=0.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity349
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (u q : K) (n : ℕ)
 (hn : 1 ≤ n)
 (h_domain : True) :
 (((rogersSzego ((u * q)) q (n)) - (rogersSzego (u) q (n))) + ((u * (1 - (q^n))) * (rogersSzego (u) q (n-1)))) = 0 := by
  sorry

end FiniteQBenchmark.Identity349
