import Benchmark.Gaussian
namespace FiniteQBenchmark
open scoped BigOperators
noncomputable section
variable {K : Type*} [Field K]
def kacPowerNat (x a q : K) (n : ℕ) : K :=
  ∏ i ∈ Finset.range n, (x-q^i*a)

def regular (q : K) : Prop := q ≠ 0 ∧ ∀ n : ℕ, 0 < n → q^n ≠ 1

def sillsAlpha (x q : K) (d k r : ℕ) : K :=
  if d ∣ r then let s := r/d
    (-1)^s*x^(((k:ℤ)-d)*s)*q^(((d:ℤ)*(2*k-2*d+1)*s*s-d*s)/2)*
    (1-x*q^(2*d*s))*poch x (q^d) s/((1-x)*poch (q^d) (q^d) s)
  else 0
end
end FiniteQBenchmark
