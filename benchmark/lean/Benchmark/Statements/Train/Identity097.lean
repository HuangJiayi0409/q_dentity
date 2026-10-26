import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-3.9.5 — 终止多底数级数的有限展开
Original representative source: GR2-3.9.5
Frozen statement: formulas/train/FQI-SRC-GR2-3.9.5.md
Source formula:
\sum_{k=0}^N\frac{(a,b,c;q)_k}{(q,aq/b,aq/c;q)_k}H_kz^k=\sum_{j=0}^N\frac{(aq/(bc);q)_j(a;q)_{2j}}{(q,aq/b,aq/c;q)_j}\left(-\frac{bcz}{aq}\right)^jq^{-j(j-1)/2}\sum_{k=0}^{N-j}\frac{(aq^{2j};q)_k}{(q;q)_k}H_{j+k}\left(\frac{bcz}{aq^{j+1}}\right)^k,\quad H_k=\prod_{i=1}^m\frac{(\boldsymbol c_i;q_i)_k}{(\boldsymbol d_i;q_i)_k}\left((-1)^kq_i^{k(k-1)/2}\right)^{s_i-r_i}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity097
variable {K : Type*} [Field K]

theorem statement (a b c q z : K) (m N : ℕ) (qs : Fin m → K) (cs ds : Fin m → List K)
 (hq : regular q) (hbases : ∀ i, regular (qs i)) (hp : ∀ x ∈ [a,b,c], x ≠ 0)
 (hterm : ∃ i, (qs i)^(-(N : ℤ)) ∈ cs i)
 (hd : phiDefined [a*q/b,a*q/c] q N)
 (hmd : ∀ i, ∀ k ≤ N, pochList (ds i) (qs i) k ≠ 0) :
 (∑ k ∈ Finset.range (N+1), pochList [a,b,c] q k/pochList [q,a*q/b,a*q/c] q k *
 (∏ i, multibaseTerm (qs i) (cs i) (ds i) k)*z^k) =
 ∑ j ∈ Finset.range (N+1), poch (a*q/(b*c)) q j*poch a q (2*j) /
 pochList [q,a*q/b,a*q/c] q j * (-b*c*z/(a*q))^j*q^(-((j : ℤ)*(j-1)/2)) *
 ∑ k ∈ Finset.range (N-j+1), poch (a*q^(2*j)) q k/poch q q k *
 (∏ i, multibaseTerm (qs i) (cs i) (ds i) (j+k)) * (b*c*z/(a*q^(j+1)))^k := by
  sorry

end FiniteQBenchmark.Identity097
