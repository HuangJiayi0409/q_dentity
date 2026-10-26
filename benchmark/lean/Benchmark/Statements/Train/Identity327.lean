import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-AQ-8.56 — Andrews–Baxter–Forrester 双端终止变换
Original representative source: AQ-8.56
Frozen statement: formulas/train/FQI-SRC-AQ-8.56.md
Source formula:
\begin{aligned}&\sum_{r=-R}^N\frac{1-aq^{2r}}{1-a}\frac{(aq^{-R},q^{-N};q)_r}{(q^{R+1},aq^{N+1};q)_r}\prod_{i=1}^k\frac{(b_i,c_i;q)_r}{(aq/b_i,aq/c_i;q)_r}\left(\frac{a^kq^{k+N+R}}{\prod_{i=1}^kb_ic_i}\right)^r\\&=\frac{(q/a,aq/(b_1c_1);q)_R(aq,aq/(b_kc_k);q)_N}{(q/b_1,q/c_1;q)_R(aq/b_k,aq/c_k;q)_N}\sum_{\substack{m_1\ge-R,\ m_2,\ldots,m_{k-1}\ge0\\M_{k-1}\le N}}\frac{(aq^{R+1}/(b_1c_1);q)_{m_1}}{(q^{R+1};q)_{m_1}}\prod_{i=2}^{k-1}\frac{(aq/(b_ic_i);q)_{m_i}}{(q;q)_{m_i}}\\&\qquad\times\prod_{i=1}^{k-1}\frac{(b_{i+1},c_{i+1};q)_{M_i}}{(aq/b_i,aq/c_i;q)_{M_i}}\frac{(q^{-N};q)_{M_{k-1}}}{(b_kc_kq^{-N}/a;q)_{M_{k-1}}}\frac{a^{\sum_{i=1}^{k-2}M_i}q^{\sum_{i=1}^{k-1}M_i}}{\prod_{i=1}^{k-2}(b_{i+1}c_{i+1})^{M_i}}.\end{aligned}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity327
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a q : K) (k N R : ℕ) (b c : ℕ → K)
 (ha : a ≠ 0) (ha1 : a ≠ 1) (hq : q ≠ 0) (hbc : ∀ i ≤ k+1, b i*c i ≠ 0)
 (h_domain : ∀ r ∈ Finset.Icc (-(R:ℤ) : ℤ) (N : ℤ), ((1 - a) ≠ 0 ∧
    pochListIntDefined [(a * (q^((-(R : ℤ)) : ℤ))),(q^((-(N : ℤ)) : ℤ))] q (r) ∧
    pochListIntDefined [(q^(((R : ℤ)+1) : ℤ)),(a * (q^(((N : ℤ)+1) : ℤ)))] q (r) ∧
    (pochListInt [(q^(((R : ℤ)+1) : ℤ)),(a * (q^(((N : ℤ)+1) : ℤ)))] q (r)) ≠ 0 ∧
    ∀ i : Fin (k+2), (pochListIntDefined [(b (i.val)),(c (i.val))] q (r) ∧
    (b (i.val)) ≠ 0 ∧
    (c (i.val)) ≠ 0 ∧
    pochListIntDefined [((a * q) / (b (i.val))),((a * q) / (c (i.val)))] q (r) ∧
    (pochListInt [((a * q) / (b (i.val))),((a * q) / (c (i.val)))] q (r)) ≠ 0) ∧
    (∏ i : Fin (k+2), b i.val*c i.val) ≠ 0) ∧
    a ≠ 0 ∧
    ((b (0)) * (c (0))) ≠ 0 ∧
    ((b (k+1)) * (c (k+1))) ≠ 0 ∧
    (b (0)) ≠ 0 ∧
    (c (0)) ≠ 0 ∧
    (b (k+1)) ≠ 0 ∧
    (c (k+1)) ≠ 0 ∧
    ((pochList [(q / (b (0))),(q / (c (0)))] q (R)) * (pochList [((a * q) / (b (k+1))),((a * q) / (c (k+1)))] q (N))) ≠ 0 ∧
    ∀ v ∈ (subCompositions (k+1) (N+R)), (((b (0)) * (c (0))) ≠ 0 ∧
    pochListIntDefined [((a * (q^(((R : ℤ)+1) : ℤ))) / ((b (0)) * (c (0))))] q (((v 0).val : ℤ)-(R:ℤ)) ∧
    pochListIntDefined [(q^(((R : ℤ)+1) : ℤ))] q (((v 0).val : ℤ)-(R:ℤ)) ∧
    (pochListInt [(q^(((R : ℤ)+1) : ℤ))] q (((v 0).val : ℤ)-(R:ℤ))) ≠ 0 ∧
    ∀ i : Fin k, (((b (i.val+1)) * (c (i.val+1))) ≠ 0 ∧
    (pochList [q] q ((v i.succ).val)) ≠ 0) ∧
    ∀ i : Fin (k+1), (pochListIntDefined [(b (i.val+1)),(c (i.val+1))] q (((∑ h ∈ Finset.univ.filter (fun h : Fin (k+1) => h ≤ i), ((v h).val : ℤ))-(R:ℤ))) ∧
    (b (i.val)) ≠ 0 ∧
    (c (i.val)) ≠ 0 ∧
    pochListIntDefined [((a * q) / (b (i.val))),((a * q) / (c (i.val)))] q (((∑ h ∈ Finset.univ.filter (fun h : Fin (k+1) => h ≤ i), ((v h).val : ℤ))-(R:ℤ))) ∧
    (pochListInt [((a * q) / (b (i.val))),((a * q) / (c (i.val)))] q (((∑ h ∈ Finset.univ.filter (fun h : Fin (k+1) => h ≤ i), ((v h).val : ℤ))-(R:ℤ)))) ≠ 0) ∧
    pochListIntDefined [(q^((-(N : ℤ)) : ℤ))] q (((∑ h : Fin (k+1), ((v h).val : ℤ))-(R:ℤ))) ∧
    a ≠ 0 ∧
    pochListIntDefined [((((b (k+1)) * (c (k+1))) * (q^((-(N : ℤ)) : ℤ))) / a)] q (((∑ h : Fin (k+1), ((v h).val : ℤ))-(R:ℤ))) ∧
    (pochListInt [((((b (k+1)) * (c (k+1))) * (q^((-(N : ℤ)) : ℤ))) / a)] q (((∑ h : Fin (k+1), ((v h).val : ℤ))-(R:ℤ)))) ≠ 0 ∧
    (∏ i : Fin k, ((b (i.val+1)*c (i.val+1))^((∑ h ∈ Finset.univ.filter (fun h : Fin (k+1) => h ≤ i.castSucc), ((v h).val : ℤ))-(R:ℤ)))) ≠ 0)) :
 (∑ r ∈ Finset.Icc (-(R:ℤ) : ℤ) (N : ℤ), ((((((1 - (a * (q^(2*r)))) / (1 - a)) * (pochListInt [(a * (q^((-(R : ℤ)) : ℤ))),(q^((-(N : ℤ)) : ℤ))] q (r))) / (pochListInt [(q^(((R : ℤ)+1) : ℤ)),(a * (q^(((N : ℤ)+1) : ℤ)))] q (r))) * (∏ i : Fin (k+2), ((pochListInt [(b (i.val)),(c (i.val))] q (r)) / (pochListInt [((a * q) / (b (i.val))),((a * q) / (c (i.val)))] q (r))))) * ((((a^(k+2)) * (q^(((k : ℤ)+2+(N : ℤ)+(R : ℤ)) : ℤ))) / (∏ i : Fin (k+2), b i.val*c i.val))^r))) = ((((pochList [(q / a),((a * q) / ((b (0)) * (c (0))))] q (R)) * (pochList [(a * q),((a * q) / ((b (k+1)) * (c (k+1))))] q (N))) / ((pochList [(q / (b (0))),(q / (c (0)))] q (R)) * (pochList [((a * q) / (b (k+1))),((a * q) / (c (k+1)))] q (N)))) * (∑ v ∈ (subCompositions (k+1) (N+R)), (((((((((pochListInt [((a * (q^(((R : ℤ)+1) : ℤ))) / ((b (0)) * (c (0))))] q (((v 0).val : ℤ)-(R:ℤ))) / (pochListInt [(q^(((R : ℤ)+1) : ℤ))] q (((v 0).val : ℤ)-(R:ℤ)))) * (∏ i : Fin k, ((pochList [((a * q) / ((b (i.val+1)) * (c (i.val+1))))] q ((v i.succ).val)) / (pochList [q] q ((v i.succ).val))))) * (∏ i : Fin (k+1), ((pochListInt [(b (i.val+1)),(c (i.val+1))] q (((∑ h ∈ Finset.univ.filter (fun h : Fin (k+1) => h ≤ i), ((v h).val : ℤ))-(R:ℤ)))) / (pochListInt [((a * q) / (b (i.val))),((a * q) / (c (i.val)))] q (((∑ h ∈ Finset.univ.filter (fun h : Fin (k+1) => h ≤ i), ((v h).val : ℤ))-(R:ℤ))))))) * (pochListInt [(q^((-(N : ℤ)) : ℤ))] q (((∑ h : Fin (k+1), ((v h).val : ℤ))-(R:ℤ))))) / (pochListInt [((((b (k+1)) * (c (k+1))) * (q^((-(N : ℤ)) : ℤ))) / a)] q (((∑ h : Fin (k+1), ((v h).val : ℤ))-(R:ℤ))))) * (a^(∑ i : Fin k, ((∑ h ∈ Finset.univ.filter (fun h : Fin (k+1) => h ≤ i.castSucc), ((v h).val : ℤ))-(R:ℤ))))) * (q^(∑ i : Fin (k+1), ((∑ h ∈ Finset.univ.filter (fun h : Fin (k+1) => h ≤ i), ((v h).val : ℤ))-(R:ℤ))))) / (∏ i : Fin k, ((b (i.val+1)*c (i.val+1))^((∑ h ∈ Finset.univ.filter (fun h : Fin (k+1) => h ≤ i.castSucc), ((v h).val : ℤ))-(R:ℤ))))))) := by
  sorry

end FiniteQBenchmark.Identity327
