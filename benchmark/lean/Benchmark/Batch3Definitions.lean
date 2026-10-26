import Benchmark.Batch2Proofs
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

namespace FiniteQBenchmark
open scoped BigOperators
noncomputable section
variable {K : Type*} [Field K]

/-- Fixed logarithm of the base; negative integer lower indices have value zero. -/
def generalizedGaussian (L alpha : ℂ) (k : ℤ) : ℂ :=
  if k < 0 then 0 else
  poch (Complex.exp (L*(alpha-k+1))) (Complex.exp L) k.toNat /
    poch (Complex.exp L) (Complex.exp L) k.toNat

/-- Weak compositions, with a finite coordinate bound forced by the total. -/
def compositions (d N : ℕ) : Finset (Fin d → Fin (N+1)) := by
  classical
  exact Finset.univ.filter (fun k => (∑ i, (k i).val) = N)

def subCompositions (d N : ℕ) : Finset (Fin d → Fin (N+1)) := by
  classical
  exact Finset.univ.filter (fun k => (∑ i, (k i).val) ≤ N)

def vandermonde {d : ℕ} (z : Fin d → K) : K :=
  ∏ r, ∏ s ∈ Finset.univ.filter (r < ·), (z r-z s)

/-- Words have their exact prescribed length and multiplicities. -/
def multisetWords {r : ℕ} (m : Fin r → ℕ) : Finset (Fin (∑ i, m i) → Fin r) := by
  classical
  exact Finset.univ.filter (fun w => ∀ i, (Finset.univ.filter (w · = i)).card = m i)

def wordInversions {l r : ℕ} (w : Fin l → Fin r) : ℕ :=
  ∑ i, (Finset.univ.filter (fun j => i < j ∧ w j < w i)).card

/-- AP's index is the sum of one-based descent positions. -/
def wordIndex {l r : ℕ} (w : Fin l → Fin r) : ℕ :=
  ∑ i, ∑ j ∈ Finset.univ.filter (fun j => j.val = i.val+1 ∧ w j < w i), i.val+1

def wordStatisticCount {r : ℕ} (m : Fin r → ℕ)
    (stat : (Fin (∑ i, m i) → Fin r) → ℕ) (s : ℕ) : ℕ :=
  ((multisetWords m).filter (fun w => stat w = s)).card

def pairMultiplicity {r : ℕ} (m : Fin r → ℕ) : ℕ :=
  ∑ i, ∑ j ∈ Finset.univ.filter (i < ·), m i*m j

def schurDInt (q : K) (n : ℤ) : K :=
  if n = -1 then 1 else if n < 0 then 0 else schurD q (n.toNat+1)

/-- AP 7.E11: strict gap is selected by the smaller adjacent part. -/
def apGollnitzAllowed (s : Finset ℕ) : Prop :=
  (∀ j ∈ s, j ≠ 0 ∧ j ≠ 1 ∧ j ≠ 3) ∧
  ∀ pair ∈ (s.sort (· ≥ ·)).zip (s.sort (· ≥ ·)).tail,
    pair.2 + 6 ≤ pair.1 ∧
    (pair.2 % 6 = 0 ∨ pair.2 % 6 = 1 ∨ pair.2 % 6 = 3 → pair.2 + 6 < pair.1)

def apGollnitz (q : K) (N : ℕ) : K := by
  classical
  exact ∑ s ∈ ((Finset.range (N+1)).powerset).filter apGollnitzAllowed, q^(∑ j ∈ s, j)

/-- Coefficient recurrence from the defining generating function:
F(x)=(1+xq²)(1+xq⁴)(1+xq⁵)/(1-x) F(q⁶x).
Clearing (q⁶;q⁶)_n gives this polynomial recurrence, including roots of unity. -/
def apLambda (q : K) : ℕ → K
  | 0 => 1
  | n+1 => (1+(q^2+q^4+q^5)*q^(6*n))*apLambda q n +
      (if n = 0 then 0 else (q^6+q^7+q^9)*q^(6*(n-1))*(1-q^(6*n))*apLambda q (n-1)) +
      (if n ≤ 1 then 0 else q^11*q^(6*(n-2))*(1-q^(6*n))*(1-q^(6*(n-1)))*apLambda q (n-2))

/-- Transpose of AP's k rows and r columns: r rows, k columns, zero padding; the first row is fixed to n.
Each column is bounded by its first entry, so the finite enumeration is exact. -/
def planeRows {k : ℕ} (r : ℕ) (n : Fin k → ℕ) :
    Finset (Fin r → (j : Fin k) → Fin (n j+1)) := by
  classical
  exact Finset.univ.filter (fun a =>
    (∀ i, Antitone (fun j => (a i j).val)) ∧
    (∀ j, Antitone (fun i => (a i j).val)) ∧
    (∀ i, i.val = 0 → ∀ j, (a i j).val = n j))

def planePi {k : ℕ} (q : K) (r : ℕ) (n : Fin k → ℕ) : K :=
  ∑ a ∈ planeRows r n, q^(∑ i, ∑ j, (a i j).val)

def planeBox (k r n : ℕ) : Finset (Fin r → Fin k → Fin (n+1)) := by
  classical
  exact Finset.univ.filter (fun a =>
    (∀ i, Antitone (a i)) ∧ (∀ j, Antitone (fun i => a i j)))

def planeBoxPi (q : K) (k r n : ℕ) : K :=
  ∑ a ∈ planeBox k r n, q^(∑ i, ∑ j, (a i j).val)

/-- AP's finite geometric sum, also defined when the ratio is 1. -/
def geometric (z : K) (s : ℕ) : K := ∑ h ∈ Finset.range s, z^h

def sieveF (q : K) (T D R E : ℤ) : K :=
  q^E * geometric (q^D) (R+1).toNat * gaussianInt q T (D-1) +
  ∑ j ∈ Finset.range (R-1).toNat,
    q^(E+D+j+1) * geometric (q^D) (R-j-1).toNat * gaussianInt q (T+j) (D-2)

def sieveSmallF (q : K) (A r X Y L : ℤ) : K :=
  sieveF q (2*A+X) (A+Y+1) r L

end
end FiniteQBenchmark
