"""Exact original finite-product source export to an evaluated difference tower."""
import importlib
import importlib.util
from dataclasses import replace
from pathlib import Path
import re
import tempfile
import unittest
from agent_v2.storage import IntegrityError,RunStore,freeze_source,load_train

class DifferenceRingFrontendTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.difference_ring_frontend'))
        self.module=importlib.import_module('agent_v2.difference_ring_frontend')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name);self.store=RunStore.create(self.root/'runs')
        self.source=load_train('FQI-SRC-FINE-2.1',self.store)
    def altered(self,text):
        path=self.root/'Changed.lean';path.write_text(text)
        return freeze_source(path,'structural_test_only',self.source.theorem,self.store)
    def front(self,source=None):return self.module.analyze_source((source or self.source).to_dict(),self.store.root)
    def test_original_context_and_symbolic_n_tower_are_exact(self):
        f=self.front();self.assertEqual(f['status'],'applicable',f)
        self.assertEqual([b['name'] for b in f['binders']],['K',None,'a','q','n','hn','h_domain'])
        self.assertEqual(f['source'],self.source.to_dict());self.assertFalse(f['adds_original_assumptions'])
        self.assertEqual(f['symbols'],{'field':'K','parameter':'a','base':'q','bound':'n','positive_bound':'hn'})
        self.assertIn('(n - 1)',f['mapping']['p']);self.assertIn('(1 ≤ n)',f['local_proposition'])
        self.assertIn('(h_domain : True)',f['step_relation'])
        self.assertEqual([h['name'] for h in f['core_request']['input']['goal']['hypotheses']],['h0'])
        from agent_v2.symbolic_methods import validate_request
        validate_request(f['core_request'])
    def test_alpha_rename_and_extra_safe_binders_are_preserved(self):
        text=self.source.declaration
        for old,new in [('K','F'),('a','z'),('q','r'),('n','m'),('hn','hpos')]:text=re.sub(r'\b'+old+r'\b',new,text)
        text=text.replace('(h_domain : True)','(h_domain : True) (extra : True) (qv2inst : ℕ)')
        f=self.front(self.altered(text));self.assertEqual(f['status'],'applicable',f)
        self.assertEqual(f['symbols']['positive_bound'],'hpos');self.assertIn('(extra : True)',f['local_proposition'])
        self.assertIn('(qv2inst : ℕ)',f['original_proposition']);self.assertIn('(z * r)',f['mapping']['aq'])
    def test_shift_bound_parameter_and_hypothesis_changes_are_rejected(self):
        for old,new in [('(n-1)','(n+1)'),('q^2','q^3'),('(1 - (a * q))','(1 + (a * q))'),
                        ('(hn : 1 ≤ n)','(hn : 0 ≤ n)'),('(hn : 1 ≤ n)','(hn : n ≤ 1)'),
                        ('(n : ℕ)','(n : ℤ)'),('[(a * q)]','[(q * a)]')]:
            with self.subTest(change=new):self.assertEqual(self.front(self.altered(self.source.declaration.replace(old,new)))['status'],'not_applicable')
    def test_unknown_commands_hypotheses_shadowing_and_imports_are_rejected(self):
        for text in [self.source.declaration+'\n#eval 1',self.source.declaration.replace('(h_domain : True)','(h_domain : q ≠ 0)'),
                     self.source.declaration.replace('(h_domain : True)','(h_domain : True) (q : K)'),
                     self.source.declaration.replace('Benchmark.Batch4Proofs','Arbitrary.Module')]:
            self.assertEqual(self.front(self.altered(text))['status'],'not_applicable')
    def test_real_mismatch_and_source_integrity(self):
        other=load_train('FQI-GAUSS-ALTERNATING',self.store);self.assertEqual(self.front(other)['status'],'not_applicable')
        for source in [replace(self.source,Gamma='True'),replace(self.source,theorem='Other.statement'),replace(self.source,proposition='True')]:
            with self.assertRaises(IntegrityError):self.front(source)
if __name__=='__main__':unittest.main()
