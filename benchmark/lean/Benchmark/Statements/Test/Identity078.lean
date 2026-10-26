import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex19 — 平衡终止 10φ9 的参数重排
Original representative source: GR2-2.Ex19
Frozen statement: formulas/test/FQI-SRC-GR2-2.Ex19.md
Source formula:
W_{10}^{[n]}(a;b,c,d,e,f,g,q^{-n};q,q)=\frac{(aq,aq/(ce),aq/(de),aq/(ef),aq/(eg),b;q)_n}{(aq/c,aq/d,aq/e,aq/f,aq/g,b/e;q)_n}e^nW_{10}^{[n]}(eq^{-n}/b;e,aq/(bc),aq/(bd),aq/(bf),aq/(bg),eq^{-n}/a,q^{-n};q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity078
variable {K : Type*} [Field K]

theorem statement (a b c d e f g q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c,d,e,f,g], x ≠ 0) (hbal : a^3*q^(n+2)=b*c*d*e*f*g)
 (hl : wDefined a [b,c,d,e,f,g,q^(-(n : ℤ))] q n)
 (hr : wDefined (e*q^(-(n : ℤ))/b)
 [e,a*q/(b*c),a*q/(b*d),a*q/(b*f),a*q/(b*g),e*q^(-(n : ℤ))/a,q^(-(n : ℤ))] q n)
 (hf : pochList [a*q/c,a*q/d,a*q/e,a*q/f,a*q/g,b/e] q n ≠ 0) :
 wellPoisedRaw a [b,c,d,e,f,g,q^(-(n : ℤ))] q q n =
 pochList [a*q,a*q/(c*e),a*q/(d*e),a*q/(e*f),a*q/(e*g),b] q n /
 pochList [a*q/c,a*q/d,a*q/e,a*q/f,a*q/g,b/e] q n*e^n *
 wellPoisedRaw (e*q^(-(n : ℤ))/b)
 [e,a*q/(b*c),a*q/(b*d),a*q/(b*f),a*q/(b*g),e*q^(-(n : ℤ))/a,q^(-(n : ℤ))] q q n := by
  sorry

end FiniteQBenchmark.Identity078
