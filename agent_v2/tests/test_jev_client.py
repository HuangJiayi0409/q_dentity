"""Offline TypeSafe Choice contract tests; no live scores are asserted."""
import json
import tempfile
import unittest
from pathlib import Path

from agent_v2.jev_client import JevConfig, JevSelector, JevUnavailable
from agent_v2.models import Budget, JointAction, Source, initial_state


class JevSelectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.key = 'jev-private-unit-test-key-932'
        credentials = self.root/'credential'; credentials.write_text(self.key)
        self.config = JevConfig(credential_path=str(credentials), max_calls=1)
        source = Source('synthetic', 'source.lean', 'source.lean', 'a'*64, 'demo',
                        'theorem demo : True := by sorry', 'exact context', 'True')
        self.state, _ = initial_state(source, Budget(100, 5))
        self.actions = (JointAction('cas_product', 'identity', 'original', 'original', 'CAS', 'product', {}),
                        JointAction('local_proof', 'identity', 'original', 'original', 'LLM', 'local', {}))

    def tearDown(self): self.tmp.cleanup()

    def transport(self, choice='local_proof', confidence=0.7, probabilities=None):
        def send(endpoint, payload, headers, seconds):
            self.sent = payload
            return 200, json.dumps({'model': 'jev-live', 'answers': {'compatible_route': {
                'type': 'choice', 'choice': choice, 'confidence': confidence,
                'probabilities': probabilities or {'cas_product': 0.2, 'local_proof': 0.8}}},
                'usage': {'input_tokens': 34, 'output_tokens': 12}}).encode()
        return send

    def test_choice_bound_to_exact_legal_ids_and_real_confidence(self):
        selector = JevSelector(self.config, attempt_root=self.root/'attempts', transport=self.transport())
        result = selector(self.state, self.actions)
        self.assertEqual(result, {'route_id': 'local_proof', 'confidence': 0.7, 'rationale': ''})
        self.assertEqual(self.sent['state']['residual']['G']['proposition'], 'True')
        self.assertEqual(self.sent['state']['residual']['O'][0]['proposition'], 'True')
        self.assertNotIn('Gamma', self.sent['state']['residual'])
        self.assertNotIn('snapshot_path', json.dumps(self.sent))
        self.assertNotIn('theorem demo', json.dumps(self.sent))
        self.assertEqual(set(self.sent['questions']['compatible_route']['criteria']), {'cas_product', 'local_proof'})
        self.assertEqual(selector.last_result['usage'], {'input_tokens': 34, 'output_tokens': 12})
        self.assertEqual(selector.calls_used, 1)
        for p in (self.root/'attempts').rglob('*'):
            if p.is_file(): self.assertNotIn(self.key, p.read_text())

    def test_foreign_choice_and_foreign_probability_ids_are_rejected(self):
        for i, transport in enumerate((self.transport(choice='foreign'),
                                       self.transport(probabilities={'foreign': 0.2, 'local_proof': 0.8}))):
            selector = JevSelector(self.config, attempt_root=self.root/str(i), transport=transport)
            with self.assertRaises(JevUnavailable): selector(self.state, self.actions)
            self.assertIsNone(selector.last_result['content'])
            self.assertEqual(selector.last_result['model_calls'], 1)

    def test_missing_or_invalid_confidence_is_not_invented(self):
        for i, value in enumerate((None, '0.9', -0.1, 1.1, float('nan'), True)):
            selector = JevSelector(self.config, attempt_root=self.root/str(i), transport=self.transport(confidence=value))
            with self.assertRaises(JevUnavailable): selector(self.state, self.actions)

    def test_no_hidden_fallback_or_call_when_limit_reached(self):
        selector = JevSelector(self.config, attempt_root=self.root/'attempts', transport=self.transport(), calls_used=1)
        with self.assertRaises(JevUnavailable): selector(self.state, self.actions)
        self.assertEqual(selector.last_result['error_code'], 'call_limit')
        self.assertEqual(selector.last_result['model_calls'], 0)
        self.assertFalse(hasattr(self, 'sent'))

    def test_duplicate_ids_are_rejected_before_api(self):
        selector = JevSelector(self.config, attempt_root=self.root/'attempts', transport=self.transport())
        with self.assertRaises(JevUnavailable): selector(self.state, [self.actions[0], self.actions[0]])
        self.assertEqual(selector.calls_used, 0)
        self.assertFalse(hasattr(self, 'sent'))

    def test_timeout_is_unavailable_and_is_a_real_attempt(self):
        def timeout(*args): raise TimeoutError(self.key)
        selector = JevSelector(self.config, attempt_root=self.root/'attempts', transport=timeout)
        with self.assertRaises(JevUnavailable): selector(self.state, self.actions)
        self.assertEqual(selector.last_result['error_code'], 'timeout')
        self.assertEqual(selector.calls_used, 1)
