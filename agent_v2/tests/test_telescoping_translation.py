"""CAS-result translation tests; mocked constructions never count as Lean evidence."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from agent_v2.formal_frontend import analyze_source
from agent_v2.models import Candidate
from agent_v2.storage import RunStore, load_train
from agent_v2.telescoping_translation import local_proof, translate_candidate


class TelescopingTranslationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='qv2-translation-')
        self.addCleanup(self.temp.cleanup)
        self.store = RunStore.create(Path(self.temp.name))
        source = load_train('FQI-SRC-AP-3.3.9', self.store)
        self.frontend = analyze_source(source.to_dict(), self.store.root)
        self.raw = {'schema_version': 1, 'status': 'constructed', 'solver': 'q_gosper',
                    'request_sha256': hashlib.sha256(json.dumps(self.frontend['core_request'], sort_keys=True,
                                                               ensure_ascii=False).encode()).hexdigest(),
                    'original_identity_proved': False,
                    'normalized_input': {'k_shift': 'q*(1-a*X)/(1-q*X)'},
                    'result': {'status': 'constructed', 'certificate': '(X-1)/(X*a-X)'}}

    def test_constructed_result_generates_only_an_unverified_independent_candidate(self):
        result = translate_candidate(self.frontend, self.raw)
        self.assertEqual(result['status'], 'candidate_ready')
        c = Candidate.from_dict(result['candidate'])
        self.assertEqual(c.proposition, self.frontend['local_proposition'])
        self.assertEqual(c.source_sha256, self.frontend['source']['sha256'])
        self.assertEqual(c.proof_term, local_proof(self.frontend))
        self.assertEqual(c.theorem, 'AgentV2Candidate.proof')
        self.assertIsNone(c.closes)
        self.assertEqual(c.replaces, ())
        self.assertEqual(c.dependencies, ())
        self.assertFalse(result['lean_verified'])
        self.assertEqual(result['representation']['lower_shift'], 1)
        self.assertEqual(result['representation']['coefficient'], '1')

    def test_equivalent_symbolic_witness_is_accepted(self):
        self.raw['result']['certificate'] = '(1-X)/(X*(1-a))'
        self.assertEqual(translate_candidate(self.frontend, self.raw)['status'], 'candidate_ready')

    def test_nonconstructed_wrong_ratio_wrong_request_and_wrong_solver_are_pending(self):
        mutations = [lambda r: r.update(status='no_solution_in_class'),
                     lambda r: r['result'].update(certificate='1'),
                     lambda r: r.update(request_sha256='0'*64),
                     lambda r: r.update(solver='q_zeilberger'),
                     lambda r: r.update(schema_version=True),
                     lambda r: r['normalized_input'].update(k_shift='q'),
                     lambda r: r.update(original_identity_proved=True)]
        for change in mutations:
            raw = copy.deepcopy(self.raw); change(raw)
            result = translate_candidate(self.frontend, raw)
            self.assertEqual(result['status'], 'translation_pending')
            self.assertNotIn('candidate', result)

    def test_untrusted_cas_expression_never_evaluates_python_or_unbounded_arithmetic(self):
        for expression in ['__import__("os").system("false")', 'X.__class__', 'sin(X)',
                           'X**10000000', '1/0', 'a+b', 'True', '1.0', '9'*1000,
                           '+'.join(['X']*200), '(X+1)**12']:
            with self.subTest(expression=expression[:40]):
                raw = copy.deepcopy(self.raw); raw['result']['certificate'] = expression
                result = translate_candidate(self.frontend, raw)
                self.assertEqual(result['status'], 'translation_pending')
                self.assertNotIn('candidate', result)


if __name__ == '__main__':
    unittest.main()
