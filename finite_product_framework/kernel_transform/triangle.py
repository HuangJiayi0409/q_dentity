"""Bounded exact search for finite affine-domain kernel transpositions.

Rows encode a*x0+b*x1+c*N+d >= 0. N stays a symbolic parameter.
The output carries nonnegative integer row combinations for both support
implications, finite bounds and every natural sequence index. No Lean proof or
historical theorem is used by this mathematical constructor.
"""
from itertools import permutations,product

ALGORITHM='coordinate permutation with exact nonnegative affine witnesses'
FINITE_ROWS=[[1,0,0,0],[-1,0,1,0],[0,1,0,0],[0,-1,1,0]]


def _witness(rows,target,bound):
    for coefficients in product(range(bound+1),repeat=len(rows)):
        combined=[sum(c*row[j] for c,row in zip(coefficients,rows)) for j in range(4)]
        if combined==target:return list(coefficients)
    return None


def _witnesses(rows,targets,bound):
    result=[_witness(rows,target,bound) for target in targets]
    return None if any(item is None for item in result) else result


def _transport(row,permutation):return [row[permutation[0]],row[permutation[1]],row[2],row[3]]
def _factors(items):return sorted((item['sequence'],tuple(item['index'])) for item in items)


def construct(raw):
    left,right=raw['left_domain'],raw['right_domain'];bound=raw['max_multiplier']
    left_finite=_witnesses(left,FINITE_ROWS,bound);right_finite=_witnesses(right,FINITE_ROWS,bound)
    left_indices=_witnesses(left,[item['index'] for item in raw['left_factors']],bound)
    right_indices=_witnesses(right,[item['index'] for item in raw['right_factors']],bound)
    if any(value is None for value in (left_finite,right_finite,left_indices,right_indices)):return []
    for count,permutation in enumerate(permutations(range(raw['coordinates'])),1):
        transported=[_transport(row,permutation) for row in left]
        forward=_witnesses(transported,right,bound)
        backward=_witnesses(right,transported,bound)
        factors=[{'sequence':item['sequence'],'index':_transport(item['index'],permutation)}
                 for item in raw['left_factors']]
        if forward is None or backward is None or _factors(factors)!=_factors(raw['right_factors']):continue
        inverse=[permutation.index(i) for i in range(raw['coordinates'])]
        return [{'plan':'constructed_triangular_transpose',
            'certificate':{'algorithm':ALGORITHM,'parameter':raw['parameter'],'type':raw['type'],
                'coordinates':raw['coordinates'],'permutation':list(permutation),'inverse_permutation':inverse,
                'left_domain':left,'right_domain':right,'transported_left_domain':transported,
                'left_factors':raw['left_factors'],'right_factors':raw['right_factors'],
                'transported_left_factors':factors,'forward_implications':forward,'backward_implications':backward,
                'left_finite_bounds':left_finite,'right_finite_bounds':right_finite,
                'left_index_guards':left_indices,'right_index_guards':right_indices,
                'max_multiplier':bound,'permutations_tried':count,
                'bound_specialized':False,'index_arithmetic':'natural with certified nonnegative affine indices'}}]
    return []
