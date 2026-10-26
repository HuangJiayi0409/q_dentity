import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.Ex41 — 小 q-Jacobi 的有限加法公式
Original representative source: GR2-7.Ex41
Frozen statement: formulas/train/FQI-SRC-GR2-7.Ex41.md
Source formula:
\ell_n(q^z;1,1)\ell_y(q^z;q^x,0)=\ell_n(q^{x+y};1,1)\ell_n(q^y;1,1)\ell_y(q^z;q^x,0)+\sum_{k=1}^n\frac{(q;q)_{x+y+k}(q;q)_{n+k}q^{k(k+y-n)}}{(q;q)_{x+y}(q;q)_{n-k}(q;q)_k^2}\ell_{n-k}(q^{x+y};q^k,q^k)\ell_{n-k}(q^y;q^k,q^k)\ell_{y+k}(q^z;q^x,0)+\sum_{k=1}^{\min(n,y)}\frac{(q;q)_y(q;q)_{n+k}q^{k(x+y-n+1)}}{(q;q)_{y-k}(q;q)_{n-k}(q;q)_k^2}\ell_{n-k}(q^{x+y-k};q^k,q^k)\ell_{n-k}(q^{y-k};q^k,q^k)\ell_{y-k}(q^z;q^x,0).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity157
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (n x y z : ℕ)
 (hbase : regular q) 
 (h_domain : phiDefined [(1 * q)] q (n) ∧
    phiDefined [((q^(((x : ℤ)) : ℤ)) * q)] q (y) ∧
    ∀ k ∈ Finset.Icc (1) (n), ((((pochList [q] q (x+y)) * (pochList [q] q (n-k))) * ((pochList [q] q (k))^2)) ≠ 0 ∧
    phiDefined [((q^(((k : ℤ)) : ℤ)) * q)] q (n-k) ∧
    phiDefined [((q^(((x : ℤ)) : ℤ)) * q)] q (y+k)) ∧
    ∀ k ∈ Finset.Icc (1) (min n y), ((((pochList [q] q (y-k)) * (pochList [q] q (n-k))) * ((pochList [q] q (k))^2)) ≠ 0 ∧
    phiDefined [((q^(((k : ℤ)) : ℤ)) * q)] q (n-k) ∧
    phiDefined [((q^(((x : ℤ)) : ℤ)) * q)] q (y-k))) :
 ((phi [(q^((-((n : ℤ))) : ℤ)),((1 * 1) * (q^(((n : ℤ)+1) : ℤ)))] [(1 * q)] q (q * (q^(((z : ℤ)) : ℤ))) (n)) * (phi [(q^((-((y : ℤ))) : ℤ)),(((q^(((x : ℤ)) : ℤ)) * 0) * (q^(((y : ℤ)+1) : ℤ)))] [((q^(((x : ℤ)) : ℤ)) * q)] q (q * (q^(((z : ℤ)) : ℤ))) (y))) = (((((phi [(q^((-((n : ℤ))) : ℤ)),((1 * 1) * (q^(((n : ℤ)+1) : ℤ)))] [(1 * q)] q (q * (q^(((x : ℤ)+(y : ℤ)) : ℤ))) (n)) * (phi [(q^((-((n : ℤ))) : ℤ)),((1 * 1) * (q^(((n : ℤ)+1) : ℤ)))] [(1 * q)] q (q * (q^(((y : ℤ)) : ℤ))) (n))) * (phi [(q^((-((y : ℤ))) : ℤ)),(((q^(((x : ℤ)) : ℤ)) * 0) * (q^(((y : ℤ)+1) : ℤ)))] [((q^(((x : ℤ)) : ℤ)) * q)] q (q * (q^(((z : ℤ)) : ℤ))) (y))) + (∑ k ∈ Finset.Icc (1) (n), (((((((pochList [q] q (x+y+k)) * (pochList [q] q (n+k))) * (q^(((k : ℤ)*((k : ℤ)+(y : ℤ)-(n : ℤ))) : ℤ))) / (((pochList [q] q (x+y)) * (pochList [q] q (n-k))) * ((pochList [q] q (k))^2))) * (phi [(q^((-((n : ℤ)-(k : ℤ))) : ℤ)),(((q^(((k : ℤ)) : ℤ)) * (q^(((k : ℤ)) : ℤ))) * (q^(((n : ℤ)-(k : ℤ)+1) : ℤ)))] [((q^(((k : ℤ)) : ℤ)) * q)] q (q * (q^(((x : ℤ)+(y : ℤ)) : ℤ))) (n-k))) * (phi [(q^((-((n : ℤ)-(k : ℤ))) : ℤ)),(((q^(((k : ℤ)) : ℤ)) * (q^(((k : ℤ)) : ℤ))) * (q^(((n : ℤ)-(k : ℤ)+1) : ℤ)))] [((q^(((k : ℤ)) : ℤ)) * q)] q (q * (q^(((y : ℤ)) : ℤ))) (n-k))) * (phi [(q^((-((y : ℤ)+(k : ℤ))) : ℤ)),(((q^(((x : ℤ)) : ℤ)) * 0) * (q^(((y : ℤ)+(k : ℤ)+1) : ℤ)))] [((q^(((x : ℤ)) : ℤ)) * q)] q (q * (q^(((z : ℤ)) : ℤ))) (y+k))))) + (∑ k ∈ Finset.Icc (1) (min n y), (((((((pochList [q] q (y)) * (pochList [q] q (n+k))) * (q^(((k : ℤ)*((x : ℤ)+(y : ℤ)-(n : ℤ)+1)) : ℤ))) / (((pochList [q] q (y-k)) * (pochList [q] q (n-k))) * ((pochList [q] q (k))^2))) * (phi [(q^((-((n : ℤ)-(k : ℤ))) : ℤ)),(((q^(((k : ℤ)) : ℤ)) * (q^(((k : ℤ)) : ℤ))) * (q^(((n : ℤ)-(k : ℤ)+1) : ℤ)))] [((q^(((k : ℤ)) : ℤ)) * q)] q (q * (q^(((x : ℤ)+(y : ℤ)-(k : ℤ)) : ℤ))) (n-k))) * (phi [(q^((-((n : ℤ)-(k : ℤ))) : ℤ)),(((q^(((k : ℤ)) : ℤ)) * (q^(((k : ℤ)) : ℤ))) * (q^(((n : ℤ)-(k : ℤ)+1) : ℤ)))] [((q^(((k : ℤ)) : ℤ)) * q)] q (q * (q^(((y : ℤ)-(k : ℤ)) : ℤ))) (n-k))) * (phi [(q^((-((y : ℤ)-(k : ℤ))) : ℤ)),(((q^(((x : ℤ)) : ℤ)) * 0) * (q^(((y : ℤ)-(k : ℤ)+1) : ℤ)))] [((q^(((x : ℤ)) : ℤ)) * q)] q (q * (q^(((z : ℤ)) : ℤ))) (y-k))))) := by
  sorry

end FiniteQBenchmark.Identity157
