import Benchmark.Batch2Auxiliary

namespace FiniteQBenchmark
open scoped BigOperators
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem firstTermination_le (as : List K) (q : K) (n : ℕ) :
    firstTermination as q n ≤ n := by
  classical
  unfold firstTermination
  dsimp only
  split
  next h =>
    exact Nat.le_of_lt_succ (Finset.mem_range.mp (Finset.mem_filter.mp (Finset.min'_mem _ h)).1)
  next h => exact le_rfl

theorem firstTermination_spec (as : List K) (q : K) (n : ℕ)
    (h : ∃ k ≤ n, ∃ a ∈ as, 1-a*q^k=0) :
    terminatesAt as q (firstTermination as q n) := by
  classical
  let ts := (Finset.range (n+1)).filter (fun k => ∃ a ∈ as, 1-a*q^k=0)
  have ht : ts.Nonempty := by
    obtain ⟨k,hk,ha⟩ := h
    exact ⟨k,Finset.mem_filter.mpr ⟨Finset.mem_range.mpr (by omega),ha⟩⟩
  have heq : firstTermination as q n = ts.min' ht := by simp [firstTermination,ts,ht]
  rw [heq]
  constructor
  · exact (Finset.mem_filter.mp (Finset.min'_mem ts ht)).2
  · intro k hk a ha hz
    have hb : ts.min' ht ≤ n := by rw [←heq]; exact firstTermination_le as q n
    have hm : k ∈ ts := Finset.mem_filter.mpr ⟨Finset.mem_range.mpr (by omega),a,ha,hz⟩
    have := Finset.min'_le ts k hm
    omega

theorem poch_zero_after (a q : K) (l k : ℕ) (h : 1-a*q^l=0) (hl : l < k) :
    poch a q k = 0 := by
  exact Finset.prod_eq_zero (Finset.mem_range.mpr hl) h

theorem pochList_zero_of_member (as : List K) (q : K) (k : ℕ) (a : K)
    (ha : a ∈ as) (hz : poch a q k = 0) : pochList as q k = 0 := by
  induction as with
  | nil => simp at ha
  | cons b bs ih =>
    simp only [List.mem_cons] at ha
    rcases ha with rfl | ha
    · simp [pochList_cons,hz]
    · simp [pochList_cons,ih ha]

theorem phiTerm_zero_after (as bs : List K) (q z : K) (l k : ℕ)
    (h : terminatesAt as q l) (hl : l < k) : phiTerm as bs q z k = 0 := by
  obtain ⟨a,ha,hz⟩ := h.1
  have hp := pochList_zero_of_member as q k a ha (poch_zero_after a q l k hz hl)
  simp [phiTerm,hp]

/-- A recursively constructed solution is uniquely specified by its two initial values and equation. -/
theorem recurrencePair_unique (A B C : ℕ → K) (f : ℕ → K × K)
    (h0 : f 0 = (0,1))
    (hprev : ∀ n, (f (n+1)).1 = (f n).2)
    (heq : ∀ n, A n*(f (n+1)).2+C n*(f n).1=B n*(f n).2)
    (ha : ∀ n, A n ≠ 0) (n : ℕ) : f n = recurrencePair A B C n := by
  induction n with
  | zero => exact h0
  | succ n ih =>
    apply Prod.ext
    · simpa [recurrencePair,ih] using hprev n
    · have h := heq n
      rw [ih] at h
      simp only [recurrencePair]
      apply (eq_div_iff (ha n)).mpr
      linear_combination h

/-- The shifted Laurent coordinate has exactly the denominator used by D_q. -/
theorem aw_coordinate_difference (s z : K) (hs : s ≠ 0) (hz : z ≠ 0) :
    (s*z+(s*z)⁻¹)/2-(z/s+(z/s)⁻¹)/2 = (s-s⁻¹)*(z-z⁻¹)/2 := by
  field_simp
  <;> ring

/-- A zero outer coefficient means the inner expression need not be evaluated. -/
theorem zero_weighted_term (c x : K) : (if c=0 then 0 else c*x) = c*x := by
  classical
  split <;> simp_all

theorem recurrencePair_previous (A B C : ℕ → K) (n : ℕ) :
    (recurrencePair A B C n).1 =
      if n=0 then 0 else (recurrencePair A B C (n-1)).2 := by
  cases n <;> simp [recurrencePair]

theorem associatedAW_equation (z a b c d rho q : K) (n : ℕ)
    (ha : awAssocA a b c d q (rho*q^n) ≠ 0) :
    (z+z⁻¹-a-a⁻¹+awAssocA a b c d q (rho*q^n)+awAssocC a b c d q (rho*q^n)) *
        associatedAW z a b c d rho q n =
    awAssocA a b c d q (rho*q^n)*associatedAW z a b c d rho q (n+1) +
    awAssocC a b c d q (rho*q^n)*(if n=0 then 0 else associatedAW z a b c d rho q (n-1)) := by
  simpa only [associatedAW,recurrencePair_previous] using
    (recurrencePair_equation (fun j => awAssocA a b c d q (rho*q^j))
      (fun j => z+z⁻¹-a-a⁻¹+awAssocA a b c d q (rho*q^j)+awAssocC a b c d q (rho*q^j))
      (fun j => awAssocC a b c d q (rho*q^j)) n ha).symm

theorem associatedUltra_equation (z alpha beta q : K) (n : ℕ)
    (ha : (1-alpha*q^(n+1))/(1-alpha*beta*q^n) ≠ 0) :
    (z+z⁻¹)*associatedUltra z alpha beta q n =
      (1-alpha*q^(n+1))/(1-alpha*beta*q^n)*associatedUltra z alpha beta q (n+1) +
      (1-alpha*beta^2*q^((n:ℤ)-1))/(1-alpha*beta*q^n)*
        (if n=0 then 0 else associatedUltra z alpha beta q (n-1)) := by
  simpa only [associatedUltra,recurrencePair_previous] using
    (recurrencePair_equation (fun j => (1-alpha*q^(j+1))/(1-alpha*beta*q^j))
      (fun _ => z+z⁻¹)
      (fun j => (1-alpha*beta^2*q^((j:ℤ)-1))/(1-alpha*beta*q^j)) n ha).symm

/-- Telescoping a finite Laurent geometric progression, including its removable values. -/
theorem laurent_geometric_step (z : K) (hz : z ≠ 0) (d : ℤ) (r n : ℕ) :
    (z^r-1)*(∑ k ∈ Finset.range (n+1), z^(d-(r:ℤ)*k)) =
      z^(d+r)-z^(d-(r:ℤ)*n) := by
  induction n with
  | zero =>
    simp only [Nat.zero_add,Finset.sum_range_one,Nat.cast_zero,mul_zero,sub_zero]
    rw [zpow_add₀ hz,zpow_natCast]
    ring
  | succ n ih =>
    rw [Finset.sum_range_succ,mul_add,ih]
    have hstep : z^r*z^(d-(r:ℤ)*(n+1)) = z^(d-(r:ℤ)*n) := by
      rw [←zpow_natCast z r,←zpow_add₀ hz]
      congr 1
      ring
    push_cast
    linear_combination hstep

theorem laurent_geometric_weighted (z c : K) (hz : z ≠ 0) (d : ℤ) (n : ℕ) :
    (z-c)*(∑ k ∈ Finset.range (n+1), c^k*z^(d-k)) =
      z^(d+1)-c^(n+1)*z^(d-n) := by
  induction n with
  | zero =>
    simp only [Nat.zero_add,Finset.sum_range_one,Nat.cast_zero,sub_zero,pow_zero,one_mul,pow_one]
    rw [zpow_add₀ hz,zpow_one]
    ring
  | succ n ih =>
    rw [Finset.sum_range_succ,mul_add,ih]
    have hstep : z*z^(d-((n:ℤ)+1)) = z^(d-n) := by
      calc
        _ = z^((1:ℤ)+(d-((n:ℤ)+1))) := by rw [zpow_add₀ hz,zpow_one]
        _ = _ := by congr 1; ring
    push_cast
    rw [pow_succ c (n+1)]
    linear_combination c^(n+1)*hstep

theorem laurent_odd_quotient (z : K) (hz : z ≠ 0) (n : ℕ) (hd : z-1 ≠ 0) :
    (∑ k ∈ Finset.range (2*n+1), z^((n:ℤ)-k)) =
      (z^((n:ℤ)+1)-z^(-(n:ℤ)))/(z-1) := by
  have h := laurent_geometric_step z hz (n:ℤ) 1 (2*n)
  have he : (n:ℤ)-1*(2*n) = -(n:ℤ) := by ring
  simp only [pow_one,Nat.cast_one,Nat.cast_mul,Nat.cast_ofNat,one_mul] at h
  have he' : (n:ℤ)-2*n = -(n:ℤ) := by ring
  rw [he'] at h
  apply (eq_div_iff hd).mpr
  simpa [mul_comm] using h

theorem laurent_alternating_quotient (z : K) (hz : z ≠ 0) (n : ℕ) (hd : z+1 ≠ 0) :
    (∑ k ∈ Finset.range (2*n+1), (-1:K)^k*z^((n:ℤ)-k)) =
      (z^((n:ℤ)+1)+z^(-(n:ℤ)))/(z+1) := by
  have h := laurent_geometric_weighted z (-1) hz (n:ℤ) (2*n)
  have he : (n:ℤ)-2*n = -(n:ℤ) := by ring
  have hp : (-1:K)^(2*n+1) = -1 := by simp [pow_add,pow_mul]
  simp only [Nat.cast_mul,Nat.cast_ofNat,he,hp,sub_neg_eq_add,neg_mul,one_mul] at h
  apply (eq_div_iff hd).mpr
  simpa [mul_comm] using h

theorem laurent_even_quotient (z : K) (hz : z ≠ 0) (n : ℕ) (hd : z-z⁻¹ ≠ 0) :
    (∑ k ∈ Finset.range (n+1), z^((n:ℤ)-2*k)) =
      (z^((n:ℤ)+1)-z^(-(n:ℤ)-1))/(z-z⁻¹) := by
  have h := laurent_geometric_step z hz (n:ℤ) 2 n
  have he : (n:ℤ)-2*n = -(n:ℤ) := by ring
  simp only [Nat.cast_ofNat,he] at h
  have hm (t : ℤ) : z*z^t = z^(t+1) := by rw [zpow_add₀ hz,zpow_one]; ring
  have hnum : z*(z^((n:ℤ)+1)-z^(-(n:ℤ)-1)) = z^((n:ℤ)+2)-z^(-(n:ℤ)) := by
    rw [mul_sub,hm,hm]
    congr 1 <;> congr 1 <;> ring
  apply (eq_div_iff hd).mpr
  apply mul_left_cancel₀ hz
  rw [hnum]
  calc
    z*((∑ k ∈ Finset.range (n+1), z^((n:ℤ)-2*k))*(z-z⁻¹)) =
      (z^2-1)*(∑ k ∈ Finset.range (n+1), z^((n:ℤ)-2*k)) := by field_simp <;> ring
    _ = _ := h

end FiniteQBenchmark
