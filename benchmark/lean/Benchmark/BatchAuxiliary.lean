import Benchmark.BatchDefinitions

namespace FiniteQBenchmark
open scoped BigOperators
variable {K : Type*} [Field K]

theorem regular_poch_nonzero (q : K) (hq : regular q) (n : ℕ) : poch q q n ≠ 0 := by
  apply Finset.prod_ne_zero_iff.mpr
  intro j hj
  apply sub_ne_zero.mpr
  intro h
  apply hq.2 (j+1) (by omega)
  simpa [pow_succ, mul_comm] using h.symm

theorem poch_head (a q : K) (n : ℕ) :
    poch a q (n+1) = (1-a)*poch (a*q) q n := by
  unfold poch
  rw [Finset.prod_range_succ']
  simp only [pow_zero, mul_one]
  rw [mul_comm]
  congr 1
  apply Finset.prod_congr rfl
  intro j hj
  simp only [pow_succ]
  ring

/-- The removable factor in W is canceled by a proved identity. -/
theorem wellPoisedNumerator_eq_raw (a q : K) (k : ℕ) (ha : a ≠ 1) :
    wellPoisedNumerator a q k = (1-a*q^(2*k))/(1-a)*poch a q k := by
  have h : 1-a ≠ 0 := sub_ne_zero.mpr (Ne.symm ha)
  cases k with
  | zero => simp [wellPoisedNumerator, h]
  | succ k =>
    simp only [wellPoisedNumerator, Nat.succ_ne_zero, ite_false, Nat.add_sub_cancel,
      poch_head]
    field_simp

theorem wellPoised_eq_raw (a : K) (bs : List K) (q z : K) (n : ℕ) (ha : a ≠ 1) :
    wellPoised a bs q z n = wellPoisedRaw a bs q z n := by
  apply Finset.sum_congr rfl
  intro k hk
  simp only [wellPoisedNumerator_eq_raw a q k ha, pochList_cons]
  ring

@[simp] theorem gollnitz_neg_one (t q : K) : gollnitz t q (-1) = 1 := by
  simp [gollnitz]

@[simp] theorem gollnitz_neg_seven (t q : K) : gollnitz t q (-7) = 0 := by
  simp [gollnitz]

@[simp] theorem bibasicT_neg_one (a b c p q : K) : bibasicT a b c p q (-1) = 0 := by
  simp [bibasicT]

theorem jackson_of_ne_zero (q x : ℂ) (f : ℂ → ℂ) (hx : x ≠ 0) :
    jackson q f x = (f x-f (q*x))/((1-q)*x) := by
  simp [jackson, hx]

/-- The spectral coordinate for -x uses -t, with the same reciprocal convention. -/
theorem spectral_neg (t : K) : ((-t)+(-t)⁻¹)/2 = -((t+t⁻¹)/2) := by
  simp only [inv_neg]
  ring

/-- GR's specified exponential is indeed a primitive m-th root, by mathlib. -/
theorem canonical_root_primitive (m : ℕ) (hm : 0 < m) :
    IsPrimitiveRoot (Complex.exp (2 * Real.pi * Complex.I * (1/(m : ℂ)))) m := by
  simpa using Complex.isPrimitiveRoot_exp_of_coprime 1 m (by omega) (Nat.coprime_one_left m)

/-- Longer alternating subsequences have the required prefix. -/
theorem oscillates_prefix {a b k i mu nu : ℕ} (l : Fin b → Fin (a+1)) (pos : Bool)
    (h : mu ≤ nu) (hnu : oscillates pos k i nu l) : oscillates pos k i mu l := by
  obtain ⟨js, hjs, hp⟩ := hnu
  refine ⟨fun t => js (Fin.castLE h t), ?_, ?_⟩
  · intro x y hxy
    exact hjs hxy
  · intro t
    exact hp (Fin.castLE h t)


end FiniteQBenchmark
#print axioms FiniteQBenchmark.gaussian_eq_quotient
#print axioms FiniteQBenchmark.regular_poch_nonzero
#print axioms FiniteQBenchmark.wellPoised_eq_raw
#print axioms FiniteQBenchmark.gollnitz_neg_one
#print axioms FiniteQBenchmark.gollnitz_neg_seven
#print axioms FiniteQBenchmark.bibasicT_neg_one
#print axioms FiniteQBenchmark.jackson_of_ne_zero
#print axioms FiniteQBenchmark.spectral_neg

#print axioms FiniteQBenchmark.canonical_root_primitive
#print axioms FiniteQBenchmark.oscillates_prefix
