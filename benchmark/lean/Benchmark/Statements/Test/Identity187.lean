import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-8.Ex16 — 终止 10W9 的 4φ3 表示
Original representative source: GR2-8.Ex16
Frozen statement: formulas/test/FQI-SRC-GR2-8.Ex16.md
Source formula:
W_{10}^{[n]}(a;s,-s,-q,a^2/b,a^2/c,b,c;q,q/a)=\frac{(aq,a^2/c;q)_n}{(a^2,aq/c;q)_n}{}_4\phi_3^{[n]}(a,b,c,bc/a;bq/a,cq/a,bcq/a^2;q,q^2/a^2),\quad b=q^{-n},\ s^2=q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity187
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c s q : K) (n : ℕ)
 (hbase : regular q) (hb : b = q^(-(n:ℤ))) (hs : s^2 = q) (hnz : ∀ v ∈ [a,c], v ≠ 0)
 (h_domain : a ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    wDefined a [s,(-s),(-q),((a * a) / b),((a * a) / c),b,c] q (n) ∧
    (pochList [(a * a),((a * q) / c)] q (n)) ≠ 0 ∧
    (a * a) ≠ 0 ∧
    phiDefined [((b * q) / a),((c * q) / a),(((b * c) * q) / (a * a))] q (n)) :
 (wellPoisedRaw a [s,(-s),(-q),((a * a) / b),((a * a) / c),b,c] q (q / a) (n)) = (((pochList [(a * q),((a * a) / c)] q (n)) / (pochList [(a * a),((a * q) / c)] q (n))) * (phi [a,b,c,((b * c) / a)] [((b * q) / a),((c * q) / a),(((b * c) * q) / (a * a))] q ((q * q) / (a * a)) (n))) := by
  sorry

end FiniteQBenchmark.Identity187
