import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Tactic
import Mathlib.LinearAlgebra.Lagrange
import Mathlib.Algebra.Polynomial.RingDivision
import Mathlib.RingTheory.Coprime.Lemmas
import Benchmark.InterpolationAtoms

namespace FiniteQInterpolation
open Polynomial FiniteQBenchmark
set_option autoImplicit false

/-- A finite zero certificate over a characteristic-zero integral domain.
No target identity, coefficient equality or sampled numerical approximation is assumed. -/
theorem zero_of_samples {K : Type*} [CommRing K] [IsDomain K] [CharZero K]
    (p : Polynomial K) (d : ℕ) (hd : p.natDegree ≤ d)
    (hs : ∀ i : Fin (d+1), p.eval (i.val : K) = 0) : p = 0 := by
  apply Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero p
    (f := fun i : Fin (d+1) => (i.val : K))
  · intro i j h
    exact Fin.ext (Nat.cast_injective h)
  · exact hs
  · simpa using Nat.lt_succ_of_le hd

/-- Node separation is an obligation, not a characteristic assumption. -/
theorem zero_of_nodes {K : Type*} [CommRing K] [IsDomain K]
    (p : Polynomial K) (d : ℕ) (nodes : Fin (d+1) → K)
    (hinj : Function.Injective nodes) (hd : p.natDegree ≤ d)
    (hs : ∀ i, p.eval (nodes i) = 0) : p=0 := by
  apply Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero p hinj hs
  simpa using Nat.lt_succ_of_le hd

open scoped BigOperators
/- Symbolic-length source bridge. Its equality is proved by degree and roots,
not by splitting or reindexing the product. -/
variable {K : Type*} [Field K]
noncomputable def segment (q : K) (s n : ℕ) : Polynomial K :=
  ∏ j ∈ Finset.range n, (1 - C (q^(s+j)) * X)
theorem seg_degree (q : K) (s n : ℕ) : (segment q s n).natDegree ≤ n := by
  unfold segment
  calc
    _ ≤ ∑ j ∈ Finset.range n, (1 - C (q^(s+j)) * X : Polynomial K).natDegree := natDegree_prod_le _ _
    _ ≤ ∑ j ∈ Finset.range n, 1 := by
      apply Finset.sum_le_sum
      intro i hi
      compute_degree
    _ = n := by simp
@[simp] theorem seg_zero (q : K) (s n : ℕ) : (segment q s n).eval 0 = 1 := by
  simp only [segment, eval_prod, eval_sub, eval_one, eval_mul, eval_C, eval_X, mul_zero, sub_zero, Finset.prod_const_one]
theorem seg_root (q : K) (hq : q ≠ 0) (s n j : ℕ) (hlo : s ≤ j) (hhi : j < s+n) :
    (segment q s n).eval ((q^j)⁻¹) = 0 := by
  simp only [segment, eval_prod, eval_sub, eval_one, eval_mul, eval_C, eval_X]
  apply Finset.prod_eq_zero (Finset.mem_range.mpr (show j-s<n by omega))
  rw [Nat.add_sub_of_le hlo]
  simp [pow_ne_zero _ hq]
theorem powers_injective (q : K) (hq : q ≠ 0) (hreg : ∀ n : ℕ, 0 < n → q^n ≠ 1) :
    Function.Injective (fun n : ℕ => q^n) := by
  have aux : ∀ i j : ℕ, i ≤ j → q^i = q^j → i=j := by
    intro i j h hij
    by_contra hn
    have hp : 0 < j-i := by omega
    have he : q^(j-i) = 1 := by
      apply (mul_left_cancel₀ (pow_ne_zero i hq))
      rw [← pow_add, Nat.add_sub_of_le h, mul_one]
      exact hij.symm
    exact hreg _ hp he
  intro i j hij
  rcases le_total i j with h | h
  · exact aux i j h hij
  · exact (aux j i h hij.symm).symm

theorem eq_of_geometric_roots (q : K) (hq : q ≠ 0)
    (hreg : ∀ n : ℕ, 0<n → q^n ≠ 1) (n : ℕ)
    (p r : Polynomial K) (hp : p.natDegree ≤ n) (hr : r.natDegree ≤ n)
    (hzero : p.eval 0 = r.eval 0)
    (hroots : ∀ j : Fin n, p.eval ((q^j.val)⁻¹) = r.eval ((q^j.val)⁻¹)) : p=r := by
  apply sub_eq_zero.mp
  apply Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero (p-r)
    (f := fun i : Option (Fin n) => i.elim 0 (fun j => (q^j.val)⁻¹))
  · intro i j h
    cases i with
    | none =>
      cases j with
      | none => rfl
      | some j =>
        simp only [Option.elim_none, Option.elim_some, zero_eq_inv] at h
        exact False.elim ((pow_ne_zero _ hq) h.symm)
    | some i =>
      cases j with
      | none => simp [pow_ne_zero _ hq] at h
      | some j =>
        congr 1
        apply Fin.ext
        apply powers_injective q hq hreg
        simpa using congrArg Inv.inv h
  · intro i
    cases i with
    | none => simpa using sub_eq_zero.mpr hzero
    | some j => simpa using sub_eq_zero.mpr (hroots j)
  · have hd := natDegree_sub_le p r
    have hm : max p.natDegree r.natDegree ≤ n := max_le hp hr
    simpa using Nat.lt_succ_of_le (hd.trans hm)

theorem segment_split (q : K) (hq : q ≠ 0)
    (hreg : ∀ n : ℕ, 0<n → q^n ≠ 1) (n k : ℕ) (hk : k≤n) :
    segment q k (n-k) * segment q 0 k = segment q 0 n := by
  apply eq_of_geometric_roots q hq hreg n
  · exact (natDegree_mul_le).trans ((Nat.add_le_add (seg_degree q k (n-k)) (seg_degree q 0 k)).trans (by omega))
  · exact seg_degree q 0 n
  · simp
  · intro j
    have right := seg_root q hq 0 n j.val (by omega) (by simpa using j.isLt)
    rw [right, eval_mul]
    by_cases hj : j.val < k
    · rw [seg_root q hq 0 k j.val (by omega) (by omega), mul_zero]
    · rw [seg_root q hq k (n-k) j.val (by omega) (by have := j.isLt; omega), zero_mul]

theorem eval_segment (a q : K) (s n : ℕ) :
    (segment q s n).eval a = FiniteQBenchmark.poch (a*q^s) q n := by
  simp only [segment, eval_prod, eval_sub, eval_one, eval_mul, eval_C, eval_X, FiniteQBenchmark.poch]
  apply Finset.prod_congr rfl
  intro j hj
  rw [pow_add]
  ring

theorem poch_tail_roots (a q : K) (n k : ℕ) (hq : q ≠ 0)
    (hreg : ∀ n : ℕ, 0<n → q^n ≠ 1) (hk : k≤n) (hd : FiniteQBenchmark.poch a q k ≠ 0) :
    FiniteQBenchmark.poch (a*q^k) q (n-k) = FiniteQBenchmark.poch a q n / FiniteQBenchmark.poch a q k := by
  apply (eq_div_iff hd).mpr
  have hp := congrArg (Polynomial.eval a) (segment_split q hq hreg n k hk)
  simpa only [eval_mul, eval_segment, pow_zero, mul_one] using hp


variable {K : Type*} [Field K]

def triangle (n : ℕ) : ℤ := (n:ℤ)*((n:ℤ)-1)/2
lemma triangle_sum (n : ℕ) : triangle n = ∑ j ∈ Finset.range n, (j:ℤ) := by
  have h : (∑ j ∈ Finset.range n, (j:ℤ))*2 = (n:ℤ)*((n:ℤ)-1) := by
    induction n with
    | zero => simp
    | succ n ih => rw [Finset.sum_range_succ]; push_cast; nlinarith
  unfold triangle
  omega
lemma triangle_twice (n : ℕ) : 2*triangle n = (n:ℤ)*((n:ℤ)-1) := by
  have h : (∑ j ∈ Finset.range n, (j:ℤ))*2 = (n:ℤ)*((n:ℤ)-1) := by
    induction n with
    | zero => simp
    | succ n ih => rw [Finset.sum_range_succ]; push_cast; nlinarith
  rw [triangle_sum]; nlinarith
lemma prod_zpowers (q : K) (hq : q ≠ 0) (f : ℕ → ℤ) (n : ℕ) :
    ∏ j ∈ Finset.range n, q^(f j) = q^(∑ j ∈ Finset.range n, f j) := by
  induction n with
  | zero => simp
  | succ n ih => simp only [Finset.prod_range_succ, Finset.sum_range_succ, ih, zpow_add₀ hq]

noncomputable def inverseSegment (q : K) (s : ℤ) (n : ℕ) : Polynomial K :=
  ∏ j ∈ Finset.range n, (X-C (q^(s+(j:ℤ))))
lemma inverse_degree (q : K) (s : ℤ) (n : ℕ) : (inverseSegment q s n).natDegree ≤ n := by
  unfold inverseSegment
  calc
    _ ≤ ∑ j ∈ Finset.range n, (X-C (q^(s+(j:ℤ))) : Polynomial K).natDegree := natDegree_prod_le _ _
    _ ≤ ∑ j ∈ Finset.range n, 1 := by
      apply Finset.sum_le_sum
      intro j hj
      compute_degree
    _ = n := by simp
lemma inverse_zero (q : K) (hq : q≠0) (s : ℤ) (n : ℕ) :
    (inverseSegment q s n).eval 0 = (-1:K)^n * q^((n:ℤ)*s+triangle n) := by
  simp only [inverseSegment, eval_prod, eval_sub, eval_X, eval_C, zero_sub]
  have he : (∏ j ∈ Finset.range n, -(q^(s+(j:ℤ)))) =
      ∏ j ∈ Finset.range n, (-1:K)*q^(s+(j:ℤ)) := by
    apply Finset.prod_congr rfl
    intro j hj
    ring
  rw [he, Finset.prod_mul_distrib, prod_zpowers q hq]
  simp only [Finset.prod_const, Finset.card_range, Finset.sum_add_distrib,
    Finset.sum_const, nsmul_eq_mul, ← triangle_sum]
lemma inverse_eval (a q : K) (ha : a ≠ 0) (hq : q≠0) (s : ℤ) (n : ℕ) :
    (inverseSegment q s n).eval a = a^n * poch (q^s/a) q n := by
  simp only [inverseSegment, eval_prod, eval_sub, eval_X, eval_C, poch]
  have hc : (∏ _j ∈ Finset.range n, a) = a^n := by simp
  rw [← hc, ← Finset.prod_mul_distrib]
  apply Finset.prod_congr rfl
  intro j hj
  rw [zpow_add₀ hq, zpow_natCast]
  field_simp

lemma reciprocal_polynomial (q : K) (hq : regular q) (n : ℕ) :
    segment q 0 n = C ((-1:K)^n*q^(triangle n)) * inverseSegment q (1-(n:ℤ)) n := by
  apply eq_of_geometric_roots q hq.1 hq.2 n
  · exact seg_degree q 0 n
  · exact (natDegree_C_mul_le _ _).trans (inverse_degree q _ n)
  · rw [seg_zero, eval_mul, eval_C, inverse_zero q hq.1]
    have he : triangle n + ((n:ℤ)*(1-(n:ℤ))+triangle n) = 0 := by
      have := triangle_twice n; nlinarith
    calc
      1 = ((-1:K)*(-1))^n*q^(0:ℤ) := by simp
      _ = ((-1:K)^n*q^(triangle n)) * ((-1:K)^n*q^((n:ℤ)*(1-(n:ℤ))+triangle n)) := by
        rw [← he, zpow_add₀ hq.1, mul_pow]; ring
  · intro j
    rw [seg_root q hq.1 0 n j.val (by omega) (by simpa using j.isLt), eval_mul]
    have hr : (inverseSegment q (1-(n:ℤ)) n).eval ((q^j.val)⁻¹) = 0 := by
      simp only [inverseSegment, eval_prod, eval_sub, eval_X, eval_C]
      apply Finset.prod_eq_zero (Finset.mem_range.mpr (show n-1-j.val<n by have := j.isLt; omega))
      have he : 1-(n:ℤ)+((n-1-j.val:ℕ):ℤ) = -(j.val:ℤ) := by have := j.isLt; omega
      rw [he, zpow_neg, zpow_natCast, sub_self]
    rw [hr, mul_zero]

lemma poch_reciprocal (a q : K) (ha : a≠0) (hq : regular q) (n : ℕ) :
    poch a q n = (-a)^n*q^(triangle n)*poch (q^(1-(n:ℤ))/a) q n := by
  have h := congrArg (Polynomial.eval a) (reciprocal_polynomial q hq n)
  rw [eval_segment, pow_zero, mul_one, eval_mul, eval_C, inverse_eval a q ha hq.1] at h
  rw [h, neg_eq_neg_one_mul a, mul_pow]
  ring

lemma poch_shift_reciprocal (a q : K) (ha : a≠0) (hq : regular q) (s : ℤ) (n : ℕ) :
    poch (a*q^s) q n = (-a)^n*q^(s*(n:ℤ)+triangle n)*
      poch (q^(1-s-(n:ℤ))/a) q n := by
  rw [poch_reciprocal (a*q^s) q (mul_ne_zero ha (zpow_ne_zero _ hq.1)) hq n]
  have he : q^(1-(n:ℤ))/(a*q^s) = q^(1-s-(n:ℤ))/a := by
    have hi : 1-s-(n:ℤ) = (1-(n:ℤ))-s := by ring
    simp only [hi, zpow_sub₀ hq.1]
    field_simp
  rw [he]
  have hp : (q^s)^n = q^(s*(n:ℤ)) := by rw [zpow_mul, zpow_natCast]
  rw [neg_mul_eq_neg_mul, mul_pow, hp, zpow_add₀ hq.1]
  ring

lemma poch_negative_block (a q : K) (ha : a≠0) (hq : regular q) (m n : ℕ)
    (hn : n≤m) (hd : poch (q/a) q (m-n) ≠ 0) :
    poch (a*q^(-(m:ℤ))) q n =
      (poch (q/a) q m / poch (q/a) q (m-n)) * (-a)^n * q^(triangle n-(m:ℤ)*(n:ℤ)) := by
  rw [poch_shift_reciprocal a q ha hq]
  have he : q^(1-(-(m:ℤ))-(n:ℤ))/a = (q/a)*q^(m-n) := by
    have hi : 1-(-(m:ℤ))-(n:ℤ) = 1+((m-n:ℕ):ℤ) := by omega
    rw [hi, zpow_add₀ hq.1, zpow_one, zpow_natCast]
    ring
  have ht := poch_tail_roots (q/a) q m (m-n) hq.1 hq.2 (by omega) hd
  have hn' : m-(m-n)=n := by omega
  rw [hn'] at ht
  rw [he, ht]
  have hi : -(m:ℤ)*(n:ℤ)+triangle n = triangle n-(m:ℤ)*(n:ℤ) := by ring
  rw [hi]
  ring

lemma poch_shift_cross (a q : K) (hq : regular q) (m n : ℕ) :
    poch (a*q^m) q n * poch a q m = poch (a*q^n) q m * poch a q n := by
  have h₁ := congrArg (Polynomial.eval a) (segment_split q hq.1 hq.2 (m+n) m (by omega))
  have h₂ := congrArg (Polynomial.eval a) (segment_split q hq.1 hq.2 (m+n) n (by omega))
  simpa only [eval_mul, eval_segment, pow_zero, mul_one, Nat.add_sub_cancel_left,
    Nat.add_sub_cancel_right] using h₁.trans h₂.symm

lemma poch_shift_quotient (a q : K) (ha : a≠0) (hq : regular q) (m n : ℕ)
    (hd : poch (q^(1-(n:ℤ))/a) q m ≠ 0) :
    poch (a*q^(-(m:ℤ))) q n =
      (poch a q n * poch (q/a) q m / poch (q^(1-(n:ℤ))/a) q m) * q^(-(m:ℤ)*(n:ℤ)) := by
  rw [div_mul_eq_mul_div, eq_div_iff hd]
  rw [poch_shift_reciprocal a q ha hq, poch_reciprocal a q ha hq]
  have h₁ : q^(1-(-(m:ℤ))-(n:ℤ))/a = (q^(1-(n:ℤ))/a)*q^m := by
    have he : 1-(-(m:ℤ))-(n:ℤ) = (1-(n:ℤ))+(m:ℤ) := by ring
    rw [he, zpow_add₀ hq.1, zpow_natCast]; ring
  have h₂ : (q^(1-(n:ℤ))/a)*q^n = q/a := by
    rw [← zpow_natCast q n]
    calc
      _ = q^((1-(n:ℤ))+(n:ℤ))/a := by rw [zpow_add₀ hq.1]; ring
      _ = q/a := by congr 1; ring_nf; simp
  have hc := poch_shift_cross (q^(1-(n:ℤ))/a) q hq m n
  rw [h₂] at hc
  rw [h₁, zpow_add₀ hq.1]
  calc
    _ = ((-a)^n*q^(triangle n)*q^(-(m:ℤ)*(n:ℤ))) *
      (poch ((q^(1-(n:ℤ))/a)*q^m) q n * poch (q^(1-(n:ℤ))/a) q m) := by ring
    _ = _ := by rw [hc]; ring

lemma negative_triangle_div (n : ℕ) : (-(n:ℤ)*((n:ℤ)-1))/2 = -triangle n := by
  have he : -(n:ℤ)*((n:ℤ)-1) = (-triangle n)*2 := by nlinarith [triangle_twice n]
  rw [he, Int.mul_ediv_cancel _ (by decide : (2:ℤ) ≠ 0)]

/-- Surface normalization is separated from the root certificate. -/
lemma negative_block_view (a q : K) (ha : a≠0) (hq : regular q) (m n l : ℕ) (s e : ℤ)
    (hn : n≤m) (hl : l=m-n) (hs : s=-(m:ℤ))
    (he : e=triangle n-(m:ℤ)*(n:ℤ)) (hd : poch (q/a) q l ≠ 0) :
    poch (a*q^s) q n = (poch (q/a) q m / poch (q/a) q l) * (-a)^n * q^e := by
  subst l; subst s; subst e
  exact poch_negative_block a q ha hq m n hn hd

lemma reciprocal_division_view (a q : K) (ha : a≠0) (hq : regular q)
    (s e : ℤ) (t : K) (n : ℕ) (ht : t=q^(1-s-(n:ℤ))/a)
    (he : e-(n:ℤ)=s*(n:ℤ)+triangle n) :
    poch (a*q^s) q n = ((-a)/q)^n * q^e * poch t q n := by
  rw [poch_shift_reciprocal a q ha hq, ← ht, ← he, zpow_sub₀ hq.1, zpow_natCast, div_pow]
  ring

variable {K : Type*} [Field K]

/-- Arbitrary finite nodes: no numerical truncation and no CharZero assumption. -/
theorem lagrange_sum (n : ℕ) (v : Fin (n+1) → K) (hv : Function.Injective v)
    (P : Polynomial K) (hP : P.natDegree ≤ n) (x : K) :
    (∑ i : Fin (n+1), P.eval (v i) / (∏ j ∈ Finset.univ.erase i, (v i-v j)) *
      (∏ j ∈ Finset.univ.erase i, (x-v j))) = P.eval x := by
  have hp : P.degree < (Finset.univ : Finset (Fin (n+1))).card := by
    apply (Polynomial.degree_le_natDegree).trans_lt
    simp only [Finset.card_univ, Fintype.card_fin]
    exact_mod_cast Nat.lt_succ_of_le hP
  have he := congrArg (Polynomial.eval x) (Lagrange.eq_interpolate hv.injOn hp)
  rw [Lagrange.interpolate_eq_sum] at he
  simpa only [eval_finsetSum, eval_mul, eval_C, eval_prod, eval_sub, eval_X] using he.symm

noncomputable def parameterPoly {r : ℕ} (q : K) (bs : Fin r → K) (ms : Fin r → ℕ) : Polynomial K :=
  ∏ i, (segment q 0 (ms i)).comp (C (bs i)*X)
lemma parameter_degree {r : ℕ} (q : K) (bs : Fin r → K) (ms : Fin r → ℕ) :
    (parameterPoly q bs ms).natDegree ≤ ∑ i, ms i := by
  unfold parameterPoly
  apply (natDegree_prod_le _ _).trans
  apply Finset.sum_le_sum
  intro i hi
  calc
    _ ≤ (segment q 0 (ms i)).natDegree * (C (bs i)*X).natDegree := natDegree_comp_le
    _ ≤ ms i * 1 := Nat.mul_le_mul (seg_degree q 0 (ms i)) (by compute_degree)
    _ = ms i := by omega
lemma parameter_eval {r : ℕ} (q : K) (bs : Fin r → K) (ms : Fin r → ℕ) (x : K) :
    (parameterPoly q bs ms).eval x = ∏ i, poch (bs i*x) q (ms i) := by
  simp only [parameterPoly, eval_prod, eval_comp, eval_mul, eval_C, eval_X,
    eval_segment, pow_zero, mul_one]

theorem poch_lagrange_sum {r n : ℕ} (q : K) (bs : Fin r → K) (ms : Fin r → ℕ)
    (hn : (∑ i, ms i) ≤ n) (v : Fin (n+1) → K) (hv : Function.Injective v) (x : K) :
    (∑ i : Fin (n+1), (∏ j, poch (bs j*v i) q (ms j)) /
      (∏ j ∈ Finset.univ.erase i, (v i-v j)) * (∏ j ∈ Finset.univ.erase i, (x-v j))) =
      ∏ j, poch (bs j*x) q (ms j) := by
  simpa only [parameter_eval] using lagrange_sum n v hv (parameterPoly q bs ms)
    ((parameter_degree q bs ms).trans hn) x

/-- Proper rational reconstruction from all simple principal parts. -/
theorem principal_family (n : ℕ) (v : Fin (n+1) → K) (hv : Function.Injective v)
    (P : Polynomial K) (hP : P.natDegree ≤ n) (x : K)
    (hx : ∀ i, x ≠ v i) :
    (∑ i : Fin (n+1), (P.eval (v i) / (∏ j ∈ Finset.univ.erase i, (v i-v j))) / (x-v i)) =
      P.eval x / (∏ j, (x-v j)) := by
  have hp : P.degree < (Finset.univ : Finset (Fin (n+1))).card := by
    apply (Polynomial.degree_le_natDegree).trans_lt
    simp only [Finset.card_univ, Fintype.card_fin]
    exact_mod_cast Nat.lt_succ_of_le hP
  have he := congrArg (Polynomial.eval x) (Lagrange.eq_interpolate hv.injOn hp)
  rw [Lagrange.eval_interpolate_not_at_node _ (fun i hi => hx i)] at he
  have hd : (∏ j, (x-v j)) ≠ 0 := Finset.prod_ne_zero_iff.mpr (fun i _ => sub_ne_zero.mpr (hx i))
  apply (eq_div_iff hd).mpr
  rw [he]
  simp only [Lagrange.nodal, eval_prod, eval_sub, eval_X, eval_C, Lagrange.nodalWeight]
  rw [mul_comm]
  congr 1
  apply Finset.sum_congr rfl
  intro i hi
  simp only [div_eq_mul_inv, Finset.prod_inv_distrib]
  ring

theorem poch_principal_family {r n : ℕ} (q : K) (bs : Fin r → K) (ms : Fin r → ℕ)
    (hn : (∑ i, ms i) ≤ n) (v : Fin (n+1) → K) (hv : Function.Injective v) (x : K)
    (hx : ∀ i, x ≠ v i) :
    (∑ i : Fin (n+1), ((∏ j, poch (bs j*v i) q (ms j)) /
      (∏ j ∈ Finset.univ.erase i, (v i-v j))) / (x-v i)) =
      (∏ j, poch (bs j*x) q (ms j)) / (∏ j, (x-v j)) := by
  simpa only [parameter_eval] using principal_family n v hv (parameterPoly q bs ms)
    ((parameter_degree q bs ms).trans hn) x hx
lemma geometric_nodes_injective (q : K) (hq : regular q) (n : ℕ) :
    Function.Injective (fun i : Fin (n+1) => q^i.val) :=
  (powers_injective q hq.1 hq.2).comp Fin.val_injective

variable {K : Type*} [Field K]
/-- Multiplicity is certified by divisibility, valid in positive characteristic too.
Coincident roots must be represented once with their total certified multiplicity. -/
theorem zero_of_multiplicity {ι : Type*} [Fintype ι] (P : Polynomial K) (v : ι → K)
    (hv : Function.Injective v) (m : ι → ℕ)
    (hd : P.natDegree < ∑ i, m i)
    (hroot : ∀ i, (X-C (v i))^(m i) ∣ P) : P=0 := by
  by_contra hp
  have hdiv : (∏ i, (X-C (v i))^(m i)) ∣ P := by
    apply Fintype.prod_dvd_of_coprime
    · intro i j hij
      exact (Polynomial.isCoprime_X_sub_C_of_isUnit_sub
        (sub_ne_zero.mpr (hv.ne hij)).isUnit).pow
    · exact hroot
  have hdeg : (∏ i, (X-C (v i))^(m i) : Polynomial K).natDegree = ∑ i, m i := by
    rw [natDegree_prod_of_monic Finset.univ _ (fun i hi => (monic_X_sub_C (v i)).pow (m i))]
    simp only [natDegree_pow, natDegree_X_sub_C, mul_one]
  have hle := Polynomial.natDegree_le_of_dvd hdiv hp
  rw [hdeg] at hle
  omega

noncomputable def squareSegment (q : K) (n : ℕ) : Polynomial K :=
  ∏ j ∈ Finset.range n, (1-C (q^j)^2*X^2)
lemma square_degree (q : K) (n : ℕ) : (squareSegment q n).natDegree ≤ 2*n := by
  apply (natDegree_prod_le _ _).trans
  calc
    _ ≤ ∑ _j ∈ Finset.range n, 2 := by
      apply Finset.sum_le_sum
      intro i hi
      compute_degree
    _ = 2*n := by simp [Nat.mul_comm]
lemma square_eval (a q : K) (n : ℕ) : (squareSegment q n).eval a = FiniteQBenchmark.poch (a^2) (q^2) n := by
  simp only [squareSegment, eval_prod, eval_sub, eval_one, eval_mul, eval_pow, eval_C,
    eval_X, FiniteQBenchmark.poch]
  apply Finset.prod_congr rfl
  intro j hj
  rw [← pow_mul, ← pow_mul, Nat.mul_comm j 2]
  ring
lemma square_root (q : K) (hq : q≠0) (n : ℕ) (j : Fin n) :
    (squareSegment q n).eval ((q^j.val)⁻¹) = 0 := by
  simp only [squareSegment, eval_prod, eval_sub, eval_one, eval_mul, eval_pow, eval_C, eval_X]
  apply Finset.prod_eq_zero (Finset.mem_range.mpr j.isLt)
  field_simp
  ring
lemma square_neg_root (q : K) (hq : q≠0) (n : ℕ) (j : Fin n) :
    (squareSegment q n).eval (-((q^j.val)⁻¹)) = 0 := by
  simpa only [squareSegment, eval_prod, eval_sub, eval_one, eval_mul, eval_pow,
    eval_C, eval_X, neg_sq] using square_root q hq n j
lemma square_zero (q : K) (n : ℕ) : (squareSegment q n).eval 0 = 1 := by
  simp only [squareSegment, eval_prod, eval_sub, eval_one, eval_mul, eval_pow,
    eval_C, eval_X, zero_pow (by decide : (2:ℕ) ≠ 0), mul_zero, sub_zero, Finset.prod_const_one]

noncomputable def signedNode (q : K) {n : ℕ} (i : Fin n × Bool) : K :=
  if i.2 then (q^i.1.val)⁻¹ else -(q^i.1.val)⁻¹
lemma signedNode_ne_zero (q : K) (hq : q≠0) {n : ℕ} (i : Fin n × Bool) : signedNode q i ≠ 0 := by
  rcases i with ⟨j,b⟩
  cases b <;> simp [signedNode, pow_ne_zero _ hq]
lemma signedNode_injective (q : K) (hq : FiniteQBenchmark.regular q) (h₂ : (2:K) ≠ 0) (n : ℕ) :
    Function.Injective (signedNode q : Fin n × Bool → K) := by
  rintro ⟨i,b⟩ ⟨j,c⟩ h
  have hs : ((q^i.val)⁻¹)^2 = ((q^j.val)⁻¹)^2 := by
    have hh := congrArg (fun x : K => x^2) h
    cases b <;> cases c <;> simpa [signedNode] using hh
  have hij : i=j := by
    have he : (q^i.val)^2 = (q^j.val)^2 := by
      simpa only [inv_pow,inv_inv] using congrArg Inv.inv hs
    have hh := powers_injective q hq.1 hq.2 (by simpa only [←pow_mul] using he)
    apply Fin.ext
    omega
  subst j
  have hbc : b=c := by
    cases b <;> cases c
    · rfl
    · exfalso
      have hh : (2:K)*(q^i.val)⁻¹=0 := by
        simp only [signedNode, Bool.false_eq_true, ↓reduceIte] at h
        linear_combination -h
      exact (mul_ne_zero h₂ (inv_ne_zero (pow_ne_zero _ hq.1))) hh
    · exfalso
      have hh : (2:K)*(q^i.val)⁻¹=0 := by
        simp only [signedNode, Bool.false_eq_true, ↓reduceIte] at h
        linear_combination h
      exact (mul_ne_zero h₂ (inv_ne_zero (pow_ne_zero _ hq.1))) hh
    · rfl
  subst c
  rfl

lemma square_polynomial (q : K) (hq : FiniteQBenchmark.regular q) (n : ℕ) :
    squareSegment q n = segment q 0 n * (segment q 0 n).comp (-X) := by
  let P := squareSegment q n
  let R := segment q 0 n * (segment q 0 n).comp (-X)
  have hp : P.natDegree ≤ 2*n := square_degree q n
  have hr : R.natDegree ≤ 2*n := by
    apply natDegree_mul_le.trans
    have hc : ((segment q 0 n).comp (-X)).natDegree ≤ n := by
      apply natDegree_comp_le.trans
      exact (Nat.mul_le_mul (seg_degree q 0 n) (by compute_degree)).trans (by omega)
    exact (Nat.add_le_add (seg_degree q 0 n) hc).trans (by omega)
  have hzero : P.eval 0 = R.eval 0 := by simp [P,R,square_zero,eval_comp]
  have hpos (j : Fin n) : R.eval ((q^j.val)⁻¹) = 0 := by
    simp only [R,eval_mul,seg_root q hq.1 0 n j.val (by omega) (by simpa using j.isLt),zero_mul]
  have hneg (j : Fin n) : R.eval (-((q^j.val)⁻¹)) = 0 := by
    simp only [R,eval_mul,eval_comp,eval_neg,eval_X,neg_neg,
      seg_root q hq.1 0 n j.val (by omega) (by simpa using j.isLt),mul_zero]
  by_cases h₂ : (2:K)=0
  · have hn (x : K) : -x=x := by
      have hh : (2:K)*x=0 := by rw [h₂,zero_mul]
      linear_combination -hh
    let v : Option (Fin n) → K := fun i => i.elim 0 (fun j => (q^j.val)⁻¹)
    have hv : Function.Injective v := by
      intro i j h
      cases i with
      | none =>
        cases j with
        | none => rfl
        | some j => exact False.elim ((inv_ne_zero (pow_ne_zero _ hq.1)) h.symm)
      | some i =>
        cases j with
        | none => exact False.elim ((inv_ne_zero (pow_ne_zero _ hq.1)) h)
        | some j =>
          congr 1
          apply Fin.ext
          exact powers_injective q hq.1 hq.2 (by simpa [v] using congrArg Inv.inv h)
    -- The certificate is indexed by Option (Fin n); use the general finite type form below.
    have hd : (P-R).natDegree < ∑ i : Option (Fin n), (if i.isNone then 1 else 2) := by
      have hh := (natDegree_sub_le P R).trans (max_le hp hr)
      simp [Fintype.sum_option]

      omega
    have hroot (i : Option (Fin n)) : (X-C (v i))^(if i.isNone then 1 else 2) ∣ P-R := by
      cases i with
      | none =>
        simp only [v,Option.elim_none,Option.isNone_none,↓reduceIte,pow_one]
        apply dvd_iff_isRoot.mpr
        simpa [IsRoot.def,eval_sub] using sub_eq_zero.mpr hzero
      | some j =>
        simp only [v,Option.elim_some,Option.isNone_some,↓reduceIte]
        have hl : (X-C ((q^j.val)⁻¹)) ∣ (1-C (q^j.val)*X : Polynomial K) := by
          apply dvd_iff_isRoot.mpr
          simp [IsRoot.def,pow_ne_zero _ hq.1]
        have hh : (X-C ((q^j.val)⁻¹)) ∣ (1+C (q^j.val)*X : Polynomial K) := by
          apply dvd_iff_isRoot.mpr
          norm_num [IsRoot.def,pow_ne_zero _ hq.1]
          exact h₂
        have hlhs : (X-C ((q^j.val)⁻¹))^2 ∣ P := by
          have hm := mul_dvd_mul hl hh
          have hf : (1-C (q^j.val)*X)*(1+C (q^j.val)*X) = (1-C (q^j.val)^2*X^2 : Polynomial K) := by ring
          rw [hf,←pow_two] at hm
          exact hm.trans (Finset.dvd_prod_of_mem _ (Finset.mem_range.mpr j.isLt))
        have ha : X-C ((q^j.val)⁻¹) ∣ segment q 0 n := by
          apply dvd_iff_isRoot.mpr
          exact seg_root q hq.1 0 n j.val (by omega) (by simpa using j.isLt)
        have hb : X-C ((q^j.val)⁻¹) ∣ (segment q 0 n).comp (-X) := by
          apply dvd_iff_isRoot.mpr
          simpa only [IsRoot.def,eval_comp,eval_neg,eval_X,hn] using
            seg_root q hq.1 0 n j.val (by omega) (by simpa using j.isLt)
        have hrhs : (X-C ((q^j.val)⁻¹))^2 ∣ R := by simpa only [pow_two] using mul_dvd_mul ha hb
        exact dvd_sub hlhs hrhs
    -- Finite-type multiplicity checker, with symbolic index cardinality.
    have hz := zero_of_multiplicity (P-R) v hv (fun i => if i.isNone then 1 else 2) hd hroot
    exact sub_eq_zero.mp hz
  · apply Polynomial.eq_of_natDegree_lt_card_of_eval_eq P R
      (f := fun i : Option (Fin n × Bool) => i.elim 0 (signedNode q))
    · intro i j h
      cases i with
      | none =>
        cases j with
        | none => rfl
        | some j => exact False.elim (signedNode_ne_zero q hq.1 j h.symm)
      | some i =>
        cases j with
        | none => exact False.elim (signedNode_ne_zero q hq.1 i h)
        | some j => exact congrArg some (signedNode_injective q hq h₂ n h)
    · intro i
      cases i with
      | none => exact hzero
      | some i =>
        rcases i with ⟨j,b⟩
        cases b
        · exact (square_neg_root q hq.1 n j).trans (hneg j).symm
        · exact (square_root q hq.1 n j).trans (hpos j).symm
    · have hm := max_le hp hr
      simp only [Fintype.card_option,Fintype.card_prod,Fintype.card_fin,Fintype.card_bool]
      omega

lemma poch_square_roots (a q : K) (hq : FiniteQBenchmark.regular q) (n : ℕ) :
    FiniteQBenchmark.poch (a^2) (q^2) n = FiniteQBenchmark.poch a q n * FiniteQBenchmark.poch (-a) q n := by
  have h := congrArg (Polynomial.eval a) (square_polynomial q hq n)
  simpa only [square_eval,eval_mul,eval_comp,eval_neg,eval_X,eval_segment,pow_zero,mul_one] using h

lemma poch_nonzero_prefix (a q : K) {n k : ℕ} (hk : k≤n) (h : poch a q n ≠ 0) :
    poch a q k ≠ 0 := by
  simp only [poch, Finset.prod_ne_zero_iff, Finset.mem_range] at h ⊢
  intro i hi
  exact h i (lt_of_lt_of_le hi hk)
lemma poch_q_nonzero (q : K) (hq : regular q) (n : ℕ) : poch q q n ≠ 0 := by
  apply Finset.prod_ne_zero_iff.mpr
  intro i hi
  rw [← pow_succ']
  exact sub_ne_zero.mpr (Ne.symm (hq.2 (i+1) (by omega)))
lemma poch_shift_ratio (a q : K) (hq : regular q) (m k : ℕ)
    (hm : poch a q m ≠ 0) (hk : poch a q k ≠ 0) :
    poch (a*q^m) q k / poch a q k = poch (a*q^k) q m / poch a q m := by
  apply (div_eq_div_iff hk hm).mpr
  exact poch_shift_cross a q hq m k

-- An erased nodal product is split only to compute a local Lagrange weight.
lemma erased_range_product (f : ℕ → K) (k t : ℕ) :
    (∏ j ∈ (Finset.range (k+1+t)).erase k, f j) =
    (∏ j ∈ Finset.range k, f j) * (∏ j ∈ Finset.range t, f (k+1+j)) := by
  induction t with
  | zero => simp [Finset.range_add_one]
  | succ t ih =>
    rw [show k+1+(t+1)=(k+1+t)+1 by omega, Finset.range_add_one,
      Finset.erase_insert_of_ne (by omega : k+1+t ≠ k),
      Finset.prod_insert (by simp), ih, Finset.prod_range_succ]
    ring

lemma erased_fin_product (f : ℕ → K) (n : ℕ) (k : Fin (n+1)) :
    (∏ j ∈ Finset.univ.erase k, f j.val) =
    (∏ j ∈ (Finset.range (n+1)).erase k.val, f j) := by
  apply Finset.prod_bij (fun j _ => j.val)
  · intro j hj
    simp only [Finset.mem_erase, Finset.mem_univ, and_true] at hj
    simp only [Finset.mem_erase, Finset.mem_range]
    exact ⟨fun h => hj (Fin.ext h), j.isLt⟩
  · intro a ha b hb h; exact Fin.ext h
  · intro b hb
    simp only [Finset.mem_erase, Finset.mem_range] at hb
    exact ⟨⟨b,hb.2⟩, by simp only [Finset.mem_erase, Finset.mem_univ, and_true]; intro h; exact hb.1 (congrArg Fin.val h), rfl⟩
  · intros; rfl

lemma nodal_numerator (q b : K) (hb : b≠0) (n : ℕ) (k : Fin (n+1)) :
    (∏ j ∈ Finset.univ.erase k, ((1/b)-q^j.val)) =
    b⁻¹^n * poch b q k.val * poch (b*q^(k.val+1)) q (n-k.val) := by
  rw [erased_fin_product (fun j => 1/b-q^j) n k]
  have hs := erased_range_product (fun j => 1/b-q^j) k.val (n-k.val)
  simp only [show k.val+1+(n-k.val)=n+1 by omega] at hs
  rw [hs]
  have h₁ : (∏ j ∈ Finset.range k.val, ((1/b)-q^j)) = b⁻¹^k.val * poch b q k.val := by
    rw [poch, ← show (∏ _j ∈ Finset.range k.val, b⁻¹) = b⁻¹^k.val by simp, ← Finset.prod_mul_distrib]
    apply Finset.prod_congr rfl
    intro j hj
    field_simp
  have h₂ : (∏ j ∈ Finset.range (n-k.val), ((1/b)-q^(k.val+1+j))) =
      b⁻¹^(n-k.val) * poch (b*q^(k.val+1)) q (n-k.val) := by
    rw [poch, ← show (∏ _j ∈ Finset.range (n-k.val), b⁻¹) = b⁻¹^(n-k.val) by simp, ← Finset.prod_mul_distrib]
    apply Finset.prod_congr rfl
    intro j hj
    rw [pow_add]
    field_simp
  rw [h₁,h₂]
  have he : b⁻¹^k.val * b⁻¹^(n-k.val) = b⁻¹^n := by rw [← pow_add, Nat.add_sub_of_le (by omega)]
  calc
    _ = (b⁻¹^k.val * b⁻¹^(n-k.val)) * poch b q k.val * poch (b*q^(k.val+1)) q (n-k.val) := by ring
    _ = _ := by rw [he]
lemma nodal_denominator (q : K) (hq : regular q) (n : ℕ) (k : Fin (n+1)) :
    (∏ j ∈ Finset.univ.erase k, (q^k.val-q^j.val)) =
    (-1 : K)^k.val * q^((n:ℤ)*k.val-triangle k.val-k.val) *
      poch q q k.val * poch q q (n-k.val) := by
  rw [erased_fin_product (fun j => q^k.val-q^j) n k]
  have hs := erased_range_product (fun j => q^k.val-q^j) k.val (n-k.val)
  simp only [show k.val+1+(n-k.val)=n+1 by omega] at hs
  rw [hs]
  have h₁ : (∏ j ∈ Finset.range k.val, (q^k.val-q^j)) =
      (q^k.val)^k.val * poch (q^(-(k.val:ℤ))) q k.val := by
    rw [poch, ← show (∏ _j ∈ Finset.range k.val, q^k.val) = (q^k.val)^k.val by simp,
      ← Finset.prod_mul_distrib]
    apply Finset.prod_congr rfl
    intro j hj
    rw [zpow_neg, zpow_natCast]
    field_simp [hq.1]
  have h₂ : (∏ j ∈ Finset.range (n-k.val), (q^k.val-q^(k.val+1+j))) =
      (q^k.val)^(n-k.val) * poch q q (n-k.val) := by
    rw [poch, ← show (∏ _j ∈ Finset.range (n-k.val), q^k.val) = (q^k.val)^(n-k.val) by simp,
      ← Finset.prod_mul_distrib]
    apply Finset.prod_congr rfl
    intro j hj
    simp only [pow_add, pow_one]
    ring
  rw [h₁,h₂]
  have hn := poch_negative_block (1:K) q one_ne_zero hq k.val k.val (le_refl _) (by simp [poch])
  simp only [one_mul, div_one, Nat.sub_self, poch, Finset.range_zero, Finset.prod_empty] at hn
  change poch (q^(-(k.val:ℤ))) q k.val = poch q q k.val * (-1:K)^k.val * q^(triangle k.val-(k.val:ℤ)*k.val) at hn
  rw [hn]
  have he : (q^k.val)^k.val * (q^k.val)^(n-k.val) *
      q^(triangle k.val-(k.val:ℤ)*k.val) = q^((n:ℤ)*k.val-triangle k.val-k.val) := by
    rw [← pow_add, Nat.add_sub_of_le (by omega), ← pow_mul, ← zpow_natCast,
      ← zpow_add₀ hq.1]
    congr 1
    have ht := triangle_twice k.val
    push_cast
    nlinarith
  calc
    _ = ((q^k.val)^k.val * (q^k.val)^(n-k.val) * q^(triangle k.val-(k.val:ℤ)*k.val)) *
      (-1:K)^k.val * poch q q k.val * poch q q (n-k.val) := by ring
    _ = _ := by rw [he]; ring
lemma geometric_lagrange_weight (q b : K) (hq : regular q) (hb : b≠0)
    (n : ℕ) (hbn : poch (b*q) q n ≠ 0) (k : Fin (n+1)) :
    (b^n * poch q q n / poch (b*q) q n) *
      ((∏ j ∈ Finset.univ.erase k, ((1/b)-q^j.val)) /
       (∏ j ∈ Finset.univ.erase k, (q^k.val-q^j.val))) =
    (poch (q^(-(n:ℤ))) q k.val * poch b q k.val /
      (poch q q k.val * poch (b*q) q k.val)) * q^k.val := by
  have hk : k.val≤n := by omega
  have hbk := poch_nonzero_prefix (b*q) q hk hbn
  have hqk := poch_q_nonzero q hq k.val
  have hqnk := poch_q_nonzero q hq (n-k.val)
  rw [nodal_numerator q b hb, nodal_denominator q hq]
  have ht := poch_tail_roots (b*q) q n k.val hq.1 hq.2 hk hbk
  have he : b*q*q^k.val = b*q^(k.val+1) := by rw [pow_succ]; ring
  rw [he] at ht
  rw [ht]
  have hn := poch_negative_block (1:K) q one_ne_zero hq n k.val hk (by simpa using hqnk)
  simp only [one_mul, div_one] at hn
  rw [hn]
  have hz : q^((n:ℤ)*k.val-triangle k.val-k.val) *
      q^(triangle k.val-(n:ℤ)*k.val) * q^k.val = 1 := by
    rw [← zpow_natCast q k.val, ← zpow_add₀ hq.1, ← zpow_add₀ hq.1]
    convert zpow_zero q using 1 <;> congr 1 <;> ring
  have hsign : (-1:K)^k.val * (-1:K)^k.val = 1 := by rw [← mul_pow]; simp
  have hp : b^n * b⁻¹^n = 1 := by rw [← mul_pow]; simp [hb]
  field_simp [hbn,hbk,hqk,hqnk,hb,hq.1]
  linear_combination -poch q q n * poch b q k.val * (congrArg₂ (· * ·) hsign hz) + poch q q n * poch b q k.val * hp
theorem geometric_polynomial_sum (q b : K) (hq : regular q) (hb : b≠0)
    (n : ℕ) (hbn : poch (b*q) q n ≠ 0) (P : Polynomial K) (hP : P.natDegree≤n) :
    (∑ k : Fin (n+1), (poch (q^(-(n:ℤ))) q k.val * poch b q k.val /
      (poch q q k.val * poch (b*q) q k.val)) * q^k.val * P.eval (q^k.val)) =
    (b^n * poch q q n / poch (b*q) q n) * P.eval (1/b) := by
  have h := lagrange_sum n (fun k => q^k.val) (geometric_nodes_injective q hq n) P hP (1/b)
  rw [← h, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k hk
  rw [← geometric_lagrange_weight q b hq hb n hbn k]
  ring

lemma list_poch_ofFn {r : ℕ} (bs : Fin r → K) (q : K) (k : ℕ) :
    pochList (List.ofFn bs) q k = ∏ i, poch (bs i) q k := by
  simp [pochList, List.map_ofFn, List.prod_ofFn, Function.comp_def]

lemma shifted_phi_term {r : ℕ} (q b : K) (bs : Fin r → K) (ms : Fin r → ℕ)
    (hq : regular q) (hr : ∀ i, poch (bs i) q (ms i) ≠ 0) (n k : ℕ)
    (hd : pochList (q :: b*q :: List.ofFn bs) q k ≠ 0) :
    phiTerm (q^(-(n:ℤ)) :: b :: List.ofFn (fun i => bs i*q^(ms i)))
      (b*q :: List.ofFn bs) q q k =
    ((poch (q^(-(n:ℤ))) q k * poch b q k /
      (poch q q k * poch (b*q) q k)) * q^k) *
      ((parameterPoly q bs ms).eval (q^k) / (∏ i, poch (bs i) q (ms i))) := by
  have hdi : ∀ i, poch (bs i) q k ≠ 0 := by
    simp only [pochList, List.map_cons, List.prod_cons, mul_ne_zero_iff] at hd
    have hh : (∏ i, poch (bs i) q k) ≠ 0 := by
      simpa only [List.map_ofFn,List.prod_ofFn, Function.comp_def] using hd.2.2
    exact fun i => (Finset.prod_ne_zero_iff.mp hh) i (Finset.mem_univ i)
  have ratios : (∏ i, poch (bs i*q^(ms i)) q k) / (∏ i, poch (bs i) q k) =
      (∏ i, poch (bs i*q^k) q (ms i)) / (∏ i, poch (bs i) q (ms i)) := by
    rw [← Finset.prod_div_distrib, ← Finset.prod_div_distrib]
    apply Finset.prod_congr rfl
    intro i hi
    exact poch_shift_ratio (bs i) q hq (ms i) k (hr i) (hdi i)
  unfold phiTerm
  simp only [List.length_cons, List.length_ofFn]
  have he : (1:ℤ)+(r+1)-(r+1+1)=0 := by omega
  simp only [Nat.cast_add, Nat.cast_one]
  rw [he, zpow_zero, mul_one]
  simp only [pochList, List.map_cons, List.prod_cons, List.map_ofFn, List.prod_ofFn, Function.comp_def]
  rw [parameter_eval]
  calc
    _ = ((poch (q^(-(n:ℤ))) q k * poch b q k /
      (poch q q k * poch (b*q) q k)) * q^k) *
      ((∏ i, poch (bs i*q^(ms i)) q k) / (∏ i, poch (bs i) q k)) := by ring
    _ = _ := by rw [ratios]
/-- The global summation step is Lagrange uniqueness. No summation recurrence is used. -/
theorem shifted_parameter_phi (q b : K) (r n : ℕ) (bs : Fin r → K) (ms : Fin r → ℕ)
    (hq : regular q) (hb : b ≠ 0) (hn : (∑ i, ms i) ≤ n)
    (hd : phiDefined (b*q :: List.ofFn bs) q n)
    (hr : ∀ i, poch (bs i) q (ms i) ≠ 0) :
    phi (q^(-(n:ℤ)) :: b :: List.ofFn (fun i => bs i*q^(ms i)))
      (b*q :: List.ofFn bs) q q n =
    b^n*poch q q n/poch (b*q) q n *
      ∏ i, poch (bs i/b) q (ms i)/poch (bs i) q (ms i) := by
  have hbn : poch (b*q) q n ≠ 0 := by
    have h := hd n le_rfl
    simp only [pochList,List.map_cons,List.prod_cons,mul_ne_zero_iff] at h
    exact h.2.1
  unfold phi
  rw [← Fin.sum_univ_eq_sum_range]
  have ht : ∀ k : Fin (n+1), phiTerm (q^(-(n:ℤ)) :: b :: List.ofFn (fun i => bs i*q^(ms i)))
      (b*q :: List.ofFn bs) q q k.val =
      ((poch (q^(-(n:ℤ))) q k.val * poch b q k.val /
      (poch q q k.val * poch (b*q) q k.val)) * q^k.val) *
      ((parameterPoly q bs ms).eval (q^k.val) / (∏ i, poch (bs i) q (ms i))) := by
    intro k
    exact shifted_phi_term q b bs ms hq hr n k.val (hd k.val (by omega))
  simp_rw [ht]
  calc
    _ = (∑ k : Fin (n+1), (poch (q^(-(n:ℤ))) q k.val * poch b q k.val /
      (poch q q k.val * poch (b*q) q k.val)) * q^k.val *
      (parameterPoly q bs ms).eval (q^k.val)) / (∏ i, poch (bs i) q (ms i)) := by
        rw [Finset.sum_div]
        apply Finset.sum_congr rfl
        intros
        ring
    _ = _ := by
      rw [geometric_polynomial_sum q b hq hb n hbn (parameterPoly q bs ms)
        ((parameter_degree q bs ms).trans hn)]
      rw [parameter_eval, Finset.prod_div_distrib]
      simp only [mul_one_div]
      ring


open Lean Meta Elab Tactic
private partial def triangleArgs (e : Expr) : Array Expr :=
  if e.isAppOfArity ``triangle 1 then #[e.getAppArgs[0]!]
  else e.getAppArgs.foldl (fun xs arg => xs ++ triangleArgs arg) #[]
elab "interpolation_arithmetic" : tactic => withMainContext do
  let target ← getMainTarget
  for n in triangleArgs target do
    let proof ← mkAppM ``triangle_twice #[n]
    let term ← PrettyPrinter.delab proof
    evalTactic (← `(tactic| have _interp_triangle := $term))
  evalTactic (← `(tactic|
    (try simp only [negative_triangle_div, Nat.sub_mul, one_mul] at *
     all_goals first
     | omega
     | (solve | push_cast; dsimp only [triangle]; ring)
     | (solve | push_cast at *; nlinarith)
     | (solve | congr 1 <;> ring_nf <;> norm_num))))
macro "interpolation_obligations" : tactic => `(tactic|
  first
  | assumption
  | (solve | simp only [FiniteQBenchmark.regular] at *; all_goals tauto)
  | (solve | apply geometric_nodes_injective; assumption)
  | (solve | interpolation_arithmetic))

/-- Bounded structural constructors sharing polynomial representations and roots.
A marker is emitted only after every obligation for the constructor closes. -/
private def runStructural (principal : Bool) : TacticM Unit := do
  evalTactic (← `(tactic| try simp only [FiniteQBenchmark.pochList, List.map_cons,
    List.map_nil, List.prod_cons, List.prod_nil, mul_one, zpow_natCast] at *))
  let constructors : Array (String × TSyntax `tactic) := #[
    ("geometric_tail", ← `(tactic| apply poch_tail_roots)),
    ("shift_quotient", ← `(tactic| apply poch_shift_quotient)),
    ("negative_block", ← `(tactic| apply negative_block_view)),
    ("reciprocal_division", ← `(tactic| apply reciprocal_division_view)),
    ("shift_reciprocal", ← `(tactic| apply poch_shift_reciprocal)),
    ("reciprocal", ← `(tactic| apply poch_reciprocal)),
    ("shift_cross", ← `(tactic| apply poch_shift_cross)),
    ("square_multiplicity", ← `(tactic| apply poch_square_roots)),
    ("shifted_parameter_phi", ← `(tactic| apply shifted_parameter_phi)),
    ("geometric_polynomial_sum", ← `(tactic| apply geometric_polynomial_sum)),
    ("poch_lagrange", ← `(tactic| apply poch_lagrange_sum)),
    ("polynomial_lagrange", ← `(tactic| apply lagrange_sum)),
    ("poch_principal_family", ← `(tactic| apply poch_principal_family)),
    ("polynomial_principal_family", ← `(tactic| apply principal_family)),
    ("multiplicity_zero", ← `(tactic| solve_by_elim (maxDepth := 6) [zero_of_multiplicity]))]
  for (name, constructor) in constructors do
    if name.endsWith "principal_family" != principal then continue
    for reverse in [false, true] do
      let saved ← saveState
      try
        if reverse then evalTactic (← `(tactic| symm))
        evalTactic (← `(tactic| solve | $constructor <;> interpolation_obligations))
        logInfo m!"INTERPOLATION_CERTIFICATE:{name}"
        return
      catch _ => saved.restore
  throwError "INTERPOLATION_STRUCTURE_OR_OBLIGATION_UNRESOLVED"
elab "interpolation_symbolic" : tactic => runStructural false
elab "interpolation_principal" : tactic => runStructural true
end FiniteQInterpolation
