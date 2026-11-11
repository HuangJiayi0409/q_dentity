"""Actual retained mathematics behind unverified L2 request adapters."""
from pathlib import Path
import copy
import json
import tempfile
import unittest


class SymbolicMethodsTests(unittest.TestCase):
    def test_unsafe_or_inconsistent_typed_inputs_are_rejected(self):
        from agent_v2.symbolic_methods import adapter,example_request
        malformed=[]
        for op in ([],{},None):
            request=example_request('coefficient');request['input']['lhs']['op']=op;malformed.append(request)
        request=example_request('coefficient')
        request['input']['rhs']['args'][1]={'op':'atom','key':0,'display':'different'}
        malformed.append(request)
        request=example_request('macmahon');request['input']['numerator']='__import__("os")';malformed.append(request)
        request=example_request('macmahon');request['input']['numerator']=['pow','x',1000000];malformed.append(request)
        for request in malformed:
            with self.subTest(input=request),tempfile.TemporaryDirectory() as directory:
                out=adapter(request['method']).execute_request(request,Path(directory)/'a',30)
                self.assertEqual(out['sigma']['code'],'not_applicable',out)
                self.assertFalse((Path(directory)/'a/process.json').exists())

    def test_actual_core_mathematical_failures_are_not_environment_errors(self):
        from agent_v2.symbolic_methods import adapter,example_request
        for method in ('coefficient','interpolation','difference_ring','kernel_transform','spectral','macmahon'):
            request=example_request(method)
            if method=='coefficient':request['input']['rhs']={'op':'integer','value':0}
            if method=='interpolation':request['input']['goal']['rhs']={'op':'integer','value':0}
            if method=='difference_ring':request['input']['goal']['hypotheses']=[]
            if method=='kernel_transform':request['input']['matrix']['entries'][1]=copy.deepcopy(request['input']['matrix']['entries'][0])
            if method=='spectral':request['input']['right']['entries']=copy.deepcopy(request['input']['left']['entries'])
            if method=='macmahon':request['input']['denominator_monomials']=[['pow','L',2]]
            with self.subTest(method=method),tempfile.TemporaryDirectory() as directory:
                out=adapter(method).execute_request(request,Path(directory)/'a',30)
                self.assertEqual(out['status'],'incomplete',out)
                self.assertEqual(out['sigma']['code'],'not_applicable' if method=='macmahon' else 'search_exhausted')
                self.assertEqual(out['C_partial'],[]);self.assertEqual(out['O_res'],[])

    def test_worker_timeout_differs_from_prelaunch_budget_exhaustion(self):
        from agent_v2.symbolic_methods import adapter,example_request
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            prelaunch=adapter('coefficient').execute_request(example_request('coefficient'),root/'prelaunch',0.000001)
            self.assertEqual(prelaunch['status'],'budget_exhausted')
            self.assertFalse((root/'prelaunch/process.json').exists())
            timeout=adapter('coefficient').execute_request(example_request('coefficient'),root/'worker',0.08)
            self.assertEqual(timeout['status'],'budget_exhausted')
            process=json.loads((root/'worker/process.json').read_text())
            self.assertTrue(process['timed_out'])

    def test_process_failure_output_failure_and_malformed_output_are_distinct(self):
        from unittest.mock import patch
        import json
        from agent_v2.symbolic_methods import adapter,example_request,request_digest,core_inventory
        request=example_request('coefficient')
        for case,expected in [('nonzero','core_process_failed'),('missing','core_output_missing'),
                              ('malformed','malformed_core_output'),('badversion','core_output_mismatch'),
                              ('constructed_nonzero','core_exit_mismatch')]:
            with self.subTest(case=case),tempfile.TemporaryDirectory() as directory:
                path=Path(directory)/'a'
                def fake_process(*args):
                    if case=='malformed':(path/'construction.json').write_text('{')
                    if case in ('badversion','constructed_nonzero'):
                        raw={'schema_version':True if case=='badversion' else 1,'method':'coefficient',
                             'request_sha256':request_digest(request),'original_identity_proved':False,
                             'source_before':core_inventory('coefficient'),'source_after':core_inventory('coefficient'),
                             'status':'constructed','construction':{'status':'constructed'}}
                        (path/'construction.json').write_text(json.dumps(raw))
                    return {'returncode':1 if case in ('nonzero','constructed_nonzero') else 0,
                            'timed_out':False,'environment_error':None,'cleanup_survivors':[]}
                with patch('agent_v2.symbolic_methods.run_process',side_effect=fake_process):
                    out=adapter('coefficient').execute_request(request,path,30)
                self.assertEqual(out['sigma']['code'],expected,out)

    def test_each_registered_core_has_real_execution_mismatch_and_timeout(self):
        from agent_v2.symbolic_methods import METHODS, adapter, example_request, validate_request
        from agent_v2.executor import normalize_result
        for method in METHODS:
            with self.subTest(method=method), tempfile.TemporaryDirectory() as directory:
                request=example_request(method);validate_request(request)
                outcome=normalize_result(adapter(method).execute_request(request,Path(directory)/'positive',30))
                mismatch=normalize_result(adapter(method).execute_request(dict(request,input={'unsupported':True}),Path(directory)/'mismatch',30))
                self.assertEqual(mismatch.sigma.code,'not_applicable')
                self.assertEqual(outcome.C_partial,());self.assertEqual(outcome.O_res,())
                if METHODS[method].get('level')=='L0':
                    self.assertEqual(outcome.sigma.code,'capability_unavailable')
                    self.assertFalse((Path(directory)/'positive/process.json').exists())
                    continue
                self.assertEqual(outcome.status,'symbolic_constructed',outcome.to_dict())
                self.assertEqual(outcome.C_partial,());self.assertEqual(outcome.O_res,())
                self.assertFalse(outcome.original_identity_proved)
                timeout=normalize_result(adapter(method).execute_request(request,Path(directory)/'timeout',0.000001))
                self.assertEqual(timeout.status,'budget_exhausted')
                self.assertEqual(timeout.sigma.code,'timeout')

    def test_coefficient_actual_core_and_mismatch(self):
        from agent_v2.symbolic_methods import adapter, example_request, validate_request
        from agent_v2.executor import normalize_result
        request = example_request('coefficient')
        validate_request(request)
        with tempfile.TemporaryDirectory() as directory:
            result = normalize_result(adapter('coefficient').execute_request(request, Path(directory)/'a', 30))
        self.assertEqual(result.status, 'symbolic_constructed')
        self.assertEqual(result.C_partial, ())
        self.assertEqual(result.O_res, ())
        self.assertFalse(result.original_identity_proved)
        self.assertEqual(result.raw_result['construction']['residual'], '0')
        with self.assertRaises(ValueError): validate_request(dict(request, input={'closed_by_preparation': True}))


if __name__ == '__main__':
    unittest.main()
