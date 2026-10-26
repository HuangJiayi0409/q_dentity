import Benchmark.P1Atoms
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.ClearExcept

namespace FiniteQP1
open FiniteQBenchmark
variable {K : Type*} [Field K]

theorem multisum_poch_one (q : K) (n : ℕ) :
    poch 1 q n = if n=0 then 1 else 0 := by
  cases n with
  | zero => simp
  | succ n =>
    simp only [poch, Finset.prod_range_succ']
    simp

theorem multisum_poch_factor_ne (a q : K) (i n : ℕ) (hi : i < n)
    (hd : poch a q n ≠ 0) : 1-a*q^i ≠ 0 := by
  unfold poch at hd
  exact (Finset.prod_ne_zero_iff.mp hd) i (by simpa only [Finset.mem_range] using hi)

theorem multisum_poch_prefix_ne (a q : K) (m n : ℕ) (hm : m ≤ n)
    (hd : poch a q n ≠ 0) : poch a q m ≠ 0 := by
  unfold poch at hd ⊢
  apply Finset.prod_ne_zero_iff.mpr
  intro i hi
  apply (Finset.prod_ne_zero_iff.mp hd) i
  simp only [Finset.mem_range] at hi ⊢
  omega

theorem multisum_poch_shift (a q : K) (n : ℕ) (ha : 1-a ≠ 0) :
    poch (a*q) q n = poch a q n * (1-a*q^n)/(1-a) := by
  apply (eq_div_iff ha).2
  calc
    _ = poch a q (n+1) := by
      unfold poch
      rw [Finset.prod_range_succ']
      simp only [pow_zero, mul_one]
      congr 1
      apply Finset.prod_congr rfl
      intro i hi
      rw [pow_succ]
      ring
    _ = _ := poch_succ a q n

theorem multisum_poch_shift_ne (a q : K) (n : ℕ)
    (hd : poch a q (n+1) ≠ 0) : poch (a*q) q n ≠ 0 := by
  intro hz
  have h : poch a q (n+1) = poch (a*q) q n*(1-a) := by
    unfold poch
    rw [Finset.prod_range_succ']
    simp only [pow_zero, mul_one]
    congr 1
    apply Finset.prod_congr rfl
    intro i hi
    rw [pow_succ]
    ring
  apply hd
  rw [h,hz,zero_mul]

end FiniteQP1

#print axioms FiniteQP1.multisum_poch_shift
#print axioms FiniteQP1.multisum_poch_shift_ne
