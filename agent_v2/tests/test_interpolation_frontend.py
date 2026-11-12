"""A fully consumed source contract, including integer powers and hypotheses."""
import importlib
import importlib.util
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from agent_v2.storage import IntegrityError, RunStore, freeze_source, load_train


class InterpolationFrontendTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.interpolation_frontend'),
                             'source interpolation frontend is absent')
        self.module = importlib.import_module('agent_v2.interpolation_frontend')
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name); self.store = RunStore.create(self.root / 'runs')
        self.source = load_train('FQI-SRC-GR2-I-20', self.store)

    def altered(self, text):
        path = self.root / 'Changed.lean'; path.write_text(text)
        return freeze_source(path, 'structural_test_only', self.source.theorem, self.store)

    def front(self, source=None):
        return self.module.analyze_source((source or self.source).to_dict(), self.store.root)

    def test_real_source_preserves_order_domain_and_integer_exponent(self):
        front = self.front(); self.assertEqual(front['status'], 'applicable', front)
        self.assertEqual([b['name'] for b in front['binders']],
                         ['K', None, 'a', 'q', 'n', 'k', 'hbase', 'hk', 'ha', 'h_domain'])
        self.assertEqual(front['source'], self.source.to_dict())
        self.assertIn('FiniteQBenchmark.regular q', front['original_proposition'])
        self.assertIn('FiniteQBenchmark.pochList [a] q k', front['original_proposition'])
        self.assertIn('((k : ℤ) : ℤ)', front['original_proposition'])
        self.assertEqual(front['core_request']['input']['max_degree'], 1)
        self.assertIs(front['core_request']['input']['goal']['char_zero'], False)
        self.assertEqual(front['symbols'], {'field':'K','parameter':'a','base':'q','bound':'n','offset':'k'})
        from agent_v2.symbolic_methods import validate_request
        validate_request(front['core_request'])

    def test_alpha_names_extra_binders_and_collision_preserve_context(self):
        import re
        text = self.source.declaration
        for old, new in [('a','x'), ('q','r'), ('n','m'), ('k','t'), ('hbase','hr'), ('h_domain','hd')]:
            text = re.sub(r'\b'+old+r'\b', new, text)
        text = text.replace('(ha : x ≠ 0)', '(ha : x ≠ 0) (qv2j : ℕ) (extra : True)')
        front = self.front(self.altered(text))
        self.assertEqual(front['status'], 'applicable', front)
        self.assertEqual(front['factor_index'], 'qv2jx')
        self.assertIn('(extra : True)', front['original_proposition'])
        self.assertIn('(hr : (FiniteQBenchmark.regular r))', front['original_proposition'])

    def test_changed_power_range_denominator_or_hypothesis_is_rejected(self):
        for old, new in [('(n-k)', '(n+k)'), ('q^(((k : ℤ)) : ℤ)', 'q^(((n : ℤ)) : ℤ)'),
                         ('(hk : k ≤ n)', '(hk : n ≤ k)'), ('(ha : a ≠ 0)', '(ha : q ≠ 0)'),
                         ('(hbase : regular q)', '(hbase : regular a)'),
                         ('h_domain : (pochList [a] q (k))', 'h_domain : (pochList [a] q (n))')]:
            with self.subTest(change=new):
                self.assertEqual(self.front(self.altered(self.source.declaration.replace(old,new)))['status'], 'not_applicable')

    def test_unknown_commands_bindings_and_types_are_fully_consumed(self):
        for text in [self.source.declaration+'\n#eval 1\n',
                     self.source.declaration.replace('(ha : a ≠ 0)', '(ha : a ≠ 0) (other : q = 1)'),
                     self.source.declaration.replace('(n k : ℕ)', '(n k : ℤ)'),
                     self.source.declaration.replace('import Benchmark.Batch3Proofs','import Arbitrary'),
                     self.source.declaration.replace('(ha : a ≠ 0)', '(ha : a ≠ 0) (q : K)')]:
            self.assertEqual(self.front(self.altered(text))['status'], 'not_applicable')

    def test_mismatch_and_corrupt_source_cannot_be_exported(self):
        for source in [replace(self.source,Gamma='True'),replace(self.source,proposition='True'),
                       replace(self.source,theorem='Other.statement')]:
            with self.assertRaises(IntegrityError): self.front(source)
        other = load_train('FQI-FINITE-Q-BINOMIAL', self.store)
        self.assertEqual(self.front(other)['status'], 'not_applicable')


if __name__ == '__main__': unittest.main()
