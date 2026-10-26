"""Behavioral contract tests, independent of symbolic identities and train counts."""
import copy
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
from workflow import engine
from workflow.contracts import HERE,ROOT,accept_proof,save,snapshot

IDENTITY='FQI-GAUSS-ALTERNATING'

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()

    def runner(self,request,directory,timeout):
        if request['action']=='analyze':
            candidates=([{'backend':name,'applicable':True,'reason':'synthetic adapter response'}
                for name in ('target_first_order','general_q_zeilberger')] if request['kind']=='p1' else [])
            return {'status':'analyzed','candidates':candidates}
        return {'status':'resource_exhausted' if request['backend']=='target_first_order' else 'lean_failed',
                'remaining_obligations':['synthetic unresolved goal']}

    def test_construction_failure_continues_to_next_backend(self):
        r=engine.prove(IDENTITY,self.root,method='recurrence',runner=self.runner)
        self.assertEqual([a['status'] for a in r['attempts']],['resource_exhausted','lean_failed'])
        self.assertEqual(r['status'],'unproved');self.assertEqual(r['automatic_train_proofs'],0)
        self.assertTrue(r['remaining_obligations'])

    def test_lean_failure_also_continues(self):
        def fail_verification(req,d,t):
            if req['action']=='analyze':return self.runner(req,d,t)
            if req['backend']=='target_first_order':
                return {'status':'lean_failed','verification':{'status':'lean_failed'},
                        'remaining_obligations':['boundary not closed']}
            return {'status':'search_exhausted','remaining_obligations':['no relation in current budget']}
        r=engine.prove(IDENTITY,self.root,method='recurrence',runner=fail_verification)
        self.assertEqual(len(r['attempts']),2)
        self.assertEqual(r['attempts'][0]['failure_stage'],'verification')
        self.assertEqual(r['attempts'][1]['status'],'search_exhausted')
        self.assertEqual(r['automatic_train_proofs'],0)

    def test_method_filter_prevents_other_family_attempts(self):
        r=engine.prove(IDENTITY,self.root,method='telescoping',runner=self.runner)
        self.assertEqual(r['plan'],[]);self.assertEqual(len(r['analysis']),1)

    def test_no_implicit_cross_method_dispatch(self):
        with self.assertRaises(ValueError):engine.prove(IDENTITY,self.root)
        with self.assertRaises(ValueError):engine.prove(IDENTITY,self.root,method='not-a-method')

    def test_worker_rejects_cross_method_requests_before_reading_source(self):
        from workflow.worker import execute
        with self.assertRaisesRegex(ValueError,'outside selected method'):
            execute({'action':'prove','method':'telescoping','backend':'general_q_zeilberger'})

    def test_all_family_plans_stay_local(self):
        from workflow.contracts import BACKENDS,FAMILIES
        for method in FAMILIES:
            calls=[]
            def mixed(req,d,t):
                calls.append(req)
                if req['action']=='analyze':
                    return {'status':'analyzed','candidates':[{'backend':b,'applicable':True,'reason':'synthetic'} for b in BACKENDS]}
                return {'status':'search_exhausted'}
            r=engine.prove(IDENTITY,self.root,method=method,runner=mixed)
            self.assertEqual([a['backend'] for a in r['attempts']],[b for b,m in BACKENDS.items() if m==method])
            self.assertTrue(all(c['method']==method for c in calls))

    def test_unknown_backend_cannot_enter_plan(self):
        def bad(req,d,t):return {'status':'analyzed','candidates':[{'backend':'retired','applicable':True,'reason':'bad'}]}
        r=engine.prove(IDENTITY,self.root,method='recurrence',runner=bad)
        self.assertEqual(r['status'],'integrity_error');self.assertEqual(r['attempts'],[])

    def test_fake_success_rejected_without_fallback(self):
        def fake(req,d,t):
            if req['action']=='analyze':return self.runner(req,d,t)
            return {'status':'proved','remaining_obligations':[]}
        r=engine.prove(IDENTITY,self.root,method='recurrence',runner=fake)
        self.assertEqual(r['status'],'integrity_error');self.assertEqual(r['automatic_train_proofs'],0)
        self.assertEqual(len(r['attempts']),1)

    def test_global_budget_stops_further_work(self):
        def slow(req,d,t):time.sleep(.025);return self.runner(req,d,t)
        r=engine.prove(IDENTITY,self.root,method='recurrence',budget=engine.Budget(seconds=.01),runner=slow)
        self.assertEqual(r['status'],'resource_exhausted');self.assertEqual(r['attempts'],[])

    def test_scope_rejection_before_worker(self):
        def forbidden(*args):raise AssertionError('worker should not run')
        r=engine.prove('not-a-train-id',self.root,method='recurrence',runner=forbidden)
        self.assertEqual(r['status'],'invalid_input')

    def test_product_train_scope_does_not_expand_old_methods(self):
        identity='FQI-POCHHAMMER-RESIDUES'
        source=snapshot(identity,self.root,method='product')
        self.assertEqual(source['theorem'],'FiniteQBenchmark.Identity023.statement')
        with self.assertRaisesRegex(ValueError,'P1/P2'):
            snapshot(identity,self.root,method='recurrence')

    def test_product_worker_rejects_other_adapters(self):
        from workflow.worker import execute
        with self.assertRaisesRegex(ValueError,'outside selected method'):
            execute({'action':'analyze','method':'product','kind':'p1'})
        with self.assertRaisesRegex(ValueError,'outside selected method'):
            execute({'action':'prove','method':'product','backend':'ore_closure'})

    def test_interpolation_scope_and_isolation(self):
        source=snapshot('FQI-SRC-KAC-CHEUNG-1.11-12',self.root,method='interpolation')
        self.assertEqual(source['theorem'],'FiniteQBenchmark.Identity412.statement')
        from workflow.worker import execute
        with self.assertRaisesRegex(ValueError,'outside selected method'):
            execute({'action':'analyze','method':'interpolation','kind':'p2'})
        with self.assertRaisesRegex(ValueError,'outside selected method'):
            execute({'action':'prove','method':'interpolation','backend':'finite_product_indices'})

    def test_interpolation_symbolic_budget_bounds_worker(self):
        limits=[]
        def runner(req,d,t):
            if req['action']=='analyze':
                return {'status':'analyzed','candidates':[{'backend':'polynomial_interpolation','applicable':True,'reason':'synthetic'}]}
            limits.append(t)
            return {'status':'search_exhausted'}
        engine.prove(IDENTITY,self.root,method='interpolation',
                     budget=engine.Budget(symbolic_seconds=3),runner=runner)
        self.assertEqual(limits,[3])

    def test_operator_scope_isolation_and_budget(self):
        source=snapshot('FQI-SRC-KAC-CHEUNG-5.7',self.root,method='noncommutative')
        self.assertEqual(source['theorem'],'FiniteQBenchmark.Identity425.statement')
        from workflow.worker import execute
        with self.assertRaisesRegex(ValueError,'outside selected method'):
            execute({'action':'analyze','method':'noncommutative','kind':'p1'})
        with self.assertRaisesRegex(ValueError,'outside selected method'):
            execute({'action':'prove','method':'noncommutative','backend':'ore_closure'})
        limits=[]
        def runner(req,d,t):
            if req['action']=='analyze':
                return {'status':'analyzed','candidates':[{'backend':'operator_word_normalization','applicable':True,'reason':'synthetic'}]}
            limits.append(t)
            return {'status':'search_exhausted'}
        engine.prove(IDENTITY,self.root,method='noncommutative',
                     budget=engine.Budget(symbolic_seconds=3),runner=runner)
        self.assertEqual(limits,[3])

    def test_combinatorial_scope_isolation_and_budget(self):
        # Membership fixture in the current split; this test does not prove it.
        source=snapshot('FQI-RECTANGLE-PARTITIONS',self.root,method='combinatorial')
        self.assertEqual(source['theorem'],'FiniteQBenchmark.Identity006.statement')
        from workflow.worker import execute
        with self.assertRaisesRegex(ValueError,'outside selected method'):
            execute({'action':'analyze','method':'combinatorial','kind':'product'})
        with self.assertRaisesRegex(ValueError,'outside selected method'):
            execute({'action':'prove','method':'combinatorial','backend':'finite_product_indices'})
        limits=[]
        def runner(req,d,t):
            if req['action']=='analyze':
                return {'status':'analyzed','candidates':[{'backend':'weighted_bijection','applicable':True,'reason':'synthetic'},
                    {'backend':'sign_reversing_involution','applicable':True,'reason':'synthetic'}]}
            limits.append(t)
            return {'status':'search_exhausted'}
        report=engine.prove(IDENTITY,self.root,method='combinatorial',
                     budget=engine.Budget(symbolic_seconds=3),runner=runner)
        self.assertEqual(limits,[3,3])
        self.assertEqual(len(report['attempts']),2)

    def test_difference_ring_scope_isolation_and_budget(self):
        source=snapshot('FQI-SRC-FINE-2.3',self.root,method='difference_ring')
        self.assertEqual(source['theorem'],'FiniteQBenchmark.Identity343.statement')
        from workflow.worker import execute
        with self.assertRaisesRegex(ValueError,'outside selected method'):
            execute({'action':'analyze','method':'difference_ring','kind':'p1'})
        with self.assertRaisesRegex(ValueError,'outside selected method'):
            execute({'action':'prove','method':'difference_ring','backend':'ore_closure'})
        limits=[]
        def runner(req,d,t):
            if req['action']=='analyze':
                return {'status':'analyzed','candidates':[{'backend':'triangular_difference_ring','applicable':True,'reason':'synthetic'}]}
            limits.append(t)
            return {'status':'search_exhausted'}
        engine.prove(IDENTITY,self.root,method='difference_ring',
                     budget=engine.Budget(symbolic_seconds=3),runner=runner)
        self.assertEqual(limits,[3])

    def test_new_structural_methods_scope_isolation_and_budget(self):
        from workflow.worker import execute
        for method,backend,identity in [('kernel_transform','finite_kernel_certificate','FQI-SRC-AQ-3.23'),
              ('spectral','finite_spectral_certificate','FQI-RECTANGLE-PARTITIONS'),
              ('determinant','determinant_certificate','FQI-SRC-AP-11.2.4'),
              ('macmahon','finite_omega_elimination','FQI-RECTANGLE-PARTITIONS')]:
            with self.subTest(method=method):
                self.assertIn('Train/',snapshot(identity,self.root,method=method)['path'])
                with self.assertRaisesRegex(ValueError,'outside selected method'):
                    execute({'action':'analyze','method':method,'kind':'p1'})
                with self.assertRaisesRegex(ValueError,'outside selected method'):
                    execute({'action':'prove','method':method,'backend':'ore_closure'})
                limits=[]
                def runner(req,d,t):
                    if req['action']=='analyze':
                        self.assertEqual(req['kind'],method)
                        return {'status':'analyzed','candidates':[{'backend':backend,'applicable':True,'reason':'synthetic'}]}
                    limits.append(t)
                    return {'status':'search_exhausted'}
                engine.prove(identity,self.root,method=method,budget=engine.Budget(symbolic_seconds=3),runner=runner)
                self.assertEqual(limits,[3])

    def test_success_audit_rechecks_actual_artifact(self):
        source=snapshot(IDENTITY,self.root)
        original=json.loads((HERE/'p1/generated/runs'/IDENTITY/'report.json').read_text())
        attempt=self.root/'attempt';attempt.mkdir()
        proof=attempt/'Proof.lean';proof.write_bytes(Path(original['verification']['proof_file']).read_bytes())
        r=copy.deepcopy(original);r['verification']['proof_file']=str(proof)
        self.assertEqual(accept_proof(r,source,attempt)['theorem'],source['theorem'])
        bad=copy.deepcopy(r);bad['verification']['lean']['output']="'Other.statement' depends on axioms: []"
        with self.assertRaisesRegex(ValueError,'original-theorem'):accept_proof(bad,source,attempt)
        bad=copy.deepcopy(r);bad['remaining_obligations']=['boundary']
        with self.assertRaisesRegex(ValueError,'obligations'):accept_proof(bad,source,attempt)
        bad=copy.deepcopy(r);bad['verification']['lean']['output']+=' sorryAx'
        with self.assertRaisesRegex(ValueError,'Lean check'):accept_proof(bad,source,attempt)
        proof.write_text(proof.read_text()+'\n-- tampered\n')
        with self.assertRaisesRegex(ValueError,'hash'):accept_proof(r,source,attempt)

    def test_snapshot_mutation_detected(self):
        source=snapshot(IDENTITY,self.root);Path(source['snapshot']).write_text('changed')
        with self.assertRaisesRegex(ValueError,'source_changed'):accept_proof({},source,self.root)

    def test_worker_timeout_kills_descendants(self):
        fake=self.root/'fake';(fake/'workflow').mkdir(parents=True)
        marker=self.root/'child_survived'
        program='import time\nfrom pathlib import Path\ntime.sleep(1)\nPath('+repr(str(marker))+').touch()\n'
        (fake/'workflow/worker.py').write_text('import subprocess,sys,time\nsubprocess.Popen([sys.executable,"-c",'+repr(program)+'])\ntime.sleep(10)\n')
        with patch.object(engine,'HERE',fake):r=engine.call_worker({},self.root/'attempt',.2)
        self.assertEqual(r['status'],'timeout');time.sleep(1.1);self.assertFalse(marker.exists())

if __name__=='__main__':unittest.main(verbosity=2)
