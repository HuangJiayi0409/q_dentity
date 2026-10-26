import Benchmark.Batch2Definitions

namespace FiniteQBenchmark
open scoped BigOperators
variable {K : Type*} [Field K]
@[simp] theorem rising_zero (a : K) : rising a 0 = 1 := by simp [rising]
theorem rising_succ (a : K) (n : ℕ) : rising a (n+1) = rising a n*(a+n) := by
  simp [rising, Finset.prod_range_succ]
@[simp] theorem recurrencePair_zero (A B C : ℕ → K) : recurrencePair A B C 0 = (0,1) := rfl
theorem recurrencePair_prev (A B C : ℕ → K) (n : ℕ) :
  (recurrencePair A B C (n+1)).1 = (recurrencePair A B C n).2 := rfl
theorem recurrencePair_equation (A B C : ℕ → K) (n : ℕ) (h : A n ≠ 0) :
  A n*(recurrencePair A B C (n+1)).2 + C n*(recurrencePair A B C n).1 =
    B n*(recurrencePair A B C n).2 := by
  simp only [recurrencePair]
  field_simp
  <;> ring
@[simp] theorem associatedAW_zero (z a b c d rho q : K) : associatedAW z a b c d rho q 0 = 1 := rfl
@[simp] theorem associatedUltra_zero (z alpha beta q : K) : associatedUltra z alpha beta q 0 = 1 := rfl
end FiniteQBenchmark
