"""Synthesize a weighted self-adjoint separator without an input operator.

For a finite pairing, solve A f = 0, A g = g, W A = A^T W exactly.
The eigenvalues 0 and 1 are separated in every field. The target pairing is
never supplied to a simplifier as a construction equation.
"""
import sympy as s
from workflow.matrix_symbolic import ScalarCodec, checked_zero, matrix_record, scalar_finish


def construct(raw):
    codec = ScalarCodec()
    w, f, g = (codec.vector(raw[k]) for k in ('weight', 'left', 'right'))
    n = raw['size']
    variables = s.symbols('operator0:' + str(n*n))
    a = s.Matrix(n, n, variables)
    weighted = s.diag(*w)*a
    equations = list(a*f) + list(a*g-g) + [weighted[i,j]-weighted[j,i]
                  for i in range(n) for j in range(i)]
    solution = s.linsolve(equations, variables)
    if solution is s.EmptySet or not solution:
        raise ValueError('no weighted spectral separator in the finite matrix ansatz')
    values = next(iter(solution))
    free = set().union(*(x.free_symbols for x in values)) & set(variables)
    # Free operator entries may be specialized; input scalar parameters may not.
    result = s.Matrix(n,n,[s.cancel(x.subs(dict.fromkeys(free,0))) for x in values])
    checked_zero(result*f)
    checked_zero(result*g-g)
    checked_zero(s.diag(*w)*result-result.T*s.diag(*w))
    text = codec.matrix_lean(result,raw['type'])
    ws, fs, gs = (raw[k]['display'] for k in ('weight','left','right'))
    ty = raw['type']
    finish = scalar_finish()
    script = f'''  classical
  let synthOperator : Matrix (Fin {n}) (Fin {n}) ({ty}) := {text}
  apply FiniteQSpectral.orthogonal ({ws}) synthOperator ({fs}) ({gs}) (0 : {ty}) 1
  · intro i j
    fin_cases i <;> fin_cases j <;> simp [synthOperator] <;> ({finish})
  · intro i
    fin_cases i <;> simp [synthOperator, Fin.sum_univ_succ] <;> ({finish})
  · intro i
    fin_cases i <;> simp [synthOperator, Fin.sum_univ_succ] <;> ({finish})
  · exact zero_ne_one
'''
    return [dict(plan='constructed_weighted_separator',proof_script=script,
                 certificate=dict(algorithm='exact linear synthesis of weighted self-adjoint operator',
                    constructor_inputs=['weight vector','left vector','right vector'],
                    supplied_operator_required=False, eigenvalues=['0','1'],
                    operator=matrix_record(result),atoms=codec.atoms,dimension=n,
                    unknown_count=n*n,equation_count=len(equations),
                    equations=list(map(str,equations)),free_entries_set_to_zero=list(map(str,sorted(free,key=str))),
                    domain_policy='generated rational denominators checked by Lean; no extra assumptions'))]
