"""Construct the inverse from A alone, then bridge it to the target's B."""
import sympy as s
from workflow.matrix_symbolic import ScalarCodec, checked_zero, matrix_record, scalar_finish
from kernel_transform.triangle import construct as construct_triangle


def construct(raw):
    if raw.get('operation') == 'triangular_transpose':
        return construct_triangle(raw)
    codec = ScalarCodec()
    a = codec.matrix(raw['matrix'])
    if raw.get('operation') == 'composition':
        return composition(raw, codec, a)
    # The proposed inverse and the target value are deliberately NOT solver inputs.
    b = a.inv(method='DM').applyfunc(s.cancel)
    checked_zero(a*b - s.eye(a.rows))
    candidate = codec.matrix_lean(b, raw['type'])
    proposed = raw['proposed_inverse']['display']
    matrix = raw['matrix']['display']
    vector = raw['vector']
    n, ty = raw['size'], raw['type']
    finish = scalar_finish()
    script = f'''  classical
  let synthInverse : Matrix (Fin {n}) (Fin {n}) ({ty}) := {candidate}
  have synthIdentity : ∀ i j, ∑ k, ({matrix}) i k * synthInverse k j =
      if i = j then 1 else 0 := by
    intro i j
    fin_cases i <;> fin_cases j <;> simp [synthInverse, Fin.sum_univ_succ] <;> ({finish})
  have synthBridge : ({proposed}) = synthInverse := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [synthInverse] <;> ({finish})
  change (fun i => ∑ k, ({matrix}) i k * ∑ j, ({proposed}) k j * ({vector}) j) = ({vector})
  rw [synthBridge]
  exact FiniteQKernel.inverse_action ({matrix}) synthInverse ({vector}) synthIdentity
'''
    return [dict(plan='constructed_rational_inverse', proof_script=script,
                 certificate=dict(algorithm='exact symbolic matrix inversion',
                    constructor_inputs=['left kernel A'], target_inverse_used_in_search=False,
                    matrix=matrix_record(a), inverse=matrix_record(b),
                    atoms=codec.atoms, dimension=n,
                    domain_policy='all inverse denominators verified in original Lean context'))]


def composition(raw, codec, a):
    b = codec.matrix(raw['proposed_inverse'])
    c = (a*b).applyfunc(s.cancel)
    candidate = codec.matrix_lean(c, raw['type'])
    left, right = raw['matrix']['display'], raw['proposed_inverse']['display']
    target, vector = raw['target_kernel']['display'], raw['vector']
    n, ty, finish = raw['size'], raw['type'], scalar_finish()
    script = f'''  classical
  let synthComposition : Matrix (Fin {n}) (Fin {n}) ({ty}) := {candidate}
  have synthIdentity : ∀ i j, ∑ k, ({left}) i k * ({right}) k j = synthComposition i j := by
    intro i j
    fin_cases i <;> fin_cases j <;> simp [synthComposition, Fin.sum_univ_succ] <;> ({finish})
  have synthBridge : ({target}) = synthComposition := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [synthComposition] <;> ({finish})
  change (fun i => ∑ k, ({left}) i k * ∑ j, ({right}) k j * ({vector}) j) =
    (fun i => ∑ j, ({target}) i j * ({vector}) j)
  rw [synthBridge]
  exact FiniteQKernel.compose_action ({left}) ({right}) synthComposition ({vector}) synthIdentity
'''
    return [dict(plan='constructed_kernel_composition',proof_script=script,
        certificate=dict(algorithm='exact symbolic kernel multiplication',
            constructor_inputs=['left kernel A','right kernel B'],target_kernel_used_in_search=False,
            left=matrix_record(a),right=matrix_record(b),composition=matrix_record(c),
            atoms=codec.atoms,dimension=n))]
