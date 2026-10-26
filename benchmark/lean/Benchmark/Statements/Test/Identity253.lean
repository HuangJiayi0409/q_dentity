import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-II-36 — 有限双边双底数求和
Original representative source: GR2-II-36
Frozen statement: formulas/test/FQI-SRC-GR2-II-36.md
Source formula:
\sum_{k=-m}^n\frac{(1-adp^kq^k)(1-bp^k/(dq^k))}{(1-ad)(1-b/d)}\frac{(a,b;p)_k(c,ad^2/(bc);q)_k}{(dq,adq/b;q)_k(adp/c,bcp/d;p)_k}q^k=\frac{(1-a)(1-b)(1-c)(1-ad^2/(bc))}{d(1-ad)(1-b/d)(1-c/d)(1-ad/(bc))}\left[\frac{(ap,bp;p)_n(cq,ad^2q/(bc);q)_n}{(dq,adq/b;q)_n(adp/c,bcp/d;p)_n}-\frac{(c/(ad),d/(bc);p)_{m+1}(1/d,b/(ad);q)_{m+1}}{(1/c,bc/(ad^2);q)_{m+1}(1/a,1/b;p)_{m+1}}\right].
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity253
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d p q : K) (m n : ℕ)
 (hbase : regular q) (hp : regular p) (hnz : a*b*c*d ≠ 0)
 (h_domain : ∀ k ∈ Finset.Icc (-(m:ℤ)) (n:ℤ), ((d * (q^k)) ≠ 0 ∧
    d ≠ 0 ∧
    ((1 - (a * d)) * (1 - (b / d))) ≠ 0 ∧
    pochListIntDefined [a,b] (p) k ∧
    (b * c) ≠ 0 ∧
    pochListIntDefined [c,((a * (d^2)) / (b * c))] (q) k ∧
    b ≠ 0 ∧
    pochListIntDefined [(d * q),(((a * d) * q) / b)] (q) k ∧
    c ≠ 0 ∧
    pochListIntDefined [(((a * d) * p) / c),(((b * c) * p) / d)] (p) k ∧
    ((pochListInt [(d * q),(((a * d) * q) / b)] (q) k) * (pochListInt [(((a * d) * p) / c),(((b * c) * p) / d)] (p) k)) ≠ 0) ∧
    (b * c) ≠ 0 ∧
    d ≠ 0 ∧
    ((((d * (1 - (a * d))) * (1 - (b / d))) * (1 - (c / d))) * (1 - ((a * d) / (b * c)))) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    ((pochList [(d * q),(((a * d) * q) / b)] q (n)) * (pochList [(((a * d) * p) / c),(((b * c) * p) / d)] p (n))) ≠ 0 ∧
    (a * d) ≠ 0 ∧
    (a * (d^2)) ≠ 0 ∧
    a ≠ 0 ∧
    ((pochList [(1 / c),((b * c) / (a * (d^2)))] q (m+1)) * (pochList [(1 / a),(1 / b)] p (m+1))) ≠ 0) :
 (∑ k ∈ Finset.Icc (-(m:ℤ)) (n:ℤ), (((((((1 - (((a * d) * (p^k)) * (q^k))) * (1 - ((b * (p^k)) / (d * (q^k))))) / ((1 - (a * d)) * (1 - (b / d)))) * (pochListInt [a,b] (p) k)) * (pochListInt [c,((a * (d^2)) / (b * c))] (q) k)) / ((pochListInt [(d * q),(((a * d) * q) / b)] (q) k) * (pochListInt [(((a * d) * p) / c),(((b * c) * p) / d)] (p) k))) * (q^k))) = ((((((1 - a) * (1 - b)) * (1 - c)) * (1 - ((a * (d^2)) / (b * c)))) / ((((d * (1 - (a * d))) * (1 - (b / d))) * (1 - (c / d))) * (1 - ((a * d) / (b * c))))) * ((((pochList [(a * p),(b * p)] p (n)) * (pochList [(c * q),(((a * (d^2)) * q) / (b * c))] q (n))) / ((pochList [(d * q),(((a * d) * q) / b)] q (n)) * (pochList [(((a * d) * p) / c),(((b * c) * p) / d)] p (n)))) - (((pochList [(c / (a * d)),(d / (b * c))] p (m+1)) * (pochList [(1 / d),(b / (a * d))] q (m+1))) / ((pochList [(1 / c),((b * c) / (a * (d^2)))] q (m+1)) * (pochList [(1 / a),(1 / b)] p (m+1)))))) := by
  sorry

end FiniteQBenchmark.Identity253
