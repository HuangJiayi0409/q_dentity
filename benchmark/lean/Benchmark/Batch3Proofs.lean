import Benchmark.Batch3Definitions

namespace FiniteQBenchmark
open scoped BigOperators
noncomputable section
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

/-- The finite representation contains every weak composition. -/
theorem composition_coordinate_le {d N : ℕ} (k : Fin d → ℕ)
    (h : ∑ i, k i ≤ N) (j : Fin d) : k j ≤ N := by
  exact (Finset.single_le_sum (fun i _ => Nat.zero_le (k i)) (Finset.mem_univ j)).trans h

theorem compositions_complete {d N : ℕ} (k : Fin d → ℕ) (h : ∑ i, k i = N) :
    ∃ v ∈ compositions d N, ∀ i, (v i).val = k i := by
  classical
  let v : Fin d → Fin (N+1) := fun i => ⟨k i, Nat.lt_succ_of_le (composition_coordinate_le k h.le i)⟩
  exact ⟨v, by simp [compositions, v, h], fun _ => rfl⟩

theorem subCompositions_complete {d N : ℕ} (k : Fin d → ℕ) (h : ∑ i, k i ≤ N) :
    ∃ v ∈ subCompositions d N, ∀ i, (v i).val = k i := by
  classical
  let v : Fin d → Fin (N+1) := fun i => ⟨k i, Nat.lt_succ_of_le (composition_coordinate_le k h i)⟩
  exact ⟨v, by simp [subCompositions, v, h], fun _ => rfl⟩

theorem box_indices_complete {d : ℕ} (m k : Fin d → ℕ) (h : ∀ i, k i ≤ m i) :
    ∃ v : (i : Fin d) → Fin (m i+1), ∀ i, (v i).val = k i :=
  ⟨fun i => ⟨k i, Nat.lt_succ_of_le (h i)⟩, fun _ => rfl⟩

theorem composition_subtraction_exact {d N : ℕ} (k : Fin d → Fin (N+1)) (j : Fin d) :
    ((∑ i, (k i).val)-(k j).val : ℕ) + (k j).val = ∑ i, (k i).val := by
  apply Nat.sub_add_cancel
  exact Finset.single_le_sum (fun i _ => Nat.zero_le (k i).val) (Finset.mem_univ j)

theorem generalizedGaussian_negative (L alpha : ℂ) (k : ℤ) (hk : k < 0) :
    generalizedGaussian L alpha k = 0 := by simp [generalizedGaussian,hk]

theorem generalizedGaussian_zero (L alpha : ℂ) : generalizedGaussian L alpha 0 = 1 := by
  simp [generalizedGaussian]

theorem fixedLog_power_add (L a b : ℂ) :
    Complex.exp (L*(a+b)) = Complex.exp (L*a)*Complex.exp (L*b) := by
  rw [mul_add,Complex.exp_add]

theorem fixedLog_inverse_base (L : ℂ) : Complex.exp (-L) = (Complex.exp L)⁻¹ :=
  Complex.exp_neg L

theorem paired_linear_factors (u v : K) : (1-u*v)*(1+u*v) = 1-u^2*v^2 := by ring

/-- The two square-root pairs in V may be collapsed without selecting a root. -/
theorem paired_pochhammer (u q : K) (n : ℕ) :
    poch u q n*poch (-u) q n = poch (u^2) (q^2) n := by
  induction n with
  | zero => simp
  | succ n ih =>
    simp only [poch_succ]
    rw [show (q^2)^n = (q^n)^2 by rw [←pow_mul,←pow_mul]; congr 1; omega]
    calc
      _ = (poch u q n*poch (-u) q n)*((1-u*q^n)*(1+u*q^n)) := by ring
      _ = _ := by rw [ih,paired_linear_factors]

/-- Cancellation is justified away from its removable zero. -/
theorem removable_identical_ratio (u : K) (hu : u ≠ 0) : u/u = 1 := div_self hu

theorem expansion_diagonal_zero_factor (s q : K) (n : ℕ) :
    1-s^(-(0:ℤ))*q^((n:ℤ)-n) = 0 ∧ 1-s^((n:ℤ)-n-0) = 0 := by simp

theorem expansion_equal_base_factors (q : K) (hq : q ≠ 0) (j n k : ℤ) :
    1-q^(-k)*q^(j-n) = 1-q^(j-n-k) := by
  rw [←zpow_add₀ hq]
  congr 2
  ring

theorem geometric_at_one (n : ℕ) : geometric (1:K) n = n := by simp [geometric]

theorem geometric_telescope (z : K) (n : ℕ) :
    (1-z)*geometric z n = 1-z^n := by
  induction n with
  | zero => simp [geometric]
  | succ n ih =>
    simp only [geometric,Finset.sum_range_succ] at *
    rw [mul_add,ih,pow_succ]
    ring

theorem geometric_quotient (z : K) (n : ℕ) (hz : z ≠ 1) :
    geometric z n = (1-z^n)/(1-z) := by
  apply (eq_div_iff (sub_ne_zero.mpr (Ne.symm hz))).mpr
  simpa [mul_comm] using geometric_telescope z n

theorem schurDInt_neg_one (q : K) : schurDInt q (-1) = 1 := by simp [schurDInt]

theorem schurDInt_of_nat (q : K) (n : ℕ) : schurDInt q n = schurD q (n+1) := by
  simp [schurDInt,show (n:ℤ) ≠ -1 by omega]

/-- Monotone natural arrays have precisely the bounds used in planeRows. -/
theorem plane_column_bound {r k : ℕ} (hr : 0 < r) (n : Fin k → ℕ)
    (a : Fin r → Fin k → ℕ)
    (hcol : ∀ j, Antitone (fun i => a i j))
    (hfirst : ∀ j, a ⟨0,hr⟩ j = n j) (i : Fin r) (j : Fin k) : a i j ≤ n j := by
  rw [←hfirst j]
  exact hcol j (show (⟨0,hr⟩ : Fin r) ≤ i from Nat.zero_le _)

theorem planeRows_complete {r k : ℕ} (hr : 0 < r) (n : Fin k → ℕ)
    (a : Fin r → Fin k → ℕ)
    (hrow : ∀ i, Antitone (a i)) (hcol : ∀ j, Antitone (fun i => a i j))
    (hfirst : ∀ j, a ⟨0,hr⟩ j = n j) :
    ∃ v ∈ planeRows r n, ∀ i j, (v i j).val = a i j := by
  classical
  let v : Fin r → (j : Fin k) → Fin (n j+1) :=
    fun i j => ⟨a i j, Nat.lt_succ_of_le (plane_column_bound hr n a hcol hfirst i j)⟩
  refine ⟨v, ?_, fun _ _ => rfl⟩
  simp only [planeRows,Finset.mem_filter,Finset.mem_univ,true_and]
  refine ⟨hrow,hcol,?_⟩
  intro i hi j
  have he : i = ⟨0,hr⟩ := Fin.ext hi
  simpa only [v,he] using hfirst j

theorem planeBox_complete {r k n : ℕ} (a : Fin r → Fin k → ℕ)
    (hb : ∀ i j, a i j ≤ n) (hrow : ∀ i, Antitone (a i))
    (hcol : ∀ j, Antitone (fun i => a i j)) :
    ∃ v ∈ planeBox k r n, ∀ i j, (v i j).val = a i j := by
  classical
  let v : Fin r → Fin k → Fin (n+1) := fun i j => ⟨a i j, Nat.lt_succ_of_le (hb i j)⟩
  refine ⟨v, ?_, fun _ _ => rfl⟩
  simp only [planeBox,Finset.mem_filter,Finset.mem_univ,true_and]
  exact ⟨fun i x y h => hrow i h, fun j x y h => hcol j h⟩

theorem words_mem_iff {r : ℕ} (m : Fin r → ℕ) (w : Fin (∑ i, m i) → Fin r) :
    w ∈ multisetWords m ↔ ∀ i, (Finset.univ.filter (w · = i)).card = m i := by
  classical
  simp [multisetWords]

/-- AP's Lambda recurrence is polynomial; no actual denominator is introduced. -/
theorem apLambda_initial (q : K) : apLambda q 0 = 1 ∧ apLambda q 1 = 1+q^2+q^4+q^5 := by
  simp [apLambda]
  ring

theorem apLambda_step (q : K) (n : ℕ) :
    apLambda q (n+3) = (1+(q^2+q^4+q^5)*q^(6*(n+2)))*apLambda q (n+2) +
      (q^6+q^7+q^9)*q^(6*(n+1))*(1-q^(6*(n+2)))*apLambda q (n+1) +
      q^11*q^(6*n)*(1-q^(6*(n+2)))*(1-q^(6*(n+1)))*apLambda q n := by
  rw [apLambda]
  simp only [show n+2 ≠ 0 by omega,show ¬n+2 ≤ 1 by omega,ite_false]
  congr 2

/-- The chosen logarithm agrees with every integer power of the base. -/
theorem fixedLog_integer_power (q L : ℂ) (h : Complex.exp L = q) (n : ℤ) :
    Complex.exp (L*n) = q^n := by
  rw [mul_comm,Complex.exp_int_mul,h]

theorem triangular_exponent_nonnegative (j : ℤ) : 0 ≤ j*(j-1) := by
  by_cases h : j ≤ 0
  · have : j-1 ≤ 0 := by omega
    exact mul_nonneg_of_nonpos_of_nonpos h this
  · have h1 : 0 ≤ j-1 := by omega
    exact mul_nonneg (by omega) h1

theorem pentagonal_exponent_nonnegative (j : ℤ) : 0 ≤ j*(3*j+1) := by
  by_cases h : j < 0
  · exact mul_nonneg_of_nonpos_of_nonpos (by omega) (by omega)
  · exact mul_nonneg (by omega) (by omega)

/-- The finite-support hypothesis discards exactly the omitted outer terms. -/
theorem expansion_support_zero (B : ℕ → K) (N : ℕ)
    (hB : ∀ j, N < j → B j = 0) (n k : ℕ) (h : N < n+k) (u : K) :
    B (n+k)*u = 0 := by rw [hB _ h,zero_mul]

theorem apGollnitz_enumeration_complete (N : ℕ) (s : Finset ℕ)
    (hb : ∀ j ∈ s, j ≤ N) (hs : apGollnitzAllowed s) :
    s ∈ ((Finset.range (N+1)).powerset).filter apGollnitzAllowed := by
  classical
  simp only [Finset.mem_filter,Finset.mem_powerset]
  exact ⟨fun j hj => Finset.mem_range.mpr (Nat.lt_succ_of_le (hb j hj)),hs⟩

/-- Denominator-cleared algebra underlying U+V=1 in GR 11.6.5 at p=0. -/
theorem macdonald_local_algebra (a b c d : K) :
    a*(1-b)*(1-c)*(1-d)*(b*c*d-a^2) -
      (1-a)*(b*c-a)*(b*d-a)*(c*d-a) =
      (b-a)*(c-a)*(d-a)*(a-b*c*d) := by ring

theorem macdonald_local_sum (a b c d : K)
    (h : (b-a)*(c-a)*(d-a)*(a-b*c*d) ≠ 0) :
    a*(1-b)*(1-c)*(1-d)*(b*c*d-a^2)/((b-a)*(c-a)*(d-a)*(a-b*c*d)) +
    (1-a)*(b*c-a)*(b*d-a)*(c*d-a)/(-((b-a)*(c-a)*(d-a)*(a-b*c*d))) = 1 := by
  rw [div_neg,←sub_eq_add_neg,←sub_div,macdonald_local_algebra,div_self h]

/-- Three-step recurrence in the coefficient normalization used by the original
infinite generating function; this is a finite algebraic statement. -/
theorem apLambda_coefficient_equation (q : K) (n : ℕ)
    (hn : poch (q^6) (q^6) n ≠ 0)
    (h1 : 1-q^(6*(n+1)) ≠ 0) (h2 : 1-q^(6*(n+2)) ≠ 0)
    (h3 : 1-q^(6*(n+3)) ≠ 0) :
    (1-q^(6*(n+3))) * (apLambda q (n+3)/poch (q^6) (q^6) (n+3)) =
    (1+(q^2+q^4+q^5)*q^(6*(n+2))) * (apLambda q (n+2)/poch (q^6) (q^6) (n+2)) +
    (q^6+q^7+q^9)*q^(6*(n+1)) * (apLambda q (n+1)/poch (q^6) (q^6) (n+1)) +
    q^11*q^(6*n) * (apLambda q n/poch (q^6) (q^6) n) := by
  have hp (j : ℕ) : poch (q^6) (q^6) (j+1) = poch (q^6) (q^6) j*(1-q^(6*(j+1))) := by
    rw [poch_succ,←pow_succ',←pow_mul]
  rw [hp (n+2),hp (n+1),hp n,apLambda_step]
  field_simp [hn,h1,h2,h3]

/-- The coefficient recurrence determines every Lambda, including the two short
initial steps where nonexistent negative coefficients are zero. -/
theorem apLambda_unique (q : K) (f : ℕ → K) (h0 : f 0 = 1)
    (hstep : ∀ n, f (n+1) = (1+(q^2+q^4+q^5)*q^(6*n))*f n +
      (if n = 0 then 0 else (q^6+q^7+q^9)*q^(6*(n-1))*(1-q^(6*n))*f (n-1)) +
      (if n ≤ 1 then 0 else q^11*q^(6*(n-2))*(1-q^(6*n))*(1-q^(6*(n-1)))*f (n-2))) :
    ∀ n, f n = apLambda q n := by
  intro n
  induction n using Nat.strong_induction_on with
  | h n ih =>
    cases n with
    | zero => simpa only [apLambda] using h0
    | succ n =>
      rw [hstep,apLambda,ih n (by omega),ih (n-1) (by omega),ih (n-2) (by omega)]

end
end FiniteQBenchmark
