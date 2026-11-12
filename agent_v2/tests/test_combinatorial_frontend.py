"""Complete original finite q-binomial source and explicit unproved bridge."""
import importlib
import importlib.util
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from agent_v2.storage import IntegrityError,RunStore,freeze_source,load_train


class CombinatorialFrontendTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.combinatorial_frontend'))
        self.module=importlib.import_module('agent_v2.combinatorial_frontend')
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name);self.store=RunStore.create(self.root/'runs')
        self.source=load_train('FQI-FINITE-Q-BINOMIAL',self.store)
    def front(self,source=None):return self.module.analyze_source((source or self.source).to_dict(),self.store.root)
    def altered(self,text):
        path=self.root/'Changed.lean';path.write_text(text)
        return freeze_source(path,'structural_test_only',self.source.theorem,self.store)
    def test_real_source_preserves_sign_domain_and_pending_gaussian_bridge(self):
        f=self.front();self.assertEqual(f['status'],'applicable',f)
        self.assertEqual(f['source'],self.source.to_dict())
        self.assertEqual([b['name'] for b in f['binders']],['K',None,'q','z','n'])
        self.assertIn('∀ {K : Type u} [Field K]',f['original_proposition'])
        self.assertEqual(f['core_request']['method'],'combinatorial')
        request=f['core_request']['input']
        self.assertEqual(request['domain'],{'kind':'range','bound':'n'})
        self.assertEqual(request['selected_weight'],{'coefficient':-1,'z_power':1,'q_index_multiplier':1})
        self.assertEqual(request['rank_upper_offset'],1)
        self.assertFalse(f['gaussian_subset_bridge']['verified'])
        self.assertEqual(f['gaussian_subset_bridge']['status'],'pending')
        self.assertFalse(f['adds_original_assumptions']);self.assertFalse(f['bound_specialized'])
        self.assertIn('Finset.range',f['definition_binding']['declarations']['poch'])
    def test_alpha_renaming_and_extra_true_binder_preserve_the_complete_source(self):
        expected_request=self.front()['core_request']
        text=self.source.declaration.replace('(q z : K) (n : ℕ)','(a b : K) (m : ℕ) (h : True)')
        text=text.replace('(-1)^k*z^k*q^(k*(k-1)/2)*gaussian q n k','(-1)^k*b^k*a^(k*(k-1)/2)*gaussian a m k')
        text=text.replace('(n+1)','(m+1)').replace('poch z q n','poch b a m')
        f=self.front(self.altered(text));self.assertEqual(f['status'],'applicable',f)
        self.assertEqual(f['symbols']['base'],'a');self.assertEqual(f['symbols']['bound'],'m')
        self.assertIn('(h : True)',f['original_proposition'])
        self.assertEqual(f['core_request'],expected_request)
    def test_changed_sign_range_triangle_or_gaussian_indices_are_rejected(self):
        for old,new in [('(-1)^k','(1)^k'),('range (n+1)','range (n+2)'),
                        ('k*(k-1)/2','k*(k+1)/2'),('gaussian q n k','gaussian q k n'),
                        ('poch z q n','poch q z n')]:
            with self.subTest(change=new):
                self.assertEqual(self.front(self.altered(self.source.declaration.replace(old,new)))['status'],'not_applicable')
    def test_unknown_commands_and_unjustified_nonzero_hypothesis_are_rejected(self):
        for text in (self.source.declaration+'\n#eval 1',
                     self.source.declaration.replace('(n : ℕ)','(n : ℕ) (h : q ≠ 0)'),
                     self.source.declaration.replace('Benchmark.Representation','Other.Module')):
            self.assertEqual(self.front(self.altered(text))['status'],'not_applicable')
    def test_real_train_mismatch_and_corrupted_source_binding_are_rejected(self):
        self.assertEqual(self.front(load_train('FQI-GAUSS-ALTERNATING',self.store))['status'],'not_applicable')
        for source in (replace(self.source,Gamma='True'),replace(self.source,proposition='True'),
                       replace(self.source,theorem='Other.statement')):
            with self.assertRaises(IntegrityError):self.front(source)


if __name__=='__main__':unittest.main()
