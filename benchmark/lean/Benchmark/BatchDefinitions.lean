import Benchmark.Gaussian
import Mathlib.Algebra.MonoidAlgebra.Basic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.RingTheory.RootsOfUnity.Complex
import Mathlib.RingTheory.PowerSeries.Basic

namespace FiniteQBenchmark
open scoped BigOperators
noncomputable section
variable {K : Type*} [Field K]

/-- Original GR safe base domain; no convergence condition is imposed on finite sums. -/
def regular (q : K) : Prop := q ≠ 0 ∧ ∀ n : ℕ, 0 < n → q^n ≠ 1

def wellPoisedRaw (a : K) (bs : List K) (q z : K) (n : ℕ) : K :=
  ∑ k ∈ Finset.range (n+1), (1-a*q^(2*k))/(1-a) *
    pochList (a :: bs) q k / pochList (q :: bs.map (fun b => a*q/b)) q k * z^k

def wDefined (a : K) (bs : List K) (q : K) (n : ℕ) : Prop :=
  a ≠ 1 ∧ (∀ b ∈ bs, b ≠ 0) ∧ phiDefined (bs.map (fun b => a*q/b)) q n

/-- Rectangle: b rows padded by zeros, each of length at most a. -/
def rectangle (a b : ℕ) : Finset (Fin b → Fin (a+1)) := by
  classical
  exact Finset.univ.filter (fun l => Antitone l)

def rectangleWeight (q : K) (a b : ℕ) : K :=
  ∑ l ∈ rectangle a b, q ^ (∑ i, (l i).val)

/-- Successive rank at a Durfee-square row, zero-based indexing. -/
def successiveRank {a b : ℕ} (l : Fin b → Fin (a+1)) (j : Fin b) : ℤ :=
  (l j).val - ((Finset.univ.filter (fun i => j.val < (l i).val)).card : ℤ)

/-- An alternating subsequence of length μ, precisely AP Definitions 9.1–9.3.
The existential length-μ condition expresses oscillation at least μ. -/
def oscillates {a b : ℕ} (positive : Bool) (k i mu : ℕ)
    (l : Fin b → Fin (a+1)) : Prop :=
  ∃ js : Fin mu → Fin b, StrictMono js ∧ ∀ t,
    (js t).val < (l (js t)).val ∧
    (if (t.val % 2 = 0) = (positive = true)
      then (2*(k : ℤ)-i-1) < successiveRank l (js t)
      else successiveRank l (js t) ≤ -((i : ℤ)-1))

def oscillationPoly (q : K) (positive : Bool) (k i a b mu : ℕ) : K := by
  classical
  exact ∑ l ∈ (rectangle a b).filter (oscillates positive k i mu),
    q^(∑ j, (l j).val)

/-- Exact adjacent-part conditions, with the strict inequality determined by the larger part. -/
def gollnitzAllowed (s : Finset ℕ) : Prop :=
  (∀ j ∈ s, j ≠ 0 ∧ j ≠ 1 ∧ j ≠ 3) ∧
  ∀ pair ∈ (s.sort (· ≥ ·)).zip (s.sort (· ≥ ·)).tail,
    pair.2 + 6 ≤ pair.1 ∧
    (pair.1 % 6 = 0 ∨ pair.1 % 6 = 1 ∨ pair.1 % 6 = 3 → pair.2 + 6 < pair.1)

instance (s : Finset ℕ) : Decidable (gollnitzAllowed s) := by
  unfold gollnitzAllowed
  infer_instance

def gollnitz (t q : K) (N : ℤ) : K := by
  classical
  exact if N = -1 then 1 else if N < 0 then 0 else
    ∑ s ∈ ((Finset.range (N.toNat+1)).powerset).filter gollnitzAllowed,
      t^(∑ j ∈ s, if j%6 = 2 ∨ j%6 = 4 ∨ j%6 = 5 then 1 else 2) * q^(∑ j ∈ s, j)

def schurD (q : K) (n : ℕ) : K :=
  ∑ j ∈ Finset.range (n/2+1), q^(j*j) * gaussian q (n-j) j

def schurE (q : K) (n : ℕ) : K :=
  ∑ j ∈ Finset.range (n/2+1), q^(j*(j+1)) * gaussian q (n-j) j

/-- Cayley multiplicities, indexed by part sizes 1,...,n. -/
def cayleyVectors (n : ℕ) : Finset (Fin n → Fin (n+1)) := by
  classical
  exact Finset.univ.filter (fun p => (∑ j, (j.val+1)*(p j).val) = n)

/-- Concrete multivariate Laurent polynomial ring, with integer exponent vectors. -/
abbrev Laurent (m : ℕ) := AddMonoidAlgebra K (Fin m → ℤ)

def laurentScalar (m : ℕ) (c : K) : Laurent (K := K) m := AddMonoidAlgebra.single 0 c

def laurentRatio {m : ℕ} (i j : Fin m) : Laurent (K := K) m :=
  AddMonoidAlgebra.single (fun k => (if k = i then 1 else 0) - (if k = j then 1 else 0)) 1

def dysonProduct (q : K) {m : ℕ} (a : Fin m → ℕ) : Laurent (K := K) m :=
  ∏ i, ∏ j ∈ Finset.univ.filter (i < ·),
    poch (laurentRatio i j) (laurentScalar m q) (a i) *
    poch (laurentScalar m q * laurentRatio j i) (laurentScalar m q) (a j)

/-- Jackson derivative with the differentiable extension at x=0. -/
def jackson (q : ℂ) (f : ℂ → ℂ) (x : ℂ) : ℂ :=
  if x = 0 then deriv f 0 else (f x-f (q*x))/((1-q)*x)

def deltaOp (q b : K) (f : K → K) (x : K) : K := b*f (q*x)-f x

def deltaList (q : K) (bs : List K) (f : K → K) : K → K :=
  bs.foldr (deltaOp q) f

/-- GR finite Laurent definition of continuous q-ultraspherical polynomials. -/
def ultraspherical (beta t q : K) (n : ℕ) : K :=
  ∑ k ∈ Finset.range (n+1), poch beta q k * poch beta q (n-k) /
    (poch q q k * poch q q (n-k)) * t^((n : ℤ)-2*k)

def littleJacobi (x a b q : K) (n : ℕ) : K :=
  phi [q^(-(n : ℤ)),a*b*q^(n+1)] [a*q] q (q*x) n

/-- q-Racah: t=q^x is used instead of an ambiguous complex power. -/
def qRacah (t a b c q : K) (N n : ℕ) : K :=
  phi [q^(-(n : ℤ)),a*b*q^(n+1),t⁻¹,c*t*q^(-(N : ℤ))]
    [a*q,b*c*q,q^(-(N : ℤ))] q q n

/-- Askey–Wilson at x=(t+t⁻¹)/2; finite 4φ3 normalization. -/
def askeyWilson (t a b c d q : K) (n : ℕ) : K :=
  a^(-(n : ℤ)) * pochList [a*b,a*c,a*d] q n *
    phi [q^(-(n : ℤ)),a*b*c*d*q^((n : ℤ)-1),a*t,a/t] [a*b,a*c,a*d] q q n

/-- Generic multibase factor in GR (3.9.2): no implicit factorial in this factor. -/
def multibaseTerm (p : K) (as bs : List K) (k : ℕ) : K :=
  pochList as p k / pochList bs p k *
    ((-1 : K)^k*p^(k*(k-1)/2))^((bs.length : ℤ)-as.length)

/-- GR Φ with the primary factorial (p;p)_k included exactly once. -/
def bibasicPhi (as bs cs ds : List K) (p q z : K) (n : ℕ) : K :=
  ∑ k ∈ Finset.range (n+1), phiTerm as bs p z k * multibaseTerm q cs ds k

/-- Negative-length lists, used by the bidirectional matrix kernel. -/
def pochListInt (as : List K) (q : K) (n : ℤ) : K :=
  (as.map (fun a => pochInt a q n)).prod

/-- Domain of the reciprocal used in a negative-length Pochhammer. -/
def pochIntDefined (a q : K) (n : ℤ) : Prop :=
  n < 0 → poch (a*q^n) q (-n).toNat ≠ 0

def pochListIntDefined (as : List K) (q : K) (n : ℤ) : Prop :=
  ∀ a ∈ as, pochIntDefined a q n

def bibasicT (a b c p q : K) (k : ℤ) : K :=
  if k = -1 then 0 else
  pochList [a*p,b*p] p k.toNat * pochList [c*q,a*q/(b*c)] q k.toNat /
  (pochList [q,a*q/b] q k.toNat*pochList [a*p/c,b*c*p] p k.toNat)

def bibasicS (a b c d p q : K) (k : ℤ) : K :=
  pochListInt [a*p,b*p] p k*pochListInt [c*q,a*d^2*q/(b*c)] q k /
  (pochListInt [d*q,a*d*q/b] q k*pochListInt [a*d*p/c,b*c*p/d] p k)

def bibasicSDefined (a b c d p q : K) (k : ℤ) : Prop :=
  pochListIntDefined [a*p,b*p,a*d*p/c,b*c*p/d] p k ∧
  pochListIntDefined [c*q,a*d^2*q/(b*c),d*q,a*d*q/b] q k ∧
  pochListInt [d*q,a*d*q/b] q k*pochListInt [a*d*p/c,b*c*p/d] p k ≠ 0

def inverseA (a b p q : K) (n j : ℕ) : K :=
  (-1)^(n+j)*(1-a*p^j*q^j)*(1-b*p^j*q^(-(j : ℤ))) *
  pochListInt [a*p*q^n,b*p*q^(-(n : ℤ))] p ((n : ℤ)-1) /
  (poch q q (n-j)*pochList [a*p*q^n,b*p*q^(-(n : ℤ))] p j *
  poch (b*q^(1-2*(n : ℤ))/a) q (n-j))

def inverseADefined (a b p q : K) (n j : ℕ) : Prop :=
  pochListIntDefined [a*p*q^n,b*p*q^(-(n : ℤ))] p ((n : ℤ)-1) ∧
  poch q q (n-j)*pochList [a*p*q^n,b*p*q^(-(n : ℤ))] p j *
  poch (b*q^(1-2*(n : ℤ))/a) q (n-j) ≠ 0

def inverseB (a b p q : K) (j m : ℕ) : K :=
  pochList [a*p^m*q^m,b*p^m*q^(-(m : ℤ))] p (j-m) /
  pochList [q,a*q^(1+2*m)/b] q (j-m) *
  (-a*q^(1+2*m)/b)^(j-m)*q^((j-m)*(j-m-1))

end
end FiniteQBenchmark
