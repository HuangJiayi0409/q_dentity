import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-FINE-2.1 — q-Pochhammer 首项递推
Original representative source: FINE-2.1
Frozen statement: formulas/train/FQI-SRC-FINE-2.1.md
Source formula:
(aq;q)_n=(1-aq)(aq^2;q)_{n-1}\quad(n\ge1).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity342
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (n : ℕ)
 (hn : 1 ≤ n)
 (h_domain : True) :
 (pochList [(a * q)] q (n)) = ((1 - (a * q)) * (pochList [(a * (q^2))] q (n-1))) := by
  sorry

end FiniteQBenchmark.Identity342
