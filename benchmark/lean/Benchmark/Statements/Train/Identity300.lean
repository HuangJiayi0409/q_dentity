import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-11.2.2 — 固定首列平面分拆的初值
Original representative source: AP-11.2.2
Frozen statement: formulas/train/FQI-SRC-AP-11.2.2.md
Source formula:
\pi_1(n_1,\ldots,n_k;q)=q^{n_1+\cdots+n_k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity300
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (k : ℕ) (n : Fin k → ℕ) (hk : 0 < k) (hn : Antitone n) :
 planePi q 1 n = q^(∑ j, n j) := by
  sorry

end FiniteQBenchmark.Identity300
