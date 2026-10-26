import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex8 — Andrews 终止奇偶求和
Original representative source: GR2-2.Ex8
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex8.md
Source formula:
\sum_{k=0}^n\frac{(q^{-n},a;q)_k(b;q^2)_kq^k}{(q,b;q)_k(aq^{1-n};q^2)_k}=\begin{cases}0,&n=2m+1,\\\dfrac{(q,bq/a;q^2)_m}{(bq,q/a;q^2)_m},&n=2m.\end{cases}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity075
variable {K : Type*} [Field K]

theorem statement (a b q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 0)
 (hl : ∀ k ≤ n, pochList [q,b] q k * poch (a*q^(1-(n : ℤ))) (q^2) k ≠ 0)
 (hr : n%2=0 → pochList [b*q,q/a] (q^2) (n/2) ≠ 0) :
 (∑ k ∈ Finset.range (n+1), pochList [q^(-(n : ℤ)),a] q k * poch b (q^2) k*q^k /
 (pochList [q,b] q k * poch (a*q^(1-(n : ℤ))) (q^2) k)) =
 if n%2=0 then pochList [q,b*q/a] (q^2) (n/2)/pochList [b*q,q/a] (q^2) (n/2) else 0 := by
  sorry

end FiniteQBenchmark.Identity075
