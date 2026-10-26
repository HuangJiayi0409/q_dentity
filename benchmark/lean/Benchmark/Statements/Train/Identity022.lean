import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-POCHHAMMER-NEGATIVE — 负整数长度 q-Pochhammer
Original representative source: GR2-I-02
Frozen statement: formulas/train/FQI-POCHHAMMER-NEGATIVE.md
Source formula:
(a;q)_{-n}=\frac1{(aq^{-n};q)_n}=\frac{(-q/a)^nq^{n(n-1)/2}}{(q/a;q)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity022
variable {K : Type*} [Field K]

theorem statement (a q : K) (n : ℕ) (ha : a ≠ 0) (hq : q ≠ 0)
    (hneg : poch (a*q^(-(n : ℤ))) q n ≠ 0)
    (hpos : poch (q/a) q n ≠ 0) :
    pochInt a q (-(n : ℤ)) = (poch (a*q^(-(n : ℤ))) q n)⁻¹ ∧
    (poch (a*q^(-(n : ℤ))) q n)⁻¹ =
      (-q/a)^n * q^(n*(n-1)/2) / poch (q/a) q n := by
  sorry

end FiniteQBenchmark.Identity022
