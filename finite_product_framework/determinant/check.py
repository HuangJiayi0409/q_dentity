import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from determinant.pipeline import SPEC,prepare,prove_source
from workflow.structural_check import run
CASES=[
 ('symbolic_factorization','{I : Type*} [Fintype I] [DecidableEq I] [LinearOrder I] (A L U : Matrix I I ℚ) (hA : A = L*U) (hL : L.IsLowerTriangular) (hU : U.IsUpperTriangular)',
 'A.det = (∏ i, L i i)*(∏ i, U i i)',False),
 ('missing_factorization','{I : Type*} [Fintype I] [DecidableEq I] [LinearOrder I] (A L U : Matrix I I ℚ) (hL : L.IsLowerTriangular) (hU : U.IsUpperTriangular)',
 'A.det = (∏ i, L i i)*(∏ i, U i i)',False),
 ('symbolic_vandermonde','(n : ℕ) (v : Fin n → ℚ)',
 '(Matrix.vandermonde v).det = ∏ i : Fin n, ∏ j ∈ Finset.Ioi i, (v j-v i)',True),
 ('singular_allowed','(a b c : ℚ)',
 '(!![a,a*b;c,c*b] : Matrix (Fin 2) (Fin 2) ℚ).det = 0',True),
 ('wrong_sign','(a b c d : ℚ)',
 '(!![a,b;c,d] : Matrix (Fin 2) (Fin 2) ℚ).det = a*d+b*c',False),
 ('empty_matrix','(d : Fin 0 → ℚ)',
 '(Matrix.diagonal d).det = 1',True),
 ('missing_object_bridge','(x : ℚ) (d : Fin 2 → ℚ)',
 'x = (Matrix.diagonal d).det',False)]
CASES.extend([
 ('constructed_dense_plu','(q : ℚ)',
  '(!![1,q,2;2,2*q+1,3;3,3*q+2,5] : Matrix (Fin 3) (Fin 3) ℚ).det = 1',True),
 ('constructed_row_permutation','(q : ℚ)',
  '(!![0,1,0;1,q,1;0,0,1] : Matrix (Fin 3) (Fin 3) ℚ).det = -1',True),
 ('pivot_can_vanish','(q : ℚ)',
  '(!![q,1,0;q+1,0,1;q+2,1,1] : Matrix (Fin 3) (Fin 3) ℚ).det = 1-q',True),
 ('wrong_dense_value','(q : ℚ)',
  '(!![1,q,2;2,2*q+1,3;3,3*q+2,5] : Matrix (Fin 3) (Fin 3) ℚ).det = 2',False),
 ('reversed_dense_value','(q : ℚ)',
  '1 = (!![1,q,2;2,2*q+1,3;3,3*q+2,5] : Matrix (Fin 3) (Fin 3) ℚ).det',True)])
CASES.append(('constructed_plu_five','(q : ℚ)',
 '(!![0,1,0,0,0;0,0,1,0,0;0,0,0,1,0;0,0,0,0,1;q,0,0,0,0] : Matrix (Fin 5) (Fin 5) ℚ).det = q',True))
if __name__=='__main__':raise SystemExit(run(SPEC,CASES,prepare,prove_source,
    required_constructions={**{k:'constructed_symbolic_plu' for k in
        ('constructed_dense_plu','constructed_row_permutation','reversed_dense_value','constructed_plu_five')},
        'pivot_can_vanish':'constructed_division_free_determinant'}))
