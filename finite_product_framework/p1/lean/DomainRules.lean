import Benchmark.Gaussian
import Mathlib.Tactic.LinearCombination
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Tactic.Linarith

namespace FiniteQP1
open scoped BigOperators
open FiniteQBenchmark
variable {K : Type*} [Field K]

/-- Split a finite product at an arbitrary natural position, without division. -/
theorem poch_add (a q : K) (m n : ℕ) :
    poch a q (m+n) = poch a q m * poch (a*q^m) q n := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Nat.add_succ, poch_succ, ih, poch_succ, pow_add]
    ring

/-- Removing the first factor is a polynomial identity, including zero factors. -/
theorem poch_head (a q : K) (n : ℕ) :
    poch a q (n+1) = (1-a) * poch (a*q) q n := by
  have h := poch_add a q 1 n
  simpa [Nat.add_comm, poch_succ] using h

theorem poch_prefix_ne (a q : K) {m n : ℕ} (hm : m ≤ n)
    (hn : poch a q n ≠ 0) : poch a q m ≠ 0 := by
  have h : n = m+(n-m) := by omega
  rw [h, poch_add] at hn
  exact (mul_ne_zero_iff.mp hn).1

theorem phi_defined_single (c q : K) (n : ℕ) (hd : phiDefined [c] q n) :
    (∀ k ≤ n, poch q q k ≠ 0) ∧ (∀ k ≤ n, poch c q k ≠ 0) := by
  constructor <;> intro k hk
  · have h := hd k hk
    simp only [pochList_cons, pochList_nil, mul_one] at h
    exact (mul_ne_zero_iff.mp h).1
  · have h := hd k hk
    simp only [pochList_cons, pochList_nil, mul_one] at h
    exact (mul_ne_zero_iff.mp h).2

/-- Clearing a prefix denominator leaves a finite tail product. -/
theorem poch_div_prefix (a q : K) {n k : ℕ} (hk : k ≤ n)
    (hd : poch a q k ≠ 0) :
    poch a q n / poch a q k = poch (a*q^k) q (n-k) := by
  rw [show n = k+(n-k) by omega, poch_add]
  simp [hd]

theorem triangle_double (k : ℕ) :
    k*(k-1)/2 + k*(k-1)/2 + k = k*k := by
  induction k with
  | zero => simp
  | succ k ih =>
    simp only [Nat.triangle_succ]
    nlinarith

theorem triangle_split (n k : ℕ) (hk : k ≤ n) :
    n*(n-1)/2 + k*(k-1)/2 + k = n*k + (n-k)*(n-k-1)/2 := by
  obtain ⟨r, rfl⟩ := Nat.exists_eq_add_of_le hk
  simp only [Nat.add_sub_cancel_left]
  clear hk
  induction r with
  | zero => simpa using triangle_double k
  | succ r ih =>
    rw [Nat.add_succ, Nat.triangle_succ, Nat.triangle_succ]
    nlinarith

end FiniteQP1
