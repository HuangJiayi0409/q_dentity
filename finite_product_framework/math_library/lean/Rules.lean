import Benchmark.MathLibraryAtoms
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic.Ring

/-! Basic definitions, local properties and domain-preserving representations.
No benchmark target identities or method-specific certificate algorithms. -/
namespace FiniteQMathLibrary
open FiniteQBenchmark
open scoped BigOperators

section Ring
variable {K : Type*} [CommRing K]

theorem poch_definition (a q : K) (n : ℕ) :
    poch a q n = ∏ i ∈ Finset.range n, (1-a*q^i) := rfl

theorem poch_zero (a q : K) : poch a q 0 = 1 := by simp [poch]

theorem poch_successor (a q : K) (n : ℕ) :
    poch a q (n+1) = poch a q n * (1-a*q^n) := by
  simp only [poch, Finset.prod_range_succ]

theorem poch_split (a q : K) (m n : ℕ) :
    poch a q (m+n) = poch a q m * poch (a*q^m) q n := by
  induction n with
  | zero => simp [poch]
  | succ n ih =>
    rw [Nat.add_succ, poch_successor, ih, poch_successor, pow_add]
    ring

theorem poch_shift_cross (a q : K) (d k : ℕ) :
    poch (a*q^d) q k * poch a q d = poch a q k * poch (a*q^k) q d := by
  rw [mul_comm, ← poch_split, Nat.add_comm, poch_split]

theorem pochList_nil (q : K) (n : ℕ) : pochList [] q n = 1 := rfl

theorem pochList_cons (a : K) (as : List K) (q : K) (n : ℕ) :
    pochList (a::as) q n = poch a q n * pochList as q n := rfl

theorem rogersSzego_sum (t q : K) (n : ℕ) :
    rogersSzego t q n = ∑ i ∈ Finset.range (n+1), gaussian q n i * t^i := rfl

theorem gaussian_successor (q : K) (n k : ℕ) :
    gaussian q (n+1) (k+1) = gaussian q n k + q^(k+1)*gaussian q n (k+1) := rfl

theorem sum_Ico (f : ℕ → K) (a b : ℕ) :
    (∑ i ∈ Finset.Ico a b, f i) = ∑ i ∈ Finset.range (b-a), f (a+i) := by
  exact Finset.sum_Ico_eq_sum_range f a b

theorem sum_Icc (f : ℕ → K) (a b : ℕ) :
    (∑ i ∈ Finset.Icc a b, f i) = ∑ i ∈ Finset.range (b+1-a), f (a+i) := by
  rw [← Finset.Ico_add_one_right_eq_Icc]
  exact Finset.sum_Ico_eq_sum_range f a (b+1)
end Ring

section Field
variable {K : Type*} [Field K]

theorem poch_shift_quotient (a q : K) (d k : ℕ) (h : poch a q d ≠ 0) :
    poch (a*q^d) q k = poch a q k * poch (a*q^k) q d / poch a q d := by
  exact (eq_div_iff h).2 (poch_shift_cross a q d k)

theorem phi_sum (as bs : List K) (q z : K) (n : ℕ) :
    phi as bs q z n = ∑ i ∈ Finset.range (n+1), phiTerm as bs q z i := rfl

theorem phiTerm_definition (as bs : List K) (q z : K) (k : ℕ) :
    phiTerm as bs q z k = pochList as q k / pochList (q::bs) q k *
      (((-1 : K)^k * q^(k*(k-1)/2)) ^ ((1 : ℤ) + (bs.length : ℤ) - (as.length : ℤ)) * z^k) := by
  simp only [phiTerm, mul_assoc]

theorem baileySum_sum (a q : K) (alpha : ℕ → K) (n : ℕ) :
    baileySum a q alpha n = ∑ i ∈ Finset.range (n+1),
      alpha i / (poch q q (n-i) * poch (a*q) q (n+i)) := rfl

theorem geometric_sum (q : K) (n : ℕ) :
    geometric q n = ∑ i ∈ Finset.range n, q^i := rfl

theorem unitBailey_zero (a q : K) : unitBailey a q 0 = 1 := by
  simp [unitBailey]

theorem unitBailey_positive (a q : K) (n : ℕ) (h : n ≠ 0) :
    unitBailey a q n = (-1)^n * q^(n*(n-1)/2) * (1-a*q^(2*n)) *
      poch (a*q) q (n-1) / poch q q n := by
  simp only [unitBailey, if_neg h]
end Field
end FiniteQMathLibrary
