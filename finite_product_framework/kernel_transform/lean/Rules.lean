import Benchmark.Definitions
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.SimpRw
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.LinearAlgebra.Matrix.Notation

open scoped BigOperators
namespace FiniteQKernel
/-- Transposition on the entire triangular support, including N=0. -/
theorem transpose_triangle {R : Type*} [AddCommMonoid R] (N : ℕ) (f : ℕ → ℕ → R) :
    (∑ n ∈ Finset.range (N+1), ∑ r ∈ Finset.Icc n N, f n r) =
    ∑ r ∈ Finset.range (N+1), ∑ n ∈ Finset.range (r+1), f n r := by
  apply Finset.sum_comm'
  intro n r
  simp only [Finset.mem_range, Finset.mem_Icc]
  omega

/-- A finite inverse-kernel certificate acts on every input vector. -/
theorem inverse_action {R I : Type*} [CommRing R] [Fintype I] [DecidableEq I]
    (A B : I → I → R) (v : I → R)
    (h : ∀ i j, ∑ k, A i k * B k j = if i = j then 1 else 0) :
    (fun i => ∑ k, A i k * ∑ j, B k j * v j) = v := by
  funext i
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  simp_rw [← mul_assoc, ← Finset.sum_mul, h]
  simp

/-- Composition is verified at every matrix entry before acting on a sequence. -/
theorem compose_action {R I J L : Type*} [CommRing R] [Fintype I] [Fintype J]
    (A : L → I → R) (B : I → J → R) (C : L → J → R) (v : J → R)
    (h : ∀ i j, ∑ k, A i k * B k j = C i j) :
    (fun i => ∑ k, A i k * ∑ j, B k j * v j) = (fun i => ∑ j, C i j * v j) := by
  funext i
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  simp_rw [← mul_assoc, ← Finset.sum_mul, h]
end FiniteQKernel

macro "kernel_transpose" : tactic => `(tactic| (
  classical
  simp only [Finset.mul_sum, Finset.sum_mul]
  rw [FiniteQKernel.transpose_triangle]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  ring))

macro "kernel_inverse" : tactic => `(tactic| (
  classical
  first
  | apply FiniteQKernel.inverse_action; first | assumption | intro i j; fin_cases i <;> fin_cases j <;> simp [Fin.sum_univ_succ] <;> ring
  | apply FiniteQKernel.compose_action; first | assumption | intro i j; fin_cases i <;> fin_cases j <;> simp [Fin.sum_univ_succ] <;> ring))
