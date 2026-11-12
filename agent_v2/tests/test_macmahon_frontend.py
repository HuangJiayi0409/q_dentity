"""Complete original complex Source and exact finite Laurent-sum export."""
import importlib
from dataclasses import replace
from pathlib import Path
import re
import tempfile
import unittest
from agent_v2.storage import IntegrityError,RunStore,freeze_source,load_train


class MacMahonFrontendTests(unittest.TestCase):
    def setUp(self):
        self.module=importlib.import_module('agent_v2.macmahon_frontend')
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name);self.store=RunStore.create(self.root/'runs')
        self.source=load_train('FQI-SRC-GR2-7.Ex14',self.store)
    def altered(self,text):
        path=self.root/'Changed.lean';path.write_text(text)
        return freeze_source(path,'structural_test_only',self.source.theorem,self.store)
    def front(self,source=None):return self.module.analyze_source((source or self.source).to_dict(),self.store.root)
    def test_complete_complex_source_and_symbolic_finite_fiber(self):
        f=self.front();self.assertEqual(f['status'],'applicable',f)
        self.assertEqual([b['name'] for b in f['binders']],['z','q','n','hq','hz'])
        self.assertEqual(f['universe_parameters'],[]);self.assertEqual(f['ambient_context']['field'],'K')
        self.assertEqual(f['source'],self.source.to_dict());self.assertFalse(f['bound_specialized'])
        self.assertIn('Filter.Tendsto',f['original_proposition']);self.assertIn('nhdsWithin',f['original_proposition'])
        self.assertEqual(f['source_sum']['index'],'k');self.assertEqual(f['source_exponent'],{'bound':1,'index':-2,'constant':0})
        from agent_v2.symbolic_methods import validate_request
        validate_request(f['core_request'])
    def test_alpha_renaming_retains_every_original_binder_and_limit(self):
        text=self.source.declaration
        for old,new in [('K','F'),('z','w'),('q','r'),('n','m'),('k','j'),('beta','eta'),('hq','hr'),('hz','hw')]:
            text=re.sub(r'\b'+old+r'\b',new,text)
        f=self.front(self.altered(text));self.assertEqual(f['status'],'applicable',f)
        self.assertEqual(f['symbols']['scalar'],'w');self.assertEqual(f['symbols']['bound'],'m')
        self.assertEqual(f['source_sum']['index'],'j');self.assertIn('eta',f['original_proposition'])
        self.assertNotIn('Type u',f['original_proposition'])
    def test_changes_to_all_conjuncts_domains_bounds_and_nonzero_are_rejected(self):
        for old,new in [('2*k','3*k'),('n+1','n+2'),('(z q : ℂ)','(z q : ℚ)'),
                        ('(hz : z ≠ 0)','(hz : q ≠ 0)'),('z-z⁻¹ ≠ 0','z+z⁻¹ ≠ 0'),
                        ('1 ≤ n','2 ≤ n'),('(1-q^n)','(1+q^n)'),('({1}ᶜ)','({0}ᶜ)')]:
            with self.subTest(change=new):
                self.assertEqual(self.front(self.altered(self.source.declaration.replace(old,new)))['status'],'not_applicable')
    def test_unknown_commands_imports_and_shadowing_are_refused(self):
        for text in [self.source.declaration+'\n#eval 1',self.source.declaration.replace('Benchmark.Batch2Proofs','Arbitrary.Module'),
                     self.source.declaration.replace('(hz : z ≠ 0)','(hz : z ≠ 0) (z : ℂ)'),
                     self.source.declaration.replace('∑ k ∈','∑ z ∈')]:
            self.assertEqual(self.front(self.altered(text))['status'],'not_applicable')
    def test_real_mismatch_and_frozen_source_integrity(self):
        other=load_train('FQI-GAUSS-ALTERNATING',self.store);self.assertEqual(self.front(other)['status'],'not_applicable')
        for source in [replace(self.source,Gamma='True'),replace(self.source,theorem='Other.statement'),replace(self.source,proposition='True')]:
            with self.assertRaises(IntegrityError):self.front(source)

if __name__=='__main__':unittest.main()
