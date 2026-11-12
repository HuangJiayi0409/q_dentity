"""Control-only fixtures: symbolic results never constitute formal proofs."""
from pathlib import Path
import tempfile
import unittest

from agent_v2.executor import Executor
from agent_v2.graph import Graph,Outlet
from agent_v2.loop import run,resume
from agent_v2.models import Budget,Candidate,Cost,ExecutionResult,FailureSignature,Obligation,initial_state
from agent_v2.storage import RunStore,freeze_source
from agent_v2.tests.test_loop import QueueAdapter


class NoProofChecker:
    def check_partial(self,*args):raise AssertionError('symbolic scope called Lean')
    def accept_original(self,*args):raise AssertionError('symbolic scope attempted final acceptance')


class SymbolicSourceScopeTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        root=Path(temporary.name);path=root/'source.lean'
        path.write_text('theorem source : True := by sorry\n')
        self.store=RunStore.create(root/'runs','run')
        source=freeze_source(path,'synthetic-control-only','source',self.store,proposition='True')
        self.state,representation=initial_state(source,Budget(100,1))
        self.graph=Graph(source.sha256);self.graph.add_node(representation)
        self.graph.add_outlet(Outlet('symbolic','original','CAS','method',
            {'method':'telescoping','seconds':10.0},('closed_prop',)))

    def outcome(self,status='symbolic_constructed',code='translation_pending',candidates=(),obligations=()):
        return ExecutionResult(status,tuple(candidates),tuple(obligations),
            FailureSignature('translation',code,'control fixture; no mathematical acceptance','test_fixture'),
            Cost(0,1),{'execution_scope':'source_symbolic_only','remaining_work':'no Lean bridge'},(),(),False)

    def execute(self,result):
        adapter=QueueAdapter([result])
        state=run(self.state,self.graph,self.store,Executor({'method':adapter}),NoProofChecker())
        return state,adapter

    def test_symbolic_success_stops_with_original_open_and_one_charged_action(self):
        state,adapter=self.execute(self.outcome())
        self.assertEqual(state.status,'incomplete')
        self.assertEqual(self.store.read_json('run.json')['stop_reason'],'symbolic_translation_pending')
        self.assertEqual((state.C,state.O,state.links),(self.state.C,self.state.O,self.state.links))
        self.assertEqual((state.G,state.Gamma),(self.state.G,self.state.Gamma))
        self.assertEqual(len(adapter.calls),1)
        self.assertEqual(state.b.actions,0)
        self.assertLess(state.b.seconds,self.state.b.seconds)
        self.assertEqual(self.store.read_json('rounds/1/result.json')['status'],'symbolic_constructed')
        self.assertFalse(self.store.read_json('run.json')['original_identity_proved'])

    def test_resume_keeps_symbolic_boundary_without_repeating_cas_or_using_lean(self):
        first,_=self.execute(self.outcome())
        state,graph=resume(self.store,NoProofChecker())
        adapter=QueueAdapter([])
        final=run(state,graph,self.store,Executor({'method':adapter}),NoProofChecker())
        self.assertEqual(adapter.calls,[])
        self.assertEqual(final.status,'incomplete')
        self.assertEqual(self.store.read_json('run.json')['stop_reason'],'symbolic_translation_pending')
        self.assertEqual((final.C,final.O,final.links),(first.C,first.O,first.links))
        self.assertEqual(final.round_index,1)
        self.assertEqual(final.b.actions,first.b.actions)

    def test_symbolic_scope_refuses_formal_exports_before_any_checker_call(self):
        candidate=Candidate('illegal','True','by trivial','AgentV2Candidate.proof',self.state.G.sha256)
        state,_=self.execute(self.outcome(candidates=[candidate]))
        self.assertEqual(state.status,'integrity_error')
        self.assertEqual((state.C,state.O,state.links),(self.state.C,self.state.O,self.state.links))
        self.assertIn('symbolic-only',str(self.store.read_json('rounds/1/result.json')))

    def test_unverified_residuals_are_not_accepted_in_symbolic_scope(self):
        obligation=Obligation('forged','subgoal','True','True',self.state.G.sha256,'unknown')
        state,_=self.execute(self.outcome(obligations=[obligation]))
        self.assertEqual(state.status,'integrity_error')
        self.assertEqual(state.O,self.state.O)

    def test_real_failure_categories_are_not_rewritten_as_symbolic_success(self):
        state,_=self.execute(self.outcome('budget_exhausted','timeout'))
        self.assertEqual(state.status,'budget_exhausted')
        self.assertEqual(self.store.read_json('run.json')['stop_reason'],'timeout')
        self.assertEqual((state.C,state.O,state.links),(self.state.C,self.state.O,self.state.links))


if __name__=='__main__':unittest.main()
