import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.6.18 — 双底数有限三角矩阵反演
Original representative source: GR2-3.6.18
Frozen statement: formulas/train/FQI-SRC-GR2-3.6.18.md
Source formula:
\sum_{j=m}^n A_{nj}B_{jm}=\delta_{n,m},\qquad\sum_{j=m}^n B_{nj}A_{jm}=\delta_{n,m},\quad A_{nj}=\frac{(-1)^{n+j}(1-ap^jq^j)(1-bp^jq^{-j})(apq^n,bpq^{-n};p)_{n-1}}{(q;q)_{n-j}(apq^n,bpq^{-n};p)_j(bq^{1-2n}/a;q)_{n-j}},\quad B_{jm}=\frac{(ap^mq^m,bp^mq^{-m};p)_{j-m}}{(q,aq^{1+2m}/b;q)_{j-m}}(-aq^{1+2m}/b)^{j-m}q^{(j-m)(j-m-1)}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity094
variable {K : Type*} [Field K]

theorem statement (a b p q : K) (m n : ℕ) (hmn : m ≤ n) (hp : regular p) (hq : regular q)
 (ha : a ≠ 0) (hb : b ≠ 0)
 (hA : ∀ j ∈ Finset.Icc m n, inverseADefined a b p q n j ∧ inverseADefined a b p q j m)
 (hB : ∀ j ∈ Finset.Icc m n,
 pochList [q,a*q^(1+2*m)/b] q (j-m) ≠ 0 ∧ pochList [q,a*q^(1+2*j)/b] q (n-j) ≠ 0) :
 (∑ j ∈ Finset.Icc m n, inverseA a b p q n j*inverseB a b p q j m) = (if n=m then 1 else 0) ∧
 (∑ j ∈ Finset.Icc m n, inverseB a b p q n j*inverseA a b p q j m) = (if n=m then 1 else 0) := by
  sorry

end FiniteQBenchmark.Identity094
