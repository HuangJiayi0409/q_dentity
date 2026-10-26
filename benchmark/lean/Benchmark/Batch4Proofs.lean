import Benchmark.Batch4Definitions

namespace FiniteQBenchmark
open scoped BigOperators
noncomputable section
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem integerTopGaussian_zero (q : K) (v : ℤ) : integerTopGaussian q v 0 = 1 := by
  simp [integerTopGaussian]

theorem integerTopGaussian_negative_one (q : K) (hq : q ≠ 0) (h1 : 1-q ≠ 0) :
    integerTopGaussian q (-1) 1 = -q⁻¹ := by
  simp [integerTopGaussian,poch]
  field_simp
  <;> ring

theorem boundedComposition_encoding {M N : ℕ} (a : Fin M → ℕ)
    (h : ∀ i, 1 ≤ a i ∧ a i ≤ N) :
    ∃ v : Fin M → Fin N, ∀ i, (v i).val+1 = a i := by
  refine ⟨fun i => ⟨a i-1, by have := h i; omega⟩,?_⟩
  intro i
  have := h i
  dsimp
  omega

theorem aqInverseT_zero (q : K) (r : ℕ) : aqInverseT q r 0 = 1 := by
  rw [aqInverseT]
  simp

theorem aqInverseT_index_decreases (N : ℕ) (hN : N ≠ 0) (j : Fin (N/2)) :
    N-2*(j.val+1) < N := by have := j.isLt; omega

theorem aqInverseT_unique (q : K) (f : ℕ → ℕ → K)
    (h0 : ∀ r, f r 0 = 1)
    (hs : ∀ r N, N ≠ 0 → f r N =
      -∑ j : Fin (N/2), gaussian q (r+2*(j.val+1)) (j.val+1)*f (r+2*(j.val+1)) (N-2*(j.val+1))) :
    ∀ r N, f r N = aqInverseT q r N := by
  intro r N
  induction N using Nat.strong_induction_on generalizing r with
  | h N ih =>
    by_cases hN : N=0
    · subst N; rw [h0,aqInverseT_zero]
    · rw [hs r N hN,aqInverseT,dif_neg hN]
      congr 1
      apply Finset.sum_congr rfl
      intro j _
      rw [ih _ (aqInverseT_index_decreases N hN j)]

theorem aqG0Coeff_initial (q : K) : aqG0Coeff q 0 = 1 := by simp [aqG0Coeff]

theorem aqG0Coeff_equation (q : K) (n : ℕ) (h : 1-q^(3*(n+1)) ≠ 0) :
    (1-q^(3*(n+1)))*aqG0Coeff q (n+1) =
      ((q+q^2)*q^(3*n)+q^(6*n+3))*aqG0Coeff q n -
      (if n=0 then 0 else q^(6*n)*aqG0Coeff q (n-1)) := by
  rw [aqG0Coeff]
  exact mul_div_cancel₀ _ h

theorem eulerReciprocal_initial (q : K) : PowerSeries.coeff 0 (eulerReciprocalSeries q) = 1 := by
  simp [eulerReciprocalSeries]

theorem eulerProduct_initial (q : K) : PowerSeries.coeff 0 (eulerProductSeries q) = 1 := by
  simp [eulerProductSeries]

theorem eulerReciprocal_coefficient_step (q : K) (n : ℕ)
    (hn : poch q q n ≠ 0) (h1 : 1-q^(n+1) ≠ 0) :
    (1-q^(n+1))*PowerSeries.coeff (n+1) (eulerReciprocalSeries q) =
    PowerSeries.coeff n (eulerReciprocalSeries q) := by
  simp only [eulerReciprocalSeries,PowerSeries.coeff_mk,poch_succ,←pow_succ']
  field_simp

theorem triangular_successor (n : ℕ) :
    (n+1)*((n+1)-1)/2 = n*(n-1)/2+n := by
  simpa only [show 1+1=2 from rfl,Nat.choose_two_right,Nat.choose_one_right,Nat.add_comm] using Nat.choose_succ_succ' n 1

theorem eulerProduct_coefficient_step (q : K) (n : ℕ)
    (hn : poch q q n ≠ 0) (h1 : 1-q^(n+1) ≠ 0) :
    (1-q^(n+1))*PowerSeries.coeff (n+1) (eulerProductSeries q) =
    -q^n*PowerSeries.coeff n (eulerProductSeries q) := by
  simp only [eulerProductSeries,PowerSeries.coeff_mk,poch_succ,←pow_succ',triangular_successor,
    pow_add,pow_one,pow_succ (-1:K)]
  have h1' : 1-q*q^n ≠ 0 := by simpa [pow_succ'] using h1
  field_simp [hn, h1']
  all_goals ring_nf
  all_goals field_simp [h1']
  all_goals ring

theorem firstOrder_coefficients_unique (c : ℕ → K) (f g : ℕ → K)
    (h0 : f 0 = g 0) (hf : ∀ n, f (n+1)=c n*f n) (hg : ∀ n, g (n+1)=c n*g n) : f=g := by
  funext n
  induction n with
  | zero => exact h0
  | succ n ih => rw [hf,hg,ih]

theorem scaleSeries_coeff (q : K) (f : PowerSeries K) (n : ℕ) :
    PowerSeries.coeff n (scaleSeries q f) = q^n*PowerSeries.coeff n f := by
  simp [scaleSeries]

theorem eulerReciprocal_functional (q : K) (hq : regular q) :
    eulerReciprocalSeries q = scaleSeries q (eulerReciprocalSeries q)+PowerSeries.X*eulerReciprocalSeries q := by
  ext n
  cases n with
  | zero => simp [scaleSeries]
  | succ n =>
    have h := eulerReciprocal_coefficient_step q n (regular_poch_nonzero q hq n)
      (sub_ne_zero.mpr (Ne.symm (hq.2 (n+1) (by omega))))
    simp only [map_add,scaleSeries_coeff,PowerSeries.coeff_succ_X_mul]
    linear_combination h

theorem eulerProduct_functional (q : K) (hq : regular q) :
    eulerProductSeries q = scaleSeries q (eulerProductSeries q)-PowerSeries.X*scaleSeries q (eulerProductSeries q) := by
  ext n
  cases n with
  | zero => simp [scaleSeries]
  | succ n =>
    have h := eulerProduct_coefficient_step q n (regular_poch_nonzero q hq n)
      (sub_ne_zero.mpr (Ne.symm (hq.2 (n+1) (by omega))))
    simp only [map_sub,scaleSeries_coeff,PowerSeries.coeff_succ_X_mul]
    linear_combination h

theorem aqXPair_initial (a b q : K) : aqXPair a b q 0 = (a,b) := rfl

theorem aqXPair_unique (a b q : K) (v : ℕ → K×K) (h0 : v 0=(a,b))
    (hs : ∀ n, v (n+1) =
      ((v n).2+q^(2*n+1)*(v n).1,
       (v n).2+q^(2*n+1)*(v n).1+q^(n+1)*(1+q^(n+1))*((v n).2+(v n).1))) :
    ∀ n, v n=aqXPair a b q n := by
  intro n
  induction n with
  | zero => exact h0
  | succ n ih => rw [hs,aqXPair,ih]

theorem eulerIntegerFactor_constant (a : ℤ) (m : ℕ) (hm : 0 < m) :
    PowerSeries.constantCoeff (eulerIntegerFactor a m) = 1 := by
  have h : PowerSeries.constantCoeff (1-(PowerSeries.X : PowerSeries ℚ)^m) = 1 := by
    simp [ne_of_gt hm]
  unfold eulerIntegerFactor
  split <;> simp [PowerSeries.constantCoeff_inv,h]

theorem eulerIntegerFactor_inverse_valid (m : ℕ) (hm : 0 < m) :
    (1-(PowerSeries.X : PowerSeries ℚ)^m)*(1-PowerSeries.X^m)⁻¹ = 1 := by
  apply PowerSeries.mul_inv_cancel
  simp [ne_of_gt hm]

theorem eulerTransformCoeff_initial (a : ℕ → ℤ) : eulerTransformCoeff a 0 = 1 := by
  simp [eulerTransformCoeff]

theorem aqRRCoeff_initial (q : K) : aqRRCoeff q 0 = 1 := rfl

theorem aqRRCoeff_equation (q : K) (n : ℕ) (h : 1-q^(n+1) ≠ 0) :
    (1-q^(n+1))*aqRRCoeff q (n+1) = q^(2*n+1)*aqRRCoeff q n := by
  rw [aqRRCoeff]
  field_simp

theorem aqRR_functional (q : K) (hq : regular q) :
    PowerSeries.mk (aqRRCoeff q) = scaleSeries q (PowerSeries.mk (aqRRCoeff q)) +
      PowerSeries.C q * (PowerSeries.X * scaleSeries (q^2) (PowerSeries.mk (aqRRCoeff q))) := by
  ext n
  cases n with
  | zero => simp [scaleSeries]
  | succ n =>
    have h := aqRRCoeff_equation q n
      (sub_ne_zero.mpr (Ne.symm (hq.2 (n+1) (by omega))))
    simp only [map_add,PowerSeries.coeff_C_mul,PowerSeries.coeff_succ_X_mul,
      scaleSeries_coeff,PowerSeries.coeff_mk]
    simp only [pow_add,pow_one,pow_mul] at h
    linear_combination h

theorem sillsC_exponent_nonnegative (k : ℕ) (j : ℤ) (h : 0 ≤ (k:ℤ)+j) :
    0 ≤ (k:ℤ)*((k:ℤ)+j) := mul_nonneg (Nat.cast_nonneg k) h

theorem qDelta_of_nonzero (q x : ℂ) (f : ℂ → ℂ) (hx : x ≠ 0) :
    qDelta q f x = (f x-f (q*x))/x := by simp [qDelta,hx]

theorem qDelta_at_zero (q : ℂ) (f : ℂ → ℂ) : qDelta q f 0 = (1-q)*deriv f 0 := by
  simp [qDelta]

theorem qDelta_jackson (q : ℂ) (f : ℂ → ℂ) (x : ℂ) : qDelta q f x = (1-q)*jackson q f x := by
  by_cases hx : x=0
  · simp [qDelta,jackson,hx]
  by_cases hq : q=1
  · simp [qDelta,jackson,hx,hq]
  have h : 1-q ≠ 0 := sub_ne_zero.mpr (Ne.symm hq)
  simp only [qDelta,jackson,if_neg hx]
  field_simp

theorem fineHG_initial (a b t q : K) : fineHG a b t q 0 = (1,0) := rfl

theorem fineHG_step (a b t q : K) (n : ℕ) :
    (fineHG a b t q (n+1)).1 = fineM a b t q n*(fineHG a b t q n).1 ∧
    (fineHG a b t q (n+1)).2 = (fineHG a b t q n).2+fineL a b t q n*(fineHG a b t q n).1 := by
  constructor <;> rfl

theorem fineHG_unique (a b t q : K) (v : ℕ → K×K) (h0 : v 0=(1,0))
    (hs : ∀ n, v (n+1)=(fineM a b t q n*(v n).1,(v n).2+fineL a b t q n*(v n).1)) :
    ∀ n, v n=fineHG a b t q n := by
  intro n
  induction n with
  | zero => exact h0
  | succ n ih => rw [hs,fineHG,ih]

theorem fineA_initial (a b q : K) : fineA a b q 0 = 1 := by
  simp [fineA,PowerSeries.coeff_zero_eq_constantCoeff,eulerProductSeries,fineC]

theorem fineQ_indices_complete {I : Type*} [Fintype I] (r : I → ℕ) (n : ℕ) (h : ∑ i, r i=n) :
    ∃ v : I → Fin (n+1), (∑ i, (v i).val)=n ∧ ∀ i, (v i).val=r i := by
  classical
  have hb (i : I) : r i ≤ n := by
    rw [←h]
    exact Finset.single_le_sum (fun j _ => Nat.zero_le (r j)) (Finset.mem_univ i)
  exact ⟨fun i => ⟨r i,Nat.lt_succ_of_le (hb i)⟩,h,fun _ => rfl⟩

theorem sillsC_support (q : K) (n : ℕ) (j : ℤ) (hj : j < -(n:ℤ) ∨ (n:ℤ) < j) :
    sillsC q n j = 0 := by
  unfold sillsC
  apply Finset.sum_eq_zero
  intro k hk
  have hk' : k ≤ n := Nat.le_of_lt_succ (Finset.mem_range.mp hk)
  split_ifs with h
  · rcases h with ⟨h1,h2⟩
    rcases hj with h3|h3 <;> omega
  · rfl

theorem sillsAlpha_outside (x q : K) (d k r : ℕ) (h : ¬ d ∣ r) : sillsAlpha x q d k r = 0 := by
  simp [sillsAlpha,h]

theorem sillsAlpha_initial (x q : K) (d k : ℕ) (hx : x ≠ 1) : sillsAlpha x q d k 0 = 1 := by
  have h : 1-x ≠ 0 := sub_ne_zero.mpr (Ne.symm hx)
  simp [sillsAlpha,h]

theorem sillsS_neg_one (x q : K) : sillsS x q (-1) = 1 := by simp [sillsS]

theorem bilateral_shift_bounds (N R : ℕ) (m : ℤ) (hlo : -(R:ℤ) ≤ m) (hhi : m ≤ N) :
    0 ≤ m+R ∧ m+R ≤ N+R := by omega

theorem monotone_difference_exact {k N : ℕ} (v : Fin (k+1) → Fin (N+1)) (hv : Monotone v) (i : Fin k) :
    (v i.succ).val-(v i.castSucc).val+(v i.castSucc).val = (v i.succ).val := by
  apply Nat.sub_add_cancel
  exact hv (by show i.val ≤ i.val+1; omega)

end
end FiniteQBenchmark
