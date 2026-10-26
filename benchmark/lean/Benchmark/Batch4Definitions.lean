import Benchmark.Batch3Proofs
import Mathlib.RingTheory.PowerSeries.Inverse

namespace FiniteQBenchmark
open scoped BigOperators
noncomputable section
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

/-- Integer upper Gaussian: negative upper values are not discarded. -/
def integerTopGaussian (q : K) (v : ℤ) (k : ℕ) : K :=
  (∏ i ∈ Finset.range k, (1-q^(v-i))) / poch q q k

def boundedCompositionCount (N M n : ℕ) : ℕ :=
  ((Finset.univ : Finset (Fin M → Fin N)).filter
    (fun a => (∑ i, (a i).val+1) = n)).card

def aqHermite (x q : K) (r : ℕ) : K :=
  ∑ j ∈ Finset.range (r+1), gaussian q r j*x^((r:ℤ)-2*j)

/-- Triangular inverse defined by AQ (2.38), not its closed product. -/
def aqInverseT (q : K) (r N : ℕ) : K :=
  if h : N = 0 then 1 else
    -∑ j : Fin (N/2), gaussian q (r+2*(j.val+1)) (j.val+1) *
      aqInverseT q (r+2*(j.val+1)) (N-2*(j.val+1))
termination_by N
decreasing_by have := j.isLt; omega

/-- AQ (6.14), coefficients of G₀ before division by (x;q³)∞. -/
def aqG0Coeff (q : K) : ℕ → K
  | 0 => 1
  | n+1 => (((q+q^2)*q^(3*n)+q^(6*n+3))*aqG0Coeff q n -
      (if n=0 then 0 else q^(6*n)*aqG0Coeff q (n-1))) / (1-q^(3*(n+1)))

def scaleSeries (q : K) (f : PowerSeries K) : PowerSeries K :=
  PowerSeries.mk (fun n => q^n*PowerSeries.coeff n f)

/-- Coefficients of the Euler denominator, normalized by constant coefficient 1. -/
def eulerReciprocalSeries (q : K) : PowerSeries K :=
  PowerSeries.mk (fun n => 1/poch q q n)

def eulerProductSeries (q : K) : PowerSeries K :=
  PowerSeries.mk (fun n => (-1)^n*q^(n*(n-1)/2)/poch q q n)

def aqSchurCoeff (q : K) (n : ℕ) : K :=
  PowerSeries.coeff n ((PowerSeries.mk (aqG0Coeff q))*eulerReciprocalSeries (q^3))

/-- Occupied sites are 1,...,N-1; sigma=1 blocks the first site. F₀=1. -/
def aqOccupation (sigma : Bool) (N : ℕ) : Finset (Finset ℕ) :=
  ((Finset.Ico 1 N).powerset).filter (fun s =>
    (sigma = true → 1 ∉ s) ∧ ∀ i ∈ s, i+1 ∉ s)

def aqF (q : K) (sigma : Bool) (N : ℕ) : K :=
  ∑ s ∈ aqOccupation sigma N, q^(∑ j ∈ s, j)

/-- AQ (8.46)-(8.49), a distinct polynomial from F. -/
def aqG (q : K) (sigma : Bool) : ℕ → K
  | 0 => if sigma then 0 else 1
  | 1 => 1
  | 2 => if sigma then 1 else 1+q
  | n+3 => aqG q sigma (n+2)+q*aqG q sigma (n+1)-(q-q^(n+2))*aqG q sigma n

/-- Pair (X₂ₙ₋₁,X₂ₙ). -/
def aqXPair (a b q : K) : ℕ → K × K
  | 0 => (a,b)
  | n+1 => let v := aqXPair a b q n
           let u := v.2+q^(2*n+1)*v.1
           (u,u+q^(n+1)*(1+q^(n+1))*(v.2+v.1))

def aqX (a b q : K) (j : ℤ) : K :=
  if j = -1 then a else if j < 0 then 0 else
    if j.toNat % 2 = 0 then (aqXPair a b q (j.toNat/2)).2
    else (aqXPair a b q (j.toNat/2+1)).1

/-- Five-input operator AQ (10.22); integer powers retain all source shifts. -/
def aqOperator (q t : K) (n : ℤ) (x y z w v : K) : K :=
  x-(1+t*q^(6*n)*(q^(-1:ℤ)+q^(-2:ℤ)+q^(-4:ℤ)))*y -
  t^2*q^(6*n)*(q^(-3:ℤ)+q^(-5:ℤ)+q^(-6:ℤ))*(1-q^(6*n-6))*z -
  t^3*q^(12*n-13)*(t*(q^(-1:ℤ)+q^(-2:ℤ)+q^(-4:ℤ))+q^(6*n-12))*w -
  t^6*q^(18*n-32)*v

def aqJ (q t : K) (d : ℤ → K) (n : ℤ) : K :=
  aqOperator q t n (d (6*n-1)) (d (6*n-7)) (d (6*n-13)) (d (6*n-19)) (d (6*n-25))

def aqOperatorG (q t : K) (d : ℤ → K) (n : ℤ) : K :=
  d (6*n+5)-t*q^(6*n+2)*(1+q^2+q^3)*d (6*n-1) +
  t^2*q^(12*n)*(1+q+q^3)*d (6*n-7)-t^3*q^(18*n-7)*d (6*n-13)

/-- (1-X^m)^(-a), retaining integer signed multiplicities. -/
def eulerIntegerFactor (a : ℤ) (m : ℕ) : PowerSeries ℚ :=
  if 0 ≤ a then ((1-PowerSeries.X^m)⁻¹)^a.toNat else (1-PowerSeries.X^m)^(-a).toNat

def eulerTransformCoeff (a : ℕ → ℤ) (n : ℕ) : ℚ :=
  PowerSeries.coeff n (∏ m ∈ Finset.Icc 1 n, eulerIntegerFactor (a m) m)

def divisorWeight (a : ℕ → ℤ) (j : ℕ) : ℤ := ∑ d ∈ j.divisors, (d:ℤ)*a d

/-- Canonical coefficient solution of f(z)=f(qz)+zq f(q²z). -/
def aqRRCoeff (q : K) : ℕ → K
  | 0 => 1
  | n+1 => q^(2*n+1)/(1-q^(n+1))*aqRRCoeff q n

def aqH (l m v q : K) (n : ℕ) : K :=
  ∑ r ∈ Finset.range (n+1), ∑ s ∈ Finset.range (n-r+1),
    l^r*m^s*v^(n-r-s)/(poch q q r*poch q q s*poch q q (n-r-s))

/-- The polynomial extension of (f(x)-f(qx))/x at zero. -/
def qDelta (q : ℂ) (f : ℂ → ℂ) (x : ℂ) : ℂ :=
  if x = 0 then (1-q)*deriv f 0 else (f x-f (q*x))/x

/-- Signed monomials for the B_n constant term product. -/
def rootMono {n : ℕ} (v : Fin n → ℤ) : Laurent (K := K) n :=
  AddMonoidAlgebra.single v 1

def bnProduct (q : K) (n a b : ℕ) : Laurent (K := K) n :=
  let Q := laurentScalar n q
  (∏ i : Fin n, poch (rootMono (fun j => if j=i then 1 else 0)) Q a *
    poch (Q*rootMono (fun j => if j=i then -1 else 0)) Q a) *
  ∏ i : Fin n, ∏ j ∈ Finset.univ.filter (i < ·),
    poch (rootMono (fun k => (if k=i then 1 else 0)+(if k=j then 1 else 0))) Q b *
    poch (Q*rootMono (fun k => (if k=i then -1 else 0)+(if k=j then -1 else 0))) Q b *
    poch (rootMono (fun k => (if k=i then 1 else 0)-(if k=j then 1 else 0))) Q b *
    poch (Q*rootMono (fun k => (if k=j then 1 else 0)-(if k=i then 1 else 0))) Q b

def fineC (a b q : K) (n : ℕ) : K := poch (a*q) q n / poch (b*q) q n

def fineL (a b t q : K) (j : ℕ) : K := b*q^j/(b*q^j-a*t)
def fineM (a b t q : K) (j : ℕ) : K := (b*q^j-a)*t/((1-b*q^(j+1))*(b*q^j-a*t))
/-- Pair (Hₙ₋₁,Gₙ₋₁), initialized at index -1. -/
def fineHG (a b t q : K) : ℕ → K × K
  | 0 => (1,0)
  | n+1 => let v := fineHG a b t q n
           (fineM a b t q n*v.1,v.2+fineL a b t q n*v.1)

def fineA (a b q : K) (N : ℕ) : K :=
  PowerSeries.coeff N (eulerProductSeries q * PowerSeries.mk (fineC a b q))

/-- Multinomial enumerator, works for any finite parameter index type. -/
def fineQ {I : Type*} [Fintype I] (q : K) (u : I → K) (n : ℕ) : K :=
  ∑ r ∈ (Finset.univ : Finset (I → Fin (n+1))).filter (fun r => (∑ i, (r i).val) = n),
    poch q q n * ∏ i, u i^(r i).val/poch q q (r i).val

def shellPartitions (L r : ℕ) : Finset (Fin (L-r) → Fin (L+1)) :=
  (rectangle L (L-r)).filter (fun l =>
    (∀ i, 0 < (l i).val) ∧ ∃ i, (l i).val = L)

/-- q-trinomial C, with zero terms excluded before negative powers are evaluated. -/
def sillsC (q : K) (n : ℕ) (j : ℤ) : K :=
  ∑ k ∈ Finset.range (n+1),
    if 0 ≤ (k:ℤ)+j ∧ (k:ℤ)+j ≤ n-k then
      q^((k:ℤ)*((k:ℤ)+j)).toNat * gaussian q n k * gaussianInt q (n-k) ((k:ℤ)+j)
    else 0

def sillsT (x q : K) (n : ℕ) : K :=
  ∑ j ∈ Finset.Icc (-(n:ℤ)) (n:ℤ), x^j*q^(j*(3*j-1)/2).toNat*sillsC (q^3) n j

def sillsT01 (q : K) (one : Bool) (n : ℕ) (j : ℤ) : K :=
  ∑ k ∈ Finset.range (n+1), (if one then -q else -1)^k *
    gaussian (q^2) n k * gaussianInt q (2*(n:ℤ)-2*k) ((n:ℤ)-j-k)

def distinctPartitionCount (j l r : ℕ) : ℕ :=
  (((Finset.Icc 1 j).powerset).filter (fun s => s.card=l ∧ ∑ i ∈ s, i = r)).card

/-- Source alpha^(d,e,k)(x^e,q^e); e affects the Bailey base, not this expression.
The zero index is still evaluated using its displayed quotient. -/
def sillsAlpha (x q : K) (d k r : ℕ) : K :=
  if d ∣ r then let s := r/d
    (-1)^s*x^(((k:ℤ)-d)*s)*q^(((d:ℤ)*(2*k-2*d+1)*s*s-d*s)/2)*
    (1-x*q^(2*d*s))*poch x (q^d) s/((1-x)*poch (q^d) (q^d) s)
  else 0

/-- Schur gap partitions; multiples of 3 may not be adjacent with difference 3. -/
def sillsAllowed (s : Finset ℕ) : Prop :=
  (∀ j ∈ s, 0 < j) ∧
  ∀ pair ∈ (s.sort (· ≥ ·)).zip (s.sort (· ≥ ·)).tail,
    pair.2+3 ≤ pair.1 ∧ (pair.1%3=0 ∧ pair.2%3=0 → pair.2+3 < pair.1)

def sillsS (x q : K) (N : ℤ) : K :=
  if N = -1 then 1 else if N < 0 then 0 else
    ∑ s ∈ ((Finset.range (N.toNat+1)).powerset).filter sillsAllowed,
      x^(∑ j ∈ s, (if j%3=1 then (1:ℤ) else if j%3=2 then -1 else 0)) * q^(∑ j ∈ s, j)

def sillsB (q : K) (n : ℕ) : K := ∑ k ∈ Finset.range (n+1), q^(k*k)*gaussian q n k

def sillsP (q : K) (n : ℕ) : K :=
  ∑ j ∈ Finset.range (n+1), ∑ k ∈ Finset.range (min j (n-j)+1),
    q^(j*j+k*k)*gaussian (q^2) j k*gaussian (q^2) (n-k) j

end
end FiniteQBenchmark
