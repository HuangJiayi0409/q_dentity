import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex4ii — 任意阶终止基本超几何和反向求和
Original representative source: GR2-1.Ex4ii
Frozen statement: formulas/test/FQI-SRC-GR2-1.Ex4ii.md
Source formula:
{}_{r+1}\phi_s^{[n]}\!\left[\begin{matrix}a_1,\ldots,a_r,q^{-n}\\b_1,\ldots,b_s\end{matrix};q,z\right]=\frac{\prod_i(a_i;q)_n}{\prod_j(b_j;q)_n}(z/q)^n\left((-1)^nq^{n(n-1)/2}\right)^{s-r-1}\sum_{k=0}^n\frac{(q^{-n};q)_k\prod_j(q^{1-n}/b_j;q)_k}{(q;q)_k\prod_i(q^{1-n}/a_i;q)_k}\left(\frac{\prod_jb_j}{\prod_ia_i}\frac{q^{n+1}}z\right)^k.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity050
variable {K : Type*} [Field K]

theorem statement (as bs : List K) (q z : K) (n : ℕ) (hq : regular q) (hz : z ≠ 0)
 (hp : ∀ a ∈ as ++ bs, a ≠ 0) (hd : phiDefined bs q n)
 (hr : phiDefined (as.map (fun a => q^(1-(n : ℤ))/a)) q n) :
 phi (as ++ [q^(-(n : ℤ))]) bs q z n =
 pochList as q n/pochList bs q n*(z/q)^n*
 ((-1 : K)^n*q^(n*(n-1)/2))^((bs.length : ℤ)-as.length-1) *
 ∑ k ∈ Finset.range (n+1),
 pochList (q^(-(n : ℤ)) :: bs.map (fun b => q^(1-(n : ℤ))/b)) q k /
 pochList (q :: as.map (fun a => q^(1-(n : ℤ))/a)) q k *
 (bs.prod/as.prod*q^(n+1)/z)^k := by
  sorry

end FiniteQBenchmark.Identity050
