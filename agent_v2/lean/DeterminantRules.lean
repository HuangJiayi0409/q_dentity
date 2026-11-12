import Benchmark.Definitions
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-! Division-free determinant of an arbitrary two-row/two-column submatrix.
The ambient dimension and selectors remain arbitrary; selectors may repeat.
This supplies a local minor rule, not the determinant of the whole source matrix. -/
namespace AgentV2Determinant

universe u
variable {K : Type u} [CommRing K] {k : ℕ}

def minorTwo (A : Matrix (Fin k) (Fin k) K) (i0 i1 j0 j1 : Fin k) :
    Matrix (Fin 2) (Fin 2) K :=
  A.submatrix ![i0, i1] ![j0, j1]

/-- Mathlib's genuine determinant expansion, applied to the selected submatrix.
No pivot, distinctness, characteristic or nonzero assumption is required. -/
theorem minor_det (A : Matrix (Fin k) (Fin k) K) (i0 i1 j0 j1 : Fin k) :
    Matrix.det (minorTwo A i0 i1 j0 j1) =
      A i0 j0 * A i1 j1 - A i0 j1 * A i1 j0 := by
  exact Matrix.det_fin_two (minorTwo A i0 i1 j0 j1)

end AgentV2Determinant
