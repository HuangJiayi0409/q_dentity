"""Real Lean declaration lookup; never import benchmark solution modules."""
import hashlib
from pathlib import Path
import unittest

from agent_v2.library import LocalLibrary


class LocalLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.library = LocalLibrary()

    def test_actual_foundation_declaration_has_closed_type_and_current_provenance(self):
        record = self.library.lookup('And.intro')
        self.assertEqual(record['name'], 'And.intro')
        self.assertIn('Prop', record['type']); self.assertIn('→', record['type'])
        provenance = record['provenance']
        self.assertEqual(provenance['kind'], 'foundation')
        path = Path(provenance['path']); self.assertTrue(path.is_file())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), provenance['sha256'])
        self.assertNotIn('proof', record)

    def test_actual_mathlib_range_lemma_is_available_without_historical_proofs(self):
        record = self.library.lookup('Finset.prod_range_add')
        self.assertIn('CommMonoid', record['type'])
        self.assertEqual(record['provenance']['kind'], 'mathlib')
        self.assertTrue(record['provenance']['path'].endswith('Mathlib/Algebra/BigOperators/Group/Finset/Basic.lean'))
        self.assertNotIn(':=', record['type'])

    def test_allowlist_rejects_unknown_target_identity_and_command_text(self):
        for name in ('FiniteQBenchmark.identity', 'FQI-POCHHAMMER-RESIDUES', '#eval IO.println "bad"',
                     'agent_v2.generated.old.proof', 'Benchmark.Test'):
            self.assertIsNone(self.library.lookup(name))

    def test_query_is_bounded_and_types_are_searchable(self):
        records = self.library.query('range', limit=3)
        self.assertEqual(len(records), 3)
        self.assertTrue(all('range' in (r['name']+' '+r['type']).lower() for r in records))
        self.assertEqual(self.library.query('unfindable_identifier_392'), [])
        for limit in (0, 33, True):
            with self.assertRaises(ValueError): self.library.query('', limit=limit)

    def test_results_cannot_mutate_subsequent_library_answers(self):
        record = self.library.lookup('And.intro'); record['type'] = 'False'
        self.assertNotEqual(self.library.lookup('And.intro')['type'], 'False')

    def test_requested_pure_foundations_and_telescoping_types_are_available(self):
        for name in ('Finset.sum_range_sub', 'Finset.sum_range_sub\'', 'Finset.sum_congr',
                     'Nat.twoStepInduction', 'Nat.strong_induction_on', 'pow_add', 'pow_mul', 'Eq.symm',
                     'FiniteQP1.gaussian_pascal', 'FiniteQP1.gaussian_adjacent',
                     'FiniteQBenchmark.gaussian_above', 'FiniteQBenchmark.gaussian_zero_right',
                     'FiniteQBenchmark.poch_succ'):
            with self.subTest(name=name):
                record = self.library.lookup(name)
                self.assertIsNotNone(record)
                self.assertEqual(record['name'], name)
                self.assertTrue(record['type'])
                self.assertNotIn(':=', record['type'])
                self.assertNotIn('Train', record['provenance']['path'])
                self.assertNotIn('generated', record['provenance']['path'])
