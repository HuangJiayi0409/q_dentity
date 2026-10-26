import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic.Ring
import Benchmark.Gaussian
import Mathlib.Tactic.LinearCombination
import Mathlib.Data.Nat.Choose.Basic
import Benchmark.P1Atoms


/-! Shared proof assembly for P1. These theorems do not search for local relations. -/
namespace FiniteQP1
open scoped BigOperators
variable {K : Type*} [CommRing K]

theorem telescope (G : ℕ → K) (m : ℕ) :
    (∑ k ∈ Finset.range m, (G (k+1) - G k)) = G m - G 0 := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ, ih]
    ring

/-- A growing range has an extra upper term, even when the local relation telescopes. -/
theorem growing_sum_recurrence (F G : ℕ → ℕ → K) (c : ℕ → K)
    (n : ℕ)
    (hlocal : ∀ k ∈ Finset.range (n+1),
      F (n+1) k - c n * F n k = G n (k+1) - G n k) :
    (∑ k ∈ Finset.range (n+2), F (n+1) k) =
      c n * (∑ k ∈ Finset.range (n+1), F n k) +
        (G n (n+1) - G n 0 + F (n+1) (n+1)) := by
  have h := Finset.sum_congr rfl hlocal
  rw [Finset.sum_sub_distrib, ← Finset.mul_sum, telescope] at h
  rw [show n+2 = (n+1)+1 by rfl, Finset.sum_range_succ]
  calc
    _ = ((∑ k ∈ Finset.range (n+1), F (n+1) k) -
        c n * (∑ k ∈ Finset.range (n+1), F n k)) +
        c n * (∑ k ∈ Finset.range (n+1), F n k) + F (n+1) (n+1) := by ring
    _ = _ := by rw [h]; ring

/-- Forward monic recurrence: c n may vanish. No division by the target is needed. -/
theorem first_order_unique (S T c b : ℕ → K)
    (initial : S 0 = T 0)
    (left : ∀ n, S (n+1) = c n * S n + b n)
    (right : ∀ n, T (n+1) = c n * T n + b n) :
    ∀ n, S n = T n := by
  intro n
  induction n with
  | zero => exact initial
  | succ n ih => rw [left, right, ih]

/-- Assemble a complete sum identity once the branch discharges every local obligation. -/
theorem prove_growing_sum (F G : ℕ → ℕ → K) (T c b : ℕ → K)
    (hlocal : ∀ n k, k ∈ Finset.range (n+1) →
      F (n+1) k - c n * F n k = G n (k+1) - G n k)
    (boundary : ∀ n, G n (n+1) - G n 0 + F (n+1) (n+1) = b n)
    (initial : F 0 0 = T 0)
    (target : ∀ n, T (n+1) = c n * T n + b n) :
    ∀ n, (∑ k ∈ Finset.range (n+1), F n k) = T n := by
  apply first_order_unique (fun n => ∑ k ∈ Finset.range (n+1), F n k) T c b
  · simpa using initial
  · intro n
    rw [growing_sum_recurrence F G c n (hlocal n), boundary n]
  · exact target

#print axioms telescope
#print axioms growing_sum_recurrence
#print axioms first_order_unique
#print axioms prove_growing_sum
end FiniteQP1
open FiniteQBenchmark
namespace FiniteQP1
variable {K : Type*} [Field K]
/-- An alternate local recurrence for the Gaussian definition, independent of any sum identity. -/
theorem gaussian_pascal (q : K) (n k : ℕ) (hk : k ≤ n) :
    gaussian q (n+1) (k+1) = gaussian q n (k+1) + q^(n-k)*gaussian q n k := by
  induction n generalizing k with
  | zero =>
    have : k = 0 := by omega
    subst k
    simp [gaussian]
  | succ n ih =>
    by_cases he : k = n+1
    · subst k
      simp [gaussian_self, gaussian_above q (by omega : n+1 < n+1+1)]
    · have hkn : k ≤ n := by omega
      cases k with
      | zero =>
        have h := ih 0 (by omega)
        simp only [Nat.sub_zero, gaussian_zero_right] at h ⊢
        rw [gaussian, gaussian_zero_right]
        rw [h, pow_succ]
        simp only [gaussian, gaussian_zero_right, mul_one] at h
        linear_combination h
      | succ k =>
        have h0 := ih k (by omega)
        have h1 := ih (k+1) hkn
        have hp : n-k = (n-(k+1))+1 := by omega
        simp only [Nat.succ_sub_succ_eq_sub]
        simp only [gaussian] at h0 h1 ⊢
        rw [hp, pow_succ] at h0 ⊢
        simp only [pow_succ] at h0 h1 ⊢
        linear_combination h0 + (q^k*q*q) * h1
end FiniteQP1

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

end FiniteQP1

namespace FiniteQP1
open scoped BigOperators
open FiniteQBenchmark
variable {K : Type*} [Field K]

theorem fall_zero (x a q : K) : kacPowerNat x a q 0 = 1 := by
  simp [kacPowerNat]

/-- The defining finite product recurrence, with no nonzero assumptions. -/
theorem fall_succ (x a q : K) (n : ℕ) :
    kacPowerNat x a q (n+1) = kacPowerNat x a q n * (x-q^n*a) := by
  exact Finset.prod_range_succ (fun i => x-q^i*a) n

theorem product_eq_fall (x a q : K) (n : ℕ) :
    (∏ i ∈ Finset.range n, (x-a*q^i)) = kacPowerNat x a q n := by
  unfold kacPowerNat
  apply Finset.prod_congr rfl
  intro i hi
  ring

end FiniteQP1

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-1.Ex6iii — 终止 2φ0 求值
Original representative source: GR2-1.Ex6iii
Frozen statement: formulas/train/FQI-SRC-GR2-1.Ex6iii.md
Source formula:
{}_2\phi_0^{[n]}\!\left[\begin{matrix}a,q^{-n}\\-\end{matrix};q,q^n/a\right]=a^{-n}.
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity053
variable {K : Type*} [Field K]

theorem statement (a q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 0) :
 phi [a,q^(-(n : ℤ))] [] q (q^n/a) n = a^(-(n : ℤ)) := by
  rw [FiniteQP1.phi_zero_lower_sum a q (by assumption) (by assumption)]
  simp only [zpow_neg, zpow_natCast, ← inv_pow]
  let p1F := fun (p1n p1k : ℕ) => ((FiniteQBenchmark.gaussian q p1n p1k) * (FiniteQBenchmark.kacPowerNat (a)⁻¹ 1 q p1k))
  let p1T := fun (p1n : ℕ) => ((a)⁻¹ ^ p1n)
  let p1C := fun (p1n : ℕ) => (a)⁻¹
  let p1G := fun (p1n p1k : ℕ) => match p1k with
    | 0 => 0
    | p1k+1 => ((q^p1k) + ((-1) * (a)⁻¹)) * p1F p1n p1k
  try simp only [FiniteQP1.product_eq_fall]
  change (∑ p1k ∈ Finset.range (n+1), p1F n p1k) = p1T n
  refine FiniteQP1.prove_growing_sum p1F p1G p1T p1C (fun _ => 0) ?_ ?_ ?_ ?_ n
  · intro p1n p1k hmem
    cases p1k with
    | zero => simp [p1F, p1G, p1C, gaussian_zero_right, FiniteQP1.fall_zero,
        FiniteQP1.fall_succ, poch_succ] <;> ring
    | succ p1k =>
      have hle : p1k ≤ p1n := by simp only [Finset.mem_range] at hmem; omega
      dsimp only [p1F, p1G, p1C]
      solve
      | (rw [FiniteQP1.gaussian_pascal q p1n p1k hle]
         simp only [Nat.triangle_succ, pow_add, pow_succ, FiniteQP1.fall_succ]
         have hp : q^p1k * q^(p1n-p1k) = q^p1n := by
           rw [← pow_add, Nat.add_sub_of_le hle]
         simp only [← hp]
         ring)
      | (simp only [gaussian, FiniteQP1.fall_succ, pow_succ]
         ring)
      | (by_cases he : p1k = p1n
         · subst p1k
           simp [FiniteQP1.gaussian_pascal, gaussian_self, gaussian_above,
             FiniteQP1.fall_zero, FiniteQP1.fall_succ, poch_succ, pow_succ]
           <;> ring
         · have hlen : p1n-p1k = (p1n-(p1k+1))+1 := by omega
           have hp : q^p1n = q^p1k * q^(p1n-(p1k+1)) * q := by
             rw [← pow_add, ← pow_succ]
             congr 1
             omega
           solve
           | (rw [FiniteQP1.gaussian_pascal q p1n p1k hle]
              simp only [Nat.succ_sub_succ_eq_sub, hlen, FiniteQP1.fall_succ,
                poch_succ, pow_succ, hp]
              ring)
           | (simp only [gaussian, Nat.succ_sub_succ_eq_sub, hlen,
                FiniteQP1.fall_succ, poch_succ, pow_succ, hp]
              ring))
  · intro p1n
    dsimp only [p1F, p1G]
    simp only [gaussian_self, Nat.triangle_succ, pow_add, pow_succ, mul_one, sub_zero,
      FiniteQP1.fall_succ, FiniteQP1.fall_zero, Nat.sub_self, poch_zero, poch_succ]
    ring
  · simp [p1F, p1T, gaussian_zero_right, FiniteQBenchmark.poch, FiniteQP1.fall_zero]
  · intro p1n
    dsimp only [p1T, p1C]
    simp only [poch_succ, FiniteQP1.fall_succ, pow_succ]
    ring
end FiniteQBenchmark.Identity053

#print axioms FiniteQBenchmark.Identity053.statement
