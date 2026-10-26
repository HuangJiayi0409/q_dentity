import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-I-33 — 单位根参数的有限伸缩比
Original representative source: GR2-I-33
Frozen statement: formulas/train/FQI-SRC-GR2-I-33.md
Source formula:
\prod_{j=0}^{m-1}\frac{(qs\omega_m^j;q)_n}{(s\omega_m^j;q)_n}=\frac{(s^mq^m;q^m)_n}{(s^m;q^m)_n}=\frac{1-s^mq^{mn}}{1-s^m}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity239
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q s omega : K) (n m : ℕ)
 (hbase : regular q) (hm : 0 < m) (hw : IsPrimitiveRoot omega m) (hs : s^m ≠ 1)
 (h_domain : ∀ j ∈ Finset.range m, ((pochList [(s * (omega^j))] q (n)) ≠ 0) ∧
    (pochList [(s^m)] (q^m) (n)) ≠ 0 ∧
    (1 - (s^m)) ≠ 0) :
 (∏ j ∈ Finset.range m, ((pochList [((q * s) * (omega^j))] q (n)) / (pochList [(s * (omega^j))] q (n)))) = ((pochList [((s^m) * (q^m))] (q^m) (n)) / (pochList [(s^m)] (q^m) (n))) ∧
 ((pochList [((s^m) * (q^m))] (q^m) (n)) / (pochList [(s^m)] (q^m) (n))) = ((1 - ((s^m) * (q^(m*n)))) / (1 - (s^m))) := by
  sorry

end FiniteQBenchmark.Identity239
