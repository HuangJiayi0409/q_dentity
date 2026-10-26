import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.Ex21-quad — 四底数有限变换
Original representative source: GR2-3.Ex21-quad
Frozen statement: formulas/train/FQI-SRC-GR2-3.Ex21-quad.md
Source formula:
\sum_{k=0}^n K_k(a,b,c;p,q)R_{n,k}(A,B,C;P,Q)=\frac{T_n(a,b,c;p,q)}{T_n(A,B,C;P,Q)}\sum_{k=0}^nK_k(A,B,C;P,Q)R_{n,k}(a,b,c;p,q),\quad K_k=\frac{(1-ap^kq^k)(1-bp^kq^{-k})(a,b;p)_k(c,a/(bc);q)_kq^k}{(1-a)(1-b)(q,aq/b;q)_k(ap/c,bcp;p)_k},\quad T_n=\frac{(ap,bp;p)_n(cq,aq/(bc);q)_n}{(q,aq/b;q)_n(ap/c,bcp;p)_n},\quad R_{n,k}(a,b,c;p,q)=\frac{(cp^{-n}/a,p^{-n}/(bc);p)_k(q^{-n},bq^{-n}/a;q)_k}{(q^{-n}/c,bcq^{-n}/a;q)_k(p^{-n}/a,p^{-n}/b;p)_k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity114
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c p q A B C p2 q2 : K) (n : ℕ)
 (hbase : regular q) (hp : regular p) (hp2 : regular p2) (hq2 : regular q2) (hnz : ∀ x ∈ [a,b,c,A,B,C], x ≠ 0)
 (h_domain : ∀ k ∈ Finset.range (n+1), (((1 - a) * (1 - b)) ≠ 0 ∧
    (b * c) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    ((pochList [q,((a * q) / b)] q (k)) * (pochList [((a * p) / c),((b * c) * p)] p (k))) ≠ 0 ∧
    A ≠ 0 ∧
    (B * C) ≠ 0 ∧
    C ≠ 0 ∧
    B ≠ 0 ∧
    ((pochList [((q2^((-(n : ℤ)) : ℤ)) / C),(((B * C) * (q2^((-(n : ℤ)) : ℤ))) / A)] q2 (k)) * (pochList [((p2^((-(n : ℤ)) : ℤ)) / A),((p2^((-(n : ℤ)) : ℤ)) / B)] p2 (k))) ≠ 0) ∧
    (b * c) ≠ 0 ∧
    b ≠ 0 ∧
    c ≠ 0 ∧
    ((pochList [q,((a * q) / b)] q (n)) * (pochList [((a * p) / c),((b * c) * p)] p (n))) ≠ 0 ∧
    (B * C) ≠ 0 ∧
    B ≠ 0 ∧
    C ≠ 0 ∧
    ((pochList [q2,((A * q2) / B)] q2 (n)) * (pochList [((A * p2) / C),((B * C) * p2)] p2 (n))) ≠ 0 ∧
    (((pochList [(A * p2),(B * p2)] p2 (n)) * (pochList [(C * q2),((A * q2) / (B * C))] q2 (n))) / ((pochList [q2,((A * q2) / B)] q2 (n)) * (pochList [((A * p2) / C),((B * C) * p2)] p2 (n)))) ≠ 0 ∧
    ∀ k ∈ Finset.range (n+1), (((1 - A) * (1 - B)) ≠ 0 ∧
    (B * C) ≠ 0 ∧
    B ≠ 0 ∧
    C ≠ 0 ∧
    ((pochList [q2,((A * q2) / B)] q2 (k)) * (pochList [((A * p2) / C),((B * C) * p2)] p2 (k))) ≠ 0 ∧
    a ≠ 0 ∧
    (b * c) ≠ 0 ∧
    c ≠ 0 ∧
    b ≠ 0 ∧
    ((pochList [((q^((-(n : ℤ)) : ℤ)) / c),(((b * c) * (q^((-(n : ℤ)) : ℤ))) / a)] q (k)) * (pochList [((p^((-(n : ℤ)) : ℤ)) / a),((p^((-(n : ℤ)) : ℤ)) / b)] p (k))) ≠ 0)) :
 (∑ k ∈ Finset.range (n+1), ((((((((1 - ((a * (p^(((k : ℤ)) : ℤ))) * (q^(((k : ℤ)) : ℤ)))) * (1 - ((b * (p^(((k : ℤ)) : ℤ))) * (q^((-(k : ℤ)) : ℤ))))) / ((1 - a) * (1 - b))) * (pochList [a,b] p (k))) * (pochList [c,(a / (b * c))] q (k))) * (q^(((k : ℤ)) : ℤ))) / ((pochList [q,((a * q) / b)] q (k)) * (pochList [((a * p) / c),((b * c) * p)] p (k)))) * (((pochList [((C * (p2^((-(n : ℤ)) : ℤ))) / A),((p2^((-(n : ℤ)) : ℤ)) / (B * C))] p2 (k)) * (pochList [(q2^((-(n : ℤ)) : ℤ)),((B * (q2^((-(n : ℤ)) : ℤ))) / A)] q2 (k))) / ((pochList [((q2^((-(n : ℤ)) : ℤ)) / C),(((B * C) * (q2^((-(n : ℤ)) : ℤ))) / A)] q2 (k)) * (pochList [((p2^((-(n : ℤ)) : ℤ)) / A),((p2^((-(n : ℤ)) : ℤ)) / B)] p2 (k)))))) = (((((pochList [(a * p),(b * p)] p (n)) * (pochList [(c * q),((a * q) / (b * c))] q (n))) / ((pochList [q,((a * q) / b)] q (n)) * (pochList [((a * p) / c),((b * c) * p)] p (n)))) / (((pochList [(A * p2),(B * p2)] p2 (n)) * (pochList [(C * q2),((A * q2) / (B * C))] q2 (n))) / ((pochList [q2,((A * q2) / B)] q2 (n)) * (pochList [((A * p2) / C),((B * C) * p2)] p2 (n))))) * (∑ k ∈ Finset.range (n+1), ((((((((1 - ((A * (p2^(((k : ℤ)) : ℤ))) * (q2^(((k : ℤ)) : ℤ)))) * (1 - ((B * (p2^(((k : ℤ)) : ℤ))) * (q2^((-(k : ℤ)) : ℤ))))) / ((1 - A) * (1 - B))) * (pochList [A,B] p2 (k))) * (pochList [C,(A / (B * C))] q2 (k))) * (q2^(((k : ℤ)) : ℤ))) / ((pochList [q2,((A * q2) / B)] q2 (k)) * (pochList [((A * p2) / C),((B * C) * p2)] p2 (k)))) * (((pochList [((c * (p^((-(n : ℤ)) : ℤ))) / a),((p^((-(n : ℤ)) : ℤ)) / (b * c))] p (k)) * (pochList [(q^((-(n : ℤ)) : ℤ)),((b * (q^((-(n : ℤ)) : ℤ))) / a)] q (k))) / ((pochList [((q^((-(n : ℤ)) : ℤ)) / c),(((b * c) * (q^((-(n : ℤ)) : ℤ))) / a)] q (k)) * (pochList [((p^((-(n : ℤ)) : ℤ)) / a),((p^((-(n : ℤ)) : ℤ)) / b)] p (k))))))) := by
  sorry

end FiniteQBenchmark.Identity114
