import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-2.8.2 — Bailey 有限支持序列展开
Original representative source: GR2-2.8.2
Frozen statement: formulas/train/FQI-SRC-GR2-2.8.2.md
Source formula:
\sum_{k=0}^N\frac{(a,b,c;q)_k}{(q,aq/b,aq/c;q)_k}A_k=\sum_{j=0}^N\frac{(\lambda;q)_j(1-\lambda q^{2j})(\lambda b/a,\lambda c/a,aq/(bc);q)_j(a;q)_{2j}}{(q;q)_j(1-\lambda)(aq/b,aq/c,qa^2/(\lambda bc);q)_j(\lambda q;q)_{2j}}\left(\frac a\lambda\right)^j\sum_{k=0}^{N-j}\frac{(aq^{2j},a/\lambda,\lambda bcq^j/a;q)_k}{(q,\lambda q^{2j+1},a^2q^{j+1}/(\lambda bc);q)_k}A_{j+k}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity067
variable {K : Type*} [Field K]

theorem statement (a b c l q : K) (A : ℕ → K) (N : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c,l], x ≠ 0) (hl : l ≠ 1)
 (hsupport : ∀ k, N < k → A k = 0)
 (hleft : phiDefined [a*q/b,a*q/c] q N)
 (ho : ∀ j ≤ N, pochList [q,a*q/b,a*q/c,q*a^2/(l*b*c)] q j * poch (l*q) q (2*j) ≠ 0)
 (hi : ∀ j ≤ N, phiDefined [l*q^(2*j+1),a^2*q^(j+1)/(l*b*c)] q (N-j)) :
 (∑ k ∈ Finset.range (N+1), pochList [a,b,c] q k/pochList [q,a*q/b,a*q/c] q k*A k) =
 ∑ j ∈ Finset.range (N+1),
 poch l q j*(1-l*q^(2*j))*pochList [l*b/a,l*c/a,a*q/(b*c)] q j*poch a q (2*j) /
 (poch q q j*(1-l)*pochList [a*q/b,a*q/c,q*a^2/(l*b*c)] q j*poch (l*q) q (2*j)) * (a/l)^j *
 ∑ k ∈ Finset.range (N-j+1),
 pochList [a*q^(2*j),a/l,l*b*c*q^j/a] q k /
 pochList [q,l*q^(2*j+1),a^2*q^(j+1)/(l*b*c)] q k*A (j+k) := by
  sorry

end FiniteQBenchmark.Identity067
