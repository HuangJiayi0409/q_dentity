"""Transport and failure-isolation regressions without solver or Lean mocks of success."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

from workflow import engine, preprocessed
from workflow.contracts import FAMILIES, HERE, snapshot


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()

    def test_failed_preprocessing_never_dispatches_solver(self):
        calls=[]
        def runner(req,d,timeout):
            calls.append(req['action'])
            return dict(status='adapter_failed',error='synthetic invalid equivalence')
        result=engine.prove('FQI-BAILEY-INVERSION',self.root,method='recurrence',
                            preprocess=True,runner=runner)
        self.assertEqual(result['status'],'preprocessing_failed')
        self.assertEqual(calls,['preprocess'])
        self.assertEqual(result['automatic_train_proofs'],0)

    def test_historical_gate_only_removed_in_new_path(self):
        with self.assertRaisesRegex(ValueError,'P1/P2'):
            snapshot('FQI-BAILEY-INVERSION',self.root,'recurrence')
        for method in FAMILIES:
            with self.subTest(method=method):
                result=snapshot('FQI-BAILEY-INVERSION',self.root,method,preprocess=True)
                self.assertIn('/Train/',result['path'])

    def test_all_twelve_slots_use_the_shared_goal_transport(self):
        source=snapshot('FQI-POCHHAMMER-RESIDUES',self.root,'product')
        text=Path(source['snapshot']).read_text()
        (self.root/'original.lean').write_text(text)
        token=preprocessed.ACTIVE.set(dict(directory=str(self.root)))
        try:
            from product.pipeline import slot as product
            from interpolation.pipeline import slot as interpolation
            from noncommutative.pipeline import slot as operator
            from combinatorial.pipeline import slot as combinatorial
            from difference_ring.pipeline import slot as difference
            from workflow.structural import slot as structural
            def load(name,relative):
                spec=importlib.util.spec_from_file_location(name,HERE/relative)
                module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
                return module
            p1=load('connection_p1','p1/lean_pipeline.py').proof_slot
            p2=load('connection_p2','p2/run.py').proof_slot
            slots={'telescoping':p1,'recurrence':p1,'coefficient':p2,'product':product,
                   'interpolation':lambda s,p:interpolation(s,p.strip()),'noncommutative':operator,
                   'combinatorial':combinatorial,'difference_ring':difference}
            for method,module in [('kernel_transform','KernelRules'),('spectral','SpectralRules'),
                                  ('determinant','DeterminantRules'),('macmahon','MacMahonRules')]:
                slots[method]=lambda s,p,m=module:structural(s,p,m)
            self.assertEqual(set(slots),set(FAMILIES))
            original_declaration=text.split('theorem statement',1)[1].split('  sorry',1)[0]
            for method,slot in slots.items():
                with self.subTest(method=method):
                    output=slot(text,'  exact synthetic_backend_proof')
                    self.assertIn(original_declaration,output)
                    self.assertEqual(output.count('preprocess_enter '),1)
                    self.assertLess(output.index('preprocess_enter '),output.index('exact synthetic_backend_proof'))
                    self.assertNotIn('  sorry',output)
                    with self.assertRaisesRegex(ValueError,'source_mismatch'):
                        slot(text.replace('(hm : 0 < m)','(hm : False)'),'  trivial')
        finally:preprocessed.ACTIVE.reset(token)

    def test_tampered_artifact_rejected_before_source_loading(self):
        path=self.root/'bundle.json';path.write_text('{}')
        descriptor=dict(directory=str(self.root),files=[dict(path=str(path),sha256='incorrect')])
        with self.assertRaisesRegex(ValueError,'artifact_changed'):
            preprocessed.check(descriptor,{})


if __name__=='__main__':unittest.main(verbosity=2)
