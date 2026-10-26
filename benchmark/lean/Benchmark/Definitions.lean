import Mathlib.Algebra.BigOperators.Field
import Mathlib.Basic.Complex.Basic
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Finset.Pi
import Mathlib.Data.Int.Interval

/-! Explicit finite definitions. No theorem is used as a definition of its own conclusion. -/
namespace FiniteQBenchmark
open scoped BigOperators
noncomputable section

/-- Finite q-Pochhammer, including the empty product. -/
def poch {K : Type*} [CommRing K] (a q : K) (n : ℕ) : K :=
  ∏ j ∈ Finset.range n, (1 - a * q ^ j)

def pochList {K : Type*} [CommRing K] (as : List K) (q : K) (n : ℕ) : K :=
  (as.map (fun a => poch a q n)).prod

/-- Negative lengths are reciprocals, not zero. -/
def pochInt {K : Type*} [Field K] (a q : K) (n : ℤ) : K :=
  if 0 ≤ n then poch a q n.toNat else (poch (a * q ^ n) q (-n).toNat)⁻¹

/-- Polynomial Gaussian, defined recursively. `Gaussian.lean` proves agreement
with the finite-product quotient wherever that quotient is defined. -/
def gaussian {K : Type*} [CommRing K] (q : K) : ℕ → ℕ → K
  | _, 0 => 1
  | 0, _+1 => 0
  | n+1, k+1 => gaussian q n k + q^(k+1) * gaussian q n (k+1)

/-- Ordinary Gaussian, with zero outside its nonnegative support. -/
def gaussianInt {K : Type*} [CommRing K] (q : K) (n k : ℤ) : K :=
  if 0 ≤ n ∧ 0 ≤ k ∧ k ≤ n then gaussian q n.toNat k.toNat else 0

/-- The quotient presentation is only identified with the polynomial on its domain. -/
def gaussianQuotient {K : Type*} [Field K] (q : K) (n k : ℕ) : K :=
  if k ≤ n then poch q q n / (poch q q k * poch q q (n-k)) else 0

def rogersSzego {K : Type*} [CommRing K] (t q : K) (n : ℕ) : K :=
  ∑ k ∈ Finset.range (n+1), gaussian q n k * t ^ k

/-- Denominator nonvanishing is restricted to the actually evaluated finite terms. -/
def phiDefined {K : Type*} [Field K] (bs : List K) (q : K) (n : ℕ) : Prop :=
  ∀ k ≤ n, pochList (q :: bs) q k ≠ 0

def phiTerm {K : Type*} [Field K] (as bs : List K) (q z : K) (k : ℕ) : K :=
  pochList as q k / pochList (q :: bs) q k *
    ((-1 : K)^k * q^(k*(k-1)/2)) ^ ((1 : ℤ) + bs.length - as.length) * z^k

def phi {K : Type*} [Field K] (as bs : List K) (q z : K) (n : ℕ) : K :=
  ∑ k ∈ Finset.range (n+1), phiTerm as bs q z k

/-- Cancel (1-a) against the initial factor of (a;q)_k for k>0.
This also gives the explicitly permitted removable extension at a=1. -/
def wellPoisedNumerator {K : Type*} [CommRing K] (a q : K) (k : ℕ) : K :=
  if k = 0 then 1 else (1 - a*q^(2*k)) * poch (a*q) q (k-1)

def wellPoised {K : Type*} [Field K] (a : K) (bs : List K) (q z : K) (n : ℕ) : K :=
  ∑ k ∈ Finset.range (n+1), wellPoisedNumerator a q k * pochList bs q k /
    pochList (q :: bs.map (fun b => a*q/b)) q k * z^k

def baileySum {K : Type*} [Field K] (a q : K) (alpha : ℕ → K) (n : ℕ) : K :=
  ∑ r ∈ Finset.range (n+1), alpha r / (poch q q (n-r) * poch (a*q) q (n+r))

def baileyDefined {K : Type*} [Field K] (a q : K) (n : ℕ) : Prop :=
  ∀ j ≤ n, ∀ r ≤ j, poch q q (j-r) * poch (a*q) q (j+r) ≠ 0

def unitBailey {K : Type*} [Field K] (a q : K) (r : ℕ) : K :=
  if r = 0 then 1 else (-1)^r * q^(r*(r-1)/2) * (1-a*q^(2*r)) *
    poch (a*q) q (r-1) / poch q q r

end
end FiniteQBenchmark
