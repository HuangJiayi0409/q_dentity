import Benchmark.Representation
import Mathlib.Topology.Instances.Complex

namespace FiniteQBenchmark
open scoped BigOperators
noncomputable section
variable {K : Type*} [Field K]

def rising (a : K) (n : ℕ) : K := ∏ j ∈ Finset.range n, (a+j)
def risingList (as : List K) (n : ℕ) : K := (as.map (fun a => rising a n)).prod

def laurentMono (j : ℤ) (c : K) : AddMonoidAlgebra K ℤ := AddMonoidAlgebra.single j c

/-- At least one upper parameter first terminates at exactly n. -/
def terminatesAt (as : List K) (q : K) (n : ℕ) : Prop :=
  (∃ a ∈ as, 1-a*q^n = 0) ∧ ∀ k < n, ∀ a ∈ as, 1-a*q^k ≠ 0

/-- Least terminating length up to the requested cutoff, or the cutoff itself. -/
def firstTermination (as : List K) (q : K) (n : ℕ) : ℕ := by
  classical
  let ts := (Finset.range (n+1)).filter (fun k => ∃ a ∈ as, 1-a*q^k=0)
  exact if h : ts.Nonempty then ts.min' h else n

/-- Askey-Wilson divided difference in the Laurent coordinate. -/
def awDiff (s : K) (f : K → K) (z : K) : K :=
  (f (s*z)-f (z/s))/((s-s⁻¹)*(z-z⁻¹)/2)

/-- Generic normalized three-term solution: the previous value at degree zero is 0. -/
def recurrencePair (A B C : ℕ → K) : ℕ → K × K
  | 0 => (0,1)
  | n+1 => let v := recurrencePair A B C n; (v.2,(B n*v.2-C n*v.1)/A n)

def awAssocA (a b c d q v : K) : K :=
  a⁻¹*(1-a*b*v)*(1-a*c*v)*(1-a*d*v)*(1-a*b*c*d*v/q) /
  ((1-a*b*c*d*v^2/q)*(1-a*b*c*d*v^2))
def awAssocC (a b c d q v : K) : K :=
  a*(1-b*c*v/q)*(1-b*d*v/q)*(1-c*d*v/q)*(1-v) /
  ((1-a*b*c*d*v^2/q^2)*(1-a*b*c*d*v^2/q))
def associatedAW (z a b c d rho q : K) (n : ℕ) : K :=
  (recurrencePair (fun j => awAssocA a b c d q (rho*q^j))
    (fun j => z+z⁻¹-a-a⁻¹+awAssocA a b c d q (rho*q^j)+awAssocC a b c d q (rho*q^j))
    (fun j => awAssocC a b c d q (rho*q^j)) n).2

def associatedUltra (z alpha beta q : K) (n : ℕ) : K :=
  (recurrencePair (fun j => (1-alpha*q^(j+1))/(1-alpha*beta*q^j))
    (fun _ => z+z⁻¹)
    (fun j => (1-alpha*beta^2*q^((j:ℤ)-1))/(1-alpha*beta*q^j)) n).2

end
end FiniteQBenchmark
