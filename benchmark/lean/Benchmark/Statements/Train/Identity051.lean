import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex5 — 有限乘积的终止展开
Original representative source: GR2-1.Ex5
Frozen statement: formulas/train/FQI-SRC-GR2-1.Ex5.md
Source formula:
\frac{(c,bq^n;q)_m}{(b;q)_m}=\frac{(b/c;q)_n}{(b;q)_n}\sum_{k=0}^n\frac{(q^{-n},c;q)_k}{(q,cq^{1-n}/b;q)_k}q^k(cq^k;q)_m.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity051
variable {K : Type*} [Field K]

theorem statement (b c q : K) (m n : ℕ) (hq : regular q) (hb : b ≠ 0) (hc : c ≠ 0)
 (hbden : poch b q m ≠ 0 ∧ poch b q n ≠ 0)
 (hd : phiDefined [c*q^(1-(n : ℤ))/b] q n) :
 pochList [c,b*q^n] q m/poch b q m =
 poch (b/c) q n/poch b q n * ∑ k ∈ Finset.range (n+1),
 pochList [q^(-(n : ℤ)),c] q k/pochList [q,c*q^(1-(n : ℤ))/b] q k*q^k*poch (c*q^k) q m := by
  sorry

end FiniteQBenchmark.Identity051
