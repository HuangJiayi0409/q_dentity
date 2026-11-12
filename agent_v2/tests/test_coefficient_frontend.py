"""Source-bound all-index product coefficient export; no proof receipt fixtures."""
from dataclasses import replace
import hashlib
import importlib
from pathlib import Path
import tempfile
import unittest

from agent_v2.storage import RunStore,freeze_source,load_train


class CoefficientFrontendTests(unittest.TestCase):
    def setUp(self):
        self.module=importlib.import_module('agent_v2.coefficient_frontend')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name);self.store=RunStore.create(self.root/'runs')
        self.source=load_train('FQI-FINITE-Q-BINOMIAL',self.store)

    def analyze(self,source=None):
        return self.module.analyze_source((source or self.source).to_dict(),self.store.root)

    def altered(self,text):
        path=self.root/'Changed.lean';path.write_text(text)
        return freeze_source(path,'structural_test_only',self.source.theorem,self.store)

    def test_actual_train_full_context_and_coefficient_slice(self):
        front=self.analyze()
        self.assertEqual(front['status'],'applicable',front)
        self.assertEqual(front['source'],self.source.to_dict())
        self.assertEqual(front['symbols'],{'field':'K','base':'q','parameter':'z','bound':'n','index':'k'})
        self.assertEqual([b['name'] for b in front['binders']],['K',None,'q','z','n'])
        self.assertEqual(front['source']['Gamma'],self.source.declaration)
        self.assertIn('∀ {K : Type u} [Field K]',front['original_proposition'])
        self.assertEqual(front['core_request']['method'],'coefficient')
        self.assertEqual(len(front['core_request']['input']['goals']),2)
        self.assertEqual(set(front['coefficient_atoms']),{'u','v','w','z0'})
        self.assertFalse(front['adds_original_assumptions'])
        self.assertTrue(front['all_natural_indices'])
        from agent_v2.symbolic_methods import validate_request
        validate_request(front['core_request'])

    def test_alpha_renaming_and_extra_original_binder_are_preserved(self):
        text=self.source.declaration.replace('(q z : K) (n : ℕ)',
            '(a b : K) (m : ℕ) (h : True)')
        text=text.replace('(-1)^k*z^k*q^(k*(k-1)/2)*gaussian q n k','(-1)^k*b^k*a^(k*(k-1)/2)*gaussian a m k')
        text=text.replace('(n+1)','(m+1)').replace('poch z q n','poch b a m')
        front=self.analyze(self.altered(text))
        self.assertEqual(front['status'],'applicable',front)
        self.assertEqual(front['symbols']['base'],'a')
        self.assertIn('(h : True)',front['original_proposition'])

    def test_real_train_mismatch_cannot_be_exported(self):
        source=load_train('FQI-GAUSS-ALTERNATING',self.store)
        self.assertEqual(self.analyze(source)['status'],'not_applicable')

    def test_changed_range_factor_exponent_or_target_are_not_the_same_profile(self):
        for old,new in [('range (n+1)','range (n+2)'),('k*(k-1)/2','k*(k+1)/2'),
                        ('poch z q n','poch q z n'),('(-1)^k','(1)^k'),
                        ('gaussian q n k','gaussian q k n')]:
            with self.subTest(change=new):
                source=self.altered(self.source.declaration.replace(old,new))
                self.assertEqual(self.analyze(source)['status'],'not_applicable')

    def test_full_consumption_unknown_hypothesis_and_source_binding(self):
        for text in [self.source.declaration+'\n#eval 1\n',
                     self.source.declaration.replace('(n : ℕ)','(n : ℕ) (h : q ≠ 0)'),
                     self.source.declaration.replace('import Benchmark.Representation','import Other.Module')]:
            self.assertEqual(self.analyze(self.altered(text))['status'],'not_applicable')
        from agent_v2.storage import IntegrityError
        for altered in (replace(self.source,Gamma='True'),replace(self.source,proposition='True'),
                        replace(self.source,theorem='Other.statement')):
            with self.subTest(source=altered.theorem),self.assertRaises(IntegrityError):self.analyze(altered)


if __name__=='__main__':unittest.main()
