"""Fixed task binding tests; certificate fixtures are not Lean evidence."""
from dataclasses import replace
import importlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from agent_v2.graph import Graph
from agent_v2.models import Budget, VerifiedCertificate, initial_state
from agent_v2.recurrence_adapter import RecurrenceAdapter
from agent_v2.recurrence_frontend import analyze_source
from agent_v2.recurrence_translation import translate_candidate
from agent_v2.storage import IntegrityError, RunStore, load_train
from agent_v2.tests.test_recurrence_translation import fixture


class RecurrenceTaskTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.method_tasks'),
                             'fixed five-task dependency binding is not implemented')
        self.module = importlib.import_module('agent_v2.method_tasks')
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.store = RunStore.create(Path(temp.name)/'runs')
        raw = load_train('FQI-GAUSS-ALTERNATING', self.store)
        front = analyze_source(raw.to_dict())
        self.source = replace(raw, proposition=front['original_proposition'])
        self.front = analyze_source(self.source.to_dict())
        self.state, node = initial_state(self.source, Budget(1800, 5))
        self.graph = Graph(self.source.sha256); self.graph.add_node(node)
        self.local_outlet = self.module.initial_full_outlet(self.front, 1800, '2.0', 45)
        self.graph.add_outlet(self.local_outlet)

    def local(self):
        c = translate_candidate(self.front, fixture(self.front))['candidate']
        return VerifiedCertificate(c['id'], c['proposition'], c['proof_term'], c['source_sha256'], (),
            {'test_only': True, 'source_sha256': c['source_sha256'], 'proposition': c['proposition']})

    def test_initial_contract_declares_five_tasks_but_executes_only_local(self):
        contract = self.module.full_scope_contract(self.front)
        self.assertEqual(contract['tasks'], ['local','uniqueness_bridge','rhs_recurrence','initial_zero','initial_one'])
        self.assertEqual(contract['source_sha256'], self.source.sha256)
        self.assertEqual(self.module.bind_full_scope_outlets(self.state, self.graph), ())
        self.assertFalse(self.module.fixed_task_completed(self.state, self.local_outlet))
        self.assertEqual(len(self.graph.nodes), 1); self.assertEqual(len(self.graph.edges), 0)

    def test_real_witness_id_is_bound_only_after_approved_local_exists(self):
        local = self.local(); state = replace(self.state, C=(local,))
        before = state.to_dict()
        outlets = self.module.bind_full_scope_outlets(state, self.graph)
        self.assertEqual(len(outlets), 4)
        bridge = next(o for o in outlets if o.parameters['task']=='uniqueness_bridge')
        self.assertEqual(bridge.required_certificates, (local.id,))
        self.assertEqual(bridge.handles, ('original',))
        self.assertTrue(self.module.fixed_task_completed(state, self.local_outlet))
        self.assertEqual(state.to_dict(), before)
        for outlet in outlets: self.graph.add_outlet(outlet)
        self.assertEqual(self.module.bind_full_scope_outlets(state, self.graph), ())
        self.assertEqual(len(self.graph.outlets), 5)
        self.assertEqual(len(self.graph.nodes), 1); self.assertEqual(len(self.graph.edges), 0)

    def test_legal_candidates_do_not_repeat_local_or_offer_unopened_leaves(self):
        # Capability metadata substitute only; this unit test makes no Lean claim.
        from agent_v2.method_registry import builtin_registry
        registry=builtin_registry(); spec=registry.get('recurrence')
        registry._methods['recurrence']=replace(spec,version='2.0',scopes=('local','full'),
            tasks=('local','uniqueness_bridge','rhs_recurrence','initial_zero','initial_one'))
        with patch('agent_v2.method_registry.builtin_registry',return_value=registry):
            initial,_=self.graph.legal_candidates(self.state)
            self.assertEqual([a.theta['task'] for a in initial],['local'])
            state=replace(self.state,C=(self.local(),))
            for outlet in self.module.bind_full_scope_outlets(state,self.graph):
                self.graph.add_outlet(outlet)
            legal,reasons=self.graph.legal_candidates(state)
            self.assertEqual([a.theta['task'] for a in legal],['uniqueness_bridge'])
            self.assertIn('task_already_completed',[r['code'] for r in reasons])

    def test_existing_outlet_cannot_rebind_required_certificate_or_handles(self):
        state = replace(self.state, C=(self.local(),))
        outlets = self.module.bind_full_scope_outlets(state, self.graph)
        bridge = next(o for o in outlets if o.parameters['task']=='uniqueness_bridge')
        for altered in (replace(bridge, required_certificates=('forged',)),
                        replace(bridge, handles=('unrelated',))):
            self.graph.outlets[altered.id] = altered
            with self.assertRaises(IntegrityError):
                self.module.bind_full_scope_outlets(state, self.graph)
            del self.graph.outlets[altered.id]

    def test_unapproved_or_foreign_local_cannot_unlock_chain(self):
        local=self.local()
        for altered in (replace(local, source_sha256='0'*64), replace(local, id='forged'),
                        replace(local, proof_term='by rfl'), replace(local, proposition='True')):
            with self.subTest(case=altered.id), self.assertRaises(IntegrityError):
                self.module.bind_full_scope_outlets(replace(self.state,C=(altered,)), self.graph)

    def test_unknown_task_is_not_materialized_as_an_extra_route(self):
        forged=replace(self.local_outlet,id='recurrence-secret',
            parameters=dict(self.local_outlet.parameters,task='secret'))
        self.graph.add_outlet(forged)
        with self.assertRaises(IntegrityError):
            self.module.bind_full_scope_outlets(self.state,self.graph)

    def test_other_methods_and_local_scope_are_unchanged(self):
        local=replace(self.local_outlet,parameters={'method':'recurrence','seconds':1800})
        self.graph.outlets={local.id:local}
        self.assertEqual(self.module.bind_full_scope_outlets(self.state,self.graph),())
        self.assertFalse(self.module.fixed_task_completed(replace(self.state,C=(self.local(),)),local))

    def test_full_adapter_refuses_a_leaf_without_its_exact_open_obligation(self):
        self.assertTrue(hasattr(RecurrenceAdapter(),'execute_action'), 'recurrence full adapter absent')
        from agent_v2.models import JointAction
        action=JointAction('early','identity','original','original','CAS','method',
            {'method':'recurrence','scope':'full','task':'initial_zero'})
        with self.assertRaises(ValueError):
            RecurrenceAdapter().execute_action(self.state,action,self.store.root/'early',30)

    def test_loop_binds_declared_bridge_after_local_without_repeating_core(self):
        # Real state/graph/closure generators; a named unit-only checker avoids Lean.
        from agent_v2.executor import Executor
        from agent_v2.loop import run
        from agent_v2.method_registry import builtin_registry
        from agent_v2.models import Candidate
        from agent_v2.recurrence_closure import make_closure_candidate
        from agent_v2.tests.test_executor import RecordingChecker, result
        registry=builtin_registry(); spec=registry.get('recurrence')
        registry._methods['recurrence']=replace(spec,version='2.0',scopes=('local','full'),
            tasks=tuple(self.module.TASKS))
        local=Candidate.from_dict(translate_candidate(self.front,fixture(self.front))['candidate'])
        calls=[]
        class UnitOnlyAdapter:
            def execute_action(inner,state,action,path,seconds):
                task=action.theta['task']; calls.append(task)
                candidate=local if task=='local' else make_closure_candidate(self.front,task,
                    {c.id:c.to_dict() for c in state.C},action.id)
                return replace(result([candidate],candidate.replaces,status='symbolic_constructed'),
                    raw_result={'execution_scope':'certificate_chain','test_only':True}).to_dict()
        with patch('agent_v2.method_registry.builtin_registry',return_value=registry):
            state=replace(self.state,b=Budget(1800,2))
            final=run(state,self.graph,self.store,Executor({'method':UnitOnlyAdapter()}),RecordingChecker())
        self.assertEqual(calls,['local','uniqueness_bridge'])
        self.assertEqual(final.round_index,2)
        self.assertEqual((len(final.C),len(final.O),len(final.links)),(2,3,1))
        self.assertEqual(final.b.actions,0)


if __name__ == '__main__': unittest.main()
