import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from macmahon.pipeline import SPEC,prepare,prove_source
from workflow.structural_check import run
O='FiniteQMacMahon.omegaGE'
F='FiniteQMacMahon.factor'
S='AddMonoidAlgebra.single'
CASES=[
 ('rectangle_encoding_symbolic','{K : Type*} [Field K] (q : K) (a b : ℕ)',
  'FiniteQMacMahon.omegaAll (FiniteQMacMahon.rectangleEncoding q a b) = FiniteQBenchmark.rectangleWeight q a b',True),
 ('symbolic_triangle','{R : Type*} [CommSemiring R] (n m : ℕ) (u v : ℕ → R)',
  f'{O} ({F} (Finset.range (n+1)) 1 u * {F} (Finset.range (m+1)) (-1) v) = ∑ i ∈ Finset.range (n+1), ∑ j ∈ Finset.range (min i m+1), u i * v j',True),
 ('signed_affine_constraint','(s t : Finset ℕ) (a b c : ℤ) (u v : ℕ → ℚ)',
  f'{O} ({S} c (1:ℚ) * {F} s a u * {F} t b v) = ∑ i ∈ s, ∑ j ∈ t, if 0 ≤ c+a*(i:ℤ)+b*(j:ℤ) then u i*v j else 0',True),
 ('q_weighted_finite','(q z : ℚ)',
  f'{O} ({F} (Finset.range 3) 1 (fun i => q^i) * {F} (Finset.range 3) (-1) (fun j => z^j)) = 1+q+q*z+q^2+q^2*z+q^2*z^2',True),
 ('negative_exponents_cancel','(x y : ℚ)',
  f'{O} ({S} (-2) x * {S} 3 y) = x*y',True),
 ('empty_support','(a : ℤ) (u : ℕ → ℚ)',
  f'{O} ({F} ∅ a u) = 0',True),
 ('two_auxiliary_constraints','(x : ℚ)',
  f'{O} ({O} ({S} 2 ({S} (-1) x))) = 0',True),
 ('two_auxiliary_survive','(x : ℚ)',
  f'{O} ({O} ({S} 2 ({S} 0 x))) = x',True),
 ('wrong_projection_before_product','(x y : ℚ)',
  f'{O} ({S} (-2) x * {S} 3 y) = {O} ({S} (-2) x) * {O} ({S} 3 y)',False),
 ('wrong_boundary','(q : ℚ)',
  f'{O} ({F} (Finset.range 2) 1 (fun i => q^i) * {F} (Finset.range 2) (-1) (fun j => q^j)) = 1+q',False),
 ('wrong_constraint_sign','(x y : ℚ)',
  f'{O} ({S} (-3) x * {S} 2 y) = x*y',False),
]
CASES += [
 ('chain_series_factorization','{K : Type*} [Field K] (q : K) (b : ℕ)',
  'FiniteQMacMahon.rectangleSeries q b = FiniteQMacMahon.coneProduct q b',True),
 ('rational_denominator_certificate','{R : Type*} [CommRing R] (q : R) (b : ℕ)',
  'FiniteQMacMahon.coneProduct q b * (∏ i ∈ Finset.range (b+1), (1-PowerSeries.C (q^i)*PowerSeries.X)) = 1',True),
 ('general_geometric_factor','{R : Type*} [CommRing R] (c : R)',
  'FiniteQMacMahon.geometric c * (1-PowerSeries.C c*PowerSeries.X) = 1',True),
 ('rectangle_original_renamed','{K : Type*} [Field K] (t : K) (N r : ℕ) (hr : r ≤ N)',
  'FiniteQBenchmark.gaussian t N r = FiniteQBenchmark.rectangleWeight t (N-r) r',True),
 ('rectangle_reversed','{K : Type*} [Field K] (q : K) (a b : ℕ)',
  'FiniteQBenchmark.rectangleWeight q a b = FiniteQBenchmark.gaussian q (a+b) b',True),
 ('zero_base_allowed','(a b : ℕ)',
  'FiniteQBenchmark.rectangleWeight (0:ℚ) a b = FiniteQBenchmark.gaussian 0 (a+b) b',True),
 ('unit_base_allowed','(a b : ℕ)',
  'FiniteQBenchmark.rectangleWeight (1:ℚ) a b = FiniteQBenchmark.gaussian 1 (a+b) b',True),
 ('missing_index_bound','(q : ℚ) (n k : ℕ)',
  'FiniteQBenchmark.gaussian q n k = FiniteQBenchmark.rectangleWeight q (n-k) k',False),
 ('wrong_rectangle_weight','(q : ℚ) (a b : ℕ)',
  'FiniteQBenchmark.rectangleWeight q a b = q * FiniteQBenchmark.gaussian q (a+b) b',False),
 ('missing_geometric_factor','(q : ℚ) (b : ℕ)',
  'FiniteQMacMahon.coneProduct q b * (∏ i ∈ Finset.range b, (1-PowerSeries.C (q^i)*PowerSeries.X)) = 1',False),
]
if __name__=='__main__':raise SystemExit(run(SPEC,CASES,prepare,prove_source))
