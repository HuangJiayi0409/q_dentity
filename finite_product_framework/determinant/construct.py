"""Automatic symbolic PLU, with a division-free evaluation fallback.

Both constructions receive only the matrix, never the claimed determinant.
SymPy results are untrusted; factorization and evaluation are rebuilt in Lean.
"""
import sympy as s
from workflow.matrix_symbolic import ScalarCodec, checked_zero, matrix_record, scalar_finish


def det_finish(names):
    rules = [*names, 'Matrix.det_succ_row_zero', 'Matrix.det_fin_two',
             'Matrix.det_fin_three', 'Fin.sum_univ_succ', 'Matrix.submatrix_apply',
             'Fin.succAbove']
    return 'simp [' + ', '.join(rules) + '] <;> (' + scalar_finish() + ')'


def construct(raw):
    codec = ScalarCodec()
    a = codec.matrix(raw['matrix'])
    n, ty = raw['size'], raw['type']
    matrix = raw['matrix']['display']
    value = s.factor(a.det(method='berkowitz'))
    lean_value = codec.lean(value)
    prefix = '  classical\n' + ('  symm\n' if raw['reverse'] else '')
    result = []
    l,u,swaps = a.LUdecomposition()
    p = s.eye(n)
    for i,j in swaps:
        p.row_swap(i,j)
    checked_zero(p*a-l*u)
    sign = (-1)**len(swaps)
    diagonal = s.prod(u[i,i] for i in range(n))
    checked_zero([value-sign*diagonal])
    declarations = '\n'.join(f'  let {name} : Matrix (Fin {n}) (Fin {n}) ({ty}) := '+codec.matrix_lean(m,ty)
                  for name,m in [('synthP',p),('synthL',l),('synthU',u)])
    finish = scalar_finish()
    # Triangular determinants are evaluated after checking the independently
    # constructed factorization; no existing L/U or hA is searched for.
    plu = prefix + declarations + f'''
  have synthFactor : synthP * ({matrix}) = synthL * synthU := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [synthP, synthL, synthU, Matrix.mul_apply, Fin.sum_univ_succ] <;> ({finish})
  have synthPDet : synthP.det = ({sign} : {ty}) := by
    {det_finish(['synthP'])}
  have synthLDet : synthL.det = (1 : {ty}) := by
    {det_finish(['synthL'])}
  have synthUDet : synthU.det = ({codec.lean(diagonal)} : {ty}) := by
    {det_finish(['synthU'])}
  have synthRelation := congrArg Matrix.det synthFactor
  rw [Matrix.det_mul, Matrix.det_mul, synthPDet, synthLDet, synthUDet] at synthRelation
  have synthValue : ({matrix}).det = ({lean_value} : {ty}) := by
    calc
      _ = ({sign} : {ty}) * ({codec.lean(diagonal)}) := by
        linear_combination ({sign} : {ty}) * synthRelation
      _ = _ := by {finish}
  rw [synthValue] <;> ({finish})
'''
    result.append(dict(plan='constructed_symbolic_plu',proof_script=plu,
        certificate=dict(algorithm='symbolic LU with row permutation',constructor_inputs=['matrix'],
            target_value_used_in_search=False,matrix=matrix_record(a),permutation=matrix_record(p),
            lower=matrix_record(l),upper=matrix_record(u),row_swaps=swaps,
            determinant=str(value),atoms=codec.atoms,dimension=n)))
    # This fallback also covers zero/singular pivots and parameter specializations
    # for which the generic rational PLU denominators cannot be discharged.
    direct = prefix + f'''  have synthValue : ({matrix}).det = ({lean_value} : {ty}) := by
    {det_finish([])}
  rw [synthValue] <;> ({finish})
'''
    result.append(dict(plan='constructed_division_free_determinant',proof_script=direct,
        certificate=dict(algorithm='Berkowitz determinant; Lean cofactor reconstruction',
            constructor_inputs=['matrix'],target_value_used_in_search=False,
            matrix=matrix_record(a),determinant=str(value),atoms=codec.atoms,dimension=n,
            domain_policy='no pivot division; any input divisions still require original-domain verification')))
    return result
