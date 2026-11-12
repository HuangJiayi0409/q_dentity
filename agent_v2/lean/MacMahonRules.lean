import Benchmark.BatchDefinitions
import Mathlib.Algebra.BigOperators.NatAntidiagonal
import Mathlib.RingTheory.PowerSeries.Basic
import Mathlib.Tactic.Ring

/-! Controlled formal-series realization of a two-factor Omega result.
All coefficients are finite sums. The temporary regulator is specialized only
after the coefficient fiber is bounded by the original natural degree. -/
open scoped BigOperators
namespace AgentV2MacMahon

/-- Formal geometric expansion; no analytic convergence is involved. -/
def geometric (c : ℂ) : PowerSeries ℂ := PowerSeries.mk (fun n => c ^ n)

theorem geometric_denominator (c : ℂ) :
    geometric c * (1 - PowerSeries.C c * PowerSeries.X) = 1 := by
  ext n
  cases n with
  | zero => simp [geometric]
  | succ n =>
    simp [mul_sub, ← mul_assoc, PowerSeries.coeff_succ_mul_X, geometric, pow_succ]

theorem two_factor_constant (z rho : ℂ) :
    PowerSeries.constantCoeff
      ((1 - PowerSeries.C z * PowerSeries.X) *
       (1 - PowerSeries.C (rho * z⁻¹) * PowerSeries.X)) = 1 := by
  simp

/-- The two constructed rational factors are units of the formal series ring. -/
theorem two_factor_denominator (z rho : ℂ) :
    (geometric z * geometric (rho * z⁻¹)) *
      ((1 - PowerSeries.C z * PowerSeries.X) *
       (1 - PowerSeries.C (rho * z⁻¹) * PowerSeries.X)) = 1 := by
  calc
    _ = (geometric z * (1 - PowerSeries.C z * PowerSeries.X)) *
        (geometric (rho * z⁻¹) * (1 - PowerSeries.C (rho * z⁻¹) * PowerSeries.X)) := by ring
    _ = 1 := by rw [geometric_denominator, geometric_denominator, one_mul]

/-- Omega's nonnegative auxiliary exponent is the exact finite source fiber. -/
theorem finite_fiber (n k : ℕ) : 0 ≤ (n : ℤ) - k ↔ k ∈ Finset.range (n+1) := by
  simp only [Finset.mem_range]
  omega

theorem source_power (z : ℂ) (n k : ℕ) (hz : z ≠ 0) (hk : k ≤ n) :
    (z⁻¹)^k * z^(n-k) = z^((n:ℤ)-2*k) := by
  calc
    _ = z^(-(k:ℤ)) * z^((n-k:ℕ):ℤ) := by simp [zpow_neg, zpow_natCast, inv_pow]
    _ = z^(-(k:ℤ) + ((n-k:ℕ):ℤ)) := (zpow_add₀ hz _ _).symm
    _ = z^((n:ℤ)-2*k) := by congr 1; omega

/-- Cauchy convolution in each finite fiber retains the regulator until now. -/
theorem regulated_coeff (z rho : ℂ) (n : ℕ) (hz : z ≠ 0) :
    PowerSeries.coeff n (geometric z * geometric (rho * z⁻¹)) =
      ∑ k ∈ Finset.range (n+1), rho^k * z^((n:ℤ)-2*k) := by
  rw [mul_comm (geometric z) (geometric (rho * z⁻¹)), PowerSeries.coeff_mul,
    Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]
  simp only [geometric, PowerSeries.coeff_mk]
  apply Finset.sum_congr rfl
  intro k hk
  have hle : k ≤ n := Nat.le_of_lt_succ (Finset.mem_range.mp hk)
  rw [mul_pow, mul_assoc, source_power z n k hz hle]

/-- Removing the regulator is substitution into a finite polynomial fiber. -/
theorem source_coeff (z : ℂ) (n : ℕ) (hz : z ≠ 0) :
    PowerSeries.coeff n (geometric z * geometric z⁻¹) =
      ∑ k ∈ Finset.range (n+1), z^((n:ℤ)-2*k) := by
  simpa using regulated_coeff z 1 n hz

/-- Formal rational semantics and the source coefficient share one candidate. -/
theorem source_realization (z : ℂ) (n : ℕ) (hz : z ≠ 0) :
    ((geometric z * geometric z⁻¹) *
      ((1 - PowerSeries.C z * PowerSeries.X) *
       (1 - PowerSeries.C z⁻¹ * PowerSeries.X)) = 1) ∧
    (PowerSeries.coeff n (geometric z * geometric z⁻¹) =
      ∑ k ∈ Finset.range (n+1), z^((n:ℤ)-2*k)) := by
  constructor
  · simpa using two_factor_denominator z 1
  · exact source_coeff z n hz

end AgentV2MacMahon
