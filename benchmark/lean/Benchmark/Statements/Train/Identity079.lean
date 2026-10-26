import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.Ex20 — 终止 10φ9 的有限 4φ3 展开
Original representative source: GR2-2.Ex20
Frozen statement: formulas/train/FQI-SRC-GR2-2.Ex20.md
Source formula:
W_{10}^{[n]}(a;b,c,d,e,f,g,q^{-n};q,a^3q^{n+3}/(bcdefg))=\frac{(aq,aq/(fg);q)_n}{(aq/f,aq/g;q)_n}\sum_{j=0}^n\frac{(q^{-n},f,g,aq/(de);q)_jq^j}{(q,aq/d,aq/e,fgq^{-n}/a;q)_j}{}_4\phi_3^{[j]}(q^{-j},d,e,aq/(bc);aq/b,aq/c,deq^{-j}/a;q,q).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity079
variable {K : Type*} [Field K]

theorem statement (a b c d e f g q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c,d,e,f,g], x ≠ 0)
 (hl : wDefined a [b,c,d,e,f,g,q^(-(n : ℤ))] q n)
 (hf : pochList [a*q/f,a*q/g] q n ≠ 0)
 (ho : phiDefined [a*q/d,a*q/e,f*g*q^(-(n : ℤ))/a] q n)
 (hi : ∀ j ≤ n, phiDefined [a*q/b,a*q/c,d*e*q^(-(j : ℤ))/a] q j) :
 wellPoisedRaw a [b,c,d,e,f,g,q^(-(n : ℤ))] q (a^3*q^(n+3)/(b*c*d*e*f*g)) n =
 pochList [a*q,a*q/(f*g)] q n/pochList [a*q/f,a*q/g] q n *
 ∑ j ∈ Finset.range (n+1), pochList [q^(-(n : ℤ)),f,g,a*q/(d*e)] q j*q^j /
 pochList [q,a*q/d,a*q/e,f*g*q^(-(n : ℤ))/a] q j *
 phi [q^(-(j : ℤ)),d,e,a*q/(b*c)] [a*q/b,a*q/c,d*e*q^(-(j : ℤ))/a] q q j := by
  sorry

end FiniteQBenchmark.Identity079
