import Benchmark.Batch4Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-SILLS-1.75-rec — 有限五重乘积和的一阶递推
Original representative source: SILLS-1.75-rec
Frozen statement: formulas/train/FQI-SRC-SILLS-1.75-rec.md
Source formula:
f_n=\frac{f_{n-1}}{(1-q^{n-1}/x)(1-xq^n)},\quad f_0=1-x^2q.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity360
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (x q : K) (n : ℕ)
 (hn : 1 ≤ n) (hx : x ≠ 0) (hq : q ≠ 0)
 (h_domain : ∀ k ∈ Finset.Icc (-(n:ℤ) : ℤ) ((n:ℤ) : ℤ), (((pochList [((x^2) * (q^2))] q (((n:ℤ)+k).toNat)) * (pochList [(x^(-2:ℤ))] q (((n:ℤ)-k).toNat))) ≠ 0) ∧
    ∀ k ∈ Finset.Icc (-((n-1:ℕ):ℤ) : ℤ) (((n-1:ℕ):ℤ) : ℤ), (((pochList [((x^2) * (q^2))] q ((((n-1:ℕ):ℤ)+k).toNat)) * (pochList [(x^(-2:ℤ))] q ((((n-1:ℕ):ℤ)-k).toNat))) ≠ 0) ∧
    x ≠ 0 ∧
    ((1 - ((q^(n-1)) / x)) * (1 - (x * (q^n)))) ≠ 0 ∧
    ∀ k ∈ Finset.Icc (-(0:ℤ) : ℤ) ((0:ℤ) : ℤ), (((pochList [((x^2) * (q^2))] q (((0:ℤ)+k).toNat)) * (pochList [(x^(-2:ℤ))] q (((0:ℤ)-k).toNat))) ≠ 0)) :
 (∑ k ∈ Finset.Icc (-(n:ℤ) : ℤ) ((n:ℤ) : ℤ), (((((-1:K)^k*q^(k*(3*k+1)/2).toNat*x^(3*k)) * (gaussianInt q (2*(n:ℤ)) ((n:ℤ)+k))) * (1 - ((x^2) * (q^(2*k+1))))) / ((pochList [((x^2) * (q^2))] q (((n:ℤ)+k).toNat)) * (pochList [(x^(-2:ℤ))] q (((n:ℤ)-k).toNat))))) = ((∑ k ∈ Finset.Icc (-((n-1:ℕ):ℤ) : ℤ) (((n-1:ℕ):ℤ) : ℤ), (((((-1:K)^k*q^(k*(3*k+1)/2).toNat*x^(3*k)) * (gaussianInt q (2*((n-1:ℕ):ℤ)) (((n-1:ℕ):ℤ)+k))) * (1 - ((x^2) * (q^(2*k+1))))) / ((pochList [((x^2) * (q^2))] q ((((n-1:ℕ):ℤ)+k).toNat)) * (pochList [(x^(-2:ℤ))] q ((((n-1:ℕ):ℤ)-k).toNat))))) / ((1 - ((q^(n-1)) / x)) * (1 - (x * (q^n))))) ∧
 (∑ k ∈ Finset.Icc (-(0:ℤ) : ℤ) ((0:ℤ) : ℤ), (((((-1:K)^k*q^(k*(3*k+1)/2).toNat*x^(3*k)) * (gaussianInt q (2*(0:ℤ)) ((0:ℤ)+k))) * (1 - ((x^2) * (q^(2*k+1))))) / ((pochList [((x^2) * (q^2))] q (((0:ℤ)+k).toNat)) * (pochList [(x^(-2:ℤ))] q (((0:ℤ)-k).toNat))))) = (1 - ((x^2) * q)) := by
  sorry

end FiniteQBenchmark.Identity360
