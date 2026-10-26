import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kernel_transform.pipeline import SPEC,prepare,prove_source
from workflow.structural_check import run
C='(t : ℚ) (v : Fin 2 → ℚ)'
A='(!![1,t;0,1] : Matrix (Fin 2) (Fin 2) ℚ)'
B='(!![1,-t;0,1] : Matrix (Fin 2) (Fin 2) ℚ)'
CASES=[
 ('inverse_shear',C,f'(fun i => ∑ k, {A} i k * ∑ j, {B} k j * v j) = v',True),
 ('wrong_inverse',C,f'(fun i => ∑ k, {A} i k * ∑ j, {A} k j * v j) = v',False),
 ('transpose','(N : ℕ) (a b : ℕ → ℚ) (K : ℕ → ℕ → ℚ)',
 '(∑ i ∈ Finset.range (N+1), a i * ∑ j ∈ Finset.Icc i N, K i j * b j) = ∑ j ∈ Finset.range (N+1), b j * ∑ i ∈ Finset.range (j+1), a i * K i j',True),
 ('wrong_endpoint','(N : ℕ) (a b : ℕ → ℚ) (K : ℕ → ℕ → ℚ)',
 '(∑ i ∈ Finset.range (N+1), a i * ∑ j ∈ Finset.Icc i N, K i j * b j) = ∑ j ∈ Finset.range (N+1), b j * ∑ i ∈ Finset.range j, a i * K i j',False),
 ('arbitrary_inverse','{I : Type*} [Fintype I] [DecidableEq I] (A B : I → I → ℚ) (v : I → ℚ) (h : ∀ i j, ∑ k, A i k * B k j = if i = j then 1 else 0)',
 '(fun i => ∑ k, A i k * ∑ j, B k j * v j) = v',False),
 ('composition','{I J L : Type*} [Fintype I] [Fintype J] (A : L → I → ℚ) (B : I → J → ℚ) (C : L → J → ℚ) (v : J → ℚ) (h : ∀ i j, ∑ k, A i k * B k j = C i j)',
 '(fun i => ∑ k, A i k * ∑ j, B k j * v j) = (fun i => ∑ j, C i j * v j)',False)]
# These two true conditional statements now test that certificate-only replay
# is not counted as automatic construction in the production entry.
C3='(q : ℚ) (v : Fin 3 → ℚ)'
A3='(!![1,q,0;0,1,q;0,0,1] : Matrix (Fin 3) (Fin 3) ℚ)'
B3='(!![1,-q,q^2;0,1,-q;0,0,1] : Matrix (Fin 3) (Fin 3) ℚ)'
CASES.extend([
 ('constructed_inverse_three',C3,f'(fun i => ∑ k, {A3} i k * ∑ j, {B3} k j * v j) = v',True),
 ('wrong_inverse_three',C3,f'(fun i => ∑ k, {A3} i k * ∑ j, {A3} k j * v j) = v',False),
 ('singular_kernel','(v : Fin 2 → ℚ)',
  '(fun i => ∑ k, (!![1,0;0,0] : Matrix (Fin 2) (Fin 2) ℚ) i k * ∑ j, (!![1,0;0,1] : Matrix (Fin 2) (Fin 2) ℚ) k j * v j) = v',False),
 ('missing_inverse_domain','(q : ℚ) (v : Fin 2 → ℚ)',
  '(fun i => ∑ k, (!![q,0;0,1] : Matrix (Fin 2) (Fin 2) ℚ) i k * ∑ j, (!![q⁻¹,0;0,1] : Matrix (Fin 2) (Fin 2) ℚ) k j * v j) = v',False),
 ('inverse_domain_present','(q : ℚ) (hq : q ≠ 0) (v : Fin 2 → ℚ)',
  '(fun i => ∑ k, (!![q,0;0,1] : Matrix (Fin 2) (Fin 2) ℚ) i k * ∑ j, (!![q⁻¹,0;0,1] : Matrix (Fin 2) (Fin 2) ℚ) k j * v j) = v',True)])
CASES.append(('constructed_composition','(q : ℚ) (v : Fin 2 → ℚ)',
 '(fun i => ∑ k, (!![1,q;0,1] : Matrix (Fin 2) (Fin 2) ℚ) i k * ∑ j, (!![1,0;q,1] : Matrix (Fin 2) (Fin 2) ℚ) k j * v j) = (fun i => ∑ j, (!![1+q^2,q;q,1] : Matrix (Fin 2) (Fin 2) ℚ) i j * v j)',True))
A5='(!!['+';'.join(','.join('1' if i==j else 'q' if j==i+1 else '0' for j in range(5)) for i in range(5))+'] : Matrix (Fin 5) (Fin 5) ℚ)'
B5='(!!['+';'.join(','.join(f'(-q)^{j-i}' if j>=i else '0' for j in range(5)) for i in range(5))+'] : Matrix (Fin 5) (Fin 5) ℚ)'
CASES.append(('constructed_inverse_five','(q : ℚ) (v : Fin 5 → ℚ)',
 f'(fun i => ∑ k, {A5} i k * ∑ j, {B5} k j * v j) = v',True))
if __name__=='__main__':raise SystemExit(run(SPEC,CASES,prepare,prove_source,
    required_constructions={**{k:'constructed_rational_inverse' for k in
         ('inverse_shear','constructed_inverse_three','inverse_domain_present','constructed_inverse_five')},
         'constructed_composition':'constructed_kernel_composition'}))
