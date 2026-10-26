import Benchmark.P1Atoms
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Tactic.LinearCombination

namespace FiniteQP1
open FiniteQBenchmark
variable {K : Type*} [Field K]

theorem regular_poch_ne (q : K) (hq : regular q) (n : ℕ) : poch q q n ≠ 0 := by
  unfold poch
  apply Finset.prod_ne_zero_iff.mpr
  intro i hi
  apply sub_ne_zero.mpr
  rw [mul_comm, ← pow_succ]
  exact Ne.symm (hq.2 (i+1) (by omega))

/-- A terminating upper factor, as a polynomial identity after clearing q powers. -/
theorem terminating_product (q : K) (hq : q ≠ 0) (n k : ℕ) (hk : k ≤ n) :
    poch ((q^n)⁻¹) q k * (q^n)^k * poch q q (n-k) =
      (-1:K)^k * q^(k*(k-1)/2) * poch q q n := by
  induction k with
  | zero => simp
  | succ k ih =>
    have hkn : k ≤ n := by omega
    have hlen : n-k = (n-(k+1))+1 := by omega
    have hp : q^n = q^k * q^(n-(k+1)) * q := by
      rw [← pow_add, ← pow_succ]
      congr 1
      omega
    calc
      _ = -q^k * (poch ((q^n)⁻¹) q k * (q^n)^k * poch q q (n-k)) := by
        rw [poch_succ, pow_succ, hlen, poch_succ]
        have hn : q^n ≠ 0 := pow_ne_zero _ hq
        field_simp
        rw [hp]
        ring
      _ = _ := by
        rw [ih hkn]
        simp only [Nat.triangle_succ, pow_succ, pow_add]
        ring

theorem terminating_quotient (q : K) (hq : q ≠ 0) (n k : ℕ) (hk : k ≤ n)
    (hden : ∀ j ≤ n, poch q q j ≠ 0) :
    poch ((q^n)⁻¹) q k / poch q q k =
      ((-1:K)^k * q^(k*(k-1)/2)) * gaussian q n k / (q^n)^k := by
  have h := terminating_product q hq n k hk
  rw [gaussian_eq_quotient q n k hden]
  simp only [gaussianQuotient, if_pos hk]
  have hk0 := hden k hk
  have hl0 := hden (n-k) (by omega)
  have hn0 : (q^n)^k ≠ 0 := pow_ne_zero _ (pow_ne_zero _ hq)
  field_simp
  simp only [one_div]
  linear_combination h

theorem phi_zero_lower_term (a q : K) (hq : regular q) (ha : a ≠ 0)
    (n k : ℕ) (hk : k ≤ n) :
    phiTerm [a,q^(-(n:ℤ))] [] q (q^n/a) k =
      gaussian q n k * ((a⁻¹)^k * poch a q k) := by
  have hd : ∀ j ≤ n, poch q q j ≠ 0 := fun j _ => regular_poch_ne q hq j
  have ht := terminating_quotient q hq.1 n k hk hd
  have hp : ((-1:K)^k * q^(k*(k-1)/2)) ≠ 0 :=
    mul_ne_zero (pow_ne_zero _ (neg_ne_zero.mpr one_ne_zero)) (pow_ne_zero _ hq.1)
  simp only [phiTerm, pochList_cons, pochList_nil, mul_one, List.length_nil,
    List.length_cons, zpow_neg, zpow_natCast]
  norm_num only
  rw [mul_div_assoc, ht]
  simp only [div_pow, inv_pow]
  have hn0 : (q^n)^k ≠ 0 := pow_ne_zero _ (pow_ne_zero _ hq.1)
  have ha0 : a^k ≠ 0 := pow_ne_zero _ ha
  field_simp [hq.1]
  <;> ring

theorem inverse_poch (a q : K) (ha : a ≠ 0) (k : ℕ) :
    (a⁻¹)^k * poch a q k = kacPowerNat a⁻¹ 1 q k := by
  induction k with
  | zero => simp [kacPowerNat]
  | succ k ih =>
    simp only [kacPowerNat, Finset.prod_range_succ] at ih ⊢
    rw [pow_succ, poch_succ]
    rw [← ih]
    field_simp
    <;> ring

theorem phi_zero_lower_sum (a q : K) (hq : regular q) (ha : a ≠ 0) (n : ℕ) :
    phi [a,q^(-(n:ℤ))] [] q (q^n/a) n =
      ∑ k ∈ Finset.range (n+1), gaussian q n k * kacPowerNat a⁻¹ 1 q k := by
  unfold phi
  apply Finset.sum_congr rfl
  intro k hk
  rw [phi_zero_lower_term a q hq ha n k (by simp only [Finset.mem_range] at hk; omega),
    inverse_poch a q ha k]

set_option maxRecDepth 2048 in
/-- Term representation after clearing the original lower-parameter product. -/
theorem phi_balanced_term (a c q : K) (n k : ℕ) (hq : q ≠ 0) (ha : a ≠ 0)
    (hd : phiDefined [c] q n) (hk : k ≤ n) :
    phiTerm [a,q^(-(n:ℤ))] [c] q (c*q^n/a) k * poch c q n =
      gaussian q n k * (-(c/a))^k * q^(k*(k-1)/2) * poch a q k *
        poch ((a*(c/a))*q^k) q (n-k) := by
  obtain ⟨hqd,hcd⟩ := phi_defined_single c q n hd
  have ht := terminating_quotient q hq n k hk hqd
  have hs := poch_add c q k (n-k)
  rw [Nat.add_sub_of_le hk] at hs
  have hck := hcd k hk
  have hqk := hqd k hk
  have hqn : (q^n)^k ≠ 0 := pow_ne_zero _ (pow_ne_zero _ hq)
  have hak : a^k ≠ 0 := pow_ne_zero _ ha
  have hac : a*(c/a) = c := by field_simp
  rw [hac]
  simp only [phiTerm, pochList_cons, pochList_nil, mul_one, List.length_nil,
    List.length_cons, zpow_neg, zpow_natCast]
  norm_num only
  rw [show poch a q k * poch ((q^n)⁻¹) q k / (poch q q k * poch c q k) =
    poch a q k * (poch ((q^n)⁻¹) q k / poch q q k) / poch c q k by ring]
  rw [ht, hs]
  rw [neg_pow (c/a)]
  simp only [div_pow, mul_pow]
  field_simp
  <;> ring

/-- Finite-sum representation only; this theorem does not evaluate the sum. -/
theorem phi_balanced_sum (a c q : K) (n : ℕ) (hq : q ≠ 0) (ha : a ≠ 0)
    (hd : phiDefined [c] q n) :
    phi [a,q^(-(n:ℤ))] [c] q (c*q^n/a) n =
      (∑ k ∈ Finset.range (n+1), gaussian q n k * (-(c/a))^k *
        q^(k*(k-1)/2) * poch a q k * poch ((a*(c/a))*q^k) q (n-k)) / poch c q n := by
  apply (eq_div_iff ((phi_defined_single c q n hd).2 n le_rfl)).2
  unfold phi
  rw [Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro k hk
  exact phi_balanced_term a c q n k hq ha hd (by simp only [Finset.mem_range] at hk; omega)

/-- A triangular q-power clears the terminating parameter's negative powers. -/
theorem phi_q_term (a c q : K) (n k : ℕ) (hq : q ≠ 0) (ha : a ≠ 0)
    (hd : phiDefined [c] q n) (hk : k ≤ n) :
    phiTerm [a,q^(-(n:ℤ))] [c] q q k * poch c q n * q^(n*(n-1)/2) =
      gaussian q n k * (-1:K)^k * q^((n-k)*(n-k-1)/2) * poch a q k *
        poch ((a*(c/a))*q^k) q (n-k) := by
  obtain ⟨hqd,hcd⟩ := phi_defined_single c q n hd
  have ht := terminating_quotient q hq n k hk hqd
  have hs := poch_add c q k (n-k)
  rw [Nat.add_sub_of_le hk] at hs
  have hck := hcd k hk
  have hqn : (q^n)^k ≠ 0 := pow_ne_zero _ (pow_ne_zero _ hq)
  have hac : a*(c/a) = c := by field_simp
  have hp : q^(n*(n-1)/2)*q^(k*(k-1)/2)*q^k =
      (q^n)^k*q^((n-k)*(n-k-1)/2) := by
    rw [← pow_add, ← pow_add, ← pow_mul, ← pow_add, triangle_split n k hk]
  rw [hac]
  simp only [phiTerm, pochList_cons, pochList_nil, mul_one, List.length_nil,
    List.length_cons, zpow_neg, zpow_natCast]
  norm_num only
  rw [show poch a q k * poch ((q^n)⁻¹) q k / (poch q q k * poch c q k) =
    poch a q k * (poch ((q^n)⁻¹) q k / poch q q k) / poch c q k by ring]
  rw [ht, hs]
  field_simp
  linear_combination gaussian q n k * poch a q k * poch (q^k*c) q (n-k) * hp

/-- Representation of a terminating sum after two justified scalar clearings. -/
theorem phi_q_sum (a c q : K) (n : ℕ) (hq : q ≠ 0) (ha : a ≠ 0)
    (hd : phiDefined [c] q n) :
    phi [a,q^(-(n:ℤ))] [c] q q n * poch c q n * q^(n*(n-1)/2) =
      ∑ k ∈ Finset.range (n+1), gaussian q n k * (-1:K)^k *
        q^((n-k)*(n-k-1)/2) * poch a q k * poch ((a*(c/a))*q^k) q (n-k) := by
  unfold phi
  rw [Finset.sum_mul, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro k hk
  exact phi_q_term a c q n k hq ha hd (by simp only [Finset.mem_range] at hk; omega)

end FiniteQP1
