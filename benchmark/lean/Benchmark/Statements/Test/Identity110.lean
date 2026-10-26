import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.Ex12 — 倒序型有限双底数二次变换
Original representative source: GR2-3.Ex12
Frozen statement: formulas/test/FQI-SRC-GR2-3.Ex12.md
Source formula:
\Phi_n[q^{-2n},-q^{2-n},b^2,c^2;-q^{-n},q^{2-2n}/b^2,q^{2-2n}/c^2\mid d,-q^{1-n}/w;-q^{1-n}/d,w;q^2,q;wq^{2-n}/(b^2c^2d)]=\frac{(-1,w/d;q)_n}{(-d,w;q)_n}d^n{}_5\phi_4^{[\lfloor n/2\rfloor]}(d^2,q^{2-2n}/(b^2c^2),q^{2-2n}/w^2,q^{-n},q^{1-n};q^{2-2n}/b^2,q^{2-2n}/c^2,dq^{1-n}/w,dq^{2-n}/w;q^2,q^2).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity110
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (b c d w q : K) (n : ℕ)
 (hbase : regular q) (hp : ∀ x ∈ [b,c,d,w], x ≠ 0)
 (h_domain : (b * b) ≠ 0 ∧
    (c * c) ≠ 0 ∧
    w ≠ 0 ∧
    d ≠ 0 ∧
    ((((b * b) * c) * c) * d) ≠ 0 ∧
    phiDefined [(-(q^((-(n : ℤ)) : ℤ))),((q^((2-2*(n : ℤ)) : ℤ)) / (b * b)),((q^((2-2*(n : ℤ)) : ℤ)) / (c * c))] (q^2) (n) ∧
    ∀ k ≤ (n), pochList [((-(q^((1-(n : ℤ)) : ℤ))) / d),w] q k ≠ 0 ∧
    (pochList [(-d),w] q (n)) ≠ 0 ∧
    (((b * b) * c) * c) ≠ 0 ∧
    (w * w) ≠ 0 ∧
    phiDefined [((q^((2-2*(n : ℤ)) : ℤ)) / (b * b)),((q^((2-2*(n : ℤ)) : ℤ)) / (c * c)),((d * (q^((1-(n : ℤ)) : ℤ))) / w),((d * (q^((2-(n : ℤ)) : ℤ))) / w)] (q * q) (n/2)) :
 (bibasicPhi [(q^((-2*(n : ℤ)) : ℤ)),(-(q^((2-(n : ℤ)) : ℤ))),(b * b),(c * c)] [(-(q^((-(n : ℤ)) : ℤ))),((q^((2-2*(n : ℤ)) : ℤ)) / (b * b)),((q^((2-2*(n : ℤ)) : ℤ)) / (c * c))] [d,((-(q^((1-(n : ℤ)) : ℤ))) / w)] [((-(q^((1-(n : ℤ)) : ℤ))) / d),w] (q^2) q ((w * (q^((2-(n : ℤ)) : ℤ))) / ((((b * b) * c) * c) * d)) (n)) = ((((pochList [-1,(w / d)] q (n)) / (pochList [(-d),w] q (n))) * (d^n)) * (phi [(d * d),((q^((2-2*(n : ℤ)) : ℤ)) / (((b * b) * c) * c)),((q^((2-2*(n : ℤ)) : ℤ)) / (w * w)),(q^((-(n : ℤ)) : ℤ)),(q^((1-(n : ℤ)) : ℤ))] [((q^((2-2*(n : ℤ)) : ℤ)) / (b * b)),((q^((2-2*(n : ℤ)) : ℤ)) / (c * c)),((d * (q^((1-(n : ℤ)) : ℤ))) / w),((d * (q^((2-(n : ℤ)) : ℤ))) / w)] (q * q) (q * q) (n/2))) := by
  sorry

end FiniteQBenchmark.Identity110
