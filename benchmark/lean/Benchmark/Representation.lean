import Benchmark.InitialValues

namespace FiniteQBenchmark
open scoped BigOperators

/-- The recursive Gaussian is a polynomial construction, compatible with coefficient maps. -/
theorem map_gaussian {R S : Type*} [CommRing R] [CommRing S]
    (f : R →+* S) (q : R) (n k : ℕ) :
    f (gaussian q n k) = gaussian (f q) n k := by
  induction n generalizing k with
  | zero => cases k <;> simp [gaussian]
  | succ n ih => cases k <;> simp [gaussian, ih]

theorem gaussian_polynomial_eval {R : Type*} [CommRing R] (q : R) (n k : ℕ) :
    Polynomial.eval q (gaussian (Polynomial.X : Polynomial R) n k) = gaussian q n k := by
  simpa using map_gaussian (Polynomial.evalRingHom q) Polynomial.X n k

/-- The finite enumeration for Cayley's identity loses no admissible multiplicity vector. -/
theorem cayley_multiplicity_bound (n : ℕ) (p : Fin n → ℕ)
    (hsum : (∑ j, (j.val+1)*p j) = n) (i : Fin n) : p i ≤ n := by
  have ht : (i.val+1)*p i ≤ ∑ j : Fin n, (j.val+1)*p j :=
    Finset.single_le_sum (f := fun j : Fin n => (j.val+1)*p j) (fun j _ => Nat.zero_le _) (Finset.mem_univ i)
  rw [hsum] at ht
  have hi : 1 ≤ i.val+1 := by omega
  nlinarith

/-- The objects counted in the finite-field statement really form a finite type. -/
theorem finite_subspace_family (F : Type*) [Field F] [Fintype F] (n k : ℕ) :
    Finite {U : Submodule F (Fin n → F) // Module.finrank F U = k} := by
  haveI : Finite (Submodule F (Fin n → F)) :=
    Finite.of_injective (fun U : Submodule F (Fin n → F) => (U : Set (Fin n → F)))
      (fun U V h => SetLike.coe_injective h)
  infer_instance

/-- Normalization of the terminating lower parameter in W. -/
theorem terminating_lower_parameter {K : Type*} [Field K] (a q : K) (n : ℕ) :
    a*q/(q^(-(n : ℤ))) = a*q^(n+1) := by
  simp [zpow_neg, div_eq_mul_inv, pow_succ, mul_assoc, mul_comm, mul_left_comm]

end FiniteQBenchmark
#print axioms FiniteQBenchmark.gaussian_polynomial_eval
#print axioms FiniteQBenchmark.cayley_multiplicity_bound
#print axioms FiniteQBenchmark.finite_subspace_family
#print axioms FiniteQBenchmark.terminating_lower_parameter
