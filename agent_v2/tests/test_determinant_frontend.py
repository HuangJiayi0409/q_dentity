"""Source matrix parsing preserves arbitrary dimension, finite indices and casts."""
import importlib
import importlib.util
import re
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from agent_v2.storage import IntegrityError,RunStore,freeze_source,load_train


class DeterminantFrontendTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.determinant_frontend'),
                             'source determinant frontend is absent')
        self.module=importlib.import_module('agent_v2.determinant_frontend')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name);self.store=RunStore.create(self.root/'runs')
        self.source=load_train('FQI-SRC-AP-11.2.4',self.store)

    def front(self,source=None):return self.module.analyze_source((source or self.source).to_dict(),self.store.root)

    def altered(self,text):
        path=self.root/'Changed.lean';path.write_text(text)
        return freeze_source(path,'structural_test_only',self.source.theorem,self.store)

    def test_actual_source_is_arbitrary_k_with_all_original_binders(self):
        front=self.front();self.assertEqual(front['status'],'applicable',front)
        self.assertEqual([x['name'] for x in front['binders']],['K',None,'q','k','r','n','hk','hr','hn'])
        self.assertEqual(front['source'],self.source.to_dict())
        self.assertIn('(n : Fin k → ℕ)',front['original_proposition'])
        self.assertIn('FiniteQBenchmark.planePi',front['original_proposition'])
        self.assertIn('FiniteQBenchmark.gaussianInt',front['matrix_term'])
        self.assertIn('.toNat',front['matrix_term']);self.assertIn(': ℤ',front['matrix_term'])
        self.assertEqual(front['symbols'],{'field':'K','base':'q','dimension':'k','height':'r','sequence':'n'})
        self.assertEqual(len(front['minor_entries']),4)
        self.assertEqual(front['core_request']['input']['size'],2)
        self.assertIs(front['specializes_original_dimension'],False)
        from agent_v2.symbolic_methods import validate_request
        validate_request(front['core_request'])

    def test_alpha_rename_field_sequence_indices_and_unused_extra_binder(self):
        text=self.source.declaration
        for old,new in [('K','L'),('q','b'),('k','d'),('r','s'),('n','f'),('i','row'),('j','col')]:
            text=re.sub(r'\b'+old+r'\b',new,text)
        text=text.replace('(hn : Antitone f)','(hn : Antitone f) (qv2i0 : Fin d → ℕ) (extra : True)')
        # Unused higher-order binders are deliberately unsupported; the original f is retained.
        self.assertEqual(self.front(self.altered(text))['status'],'not_applicable')
        text=text.replace('(qv2i0 : Fin d → ℕ)','(qv2i0 : ℕ)')
        front=self.front(self.altered(text));self.assertEqual(front['status'],'applicable',front)
        self.assertEqual(front['selectors'][0],'qv2i0x')
        self.assertIn('(f : Fin d → ℕ)',front['original_proposition'])
        self.assertIn('(extra : True)',front['original_proposition'])

    def test_changed_matrix_integer_arithmetic_or_original_target_rejected(self):
        for old,new in [('i.val:ℤ)-j.val-1','i.val:ℤ)-j.val+1'),('/2).toNat','/3).toNat'),
                         ('(n j:ℤ)+r-1','(n i:ℤ)+r-1'),('(r:ℤ)-i.val+j.val-1','(r:ℤ)+i.val+j.val-1'),
                         ('planePi q r n','planePi q k n'),('q^(∑ j, n j)','q^(∑ j, n j+1)'),
                         ('(hk : 0 < k)','(hk : 0 < r)'),('Antitone n','Monotone n')]:
            with self.subTest(change=new):
                self.assertNotEqual(self.source.declaration.replace(old,new),self.source.declaration)
                self.assertEqual(self.front(self.altered(self.source.declaration.replace(old,new)))['status'],'not_applicable')

    def test_unknown_commands_hypotheses_and_lambda_shadowing_rejected(self):
        for text in [self.source.declaration+'\n#eval 1\n',
                     self.source.declaration.replace('(hn : Antitone n)','(hn : Antitone n) (h : q ≠ 0)'),
                     self.source.declaration.replace('fun i j : Fin k','fun q j : Fin k'),
                     self.source.declaration.replace('import Benchmark.Batch3Proofs','import Other'),
                     self.source.declaration.replace('(k r : ℕ)','(k r : ℤ)')]:
            self.assertEqual(self.front(self.altered(text))['status'],'not_applicable')

    def test_source_integrity_and_real_mismatch(self):
        for source in [replace(self.source,Gamma='True'),replace(self.source,proposition='True'),
                       replace(self.source,theorem='Other.statement')]:
            with self.assertRaises(IntegrityError):self.front(source)
        other=load_train('FQI-SRC-GR2-I-20',self.store)
        self.assertEqual(self.front(other)['status'],'not_applicable')


if __name__=='__main__':unittest.main()
