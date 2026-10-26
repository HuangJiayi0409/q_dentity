import Benchmark.GaussianRules
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.BigOperators.Group.Finset.Sigma
import Mathlib.Order.Fin.Basic
import Mathlib.RingTheory.PowerSeries.Basic
import Benchmark.StructuralAtoms
import Mathlib.Algebra.MonoidAlgebra.Basic
import Mathlib.Algebra.BigOperators.Finsupp.Basic
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic.Ring
import Mathlib.Tactic.SimpRw

open scoped BigOperators
noncomputable section
namespace FiniteQMacMahon
attribute [local instance] Classical.propDecidable
variable {R : Type*} [CommSemiring R]

/-- Finite MacMahon Omega: retain nonnegative auxiliary exponents and set lambda=1.
This is additive, deliberately NOT multiplicative. -/
def omegaGE : AddMonoidAlgebra R ℤ →+ R where
  toFun f := f.coeff.sum (fun e c => if 0 ≤ e then c else 0)
  map_zero' := by simp
  map_add' f g := by
    simp only [AddMonoidAlgebra.coeff_add]
    apply Finsupp.sum_add_index'
    · intro e; simp
    · intro e a b; split_ifs <;> simp

@[simp] theorem omega_single (e : ℤ) (c : R) :
    omegaGE (AddMonoidAlgebra.single e c) = if 0 ≤ e then c else 0 := by
  change (Finsupp.single e c).sum (fun e c => if 0 ≤ e then c else 0) = _
  rw [Finsupp.sum_single_index]
  split_ifs <;> rfl

/-- Encoding one bounded coordinate, including its signed constraint coefficient. -/
def factor (s : Finset ℕ) (a : ℤ) (w : ℕ → R) : AddMonoidAlgebra R ℤ :=
  ∑ i ∈ s, AddMonoidAlgebra.single (a * (i : ℤ)) (w i)

/-- Sound constraint encoding for an arbitrary finite set of integer points. -/
theorem encode {I : Type*} (s : Finset I) (e : I → ℤ) (w : I → R) :
    omegaGE (∑ i ∈ s, AddMonoidAlgebra.single (e i) (w i)) =
      ∑ i ∈ s, if 0 ≤ e i then w i else 0 := by
  simp

/-- Eliminate the auxiliary variable after convolution; projection before
multiplication would be unsound when opposite signs cancel. -/
theorem eliminate_pair (s t : Finset ℕ) (a b c : ℤ) (u v : ℕ → R) :
    omegaGE (AddMonoidAlgebra.single c (1 : R) * factor s a u * factor t b v) =
      ∑ i ∈ s, ∑ j ∈ t,
        if 0 ≤ c + a * (i : ℤ) + b * (j : ℤ) then u i * v j else 0 := by
  simp only [factor, Finset.mul_sum, Finset.sum_mul, AddMonoidAlgebra.single_mul_single,
    map_sum, omega_single, one_mul]
  rw [Finset.sum_comm]

/-- Unit-coefficient inequality elimination, valid for symbolic bounds. -/
theorem eliminate_upper (n m : ℕ) (w : ℕ → R) :
    (∑ j ∈ Finset.range (m+1), if j ≤ n then w j else 0) =
      ∑ j ∈ Finset.range (min n m+1), w j := by
  rw [← Finset.sum_filter]
  congr 1
  ext j
  simp only [Finset.mem_filter, Finset.mem_range]
  omega

/-- Closed finite Omega elimination of i-j >= 0, with arbitrary weights. -/
theorem eliminate_triangle (n m : ℕ) (u v : ℕ → R) :
    omegaGE (factor (Finset.range (n+1)) 1 u * factor (Finset.range (m+1)) (-1) v) =
      ∑ i ∈ Finset.range (n+1), ∑ j ∈ Finset.range (min i m+1), u i * v j := by
  simp only [factor, Finset.sum_mul, Finset.mul_sum, AddMonoidAlgebra.single_mul_single,
    map_sum, omega_single]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i hi
  simp only [one_mul, neg_one_mul]
  have h (j : ℕ) : (0 ≤ (i : ℤ) + -(j : ℤ)) ↔ j ≤ i := by omega
  simp_rw [h]
  exact eliminate_upper i m (fun j => u i * v j)

/-- Simultaneous finite Omega for a family of auxiliary variables. -/
def omegaAll {D : Type*} : AddMonoidAlgebra R (D → ℤ) →+ R where
  toFun f := f.coeff.sum (fun e c => if ∀ d, 0 ≤ e d then c else 0)
  map_zero' := by simp
  map_add' f g := by
    simp only [AddMonoidAlgebra.coeff_add]
    apply Finsupp.sum_add_index'
    · intro e; simp
    · intro e a b; split_ifs <;> simp

@[simp] theorem omegaAll_single {D : Type*} (e : D → ℤ) (c : R) :
    omegaAll (AddMonoidAlgebra.single e c) = if ∀ d, 0 ≤ e d then c else 0 := by
  change (Finsupp.single e c).sum (fun e c => if ∀ d, 0 ≤ e d then c else 0) = _
  rw [Finsupp.sum_single_index]
  split_ifs <;> rfl

/-- Encode all order constraints, without fixing the rectangle dimensions. -/
def rectangleEncoding {K : Type*} [Field K] (q : K) (a b : ℕ) :
    AddMonoidAlgebra K (Fin b × Fin b → ℤ) :=
  ∑ l : Fin b → Fin (a+1), AddMonoidAlgebra.single
    (fun p => if p.1 ≤ p.2 then ((l p.1).val : ℤ) - (l p.2).val else 0)
    (q ^ (∑ i, (l i).val))

/-- A genuine object-to-constraint bridge, not a proof of its Gaussian evaluation. -/
theorem rectangle_omega {K : Type*} [Field K] (q : K) (a b : ℕ) :
    omegaAll (rectangleEncoding q a b) = FiniteQBenchmark.rectangleWeight q a b := by
  classical
  simp only [rectangleEncoding, map_sum, omegaAll_single,
    FiniteQBenchmark.rectangleWeight, FiniteQBenchmark.rectangle, Finset.sum_filter]
  apply Finset.sum_congr rfl
  intro l hl
  have h : (∀ p : Fin b × Fin b, 0 ≤ if p.1 ≤ p.2 then
      ((l p.1).val : ℤ) - (l p.2).val else 0) ↔ Antitone l := by
    constructor
    · intro hp i j hij
      have hx := hp (i,j)
      simp only [hij, ↓reduceIte] at hx
      change (l j).val ≤ (l i).val
      omega
    · intro hl p
      split_ifs with hp
      · have hx := hl hp
        change (l p.2).val ≤ (l p.1).val at hx
        omega
      · exact le_refl 0
  simp only [h]
end FiniteQMacMahon

macro "macmahon_eliminate" : tactic => `(tactic| (
  classical
  first
  | with_reducible exact FiniteQMacMahon.rectangle_omega _ _ _
  | with_reducible exact (FiniteQMacMahon.rectangle_omega _ _ _).symm
  | with_reducible exact FiniteQMacMahon.eliminate_triangle _ _ _ _
  | with_reducible exact (FiniteQMacMahon.eliminate_triangle _ _ _ _).symm
  | with_reducible exact FiniteQMacMahon.eliminate_pair _ _ _ _ _ _ _
  | with_reducible exact (FiniteQMacMahon.eliminate_pair _ _ _ _ _ _ _).symm
  | with_reducible exact FiniteQMacMahon.encode _ _ _
  | with_reducible exact (FiniteQMacMahon.encode _ _ _).symm
  | (simp [FiniteQMacMahon.factor, Finset.sum_mul, Finset.mul_sum, mul_add, add_mul,
      AddMonoidAlgebra.single_mul_single, map_sum, FiniteQMacMahon.omega_single, FiniteQMacMahon.omegaAll_single,
      Finset.sum_range_succ, Finset.sum_range_zero] <;> ring)))


open scoped BigOperators
noncomputable section
namespace FiniteQMacMahon
attribute [local instance] Classical.propDecidable
abbrev Rect (a b : ℕ) := {l : Fin b → Fin (a+1) // Antitone l}

def splitHead {a b : ℕ} (l : Rect a (b+1)) : Σ t : Fin (a+1), Rect t.val b :=
  ⟨l.val 0, ⟨fun i => ⟨(l.val i.succ).val, by
    have h := l.property (Fin.zero_le i.succ)
    have : (l.val i.succ).val ≤ (l.val 0).val := h
    omega⟩, by
      intro i j hij
      exact l.property (Fin.succ_le_succ_iff.mpr hij)⟩⟩

def joinHead {a b : ℕ} (p : Σ t : Fin (a+1), Rect t.val b) : Rect a (b+1) :=
  ⟨Fin.cons p.1 (fun i => ⟨(p.2.val i).val, by
      have h := (p.2.val i).isLt
      have ht := p.1.isLt
      omega⟩), by
    intro i
    refine Fin.cases ?_ (fun i => ?_) i
    · intro j hij
      refine Fin.cases ?_ (fun j => ?_) j
      · exact le_rfl
      · change (p.2.val j).val ≤ p.1.val
        exact Nat.le_of_lt_succ (p.2.val j).isLt
    · intro j
      refine Fin.cases ?_ (fun j => ?_) j
      · intro hij; exact False.elim (by simp at hij)
      · intro hij; exact p.2.property (Fin.succ_le_succ_iff.mp hij)⟩

def headEquiv (a b : ℕ) : Rect a (b+1) ≃ Σ t : Fin (a+1), Rect t.val b where
  toFun := splitHead
  invFun := joinHead
  left_inv l := by
    apply Subtype.ext
    funext i
    refine Fin.cases ?_ (fun i => ?_) i <;> rfl
  right_inv p := by
    rcases p with ⟨t,l⟩
    apply Sigma.ext rfl
    apply heq_of_eq
    apply Subtype.ext
    funext i
    rfl

theorem rectangle_as_sum {K : Type*} [Field K] (q : K) (a b : ℕ) :
    FiniteQBenchmark.rectangleWeight q a b = ∑ l : Rect a b, q^(∑ i, (l.val i).val) := by
  unfold FiniteQBenchmark.rectangleWeight
  apply Finset.sum_subtype
  intro l
  simp [FiniteQBenchmark.rectangle]

theorem rectangle_head_elimination {K : Type*} [Field K] (q : K) (a b : ℕ) :
    FiniteQBenchmark.rectangleWeight q a (b+1) =
      ∑ t : Fin (a+1), q^t.val * FiniteQBenchmark.rectangleWeight q t.val b := by
  rw [rectangle_as_sum]
  simp_rw [rectangle_as_sum, Finset.mul_sum]
  rw [← Fintype.sum_sigma (fun p : Σ t : Fin (a+1), Rect t.val b =>
    q^p.1.val * q^(∑ i, (p.2.val i).val))]
  apply Fintype.sum_equiv (headEquiv a b)
  intro l
  rw [Fin.sum_univ_succ, pow_add]
  rfl

/-- Formal geometric series; no numerical convergence or invertibility assumptions. -/
def geometric {R : Type*} [CommSemiring R] (c : R) : PowerSeries R :=
  PowerSeries.mk (fun n => c^n)

def rectangleSeries {K : Type*} [Field K] (q : K) (b : ℕ) : PowerSeries K :=
  PowerSeries.mk (fun a => FiniteQBenchmark.rectangleWeight q a b)

theorem rescale_geometric {R : Type*} [CommSemiring R] (q c : R) :
    PowerSeries.rescale q (geometric c) = geometric (q*c) := by
  ext n
  simp [geometric, mul_pow]

theorem geometric_denominator {R : Type*} [CommRing R] (c : R) :
    geometric c * (1 - PowerSeries.C c * PowerSeries.X) = 1 := by
  ext n
  cases n with
  | zero => simp [geometric]
  | succ n =>
    simp [mul_sub, ← mul_assoc, PowerSeries.coeff_succ_mul_X, geometric, pow_succ]

theorem rectangle_zero {K : Type*} [Field K] (q : K) (a : ℕ) :
    FiniteQBenchmark.rectangleWeight q a 0 = 1 := by
  simp [FiniteQBenchmark.rectangleWeight, FiniteQBenchmark.rectangle, Antitone]

theorem rectangle_series_step {K : Type*} [Field K] (q : K) (b : ℕ) :
    rectangleSeries q (b+1) = PowerSeries.rescale q (rectangleSeries q b) * geometric 1 := by
  ext a
  simp only [rectangleSeries, PowerSeries.coeff_mk, PowerSeries.coeff_mul,
    PowerSeries.coeff_rescale, geometric, PowerSeries.coeff_mk, one_pow, mul_one]
  rw [Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]
  rw [rectangle_head_elimination]
  exact Fin.sum_univ_eq_sum_range (fun t => q^t * FiniteQBenchmark.rectangleWeight q t b) (a+1)

def coneProduct {R : Type*} [CommSemiring R] (q : R) (b : ℕ) : PowerSeries R :=
  ∏ i ∈ Finset.range (b+1), geometric (q^i)

theorem cone_product_step {R : Type*} [CommSemiring R] (q : R) (b : ℕ) :
    coneProduct q (b+1) = PowerSeries.rescale q (coneProduct q b) * geometric 1 := by
  unfold coneProduct
  rw [Finset.prod_range_succ']
  simp only [pow_zero, map_prod, rescale_geometric]
  congr 1
  apply Finset.prod_congr rfl
  intro i hi
  rw [pow_succ']

theorem rectangle_series_factorization {K : Type*} [Field K] (q : K) (b : ℕ) :
    rectangleSeries q b = coneProduct q b := by
  induction b with
  | zero =>
    ext a
    simp [rectangleSeries, rectangle_zero, coneProduct, geometric]
  | succ b ih => rw [rectangle_series_step, cone_product_step, ih]

/-- Rational generating-function certificate with constant denominator 1. -/
theorem cone_denominator {R : Type*} [CommRing R] (q : R) (b : ℕ) :
    coneProduct q b * (∏ i ∈ Finset.range (b+1),
      (1 - PowerSeries.C (q^i) * PowerSeries.X)) = 1 := by
  unfold coneProduct
  rw [← Finset.prod_mul_distrib]
  simp only [geometric_denominator, Finset.prod_const_one]

open FiniteQBenchmark

theorem gaussian_geometric_coefficient {K : Type*} [Field K] (q : K) (a b : ℕ) :
    (∑ t ∈ Finset.range (a+1), q^t * gaussian q (t+b) b) =
      gaussian q (a+b+1) (b+1) := by
  induction a with
  | zero => simp [gaussian_self]
  | succ a ih =>
    rw [Finset.sum_range_succ, ih]
    have h := FiniteQP1.gaussian_pascal q (a+1+b) b (by omega)
    have hs : a+1+b-b = a+1 := by omega
    rw [hs] at h
    simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using h.symm

def gaussianSeries {K : Type*} [Field K] (q : K) (b : ℕ) : PowerSeries K :=
  PowerSeries.mk (fun a => gaussian q (a+b) b)

theorem gaussian_series_step {K : Type*} [Field K] (q : K) (b : ℕ) :
    gaussianSeries q (b+1) = PowerSeries.rescale q (gaussianSeries q b) * geometric 1 := by
  ext a
  simp only [gaussianSeries, PowerSeries.coeff_mk, PowerSeries.coeff_mul,
    PowerSeries.coeff_rescale, geometric, PowerSeries.coeff_mk, one_pow, mul_one]
  rw [Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]
  exact (gaussian_geometric_coefficient q a b).symm

theorem gaussian_series_factorization {K : Type*} [Field K] (q : K) (b : ℕ) :
    gaussianSeries q b = coneProduct q b := by
  induction b with
  | zero =>
    ext a
    simp [gaussianSeries, gaussian_zero_right, coneProduct, geometric]
  | succ b ih => rw [gaussian_series_step, cone_product_step, ih]

/-- Complete Omega evaluation through the factorized chain generating function. -/
theorem omega_rectangle_evaluation {K : Type*} [Field K] (q : K) (a b : ℕ) :
    omegaAll (rectangleEncoding q a b) = gaussian q (a+b) b := by
  rw [rectangle_omega]
  have h := (rectangle_series_factorization q b).trans
    (gaussian_series_factorization q b).symm
  simpa only [rectangleSeries, gaussianSeries, PowerSeries.coeff_mk] using congrArg (PowerSeries.coeff a) h
end FiniteQMacMahon

macro "macmahon_chain" : tactic => `(tactic| (
  classical
  first
  | with_reducible exact FiniteQMacMahon.rectangle_series_factorization _ _
  | with_reducible exact FiniteQMacMahon.gaussian_series_factorization _ _
  | with_reducible exact FiniteQMacMahon.cone_denominator _ _
  | with_reducible exact FiniteQMacMahon.geometric_denominator _
  | with_reducible exact FiniteQMacMahon.rectangle_head_elimination _ _ _
  | with_reducible exact FiniteQMacMahon.omega_rectangle_evaluation _ _ _
  | (simp only [← FiniteQMacMahon.rectangle_omega, FiniteQMacMahon.omega_rectangle_evaluation] <;>
     first | rfl | (congr 1 <;> omega))))
