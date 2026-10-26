import Benchmark.Batch2Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-7.Ex37-finite — 加权有限多项式的 q 差分关系
Original representative source: GR2-7.Ex37-finite
Frozen statement: formulas/train/FQI-SRC-GR2-7.Ex37-finite.md
Source formula:
\mathcal D_q\left[\frac{U_n(z)}{(\rho qz,\rho q/z;q)_n}\right]=-\frac{1-\rho^2q^n}{1-q^{n+1}}\frac{T_n(z)U_{n+1}(sz)-T_n(z^{-1})U_{n+1}(z/s)}{(s-s^{-1})(z-z^{-1})/2},\quad T_n(z)=\frac{1-q^{-n}/(\rho sz)}{(\rho qs z;q)_n(\rho s/z;q)_{n+1}},\quad U_n(z)=A_{n,r}(\rho qz,\rho q/z;q)_n{}_6\phi_5^{[r-n]}(q^{n-r},\rho^2\lambda^2q^{n+r+1},\rho sq^n,\rho^2q^n,\rho q^{n+1}z,\rho q^{n+1}/z;\rho^2q^{2n+1},\rho\lambda q^{n+1},\rho^2q^{n+1},-\rho\lambda q^{n+1},-\rho sq^n;q,q),\quad A_{n,r}=\frac{(q;q)_n(\rho^2\lambda^2q;q)_{n+r}s^{3n^2+n-2nr}\rho^{2n}}{(q;q)_{r-n}(\rho q,\rho^2q,\rho\lambda q,-\rho q,-\rho s,-\rho s,-\rho\lambda q;q)_n},\quad s^2=q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity154
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (z rho lam s q : K) [CharZero K] (r n : ℕ)
 (hbase : regular q) (hn : 1 ≤ n) (hnr : n ≤ r) (hs : s^2 = q) (hnz : ∀ v ∈ [rho,lam,z], v ≠ 0)
 (h_domain : ¬ (r < (n)) → (((pochList [q] q (r-(n))) * (pochList [(rho * q),((rho * rho) * q),((rho * lam) * q),((-rho) * q),((-rho) * s),((-rho) * s),(((-rho) * lam) * q)] q (n))) ≠ 0) ∧
    ¬ (r < (n)) → ((s * z) ≠ 0) ∧
    ¬ (r < (n)) → (phiDefined [((rho * rho) * (q^((2*((n : ℤ))+1) : ℤ))),((rho * lam) * (q^((((n : ℤ))+1) : ℤ))),((rho * rho) * (q^((((n : ℤ))+1) : ℤ))),(((-rho) * lam) * (q^((((n : ℤ))+1) : ℤ))),(((-rho) * s) * (q^(((n : ℤ)) : ℤ)))] q (r-(n))) ∧
    (s * z) ≠ 0 ∧
    (pochList [(((rho * q) * s) * z),((rho * q) / (s * z))] q (n)) ≠ 0 ∧
    ¬ (r < (n)) → (s ≠ 0) ∧
    ¬ (r < (n)) → ((z / s) ≠ 0) ∧
    s ≠ 0 ∧
    (z / s) ≠ 0 ∧
    (pochList [(((rho * q) * z) / s),((rho * q) / (z / s))] q (n)) ≠ 0 ∧
    z ≠ 0 ∧
    2 ≠ 0 ∧
    (((s - (1 / s)) * (z - (1 / z))) / 2) ≠ 0 ∧
    (1 - (q^(((n : ℤ)+1) : ℤ))) ≠ 0 ∧
    ((rho * s) * z) ≠ 0 ∧
    ((pochList [(((rho * q) * s) * z)] q (n)) * (pochList [((rho * s) / z)] q (n+1))) ≠ 0 ∧
    ¬ (r < (n+1)) → (((pochList [q] q (r-(n+1))) * (pochList [(rho * q),((rho * rho) * q),((rho * lam) * q),((-rho) * q),((-rho) * s),((-rho) * s),(((-rho) * lam) * q)] q (n+1))) ≠ 0) ∧
    ¬ (r < (n+1)) → ((s * z) ≠ 0) ∧
    ¬ (r < (n+1)) → (phiDefined [((rho * rho) * (q^((2*((n : ℤ)+1)+1) : ℤ))),((rho * lam) * (q^((((n : ℤ)+1)+1) : ℤ))),((rho * rho) * (q^((((n : ℤ)+1)+1) : ℤ))),(((-rho) * lam) * (q^((((n : ℤ)+1)+1) : ℤ))),(((-rho) * s) * (q^(((n : ℤ)+1) : ℤ)))] q (r-(n+1))) ∧
    ((rho * s) * (1 / z)) ≠ 0 ∧
    (1 / z) ≠ 0 ∧
    ((pochList [(((rho * q) * s) * (1 / z))] q (n)) * (pochList [((rho * s) / (1 / z))] q (n+1))) ≠ 0 ∧
    ¬ (r < (n+1)) → (s ≠ 0) ∧
    ¬ (r < (n+1)) → ((z / s) ≠ 0)) :
 ((((if r < (n) then 0 else (((((((pochList [q] q (n)) * (pochList [((((rho * rho) * lam) * lam) * q)] q (n+r))) * (s^((3*((n : ℤ))^2+((n : ℤ))-2*((n : ℤ))*(r : ℤ)) : ℤ))) * (rho^((2*((n : ℤ))) : ℤ))) / ((pochList [q] q (r-(n))) * (pochList [(rho * q),((rho * rho) * q),((rho * lam) * q),((-rho) * q),((-rho) * s),((-rho) * s),(((-rho) * lam) * q)] q (n)))) * (pochList [((rho * q) * (s * z)),((rho * q) / (s * z))] q (n))) * (phi [(q^((((n : ℤ))-(r : ℤ)) : ℤ)),((((rho * rho) * lam) * lam) * (q^((((n : ℤ))+(r : ℤ)+1) : ℤ))),((rho * s) * (q^(((n : ℤ)) : ℤ))),((rho * rho) * (q^(((n : ℤ)) : ℤ))),((rho * (q^((((n : ℤ))+1) : ℤ))) * (s * z)),((rho * (q^((((n : ℤ))+1) : ℤ))) / (s * z))] [((rho * rho) * (q^((2*((n : ℤ))+1) : ℤ))),((rho * lam) * (q^((((n : ℤ))+1) : ℤ))),((rho * rho) * (q^((((n : ℤ))+1) : ℤ))),(((-rho) * lam) * (q^((((n : ℤ))+1) : ℤ))),(((-rho) * s) * (q^(((n : ℤ)) : ℤ)))] q q (r-(n))))) / (pochList [(((rho * q) * s) * z),((rho * q) / (s * z))] q (n))) - ((if r < (n) then 0 else (((((((pochList [q] q (n)) * (pochList [((((rho * rho) * lam) * lam) * q)] q (n+r))) * (s^((3*((n : ℤ))^2+((n : ℤ))-2*((n : ℤ))*(r : ℤ)) : ℤ))) * (rho^((2*((n : ℤ))) : ℤ))) / ((pochList [q] q (r-(n))) * (pochList [(rho * q),((rho * rho) * q),((rho * lam) * q),((-rho) * q),((-rho) * s),((-rho) * s),(((-rho) * lam) * q)] q (n)))) * (pochList [((rho * q) * (z / s)),((rho * q) / (z / s))] q (n))) * (phi [(q^((((n : ℤ))-(r : ℤ)) : ℤ)),((((rho * rho) * lam) * lam) * (q^((((n : ℤ))+(r : ℤ)+1) : ℤ))),((rho * s) * (q^(((n : ℤ)) : ℤ))),((rho * rho) * (q^(((n : ℤ)) : ℤ))),((rho * (q^((((n : ℤ))+1) : ℤ))) * (z / s)),((rho * (q^((((n : ℤ))+1) : ℤ))) / (z / s))] [((rho * rho) * (q^((2*((n : ℤ))+1) : ℤ))),((rho * lam) * (q^((((n : ℤ))+1) : ℤ))),((rho * rho) * (q^((((n : ℤ))+1) : ℤ))),(((-rho) * lam) * (q^((((n : ℤ))+1) : ℤ))),(((-rho) * s) * (q^(((n : ℤ)) : ℤ)))] q q (r-(n))))) / (pochList [(((rho * q) * z) / s),((rho * q) / (z / s))] q (n)))) / (((s - (1 / s)) * (z - (1 / z))) / 2)) = ((((-(1 - ((rho * rho) * (q^(((n : ℤ)) : ℤ))))) / (1 - (q^(((n : ℤ)+1) : ℤ)))) * ((((1 - ((q^((-(n : ℤ)) : ℤ)) / ((rho * s) * z))) / ((pochList [(((rho * q) * s) * z)] q (n)) * (pochList [((rho * s) / z)] q (n+1)))) * (if r < (n+1) then 0 else (((((((pochList [q] q (n+1)) * (pochList [((((rho * rho) * lam) * lam) * q)] q (n+1+r))) * (s^((3*((n : ℤ)+1)^2+((n : ℤ)+1)-2*((n : ℤ)+1)*(r : ℤ)) : ℤ))) * (rho^((2*((n : ℤ)+1)) : ℤ))) / ((pochList [q] q (r-(n+1))) * (pochList [(rho * q),((rho * rho) * q),((rho * lam) * q),((-rho) * q),((-rho) * s),((-rho) * s),(((-rho) * lam) * q)] q (n+1)))) * (pochList [((rho * q) * (s * z)),((rho * q) / (s * z))] q (n+1))) * (phi [(q^((((n : ℤ)+1)-(r : ℤ)) : ℤ)),((((rho * rho) * lam) * lam) * (q^((((n : ℤ)+1)+(r : ℤ)+1) : ℤ))),((rho * s) * (q^(((n : ℤ)+1) : ℤ))),((rho * rho) * (q^(((n : ℤ)+1) : ℤ))),((rho * (q^((((n : ℤ)+1)+1) : ℤ))) * (s * z)),((rho * (q^((((n : ℤ)+1)+1) : ℤ))) / (s * z))] [((rho * rho) * (q^((2*((n : ℤ)+1)+1) : ℤ))),((rho * lam) * (q^((((n : ℤ)+1)+1) : ℤ))),((rho * rho) * (q^((((n : ℤ)+1)+1) : ℤ))),(((-rho) * lam) * (q^((((n : ℤ)+1)+1) : ℤ))),(((-rho) * s) * (q^(((n : ℤ)+1) : ℤ)))] q q (r-(n+1)))))) - (((1 - ((q^((-(n : ℤ)) : ℤ)) / ((rho * s) * (1 / z)))) / ((pochList [(((rho * q) * s) * (1 / z))] q (n)) * (pochList [((rho * s) / (1 / z))] q (n+1)))) * (if r < (n+1) then 0 else (((((((pochList [q] q (n+1)) * (pochList [((((rho * rho) * lam) * lam) * q)] q (n+1+r))) * (s^((3*((n : ℤ)+1)^2+((n : ℤ)+1)-2*((n : ℤ)+1)*(r : ℤ)) : ℤ))) * (rho^((2*((n : ℤ)+1)) : ℤ))) / ((pochList [q] q (r-(n+1))) * (pochList [(rho * q),((rho * rho) * q),((rho * lam) * q),((-rho) * q),((-rho) * s),((-rho) * s),(((-rho) * lam) * q)] q (n+1)))) * (pochList [((rho * q) * (z / s)),((rho * q) / (z / s))] q (n+1))) * (phi [(q^((((n : ℤ)+1)-(r : ℤ)) : ℤ)),((((rho * rho) * lam) * lam) * (q^((((n : ℤ)+1)+(r : ℤ)+1) : ℤ))),((rho * s) * (q^(((n : ℤ)+1) : ℤ))),((rho * rho) * (q^(((n : ℤ)+1) : ℤ))),((rho * (q^((((n : ℤ)+1)+1) : ℤ))) * (z / s)),((rho * (q^((((n : ℤ)+1)+1) : ℤ))) / (z / s))] [((rho * rho) * (q^((2*((n : ℤ)+1)+1) : ℤ))),((rho * lam) * (q^((((n : ℤ)+1)+1) : ℤ))),((rho * rho) * (q^((((n : ℤ)+1)+1) : ℤ))),(((-rho) * lam) * (q^((((n : ℤ)+1)+1) : ℤ))),(((-rho) * s) * (q^(((n : ℤ)+1) : ℤ)))] q q (r-(n+1)))))))) / (((s - (1 / s)) * (z - (1 / z))) / 2)) := by
  sorry

end FiniteQBenchmark.Identity154
