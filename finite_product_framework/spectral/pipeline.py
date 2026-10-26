"""Automatically synthesize a weighted self-adjoint separator for a finite pairing."""
from workflow import matrix_synthesis
from spectral.construct import construct
SPEC=dict(method='spectral',module='SpectralRules',backend='finite_spectral_certificate',
 atoms=[('BatchDefinitions.lean',['regular'])],
 supported=lambda r:'Finset.sum' in r['constants'],
 scope='synthesize a weighted self-adjoint finite operator from the pairing vectors by exact linear solving',
 obligations=['Construct self-adjoint finite operator and prove eigenrelations','Close spectral separation or collision branches','For full orthogonality, prove diagonal norms and duality'],
 stages=['elaborate finite weighted pairing','solve for an unknown operator satisfying balance, A f = 0 and A g = g',
         'verify generated matrix entries and eigenrelations in the original domain without supplied spectral certificates',
         'apply proved weighted self-adjointness and spectral-separation theorem','compile original statement; no extra hypotheses'],
 plans=[])
def prepare(source,work):return matrix_synthesis.prepare(source,work,SPEC)
def prove_source(text,source,work,env,data,budget):return matrix_synthesis.prove_source(text,source,work,env,data,budget,SPEC,construct)
