"""Source contracts; no historical proof or benchmark Test inputs."""
from dataclasses import replace
from pathlib import Path
import re
import tempfile
import unittest

from agent_v2.storage import RunStore, load_train, freeze_source, IntegrityError


class RecurrenceFrontendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = RunStore.create(self.root / 'runs')
        self.source = load_train('FQI-GAUSS-ALTERNATING', self.store)

    def analyze(self, source=None):
        from agent_v2.recurrence_frontend import analyze_source
        return analyze_source((source or self.source).to_dict())

    def variant(self, text):
        path = self.root / 'variant.lean'
        path.write_text(text)
        store = RunStore.create(self.root / 'runs')
        return freeze_source(path, 'synthetic-structure-only', self.source.theorem, store)

    def test_real_train_structure_exports_only_summand_to_search(self):
        front = self.analyze()
        self.assertEqual(front['status'], 'applicable')
        self.assertEqual(front['core_request'], {'schema_version': 1, 'solver': 'q_zeilberger',
            'input': {'summand': ['mul', ['pow', -1, 'k'], ['gaussian', 'q', 'n', 'k']]}})
        self.assertIn('(m : ℕ)', front['original_proposition'])
        self.assertIn('if', front['original_proposition'])
        self.assertEqual(front['source'], self.source.to_dict())

    def test_alpha_names_and_target_change_do_not_supply_answer_to_core(self):
        text = self.source.declaration
        for old, new in [('q', 'base'), ('m', 'length'), ('j', 'index')]:
            text = re.sub(r'\b' + old + r'\b', new, text)
        text = text.replace('else 0 :=', 'else 7 :=')
        front = self.analyze(self.variant(text))
        self.assertEqual(front['status'], 'applicable')
        self.assertEqual(front['core_request'], self.analyze()['core_request'])
        self.assertIn('else 7', front['original_proposition'])

    def test_wrong_domain_unknown_command_and_unsupported_sum_reject(self):
        for text in [self.source.declaration.replace('range (m+1)', 'range (m+2)'),
                     self.source.declaration.replace('gaussian q m j', 'gaussian q (m+j) j'),
                     self.source.declaration + '\naxiom illicit : False\n']:
            with self.subTest(text=text[-80:]):
                self.assertEqual(self.analyze(self.variant(text))['status'], 'not_applicable')

    def test_context_and_claimed_original_are_immutable(self):
        for source in [replace(self.source, Gamma='True'), replace(self.source, proposition='True')]:
            with self.assertRaises(IntegrityError):
                self.analyze(source)


if __name__ == '__main__':
    unittest.main()
