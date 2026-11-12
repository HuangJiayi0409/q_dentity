"""Offline HTTP contract tests; these never call a provider."""
import json
import tempfile
import unittest
from pathlib import Path

from agent_v2.model_client import ModelClient, ModelConfig, make_model_client


class ModelClientTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.key = 'unit-test-private-token-3819'
        self.credentials = self.root / 'credential'
        self.credentials.write_text(json.dumps({'key': self.key, 'url': 'https://gateway.invalid'}))
        self.config = ModelConfig(model='configured-model', credential_path=str(self.credentials), max_calls=2)

    def tearDown(self): self.tmp.cleanup()

    def transport(self, answer=None, status=200):
        def send(endpoint, payload, headers, seconds):
            self.sent = (endpoint, payload, headers, seconds)
            return status, json.dumps(answer if answer is not None else {
                'status': 'completed', 'output': [{'type': 'message', 'content': [
                    {'type': 'output_text', 'text': '{"proof_term":"by trivial"}'}]}],
                'usage': {'input_tokens': 10, 'output_tokens': 4}}).encode()
        return send

    def call(self, client, n='a', payload=None):
        return client.generate('local_proof', payload or {'proposition': '∀ n : Nat, n = n', 'context': 'exact context'},
                               seconds=2, attempt_dir=self.root/n)

    def test_real_request_body_preserves_exact_payload_and_stores_no_auth(self):
        client = make_model_client(self.config, transport=self.transport())
        result = self.call(client)
        self.assertEqual(result['status'], 'ok'); self.assertEqual(result['content'], {'proof_term': 'by trivial'})
        self.assertEqual(result['usage'], {'input_tokens': 10, 'output_tokens': 4})
        endpoint, body, headers, seconds = self.sent
        self.assertEqual(endpoint, 'https://gateway.invalid/v1/responses')
        self.assertEqual(headers['Authorization'], 'Bearer '+self.key)
        self.assertEqual(json.loads(body['input'])['payload']['proposition'], '∀ n : Nat, n = n')
        self.assertEqual(body['model'], 'configured-model'); self.assertFalse(body['store'])
        saved = ''.join(p.read_text() for p in (self.root/'a').iterdir())
        self.assertNotIn(self.key, saved)
        self.assertIn('exact context', saved); self.assertEqual(result['model_calls'], 1)
        self.assertEqual(client.calls_used, 1)

    def test_malformed_and_failed_responses_keep_usage_and_never_prove(self):
        for i, answer in enumerate([
            {'status': 'completed', 'output': [{'type': 'message', 'content': [{'type': 'output_text', 'text': '[]'}]}]},
            {'status': 'failed', 'error': {'message': self.key}, 'usage': {'input_tokens': 5}},
            {'status': 'incomplete', 'output': [], 'usage': {'output_tokens': 3}}]):
            result = self.call(ModelClient(self.config, transport=self.transport(answer)), str(i))
            self.assertNotEqual(result['status'], 'ok'); self.assertIsNone(result['content'])
            self.assertNotIn(self.key, json.dumps(result))
        self.assertEqual(result['usage'], {'output_tokens': 3})

    def test_timeout_has_no_secret_exception_or_hidden_retry(self):
        def timeout(*args): raise TimeoutError(self.key)
        client = ModelClient(self.config, transport=timeout)
        result = self.call(client)
        self.assertEqual(result['error_code'], 'timeout'); self.assertEqual(client.calls_used, 1)
        self.assertNotIn(self.key, ''.join(p.read_text() for p in (self.root/'a').iterdir()))

    def test_call_limit_and_resume_counter_prevent_transport(self):
        client = ModelClient(self.config, transport=self.transport(), calls_used=2)
        result = self.call(client)
        self.assertEqual(result['error_code'], 'call_limit'); self.assertEqual(result['model_calls'], 0)
        self.assertFalse(hasattr(self, 'sent'))

    def test_response_secret_is_redacted_and_cannot_be_used_as_proof(self):
        answer = {'status': 'completed', 'output': [{'type': 'message', 'content': [
            {'type': 'output_text', 'text': json.dumps({'proof_term': self.key})}]}]}
        result = self.call(ModelClient(self.config, transport=self.transport(answer)))
        self.assertEqual(result['error_code'], 'secret_in_response')
        self.assertNotIn(self.key, ''.join(p.read_text() for p in (self.root/'a').iterdir()))

    def test_http_failure_sanitizes_echoed_credentials(self):
        result = self.call(ModelClient(self.config, transport=self.transport({'error': self.key}, 401)))
        self.assertEqual(result['error_code'], 'http_401'); self.assertNotIn(self.key, json.dumps(result))

    def test_prompt_containing_credential_is_rejected_before_network(self):
        client = ModelClient(self.config, transport=self.transport())
        result = self.call(client, payload={'accident': self.key})
        self.assertEqual(result['error_code'], 'secret_in_request'); self.assertEqual(client.calls_used, 0)
        self.assertFalse(hasattr(self, 'sent'))

    def test_attempt_artifacts_cannot_be_overwritten(self):
        client = ModelClient(self.config, transport=self.transport())
        self.call(client)
        with self.assertRaises(FileExistsError): self.call(client)
        self.assertEqual(client.calls_used, 1)

    def test_chat_completions_is_explicit_and_json_bound(self):
        config = ModelConfig(endpoint='https://gateway.invalid/v1/chat/completions', model='configured-model',
                             credential_path=str(self.credentials), api='chat_completions')
        response = {'choices': [{'finish_reason': 'stop', 'message': {'content': '{"proof_term":"by rfl"}'}}],
                    'usage': {'prompt_tokens': 3, 'completion_tokens': 4}}
        result = self.call(ModelClient(config, transport=self.transport(response)))
        self.assertEqual(result['content'], {'proof_term': 'by rfl'})
        self.assertEqual(self.sent[1]['response_format'], {'type': 'json_object'})

    def test_invalid_and_nonfinite_limits_never_make_requests(self):
        for limit in (0, -1, float('inf'), True):
            client = ModelClient(self.config, transport=self.transport())
            result = client.generate('proof', {}, seconds=limit, attempt_dir=self.root/str(limit))
            self.assertEqual(result['error_code'], 'invalid_seconds'); self.assertEqual(client.calls_used, 0)

    def test_real_transport_deadline_kills_a_stalled_http_worker(self):
        import time
        from unittest.mock import patch
        from agent_v2.model_client import http_post
        def stalled(*args): time.sleep(10)
        started = time.monotonic()
        with patch('agent_v2.model_client._http_worker', stalled):
            with self.assertRaises(TimeoutError):
                http_post('https://unused.invalid', {}, {}, 0.05)
        self.assertLess(time.monotonic()-started, 0.8)

    def test_escaped_response_secret_is_redacted_before_artifacts_are_saved(self):
        def send(*args):
            escaped = self.key.replace('-', r'\u002d')
            return 200, ('{"status":"failed","error":{"message":"'+escaped+'"}}').encode()
        result = self.call(ModelClient(self.config, transport=send))
        self.assertEqual(result['error_code'], 'secret_in_response')
        saved = ''.join(p.read_text() for p in (self.root/'a').iterdir())
        self.assertNotIn(self.key, saved)
        self.assertNotIn(r'\u002d', (self.root/'a'/'response.txt').read_text())

    def test_environment_credential_is_never_serialized(self):
        from unittest.mock import patch
        config = ModelConfig(endpoint='https://gateway.invalid/v1/responses', model='configured-model',
                             credential_env='UNIT_TEST_API_KEY')
        with patch.dict('os.environ', {'UNIT_TEST_API_KEY': self.key}):
            result = self.call(ModelClient(config, transport=self.transport()))
        self.assertEqual(result['status'], 'ok')
        self.assertNotIn(self.key, ''.join(p.read_text() for p in (self.root/'a').iterdir()))

    def test_overlarge_request_is_rejected_without_truncating_source(self):
        client = ModelClient(self.config, transport=self.transport())
        result = self.call(client, payload={'source': 's'*(9*1024*1024)})
        self.assertEqual(result['error_code'], 'request_too_large')
        self.assertEqual(client.calls_used, 0)

    def test_nested_generated_json_cannot_leak_escaped_credentials(self):
        content = '{"proof_term":"'+self.key.replace('-', r'\u002d')+'"}'
        answer = {'status': 'completed', 'output': [{'type': 'message', 'content': [
            {'type': 'output_text', 'text': content}]}]}
        result = self.call(ModelClient(self.config, transport=self.transport(answer)))
        self.assertEqual(result['error_code'], 'secret_in_response')
        self.assertIsNone(result['content'])
        self.assertNotIn(self.key, ''.join(p.read_text() for p in (self.root/'a').iterdir()))
        self.assertNotIn(r'\u002d', (self.root/'a'/'response.txt').read_text())

    def test_malformed_utf8_raw_response_is_retained_exactly(self):
        def send(*args): return 200, b'\xffnot-json'
        result = self.call(ModelClient(self.config, transport=send))
        self.assertEqual(result['error_code'], 'malformed_response')
        self.assertEqual((self.root/'a'/'response.txt').read_bytes(), b'\xffnot-json')

    def test_duplicate_json_fields_are_not_silently_overwritten(self):
        def send(*args):
            return 200, b'{"status":"failed","status":"completed","output":[]}'
        result = self.call(ModelClient(self.config, transport=send))
        self.assertEqual(result['error_code'], 'malformed_response')

    def test_descriptive_http_identification_is_explicit_and_recorded_without_auth(self):
        client = ModelClient(self.config, transport=self.transport())
        result = self.call(client)
        self.assertEqual(result['status'], 'ok')
        headers = self.sent[2]
        self.assertEqual(headers['User-Agent'], 'finite-q-identity-agent-v2/1.0')
        self.assertEqual(headers['Accept'], 'application/json')
        recorded = json.loads((self.root/'a'/'request.json').read_text())['headers']
        self.assertEqual(recorded['User-Agent'], headers['User-Agent'])
        self.assertEqual(recorded['Accept'], 'application/json')
        self.assertNotIn('Authorization', recorded)
        self.assertNotIn(self.key, json.dumps(recorded))

    def test_local_setup_timeout_never_counts_an_http_call(self):
        import time
        from unittest.mock import patch
        from agent_v2.model_client import _credential
        def slow_credential(config):
            time.sleep(.03)
            return 'offline-only-test-token', 'https://unused.invalid'
        client = ModelClient(self.config, transport=self.transport())
        with patch('agent_v2.model_client._credential', side_effect=slow_credential):
            result = client.generate('local_proof', {'proposition': 'True'}, seconds=.01,
                                     attempt_dir=self.root/'local_timeout')
        self.assertEqual(result['error_code'], 'timeout')
        self.assertEqual(result['model_calls'], 0)
        self.assertEqual(client.calls_used, 0)
        self.assertFalse(hasattr(self, 'sent'))
