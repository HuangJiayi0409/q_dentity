"""Construct finite symbolic inverse/composition certificates and transpose sums."""
from workflow import matrix_synthesis
from kernel_transform.construct import construct
SPEC=dict(method='kernel_transform',module='KernelRules',backend='finite_kernel_certificate',
 supported=lambda r:'Finset.sum' in r['constants'],
 scope='construct finite symbolic inverse/composition from input kernels, or transpose triangular support',
 obligations=['Close kernel identity, finite support, domain and sequence-action obligations'],
 stages=['elaborate actual finite kernels','compute inverse from A or composition from A and B using exact symbolic arithmetic',
         'verify generated kernels and their original-domain bridges; sum_comm/omega verify transpose support',
         'sum linearity and kernel composition act on arbitrary sequences','compile original theorem and audit axioms'],
 plans=[('triangular_transpose','  kernel_transpose\n  done')])
def prepare(source,work):return matrix_synthesis.prepare(source,work,SPEC)
def prove_source(text,source,work,env,data,budget):return matrix_synthesis.prove_source(text,source,work,env,data,budget,SPEC,construct)
