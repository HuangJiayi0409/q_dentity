import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-11.2.8 — 固定首列与盒内平面分拆的有限求和关系
Original representative source: AP-11.2.8
Frozen statement: formulas/train/FQI-SRC-AP-11.2.8.md
Source formula:
\Pi_{k,r}(n;q)=\sum_{n\ge n_1\ge\cdots\ge n_k\ge0}\pi_r(n_1,\ldots,n_k;q)=q^{-kn}\pi_{r+1}(\underbrace{n,\ldots,n}_{k};q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity301
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (k r n : ℕ) (hk : 0 < k) (hr : 0 < r) (hq : q ≠ 0) :
 planeBoxPi q k r n = (∑ ns ∈ rectangle n k, planePi q r (fun i => (ns i).val)) ∧
 (∑ ns ∈ rectangle n k, planePi q r (fun i => (ns i).val)) = q^(-((k:ℤ)*n))*planePi q (r+1) (fun _ : Fin k => n) := by
  sorry

end FiniteQBenchmark.Identity301
