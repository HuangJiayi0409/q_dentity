"""Real bounded affine kernel search through the controlled subprocess."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from agent_v2.executor import normalize_result
from agent_v2.kernel_transform_frontend import core_request
from agent_v2.symbolic_methods import SymbolicAdapter,example_request,validate_request


class KernelTransformCoreTests(unittest.TestCase):
    def run_core(self,request):
        with tempfile.TemporaryDirectory() as directory:
            return normalize_result(SymbolicAdapter('kernel_transform').execute_request(
                request,Path(directory)/'attempt',30))

    def test_actual_search_finds_coordinate_inverse_and_domain_implications(self):
        result=self.run_core(core_request())
        self.assertEqual(result.status,'symbolic_constructed',result.to_dict())
        certificate=result.raw_result['construction']['constructions'][0]['certificate']
        self.assertEqual(tuple(certificate['permutation']),(1,0))
        self.assertEqual(tuple(certificate['inverse_permutation']),(1,0))
        self.assertEqual(certificate['permutations_tried'],2)
        self.assertEqual(certificate['parameter'],'N')
        self.assertEqual(len(certificate['left_index_guards']),4)
        self.assertEqual(len(certificate['right_index_guards']),4)
        self.assertEqual(result.C_partial,());self.assertFalse(result.original_identity_proved)

    def test_changed_support_or_sequence_has_no_constructed_certificate(self):
        for field in ('support','factor'):
            request=core_request()
            if field=='support':request['input']['right_domain'][3]=[1,-1,0,-1]
            else:request['input']['right_factors'][2]['index']=[1,-1,0,1]
            result=self.run_core(request)
            self.assertEqual(result.status,'incomplete',result.to_dict())
            self.assertEqual(result.sigma.code,'search_exhausted');self.assertEqual(result.C_partial,())

    def test_insufficient_multiplier_search_bound_is_honest_exhaustion(self):
        request=core_request();request['input']['max_multiplier']=1
        result=self.run_core(request)
        self.assertEqual(result.status,'incomplete',result.to_dict())
        self.assertEqual(result.sigma.code,'search_exhausted')

    def test_malformed_or_unbounded_affine_requests_are_rejected(self):
        for key,value in [('coordinates',True),('coordinates',3),('max_multiplier',3),
                          ('parameter','N := 0'),('type','Field R')]:
            request=core_request();request['input'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):validate_request(request)
        for row in [[1,2,3],[True,0,0,0],[1000,0,0,0]]:
            request=core_request();request['input']['left_domain'][0]=row
            with self.subTest(row=row),self.assertRaises(ValueError):validate_request(request)

    def test_existing_explicit_inverse_stays_nonformal(self):
        result=self.run_core(example_request('kernel_transform'))
        self.assertEqual(result.status,'symbolic_constructed',result.to_dict())
        self.assertEqual(result.C_partial,());self.assertFalse(result.original_identity_proved)

    def test_worker_checks_actual_affine_helper_module_identity(self):
        import sys
        from agent_v2.symbolic_worker import construct
        construct('kernel_transform',core_request()['input'])
        # Import-environment fault only, not mathematical evidence.
        with patch.object(sys.modules['kernel_transform.triangle'],'__file__','/tmp/foreign_triangle.py'):
            with self.assertRaisesRegex(RuntimeError,'affine helper'):
                construct('kernel_transform',core_request()['input'])


if __name__=='__main__':unittest.main()
