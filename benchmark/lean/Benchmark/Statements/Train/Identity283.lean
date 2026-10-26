import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AP-11.2.1 — 固定首列平面分拆的有限递推
Original representative source: AP-11.2.1
Frozen statement: formulas/train/FQI-SRC-AP-11.2.1.md
Source formula:
\pi_{r+1}(n_1,\ldots,n_k;q)=q^{n_1+\cdots+n_k}\sum_{\substack{n_i\ge m_i\ge0\ (1\le i\le k)\\m_1\ge\cdots\ge m_k}}\pi_r(m_1,\ldots,m_k;q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity283
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (k r : ℕ) (n : Fin k → ℕ)
 (hk : 0 < k) (hr : 0 < r) (hn : Antitone n) :
 planePi q (r+1) n = q^(∑ j, n j) *
   ∑ m ∈ (Finset.univ : Finset ((j : Fin k) → Fin (n j+1))).filter
     (fun m => Antitone (fun j => (m j).val)), planePi q r (fun j => (m j).val) := by
  sorry

end FiniteQBenchmark.Identity283
