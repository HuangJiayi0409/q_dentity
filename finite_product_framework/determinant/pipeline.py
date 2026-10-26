"""Construct symbolic PLU/evaluation certificates; never assume the object bridge."""
from workflow import matrix_synthesis
from determinant.construct import construct
SPEC=dict(method='determinant',module='DeterminantRules',backend='determinant_certificate',
 atoms=[('Batch3Definitions.lean',['planeRows','planePi'])],
 supported=lambda r:'Matrix.det' in r['constants'],
 scope='construct symbolic PLU or division-free determinant; retain explicit structural evaluation',
 obligations=['Prove any original-object-to-determinant bridge','Construct and verify supported structural certificate for every symbolic size','Close all parameter/domain and boundary obligations'],
 stages=['elaborate determinant','compute symbolic PLU and a division-free determinant from matrix entries',
         'verify generated factorization and determinants in Lean; discharge pivot denominators only from original context',
         'use division-free reconstruction when generic pivots cannot be justified; retain explicit structural evaluation',
         'compile unchanged original theorem including any combinatorial bridge'],
 plans=[('determinant_evaluation','  determinant_evaluate\n  done')])
def prepare(source,work):return matrix_synthesis.prepare(source,work,SPEC)
def prove_source(text,source,work,env,data,budget):return matrix_synthesis.prove_source(text,source,work,env,data,budget,SPEC,construct)
