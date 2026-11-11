"""Independent boundary fault injection; no formal or mathematical success claims."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from agent_v2.symbolic_methods import (
    adapter, core_inventory, example_request, request_digest, validate_request,
)


class SymbolicReviewTests(unittest.TestCase):
    def fake_result(self, request, directory, payload):
        """Inject a corrupted worker result with otherwise valid provenance."""
        raw = {
            'schema_version': 1, 'method': request['method'],
            'request_sha256': request_digest(request),
            'original_identity_proved': False,
            'source_before': core_inventory(request['method']),
            'source_after': core_inventory(request['method']),
            'status': 'constructed',
        }
        raw.update(payload)
        (directory / 'construction.json').write_text(json.dumps(raw))
        return {'returncode': 0, 'timed_out': False,
                'environment_error': None, 'cleanup_survivors': []}

    def test_malformed_candidate_cannot_be_symbolic_success(self):
        request = example_request('coefficient')
        for payload in ({}, {'construction': 'not a mathematical object'},
                        {'construction': {'status': 'search_exhausted'}},
                        {'construction': {'status': 'constructed'}}):
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as tmp:
                attempt = Path(tmp) / 'attempt'
                with patch('agent_v2.symbolic_methods.run_process',
                           side_effect=lambda *args: self.fake_result(request, attempt, payload)):
                    result = adapter('coefficient').execute_request(request, attempt, 10)
                self.assertEqual(result['C_partial'], [])
                self.assertEqual(result['O_res'], [])
                self.assertFalse(result['original_identity_proved'])
                self.assertEqual(result['status'], 'integrity_error', result)

    def test_l0_methods_never_launch_worker(self):
        for method in ('product', 'noncommutative', 'combinatorial'):
            with self.subTest(method=method), tempfile.TemporaryDirectory() as tmp:
                with patch('agent_v2.symbolic_methods.run_process',
                           side_effect=AssertionError('L0 must not execute a worker')):
                    result = adapter(method).execute_request(example_request(method), Path(tmp) / 'a', 10)
                self.assertEqual(result['sigma']['code'], 'capability_unavailable')
                self.assertEqual(result['C_partial'], [])
                self.assertEqual(result['O_res'], [])

    def test_timeout_with_unreaped_process_is_environment_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            process = {'returncode': -9, 'timed_out': True,
                       'environment_error': None, 'cleanup_survivors': [1234567]}
            with patch('agent_v2.symbolic_methods.run_process', return_value=process):
                result = adapter('coefficient').execute_request(
                    example_request('coefficient'), Path(tmp) / 'a', 10)
            self.assertEqual(result['status'], 'environment_blocked', result)
            self.assertEqual(result['C_partial'], [])
            self.assertEqual(result['O_res'], [])

    def test_core_result_from_other_request_is_rejected(self):
        request = example_request('coefficient')
        with tempfile.TemporaryDirectory() as tmp:
            attempt = Path(tmp) / 'attempt'
            payload = {'request_sha256': '0' * 64,
                       'construction': {'status': 'constructed', 'residual': '0'}}
            with patch('agent_v2.symbolic_methods.run_process',
                       side_effect=lambda *args: self.fake_result(request, attempt, payload)):
                result = adapter('coefficient').execute_request(request, attempt, 10)
            self.assertEqual(result['status'], 'integrity_error')
            self.assertEqual(result['sigma']['code'], 'core_output_mismatch')

    def test_shared_atom_key_has_one_meaning(self):
        request = deepcopy(example_request('coefficient'))
        request['input']['rhs']['args'][1] = {'op': 'atom', 'key': 0, 'display': 'unrelated'}
        with self.assertRaises(ValueError):
            validate_request(request)


if __name__ == '__main__':
    unittest.main()
