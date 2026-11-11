"""Symbolic fixtures test translation boundaries, never count as CAS evidence."""
from dataclasses import replace
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from agent_v2.storage import RunStore, load_train
from agent_v2.recurrence_frontend import analyze_source


def fixture(front):
    return {'schema_version': 1, 'solver': 'q_zeilberger', 'status': 'constructed',
        'request_sha256': hashlib.sha256(json.dumps(front['core_request'], sort_keys=True,
                                                   ensure_ascii=False).encode()).hexdigest(),
        'normalized_input': {'k_shift': '(-Q + X)/(X**2*q-X)',
                             'n_shift': '(Q*X*q-X)/(Q*q-X)'},
        'result': {'status': 'constructed', 'order': 2, 'coefficients': ['Q*q-1', '0', '1'],
            'certificate': '(-Q**2*X**2*q**3+Q**2*X*q**3+Q*X**2*q**2-Q*X*q**2)/(Q**2*q**3-Q*X*q**2-Q*X*q+X**2)'},
        'original_identity_proved': False, 'unit_test_fixture': True}


class RecurrenceTranslationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = RunStore.create(Path(self.temp.name) / 'runs')
        self.source = load_train('FQI-GAUSS-ALTERNATING', self.store)
        self.front = analyze_source(self.source.to_dict())

    def translate(self, raw):
        from agent_v2.recurrence_translation import translate_candidate
        return translate_candidate(self.front, raw)

    def test_bound_recurrence_becomes_only_one_unverified_local_candidate(self):
        from agent_v2.models import Candidate
        output = self.translate(fixture(self.front))
        self.assertEqual(output['status'], 'candidate_ready', output)
        candidate = Candidate.from_dict(output['candidate'])
        self.assertIsNone(candidate.closes)
        self.assertEqual(candidate.replaces, ())
        self.assertIn('m + 2', candidate.proposition)
        self.assertNotIn('q ≠ 0', candidate.proposition)
        self.assertFalse(output['lean_verified'])
        self.assertEqual(output['certificate']['order'], 2)

    def test_bad_binding_wrong_ratio_and_corrupt_witness_remain_untranslated(self):
        raw = fixture(self.front)
        cases = [dict(raw, request_sha256='0'*64), dict(raw, solver='q_gosper')]
        for path, value in [('certificate', '0'), ('coefficients', ['1', '0', '1']), ('order', 3)]:
            other = copy.deepcopy(raw); other['result'][path] = value; cases.append(other)
        other = copy.deepcopy(raw); other['normalized_input']['n_shift'] = '1'; cases.append(other)
        for bad in cases:
            with self.subTest(raw=bad):
                self.assertEqual(self.translate(bad)['status'], 'translation_pending')

    def test_reconstruction_is_source_and_exact_template_bound(self):
        from agent_v2.recurrence_translation import reconstruct_candidate
        output = self.translate(fixture(self.front))
        c = output['candidate']
        rebuilt = reconstruct_candidate(self.front, c['proof_term'])
        self.assertEqual(rebuilt.to_dict(), c)
        with self.assertRaises(ValueError):
            reconstruct_candidate(self.front, c['proof_term'].replace('linear_combination h', 'exact False.elim (by sorry)'))

    def test_arithmetic_decoder_does_not_evaluate_code_or_unbounded_powers(self):
        from agent_v2.recurrence_translation import read_rational
        for text in ["__import__('os').system('true')", 'q**1000000', 'x', 'a', '1/0', 'Q.__class__']:
            with self.subTest(text=text), self.assertRaises((ValueError, SyntaxError)):
                read_rational(text)


if __name__ == '__main__': unittest.main()
