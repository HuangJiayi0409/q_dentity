"""Contract regressions using synthetic inputs only; no benchmark formula reads."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import sympy as s

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'p1'))
from source_ir import Converter,InputGap,node,var,nat
from expressions import expression,shift_ratio,rationalize,k,X,q
from workflow import engine
from workflow.admission import SCOPES,annotate,multisum_exit
from workflow.contracts import BACKENDS,FAMILIES
from difference_ring.algebra import ideal_witness,reduce_goal
from combinatorial.pipeline import plans


class Bases(unittest.TestCase):
    def test_base_role_is_independent_of_names(self):
        for base,scalar in [('p','q'),('q','c'),('renamed','scalar')]:
            with self.subTest(base=base,scalar=scalar):
                term=node('HMul.hMul',var(scalar),node('FiniteQBenchmark.poch',var('a'),var(base),var('j')))
                cv=Converter([term],'m','j')
                self.assertEqual(cv.names[base],'q')
                ratio=rationalize(shift_ratio(expression(cv.read(term)),k))
                self.assertEqual(s.cancel(ratio-(1-s.Symbol(cv.names['a'])*X)),0)

    def test_base_powers_share_root(self):
        term=node('HMul.hMul',node('FiniteQBenchmark.poch',var('a'),var('p'),var('k')),
                  node('FiniteQBenchmark.poch',var('b'),node('HPow.hPow',var('p'),nat(2)),var('k')))
        cv=Converter([term],'n','k')
        ratio=rationalize(shift_ratio(expression(cv.read(term)),k))
        expected=(1-s.Symbol(cv.names['a'])*X)*(1-s.Symbol(cv.names['b'])*X**2)
        self.assertEqual(s.cancel(ratio-expected),0)

    def test_distinct_structural_bases_rejected(self):
        terms=[node('FiniteQBenchmark.poch',var('a'),var(b),var('k')) for b in ('p','q')]
        with self.assertRaisesRegex(InputGap,'multiple independent bases'):Converter(terms,'n','k')

    def test_index_base_collision(self):
        term=node('FiniteQBenchmark.poch',var('a'),var('k'),var('k'))
        with self.assertRaisesRegex(InputGap,'overlapping'):Converter([term],'n','k')

    def test_geometric_base_does_not_need_name_q(self):
        cv=Converter([node('HPow.hPow',var('p'),var('k')),var('q')],'n','k')
        self.assertEqual(cv.names['p'],'q')
        self.assertNotEqual(cv.names['q'],'q')

    def test_scalar_name_alone_not_evidence(self):
        with self.assertRaisesRegex(InputGap,'no structural'):Converter([var('q'),var('n')],'n')

    def test_falling_atom_base_position(self):
        cv=Converter([node('FiniteQBenchmark.kacPowerNat',var('x'),var('a'),var('p'),var('k'))],'n','k')
        self.assertEqual(cv.names['p'],'q')


class Diagnostics(unittest.TestCase):
    def prove(self,result):
        with tempfile.TemporaryDirectory() as d, patch.object(engine,'snapshot',return_value={'synthetic':True}), \
                patch.object(engine,'check_source'):
            return engine.prove('synthetic',d,method='recurrence',runner=lambda *a:result)

    def test_analysis_timeout_is_resource_failure(self):
        r=self.prove(dict(status='timeout',error='analysis deadline'))
        self.assertEqual(r['status'],'resource_exhausted');self.assertEqual(r['failure_stage'],'analysis')
        self.assertEqual(r['error'],'analysis deadline');self.assertEqual(r['attempts'],[])

    def test_adapter_error_is_not_domain_rejection(self):
        for status in ('adapter_failed','worker_failed'):
            r=self.prove(dict(status=status,error='broken exporter'))
            self.assertEqual(r['status'],'analysis_failed');self.assertEqual(r['analysis_failure_status'],status)
            self.assertEqual(r['automatic_train_proofs'],0)

    def test_empty_completed_analysis_is_unknown(self):
        r=self.prove(dict(status='analyzed',candidates=[]))
        self.assertEqual(r['status'],'unproved');self.assertEqual(r['applicability_status'],'unknown')

    def test_explicit_domain_rejection(self):
        c=annotate(dict(backend='multisum',applicable=False,reason='unsupported syntax',
                        admission_checks=dict(core_domain='rejected',proof_exit='unavailable')))
        r=self.prove(dict(status='analyzed',candidates=[c]))
        self.assertEqual(r['applicability_status'],'outside_current_implementation')

    def test_known_missing_exit_does_not_schedule_proof(self):
        c=annotate(dict(backend='multisum',applicable=True,reason='3D core accepted',
                        admission_checks=multisum_exit(dict(dimension=3,domain='simplex'))))
        r=self.prove(dict(status='analyzed',candidates=[c]))
        self.assertEqual(r['plan'],[]);self.assertEqual(r['applicability_status'],'unknown')
        self.assertEqual(r['admission'][0]['admission']['core_domain'],'accepted')


class Admissions(unittest.TestCase):
    def test_every_backend_and_family_has_scope(self):
        self.assertEqual(set(SCOPES),set(BACKENDS));self.assertEqual(set(BACKENDS.values()),set(FAMILIES))
        for value in SCOPES.values():
            self.assertTrue({'syntax','bases','summation_dimension','coefficient_domain','order',
                             'proof_exit_scope','implementation_limits','guarantee'}<=value.keys())

    def test_boolean_candidate_does_not_certify_domain(self):
        c=annotate(dict(backend='finite_spectral_certificate',applicable=True,reason='has sum'))
        self.assertEqual(c['admission']['core_domain'],'unknown')
        self.assertFalse(c['admission']['complete_original_proof'])

    def test_multisum_domain_and_exit_differ(self):
        for dimension,domain in [(3,'simplex'),(2,'box')]:
            a=multisum_exit(dict(dimension=dimension,domain=domain))
            self.assertEqual(a['core_domain'],'accepted');self.assertEqual(a['proof_exit'],'unavailable')
        self.assertEqual(multisum_exit(dict(dimension=2,domain='simplex'))['proof_exit'],'unknown')

    def test_matrix_exporter_failure_is_not_domain_rejection(self):
        from workflow import matrix_synthesis as m
        with tempfile.TemporaryDirectory() as d, patch.object(m.structural,'slot',return_value=''), \
             patch.object(m,'lean',return_value=dict(exit_code=1,output='error: internal elaborator failure')):
            with self.assertRaisesRegex(RuntimeError,'did not complete'):
                m.extract_input('',Path(d),{},dict(method='spectral',module='SpectralRules'))

    def test_matrix_explicit_shape_rejection_is_preserved(self):
        from workflow import matrix_synthesis as m
        with tempfile.TemporaryDirectory() as d, patch.object(m.structural,'slot',return_value=''), \
             patch.object(m,'lean',return_value=dict(exit_code=1,output='error: SYNTHESIS_UNSUPPORTED: Fin index required')):
            self.assertIsNone(m.extract_input('',Path(d),{},dict(method='spectral',module='SpectralRules')))


class AlgebraAndOrientation(unittest.TestCase):
    budget=dict(max_degree=5,max_unknowns=1000,symbolic_seconds=5)
    def test_linear_combination_missed_by_ordered_division(self):
        x,y=s.symbols('x y')
        c=ideal_witness(y,[x-y,x+y],[x,y],self.budget)
        self.assertEqual(s.expand(y-c[0]*(x-y)-c[1]*(x+y)),0)

    def test_nonlinear_completion_retains_original_multipliers(self):
        x,y=s.symbols('x y');rels=[x*y-1,y*y-1]
        c=ideal_witness(x-y,rels,[x,y],self.budget)
        self.assertEqual(s.expand(x-y-sum(a*b for a,b in zip(c,rels))),0)

    def test_nonmember_is_rejected(self):
        x,y=s.symbols('x y')
        with self.assertRaisesRegex(ValueError,'outside polynomial ideal'):
            ideal_witness(y,[x],[x,y],self.budget)

    def test_budget_is_not_nonmembership(self):
        x,y=s.symbols('x y')
        with self.assertRaisesRegex(ValueError,'budget'):
            ideal_witness(y,[x-y,x+y],[x,y],dict(self.budget,max_unknowns=1))

    def test_relation_reordering_preserves_success(self):
        x,y=s.symbols('x y')
        for rels in [[x-y,x+y],[x+y,x-y]]:
            c=ideal_witness(y,rels,[x,y],self.budget)
            self.assertEqual(s.expand(y-sum(a*b for a,b in zip(c,rels))),0)

    def test_constant_nonzero_relation(self):
        x=s.Symbol('x')
        c=ideal_witness(x,[s.Integer(2)],[x],self.budget)
        self.assertEqual(s.expand(x-2*c[0]),0)

    def test_combination_pipeline_uses_completed_witness(self):
        x=dict(op='atom',key=0,display='x');y=dict(op='atom',key=1,display='y');zero=dict(op='integer',value=0)
        raw=dict(lhs=y,rhs=zero,hypotheses=[
            dict(name='hsub',lhs=dict(op='HSub.hSub',args=[x,y]),rhs=zero),
            dict(name='hadd',lhs=dict(op='HAdd.hAdd',args=[x,y]),rhs=zero)])
        result=reduce_goal(raw,self.budget)
        self.assertIn('Groebner',result['algorithm']);self.assertIn('hsub',result['script']);self.assertIn('hadd',result['script'])

    def test_zero_sum_orientation(self):
        total=node('Finset.sum',node('Finset.range',var('n')),dict(op='lambda',name='i',body=var('i')))
        forward=plans(node('Eq',total,nat(0)));reverse=plans(node('Eq',nat(0),total))
        self.assertEqual([p['rule'] for p in forward],[p['rule'] for p in reverse])
        self.assertTrue(all(not p['reverse'] for p in forward));self.assertTrue(all(p['reverse'] for p in reverse))


class StrongCoreBridge(unittest.TestCase):
    def model(self,target=0):
        from difference_ring.core_bridge import frontend
        body=node('HPow.hPow',node('Nat.cast',var('j')),nat(2))
        total=node('Finset.sum',node('Finset.range',var('m')),dict(op='lambda',name='j',body=body))
        return frontend(dict(target=node('Eq',total,nat(target)),indices=['m']))

    def test_target_not_sent_to_strong_core(self):
        a,b=self.model(0),self.model(37)
        self.assertEqual(a['request'],b['request'])
        self.assertEqual(set(a['request']['input']),{'extensions','rhs_basis'})

    def test_constructed_original_tower_antidifference(self):
        from difference_ring.core_bridge import construct
        result=construct(self.model(),dict(symbolic_seconds=5,max_unknowns=1000,max_order=4))
        g=s.sympify(result['normalized_antidifference']);v=s.Symbol('Tower0')
        self.assertEqual(s.expand(g.subs(v,v+1)-g-v**2),0)
        self.assertFalse(result['original_identity_proved'])

    def test_truncated_natural_subtraction_rejected(self):
        from difference_ring.core_bridge import frontend,BridgeGap
        sub=dict(node('HSub.hSub',var('k'),nat(1)),type='ℕ')
        total=node('Finset.sum',node('Finset.range',var('m')),dict(op='lambda',name='k',body=node('Nat.cast',sub)))
        with self.assertRaisesRegex(BridgeGap,'truncated natural'):
            frontend(dict(target=node('Eq',total,nat(0)),indices=['m']))

    def test_outer_index_dependency_rejected(self):
        from difference_ring.core_bridge import frontend,BridgeGap
        inner=node('Finset.sum',node('Finset.range',var('k')),dict(op='lambda',name='j',body=node('Nat.cast',var('k'))))
        total=node('Finset.sum',node('Finset.range',var('m')),dict(op='lambda',name='k',body=inner))
        with self.assertRaisesRegex(BridgeGap,'outer bound index'):
            frontend(dict(target=node('Eq',total,nat(0)),indices=['m']))


if __name__=='__main__':unittest.main()
