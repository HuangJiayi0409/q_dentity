import Benchmark.StructuralAtoms
import Mathlib.Tactic.Ring
import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.Vandermonde

open scoped BigOperators
namespace FiniteQDeterminant
/-- An exact LU certificate; no pivots or nonsingular-minor assumptions are added. -/
theorem factorization {K I : Type*} [CommRing K] [Fintype I] [DecidableEq I] [LinearOrder I]
    (A L U : Matrix I I K) (hA : A = L * U)
    (hL : L.IsLowerTriangular) (hU : U.IsUpperTriangular) :
    A.det = (∏ i, L i i) * (∏ i, U i i) := by
  rw [hA, Matrix.det_mul, Matrix.det_of_isLowerTriangular L hL, Matrix.det_of_isUpperTriangular hU]
end FiniteQDeterminant

/-- Evaluation templates only; no assumption-provided LU certificate fallback. -/
macro "determinant_evaluate" : tactic => `(tactic| (
  classical
  simp only [Matrix.det_mul, Matrix.det_transpose, Matrix.det_diagonal,
    Matrix.det_vandermonde, Matrix.det_one, Matrix.det_fin_two,
    Matrix.of_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
    Finset.prod_mul_distrib, mul_one, one_mul] <;> (try simp) <;> ring))

macro "determinant_structure" : tactic => `(tactic| (
  classical
  first
  | (apply FiniteQDeterminant.factorization <;> assumption)
  | (apply Matrix.det_of_isUpperTriangular; assumption)
  | (apply Matrix.det_of_isLowerTriangular; assumption)
  | (simp only [Matrix.det_mul, Matrix.det_transpose, Matrix.det_diagonal,
       Matrix.det_vandermonde, Matrix.det_one, Matrix.det_fin_two,
       Matrix.of_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
       Finset.prod_mul_distrib, mul_one, one_mul] <;> (try simp) <;> ring)))
