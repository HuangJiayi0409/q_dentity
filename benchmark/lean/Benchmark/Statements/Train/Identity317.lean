import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-3.43 — 有限 k 重 Bailey 链
Original representative source: AQ-3.43
Frozen statement: formulas/train/FQI-SRC-AQ-3.43.md
Source formula:
\begin{aligned}&\sum_{r=0}^N\frac{(q^{-N};q)_r}{(aq^{N+1};q)_r}\prod_{i=1}^k\frac{(b_i,c_i;q)_r}{(aq/b_i,aq/c_i;q)_r}\left(\frac{a^kq^{k+N}}{\prod_{i=1}^kb_ic_i}\right)^r(-1)^rq^{-r(r-1)/2}\alpha_r\\&=\frac{(aq,aq/(b_kc_k);q)_N}{(aq/b_k,aq/c_k;q)_N}\sum_{0\le n_1\le\cdots\le n_k\le N}\frac{(q^{-N};q)_{n_k}\beta_{n_1}}{(b_kc_kq^{-N}/a;q)_{n_k}}\prod_{i=1}^k(b_i,c_i;q)_{n_i}\prod_{i=1}^{k-1}\frac{(aq/(b_ic_i);q)_{n_{i+1}-n_i}(aq/(b_ic_i))^{n_i}}{(q;q)_{n_{i+1}-n_i}(aq/b_i,aq/c_i;q)_{n_{i+1}}}\,q^{n_k}.\end{aligned}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity317
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (k N : ℕ) (b c alpha : ℕ → K)
 (ha : a ≠ 0) (hq : q ≠ 0) (hbc : ∀ i ≤ k, b i*c i ≠ 0)
 (h_domain : ∀ r ∈ Finset.range (N+1), ((pochList [(a * (q^(((N : ℤ)+1) : ℤ)))] q (r)) ≠ 0 ∧
    ∀ i : Fin (k+1), ((b (i.val)) ≠ 0 ∧
    (c (i.val)) ≠ 0 ∧
    (pochList [((a * q) / (b (i.val))),((a * q) / (c (i.val)))] q (r)) ≠ 0) ∧
    (∏ i : Fin (k+1), b i.val*c i.val) ≠ 0) ∧
    ((b (k)) * (c (k))) ≠ 0 ∧
    (b (k)) ≠ 0 ∧
    (c (k)) ≠ 0 ∧
    (pochList [((a * q) / (b (k))),((a * q) / (c (k)))] q (N)) ≠ 0 ∧
    ∀ ns ∈ ((Finset.univ : Finset (Fin (k+1) → Fin (N+1))).filter Monotone), (baileyDefined a q ((ns 0).val) ∧
    a ≠ 0 ∧
    (pochList [((((b (k)) * (c (k))) * (q^((-(N : ℤ)) : ℤ))) / a)] q ((ns (Fin.last k)).val)) ≠ 0 ∧
    ∀ i : Fin k, (((b (i.val)) * (c (i.val))) ≠ 0 ∧
    (b (i.val)) ≠ 0 ∧
    (c (i.val)) ≠ 0 ∧
    ((pochList [q] q ((ns i.succ).val-(ns i.castSucc).val)) * (pochList [((a * q) / (b (i.val))),((a * q) / (c (i.val)))] q ((ns i.succ).val))) ≠ 0))) :
 (∑ r ∈ Finset.range (N+1), (((((((pochList [(q^((-(N : ℤ)) : ℤ))] q (r)) / (pochList [(a * (q^(((N : ℤ)+1) : ℤ)))] q (r))) * (∏ i : Fin (k+1), ((pochList [(b (i.val)),(c (i.val))] q (r)) / (pochList [((a * q) / (b (i.val))),((a * q) / (c (i.val)))] q (r))))) * ((((a^(k+1)) * (q^(((k : ℤ)+1+(N : ℤ)) : ℤ))) / (∏ i : Fin (k+1), b i.val*c i.val))^r)) * ((-1:K)^r)) * (q^((-(r : ℤ)*((r : ℤ)-1)/2) : ℤ))) * (alpha r))) = (((pochList [(a * q),((a * q) / ((b (k)) * (c (k))))] q (N)) / (pochList [((a * q) / (b (k))),((a * q) / (c (k)))] q (N))) * (∑ ns ∈ ((Finset.univ : Finset (Fin (k+1) → Fin (N+1))).filter Monotone), ((((((pochList [(q^((-(N : ℤ)) : ℤ))] q ((ns (Fin.last k)).val)) * (baileySum a q alpha ((ns 0).val))) / (pochList [((((b (k)) * (c (k))) * (q^((-(N : ℤ)) : ℤ))) / a)] q ((ns (Fin.last k)).val))) * (∏ i : Fin (k+1), (pochList [(b (i.val)),(c (i.val))] q ((ns i).val)))) * (∏ i : Fin k, (((pochList [((a * q) / ((b (i.val)) * (c (i.val))))] q ((ns i.succ).val-(ns i.castSucc).val)) * (((a * q) / ((b (i.val)) * (c (i.val))))^((ns i.castSucc).val))) / ((pochList [q] q ((ns i.succ).val-(ns i.castSucc).val)) * (pochList [((a * q) / (b (i.val))),((a * q) / (c (i.val)))] q ((ns i.succ).val)))))) * (q^((ns (Fin.last k)).val))))) := by
  sorry

end FiniteQBenchmark.Identity317
