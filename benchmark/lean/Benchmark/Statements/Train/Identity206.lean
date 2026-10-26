import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-10.Ex18 — 终止 q-Kampé de Fériet 双重求和
Original representative source: GR2-10.Ex18
Frozen statement: formulas/train/FQI-SRC-GR2-10.Ex18.md
Source formula:
\sum_{j=0}^n\sum_{k=0}^{n-j}\frac{(q^{-n};q)_{j+k}(a/c,c/d,c/e;q)_j(c/a,b/d,b/e;q)_kq^{j+k}}{(bc/(de);q)_{j+k}(q,a,q^{1-n}/b;q)_j(q,b,q^{1-n}/a;q)_k}=\frac{(c,ab/c;q)_n}{(a,b;q)_n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity206
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d ee q : K) (n : ℕ)
 (hbase : regular q) (hnz : a*b*c*d*ee ≠ 0)
 (h_domain : ∀ j ∈ Finset.range (n+1), (∀ k ∈ Finset.range (n-j+1), (c ≠ 0 ∧
    d ≠ 0 ∧
    ee ≠ 0 ∧
    a ≠ 0 ∧
    (d * ee) ≠ 0 ∧
    b ≠ 0 ∧
    (((pochList [((b * c) / (d * ee))] q (j+k)) * (pochList [q,a,((q^((1-(n : ℤ)) : ℤ)) / b)] q (j))) * (pochList [q,b,((q^((1-(n : ℤ)) : ℤ)) / a)] q (k))) ≠ 0)) ∧
    c ≠ 0 ∧
    (pochList [a,b] q (n)) ≠ 0) :
 (∑ j ∈ Finset.range (n+1), (∑ k ∈ Finset.range (n-j+1), (((((pochList [(q^((-(n : ℤ)) : ℤ))] q (j+k)) * (pochList [(a / c),(c / d),(c / ee)] q (j))) * (pochList [(c / a),(b / d),(b / ee)] q (k))) * (q^(((j : ℤ)+(k : ℤ)) : ℤ))) / (((pochList [((b * c) / (d * ee))] q (j+k)) * (pochList [q,a,((q^((1-(n : ℤ)) : ℤ)) / b)] q (j))) * (pochList [q,b,((q^((1-(n : ℤ)) : ℤ)) / a)] q (k)))))) = ((pochList [c,((a * b) / c)] q (n)) / (pochList [a,b] q (n))) := by
  sorry

end FiniteQBenchmark.Identity206
