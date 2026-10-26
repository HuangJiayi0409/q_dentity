import Benchmark.Batch4Proofs
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.RingTheory.Polynomial.Vieta
import Mathlib.Analysis.Calculus.Deriv.Polynomial

namespace FiniteQBenchmark
open scoped BigOperators
noncomputable section
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

/-- Borwein's defining product before separating the three residue classes. -/
def borweinBase (K : Type*) [Field K] (n : ℕ) : Polynomial K :=
  ∏ i ∈ Finset.range n,
    (1-Polynomial.X^(3*i+1))*(1-Polynomial.X^(3*i+2))

def residueEval (f : Polynomial K) (q : K) (r : ℕ) : K :=
  ∑ i ∈ f.support, if i%3=r then f.coeff i*q^(i/3) else 0

def borweinA (q : K) (n : ℕ) : K := residueEval (borweinBase K n) q 0
def borweinB (q : K) (n : ℕ) : K := -residueEval (borweinBase K n) q 1
def borweinC (q : K) (n : ℕ) : K := -residueEval (borweinBase K n) q 2

/-- Sills p.142: independent sets of {3,...,i-2}. -/
def motivatedA (q : K) (i : ℕ) : K :=
  ∑ s ∈ ((Finset.Icc 3 (i-2)).powerset).filter (fun s => ∀ j ∈ s, j+1 ∉ s),
    q^(∑ j ∈ s, j)
def motivatedB (q : K) (i : ℕ) : K := if i ≤ 3 then 0 else q^(i-1)*motivatedA q (i-1)

/-- Corrected Capparelli alpha: all three nonzero residue classes are explicit. -/
def capparelliAlpha (q : K) (n : ℕ) : K :=
  if n=0 then 1 else if n%3=1 then
    let r := n/3; -q^((9*r*r+9*r+2)/2)
  else if n%3=2 then
    let r := (n+1)/3; -q^((9*r*r-9*r+2)/2)
  else let r := n/3; q^(3*r*(3*r-1)/2)*(1+q^(3*r))

/-- Finite q power, first for nonnegative lengths. -/
def kacPowerNat (x a q : K) (n : ℕ) : K :=
  ∏ i ∈ Finset.range n, (x-q^i*a)
/-- Kac--Cheung (3.7): the negative branch is a shifted reciprocal. -/
def kacPower (x a q : K) (n : ℤ) : K :=
  if 0 ≤ n then kacPowerNat x a q n.toNat
  else (kacPowerNat x (q^n*a) q (-n).toNat)⁻¹

def kacPowerDefined (x a q : K) (n : ℤ) : Prop :=
  n < 0 → kacPowerNat x (q^n*a) q (-n).toNat ≠ 0

def qInteger (q : K) (n : ℤ) : K := (q^n-1)/(q-1)
def qFactorial (q : K) (n : ℕ) : K := ∏ j ∈ Finset.Icc 1 n, geometric q j

def kacX (f : Polynomial K) : Polynomial K := Polynomial.X*f
def kacM (q : K) (f : Polynomial K) : Polynomial K := f.comp (Polynomial.C q*Polynomial.X)

/-- Ordered independent vectors, not a quotient by change of basis. -/
def independentTuples (F : Type*) [Field F] [Fintype F] (n j : ℕ) : Finset (Fin j → Fin n → F) :=
  Finset.univ.filter (fun v => LinearIndependent F v)

def rankMatrices (F : Type*) [Field F] [Fintype F] (m n j : ℕ) : Finset (Matrix (Fin m) (Fin n) F) :=
  Finset.univ.filter (fun A => A.rank=j)

def galoisNumber (q : K) (n : ℕ) : K := ∑ j ∈ Finset.range (n+1), gaussian q n j

/-- Symmetric derivative, with polynomial/differentiable extension at zero. -/
def symJackson (q : ℂ) (f : ℂ → ℂ) (x : ℂ) : ℂ :=
  if x=0 then deriv f 0 else (f (q*x)-f (q⁻¹*x))/((q-q⁻¹)*x)

def symNumber (q : K) (n : ℕ) : K := (q^n-q^(-(n:ℤ)))/(q-q⁻¹)
def symFactorial (q : K) (n : ℕ) : K := ∏ j ∈ Finset.Icc 1 n, symNumber q j
def symGaussian (q : K) (n j : ℕ) : K := symFactorial q n/(symFactorial q j*symFactorial q (n-j))
def symPower (x a q : K) (n : ℕ) : K :=
  ∏ j ∈ Finset.range n, (x-q^((n:ℤ)-1-2*j)*a)

def pairNumber (q r : ℂ) (n : ℕ) : ℂ :=
  if q=r then (n:ℂ)*q^(n-1) else (q^n-r^n)/(q-r)

/-- Taylor family is constrained by the actual polynomial difference equation.
No nested-root assumption or root-sum recurrence is built into this predicate. -/
def quantumTaylorFamily (q r h h' a : ℂ) (T : ℕ → Polynomial ℂ) (N : ℕ) : Prop :=
  T 0=1 ∧ ∀ k ∈ Finset.Icc 1 N,
    (T k).natDegree=k ∧ (T k).eval a=0 ∧
    (T k).comp (Polynomial.C q*Polynomial.X+Polynomial.C h) -
      (T k).comp (Polynomial.C r*Polynomial.X+Polynomial.C h') =
    (Polynomial.C (q-r)*Polynomial.X+Polynomial.C (h-h'))*T (k-1)

/-- Actual sum of complex roots, counted with multiplicity. -/
def quantumRootSum (T : ℕ → Polynomial ℂ) (n : ℕ) : ℂ := ((T n).roots).sum

/-- Corrected finite triangular Taylor construction; not the book's erroneous nested product. -/
def symTaylor (q a : K) (n : ℕ) : Polynomial K :=
  if hn : n=0 then 1 else
    Polynomial.C (1/symFactorial q n)*Polynomial.X^n -
      ∑ k : Fin n, Polynomial.C (a^(n-k.val)/symFactorial q (n-k.val))*symTaylor q a k.val
termination_by n
decreasing_by exact k.isLt

end
end FiniteQBenchmark
