import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-GOLLNITZ-RECURRENCE — Göllnitz 有界分拆递推
Original representative source: SILLS-2.82-83
Frozen statement: formulas/train/FQI-GOLLNITZ-RECURRENCE.md
Source formula:
G_N=G_{N-1}+\begin{cases}tq^NG_{N-6},&N\equiv2,4,5\pmod6,\\t^2q^NG_{N-7},&N\equiv0,1,3\pmod6.\end{cases}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity026
variable {K : Type*} [Field K]

theorem statement (t q : K) (N : ℕ) (hN : 7 ≤ N) :
 gollnitz t q N = gollnitz t q ((N : ℤ)-1) +
 if N%6 = 2 ∨ N%6 = 4 ∨ N%6 = 5
 then t*q^N*gollnitz t q ((N : ℤ)-6)
 else t^2*q^N*gollnitz t q ((N : ℤ)-7) := by
  sorry

end FiniteQBenchmark.Identity026
