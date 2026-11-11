"""Independent recurrence boundary checks; no substitute mathematical evidence."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from agent_v2.storage import RunStore, load_train, freeze_source
from agent_v2.recurrence_frontend import analyze_source
from agent_v2.recurrence_translation import translate_candidate
from agent_v2.tests.test_recurrence_translation import fixture


class RecurrenceReviewTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.store = RunStore.create(self.root / 'runs')
        self.source = load_train('FQI-GAUSS-ALTERNATING', self.store)
        self.front = analyze_source(self.source.to_dict())

    def variant(self, text):
        path = self.root / 'variant.lean'
        path.write_text(text)
        store = RunStore.create(self.root / 'runs')
        return freeze_source(path, 'independent-synthetic-source', self.source.theorem, store), store

    def test_long_left_associative_tree_is_rejected_before_recursive_typechecking(self):
        source, _ = self.variant(self.source.declaration.replace(
            'else 0 :=', 'else ' + '+'.join(['q'] * 1100) + ' :='))
        checked = analyze_source(source.to_dict())
        self.assertEqual(checked['status'], 'not_applicable')
        self.assertIn('limit', checked['reason'])

    def test_nested_unary_tree_is_rejected_before_python_recursion_failure(self):
        source, _ = self.variant(self.source.declaration.replace(
            'else 0 :=', 'else ' + '- ' * 1100 + 'q :='))
        self.assertEqual(analyze_source(source.to_dict())['status'], 'not_applicable')

    def test_same_local_type_does_not_allow_borrowing_another_source_certificate_id(self):
        from agent_v2.lean_checker import LeanChecker
        candidate = translate_candidate(self.front, fixture(self.front))['candidate']
        source, store = self.variant(self.source.declaration.replace('else 0 :=', 'else 7 :='))
        other = analyze_source(source.to_dict())
        other_candidate = translate_candidate(other, fixture(other))['candidate']
        self.assertEqual(candidate['proposition'], other_candidate['proposition'])
        self.assertNotEqual(candidate['id'], other_candidate['id'])
        request = {k: other_candidate[k] for k in ('id', 'proposition', 'proof_term', 'theorem',
                                            'source_sha256', 'dependencies')}
        request['id'] = candidate['id']
        context = {'source_sha256': source.sha256, 'source': source.to_dict(),
                   'run_dir': str(store.root), 'attempt_dir': str(store.path('check')), 'seconds': 10}
        with patch('agent_v2.math_lean_profile._verify_train') as compile_candidate:
            checked = LeanChecker().check_partial(request, context)
        compile_candidate.assert_not_called()
        self.assertEqual(checked['status'], 'integrity_error')

    def test_candidate_cannot_select_additional_lean_imports_or_proof_commands(self):
        from agent_v2.lean_checker import LeanChecker
        candidate = translate_candidate(self.front, fixture(self.front))['candidate']
        request = {k: candidate[k] for k in ('id', 'proposition', 'proof_term', 'theorem',
                                            'source_sha256', 'dependencies')}
        request['proof_term'] += '\nimport Benchmark.Representation\n'
        context = {'source_sha256': self.source.sha256, 'source': self.source.to_dict(),
                   'run_dir': str(self.store.root), 'attempt_dir': str(self.store.path('check')), 'seconds': 10}
        with patch('agent_v2.math_lean_profile._verify_train') as compile_candidate:
            checked = LeanChecker().check_partial(request, context)
        compile_candidate.assert_not_called()
        self.assertFalse(checked['accepted'])
        self.assertEqual(checked['sigma']['code'], 'unsupported_term_syntax')


if __name__ == '__main__':
    unittest.main()
