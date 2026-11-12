"""Full finite triangular Source export, with exact effective Lean binders."""
import importlib
import importlib.util
import re
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from agent_v2.storage import IntegrityError,RunStore,freeze_source,load_train


class KernelTransformFrontendTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.kernel_transform_frontend'))
        self.module=importlib.import_module('agent_v2.kernel_transform_frontend')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name);self.store=RunStore.create(self.root/'runs')
        self.source=load_train('FQI-SRC-AQ-3.23',self.store)

    def front(self,source=None):return self.module.analyze_source((source or self.source).to_dict(),self.store.root)

    def altered(self,text):
        path=self.root/'Changed.lean';path.write_text(text)
        return freeze_source(path,'structural_test_only',self.source.theorem,self.store)

    def test_actual_source_keeps_arbitrary_commring_and_both_finite_supports(self):
        front=self.front();self.assertEqual(front['status'],'applicable',front)
        self.assertEqual([b['name'] for b in front['binders']],['R',None,'N','alpha','delta','u','v'])
        self.assertEqual(front['source'],self.source.to_dict())
        self.assertEqual(front['ambient_context'][0]['name'],'K')
        self.assertIn('[CommRing R]',front['original_proposition'])
        self.assertNotIn('[Field',front['original_proposition'])
        self.assertIn('Finset.Icc',front['local_proposition'])
        self.assertIn('(r - n)',front['local_proposition'])
        self.assertFalse(front['specializes_bound'])
        self.assertEqual(front['core_request']['input']['coordinates'],2)

    def test_alpha_rename_all_parameters_and_indices_and_unused_original_binder(self):
        text=self.source.declaration
        for old,new in [('K','L'),('R','S'),('N','M'),('alpha','a'),('delta','d'),('u','f'),('v','g'),('n','i'),('r','j')]:
            text=re.sub(r'\b'+old+r'\b',new,text)
        text=text.replace('(a d f g : ℕ → S)','(a d f g : ℕ → S) (extra : True)')
        front=self.front(self.altered(text));self.assertEqual(front['status'],'applicable',front)
        self.assertEqual(front['symbols']['ring'],'S');self.assertEqual(front['symbols']['bound'],'M')
        self.assertIn('(extra : True)',front['original_proposition'])
        self.assertIn('(j - i)',front['local_proposition'])

    def test_changed_domains_weights_and_sequence_types_rejected(self):
        for old,new in [('Finset.Icc n N','Finset.Icc r N'),('Finset.range (r+1)','Finset.range (N+1)'),
                         ('u (r-n)','u (n-r)'),('v (r+n)','v (r-n)'),
                         ('alpha n *','delta n *'),('[CommRing R]','[Field R]'),('(N : ℕ)','(N : ℤ)')]:
            with self.subTest(change=new):
                self.assertNotEqual(self.source.declaration.replace(old,new),self.source.declaration)
                self.assertEqual(self.front(self.altered(self.source.declaration.replace(old,new)))['status'],'not_applicable')

    def test_trailing_commands_unknown_hypotheses_and_shadowing_rejected(self):
        for text in [self.source.declaration+'\n#eval 1',
                     self.source.declaration.replace(' :\n (∑',' (h : False) :\n (∑'),
                     self.source.declaration.replace('∑ n ∈','∑ N ∈'),
                     self.source.declaration.replace('import Benchmark.Batch4Proofs','import Other')]:
            self.assertEqual(self.front(self.altered(text))['status'],'not_applicable')

    def test_source_integrity_and_real_mismatch(self):
        for source in [replace(self.source,Gamma='True'),replace(self.source,proposition='True'),
                       replace(self.source,theorem='Other.statement')]:
            with self.assertRaises(IntegrityError):self.front(source)
        other=load_train('FQI-GAUSS-ALTERNATING',self.store)
        self.assertEqual(self.front(other)['status'],'not_applicable')


if __name__=='__main__':unittest.main()
