import Benchmark.Definitions

namespace FiniteQBenchmark
open scoped BigOperators
variable {K : Type*}

@[simp] theorem poch_zero [CommRing K] (a q : K) : poch a q 0 = 1 := by
  simp [poch]

@[simp] theorem poch_succ [CommRing K] (a q : K) (n : ℕ) :
    poch a q (n+1) = poch a q n * (1-a*q^n) := by
  simp [poch, Finset.prod_range_succ]

@[simp] theorem pochList_nil [CommRing K] (q : K) (n : ℕ) :
    pochList [] q n = 1 := by
  simp [pochList]

@[simp] theorem pochList_cons [CommRing K] (a : K) (as : List K) (q : K) (n : ℕ) :
    pochList (a :: as) q n = poch a q n * pochList as q n := by
  simp [pochList]

@[simp] theorem pochList_zero [CommRing K] (as : List K) (q : K) :
    pochList as q 0 = 1 := by
  induction as with
  | nil => simp
  | cons a as ih => simp [ih]

@[simp] theorem phiTerm_zero [Field K] (as bs : List K) (q z : K) :
    phiTerm as bs q z 0 = 1 := by
  simp [phiTerm]

@[simp] theorem phi_zero [Field K] (as bs : List K) (q z : K) :
    phi as bs q z 0 = 1 := by
  simp [phi]

@[simp] theorem wellPoised_zero [Field K] (a : K) (bs : List K) (q z : K) :
    wellPoised a bs q z 0 = 1 := by
  simp [wellPoised, wellPoisedNumerator]

@[simp] theorem baileySum_zero [Field K] (a q : K) (alpha : ℕ → K) :
    baileySum a q alpha 0 = alpha 0 := by
  simp [baileySum]

@[simp] theorem unitBailey_zero [Field K] (a q : K) : unitBailey a q 0 = 1 := by
  simp [unitBailey]

end FiniteQBenchmark

#print axioms FiniteQBenchmark.poch_succ
#print axioms FiniteQBenchmark.phi_zero
#print axioms FiniteQBenchmark.wellPoised_zero
#print axioms FiniteQBenchmark.baileySum_zero
