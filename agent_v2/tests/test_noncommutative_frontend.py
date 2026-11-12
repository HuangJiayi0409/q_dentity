"""Source semantics, complete hypotheses and ordered operator roles."""
import importlib
import importlib.util
from dataclasses import replace
from pathlib import Path
import re
import tempfile
import unittest
from agent_v2.storage import IntegrityError,RunStore,freeze_source,load_train


class NoncommutativeFrontendTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.noncommutative_frontend'))
        self.module=importlib.import_module('agent_v2.noncommutative_frontend')
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name);self.store=RunStore.create(self.root/'runs')
        self.source=load_train('FQI-SRC-KAC-CHEUNG-5.7',self.store)
    def front(self,source=None):return self.module.analyze_source((source or self.source).to_dict(),self.store.root)
    def altered(self,text):
        path=self.root/'Changed.lean';path.write_text(text)
        return freeze_source(path,'structural_test_only',self.source.theorem,self.store)
    def test_full_source_has_ordered_actions_and_all_original_hypotheses(self):
        f=self.front();self.assertEqual(f['status'],'applicable',f)
        self.assertEqual(f['source'],self.source.to_dict())
        self.assertEqual([b['name'] for b in f['binders']],['K',None,'q','f','hq','hq1'])
        self.assertIn('(hq : (q ≠ 0))',f['original_proposition'])
        self.assertIn('(hq1 : (q ≠ 1))',f['original_proposition'])
        self.assertEqual(f['core_request']['input']['lhs'][0]['word'],['M','X'])
        self.assertEqual(f['core_request']['input']['rhs'][0]['word'],['X','M'])
        self.assertEqual(f['core_request']['input']['rhs'][0]['q_power'],1)
        self.assertFalse(f['degree_specialized']);self.assertFalse(f['adds_original_assumptions'])
        self.assertTrue(f['mapping']['arbitrary_polynomial'])
        self.assertIn('f.comp',f['definition_binding']['declarations']['kacM'])
    def test_alpha_rename_and_extra_true_parameter_preserve_the_full_proposition(self):
        expected_request=self.front()['core_request']
        text=self.source.declaration
        for old,new in [('K','F'),('q','r'),('f','p'),('hq','hnz'),('hq1','hne')]:
            text=re.sub(r'\b'+old+r'\b',new,text)
        text=text.replace('(hne : r ≠ 1)','(hne : r ≠ 1) (extra : True)')
        f=self.front(self.altered(text));self.assertEqual(f['status'],'applicable',f)
        self.assertEqual(f['symbols']['field'],'F');self.assertEqual(f['symbols']['polynomial'],'p')
        self.assertIn('(extra : True)',f['original_proposition'])
        self.assertEqual(f['core_request'],expected_request)
    def test_wrong_order_scalar_carrier_and_missing_original_hypothesis_are_rejected(self):
        for old,new in [('kacM q (kacX f)','kacX (kacM q f)'),('q • kacX','1 • kacX'),
                        ('(f : Polynomial K)','(f : K)'),('(hq : q ≠ 0)',''),
                        ('(hq1 : q ≠ 1)','(hq1 : q ≠ 0)'),('kacM q (kacX f)','kacM q f')]:
            with self.subTest(change=new):
                self.assertEqual(self.front(self.altered(self.source.declaration.replace(old,new)))['status'],'not_applicable')
    def test_unknown_commands_and_assumed_target_relation_are_rejected(self):
        for text in (self.source.declaration+'\n#eval 1',
                     self.source.declaration.replace('Benchmark.Batch5Proofs','Arbitrary.Module'),
                     self.source.declaration.replace('(hq1 : q ≠ 1)','(hq1 : q ≠ 1) (q : K)'),
                     self.source.declaration.replace('(hq1 : q ≠ 1)','(hq1 : q ≠ 1) (assumed : kacM q (kacX f) = q • kacX (kacM q f))')):
            self.assertEqual(self.front(self.altered(text))['status'],'not_applicable')
    def test_reverse_equality_is_bound_and_retains_original_orientation(self):
        original='kacM q (kacX f) = q • kacX (kacM q f)'
        source=self.altered(self.source.declaration.replace(original,'q • kacX (kacM q f) = kacM q (kacX f)'))
        f=self.front(source);self.assertEqual(f['status'],'applicable',f)
        self.assertEqual(f['orientation'],'scalar_XM_equals_MX')
        self.assertEqual(f['core_request']['input']['lhs'][0]['word'],['X','M'])
    def test_real_mismatch_and_source_binding_corruption_are_rejected(self):
        other=load_train('FQI-GAUSS-ALTERNATING',self.store)
        self.assertEqual(self.front(other)['status'],'not_applicable')
        for source in (replace(self.source,Gamma='True'),replace(self.source,proposition='True'),
                       replace(self.source,theorem='Other.statement')):
            with self.assertRaises(IntegrityError):self.front(source)


if __name__=='__main__':unittest.main()
