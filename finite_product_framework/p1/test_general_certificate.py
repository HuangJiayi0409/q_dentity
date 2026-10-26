"""Independent residual checks for nonzero lifted Ore certificates."""
import unittest
import sympy as s
from general_summation import lift,validate_local,construct
from expressions import n,k,q,Q,X,Poch
from core import CoreBudget
from run import construct_in_process

class CertificateTests(unittest.TestCase):
    def test_parameterized_nonzero_flux_lift(self):
        a=s.Symbol('a');F=Poch(a,q,k)*q**(n*k)
        c=[Q-1,-a*Q];R=[s.S.One]
        validate_local([F],c,R)
        lifted=lift(c,R,[F],[Q+1,s.S.One])
        self.assertEqual(s.cancel(lifted[0]-(Q+1+X)),0)
        common=[Q**2-1,-a*Q*(Q+1)+q*Q-1,-a*q*Q]
        validate_local([F],common,lifted)
        with self.assertRaisesRegex(ValueError,'local telescoper residual'):
            validate_local([F],common,[lifted[0]+1])

    def test_rational_nonzero_flux_lift(self):
        F=q**(n*k);R=[X/(q*Q-1)]
        lifted=lift([0,1],R,[F],[Q,s.S.One])
        validate_local([F],[0,Q,1],lifted)
        with self.assertRaisesRegex(ValueError,'component count'):
            validate_local([F],[0,Q,1],[])

    def test_mode_cannot_cross_methods(self):
        with self.assertRaisesRegex(ValueError,'does not match method'):
            construct_in_process({'mode':'general_recurrence'},CoreBudget(),'direct_q_gosper')

    def test_proof_hint_rejected(self):
        problem=dict(schema_version=1,source_id='synthetic',mode='general_recurrence',sides=[],certificate='1')
        with self.assertRaisesRegex(ValueError,'invalid_problem'):
            construct(problem,CoreBudget())

if __name__=='__main__':unittest.main()
