"""The product core receives a complete original finite residue product."""
import importlib
import importlib.util
from dataclasses import replace
from pathlib import Path
import re
import tempfile
import unittest
from agent_v2.storage import IntegrityError,RunStore,freeze_source,load_train


class ProductFrontendTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.product_frontend'))
        self.module=importlib.import_module('agent_v2.product_frontend')
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name);self.store=RunStore.create(self.root/'runs')
        self.source=load_train('FQI-POCHHAMMER-RESIDUES',self.store)
    def front(self,source=None):return self.module.analyze_source((source or self.source).to_dict(),self.store.root)
    def altered(self,text):
        path=self.root/'Changed.lean';path.write_text(text)
        return freeze_source(path,'structural_test_only',self.source.theorem,self.store)
    def test_original_parameters_ranges_and_positive_modulus_are_preserved(self):
        f=self.front();self.assertEqual(f['status'],'applicable',f)
        self.assertEqual(f['source'],self.source.to_dict())
        self.assertEqual([b['name'] for b in f['binders']],['K',None,'a','q','m','n','hm'])
        self.assertEqual(f['core_request']['input']['positive_parameters'],['m'])
        self.assertEqual(f['core_request']['input']['right']['bounds'],['m','n'])
        self.assertIn('(0 < m)',f['original_proposition'])
        self.assertFalse(f['bound_specialized']);self.assertFalse(f['adds_original_assumptions'])
        self.assertEqual(f['mapping']['m'],'m');self.assertEqual(f['mapping']['n'],'n')
    def test_alpha_rename_and_original_extra_binders_are_exact(self):
        expected_request=self.front()['core_request']
        text=self.source.declaration
        for old,new in [('K','F'),('a','z'),('q','r'),('m','s'),('n','t'),('j','l'),('hm','hpos')]:
            text=re.sub(r'\b'+old+r'\b',new,text)
        text=text.replace('(hpos : 0 < s)','(hpos : 0 < s) (extra : True)')
        f=self.front(self.altered(text));self.assertEqual(f['status'],'applicable',f)
        self.assertEqual(f['mapping']['m'],'s');self.assertEqual(f['mapping']['n'],'t')
        self.assertIn('(extra : True)',f['original_proposition'])
        self.assertEqual(f['core_request'],expected_request)
    def test_wrong_lengths_factors_domain_and_missing_hypothesis_are_rejected(self):
        for old,new in [('m*n','m+n'),('a*q^j','a*q^(j+1)'),('(q^m)','(q^n)'),
                        ('range m','range n'),('(hm : 0 < m)','(hm : 0 < n)'),
                        ('(hm : 0 < m)',''),('(m n : ℕ)','(m n : K)')]:
            with self.subTest(change=new):
                self.assertEqual(self.front(self.altered(self.source.declaration.replace(old,new)))['status'],'not_applicable')
    def test_unknown_commands_extra_assumptions_and_shadowing_are_rejected(self):
        for text in (self.source.declaration+'\n#eval 1',
                     self.source.declaration.replace('Benchmark.Representation','Arbitrary.Module'),
                     self.source.declaration.replace('(hm : 0 < m)','(hm : 0 < m) (q : K)'),
                     self.source.declaration.replace('(hm : 0 < m)','(hm : 0 < m) (hnz : q ≠ 0)'),
                     self.source.declaration.replace('∏ j','∏ q')):
            self.assertEqual(self.front(self.altered(text))['status'],'not_applicable')
    def test_real_mismatch_and_source_binding_errors(self):
        other=load_train('FQI-GAUSS-ALTERNATING',self.store)
        self.assertEqual(self.front(other)['status'],'not_applicable')
        for source in (replace(self.source,Gamma='True'),replace(self.source,proposition='True'),
                       replace(self.source,theorem='Other.statement')):
            with self.assertRaises(IntegrityError):self.front(source)


if __name__=='__main__':unittest.main()
