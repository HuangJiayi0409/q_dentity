"""Finite grammar tests; only two named Train sources are read, never solved here."""
from dataclasses import replace
import hashlib
from pathlib import Path
import tempfile
import unittest

from agent_v2.formal_frontend import analyze_source
from agent_v2.storage import IntegrityError, RunStore, freeze_source, load_train


class FormalFrontendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='qv2-frontend-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = RunStore.create(self.root, 'selected')
        self.source = load_train('FQI-SRC-AP-3.3.9', self.store)

    def altered(self, text, name='variant'):
        path = self.root / (name + '.lean')
        path.write_text(text)
        store = RunStore.create(self.root, name)
        return freeze_source(path, 'STRUCTURAL-VARIANT', self.source.theorem, store)

    def test_selected_train_is_recognized_with_exact_original_context(self):
        f = analyze_source(self.source.to_dict(), self.store.root)
        self.assertEqual(f['status'], 'applicable')
        self.assertEqual(f['profile'], 'gaussian_weighted_range_v1')
        self.assertEqual(f['source']['sha256'], self.source.sha256)
        self.assertEqual(f['source']['declaration'], self.source.declaration)
        self.assertEqual(f['context']['raw'], self.source.Gamma)
        self.assertEqual([b['name'] for b in f['binders']], ['K', None, 'q', 'm', 'n', 'h_domain'])
        self.assertIn('Type u', f['local_proposition'])
        self.assertIn('(n : ℕ)', f['local_proposition'])
        self.assertIn('(h_domain : True)', f['local_proposition'])
        self.assertNotIn('≠', f['local_proposition'])
        self.assertEqual(f['summation']['range']['op'], 'Finset.range')
        self.assertEqual(f['summation']['index'], 'j')
        self.assertEqual(f['mapping']['X']['lean'], 'q ^ j')
        self.assertEqual(f['core_request']['solver'], 'q_gosper')

    def test_real_train_with_different_structure_is_not_applicable(self):
        store = RunStore.create(self.root, 'different')
        other = load_train('FQI-FINITE-Q-BINOMIAL', store)
        self.assertEqual(analyze_source(other.to_dict(), store.root)['status'], 'not_applicable')

    def test_matching_is_by_structure_and_preserves_alpha_renamed_binders(self):
        import re
        text = self.source.declaration
        for old, new in [('q', 'base'), ('m', 'offset'), ('n', 'bound'), ('j', 'index'), ('h_domain', 'hcontext')]:
            text = re.sub(r'\b' + old + r'\b', new, text)
        source = self.altered(text)
        f = analyze_source(source.to_dict())
        self.assertEqual(f['status'], 'applicable')
        self.assertEqual(f['symbols']['base'], 'base')
        self.assertIn('(bound : ℕ)', f['local_proposition'])
        self.assertIn('(hcontext : True)', f['local_proposition'])
        self.assertEqual(f['source']['identity'], 'STRUCTURAL-VARIANT')

    def test_unknown_hypothesis_is_rejected_without_dropping_it(self):
        source = self.altered(self.source.declaration.replace('(h_domain : True)', '(h_domain : q ≠ 0)'))
        self.assertEqual(analyze_source(source.to_dict())['status'], 'not_applicable')

    def test_unsupported_domains_ranges_and_extra_commands_are_rejected(self):
        for i, (old, new) in enumerate([
            ('[Field K]', '[CommRing K]'), ('(n+1)', '(n-1)'),
            ('(m+j)', '(m-j)'), ('(m n : ℕ)', '(m n : ℤ)'),
            ('end FiniteQBenchmark.Identity272', 'end FiniteQBenchmark.Identity272\naxiom hidden : False'),
        ]):
            with self.subTest(new=new):
                source = self.altered(self.source.declaration.replace(old, new), 'variant'+str(i))
                self.assertEqual(analyze_source(source.to_dict())['status'], 'not_applicable')

    def test_snapshot_source_declaration_and_context_are_bound(self):
        with self.assertRaises(IntegrityError):
            analyze_source(replace(self.source, sha256='0'*64).to_dict())
        with self.assertRaises(IntegrityError):
            analyze_source(replace(self.source, Gamma='True').to_dict())
        Path(self.source.snapshot_path).write_text('changed')
        with self.assertRaises(IntegrityError):
            analyze_source(self.source.to_dict(), self.store.root)

    def test_original_proposition_rebinding_is_rejected(self):
        with self.assertRaises(IntegrityError):
            analyze_source(replace(self.source, proposition='True').to_dict())

    def test_nested_comments_are_ignored_but_incomplete_comments_are_rejected(self):
        text = self.source.declaration.replace('theorem statement', '/- outer /- inner -/ outer -/ theorem statement')
        source = self.altered(text)
        self.assertEqual(analyze_source(source.to_dict())['status'], 'applicable')
        broken = self.altered(text+'\n/- unfinished', 'broken')
        self.assertEqual(analyze_source(broken.to_dict())['status'], 'not_applicable')

    def test_deep_or_extra_expression_syntax_fails_closed(self):
        for i, replacement in enumerate(['('*100+'q'+')'*100, '(q : K)', 'q + q', '+'.join(['q']*100)]):
            source = self.altered(self.source.declaration.replace('((q^j)', '(('+replacement+'^j)'), 'deep'+str(i))
            self.assertEqual(analyze_source(source.to_dict())['status'], 'not_applicable')


if __name__ == '__main__':
    unittest.main()
