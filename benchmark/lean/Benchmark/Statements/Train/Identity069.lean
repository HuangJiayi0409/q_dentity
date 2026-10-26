import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.10.8 — 迭代 Bailey 终止 10φ9 变换
Original representative source: GR2-2.10.8
Frozen statement: formulas/train/FQI-SRC-GR2-2.10.8.md
Source formula:
W_{10}^{[n]}(a;b,c,d,e,f,a^3q^{n+2}/(bcdef),q^{-n};q,q)=\frac{(aq,aq/(de),aq/(df),aq/(ef);q)_n}{(aq/d,aq/e,aq/f,aq/(def);q)_n}W_{10}^{[n]}(defq^{-n-1}/a;aq/(bc),d,e,f,bdefq^{-n-1}/a^2,cdefq^{-n-1}/a^2,q^{-n};q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity069
variable {K : Type*} [Field K]

theorem statement (a b c d e f q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c,d,e,f], x ≠ 0)
 (hl : wDefined a [b,c,d,e,f,a^3*q^(n+2)/(b*c*d*e*f),q^(-(n : ℤ))] q n)
 (hr : wDefined (d*e*f*q^(-(n : ℤ)-1)/a)
 [a*q/(b*c),d,e,f,b*d*e*f*q^(-(n : ℤ)-1)/a^2,c*d*e*f*q^(-(n : ℤ)-1)/a^2,q^(-(n : ℤ))] q n)
 (hf : pochList [a*q/d,a*q/e,a*q/f,a*q/(d*e*f)] q n ≠ 0) :
 wellPoisedRaw a [b,c,d,e,f,a^3*q^(n+2)/(b*c*d*e*f),q^(-(n : ℤ))] q q n =
 pochList [a*q,a*q/(d*e),a*q/(d*f),a*q/(e*f)] q n /
 pochList [a*q/d,a*q/e,a*q/f,a*q/(d*e*f)] q n *
 wellPoisedRaw (d*e*f*q^(-(n : ℤ)-1)/a)
 [a*q/(b*c),d,e,f,b*d*e*f*q^(-(n : ℤ)-1)/a^2,c*d*e*f*q^(-(n : ℤ)-1)/a^2,q^(-(n : ℤ))] q q n := by
  sorry

end FiniteQBenchmark.Identity069
