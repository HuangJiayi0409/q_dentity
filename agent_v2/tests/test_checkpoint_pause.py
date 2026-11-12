"""Safe invocation limits; synthetic fixtures test control, not mathematical discovery."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from agent_v2.cli import parser
from agent_v2.executor import Executor
from agent_v2.graph import Graph, Outlet
from agent_v2.loop import resume, run
from agent_v2.models import Budget, Candidate, Obligation, initial_state
from agent_v2.storage import RunStore, freeze_source
from agent_v2.tests.test_executor import RecordingChecker, result
from agent_v2.tests.test_loop import FinalChecker, QueueAdapter


class CheckpointPauseTests(unittest.TestCase):
    def fixture(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        root=Path(temp.name); path=root/'Source.lean';path.write_text('theorem demo : True := by sorry\n')
        store=RunStore.create(root/'runs');source=freeze_source(path,'synthetic-pause','demo',store,proposition='True')
        state,node=initial_state(source,Budget(300,5));graph=Graph(source.sha256);graph.add_node(node)
        leaf=Obligation('leaf','boundary','True','True',source.sha256)
        bridge=Candidate('bridge','(True) → (True)','fun h => h','AgentV2Candidate.proof',source.sha256,(), 'original',(leaf,))
        proof=Candidate('leaf-proof','True','True.intro','AgentV2Candidate.proof',source.sha256,(), 'leaf')
        for name,handle,produces in [('bridge','original','bridge'),('leaf','leaf','leaf-proof')]:
            graph.add_outlet(Outlet(name,'original','CAS','method',{'method':'synthetic','produces_certificate':produces},
                ('closed_prop',),handles=(handle,)))
        return store,state,graph,bridge,proof,leaf

    def test_pause_preserves_remaining_actions_and_resume_continues_next_leaf(self):
        store,state,graph,bridge,proof,leaf=self.fixture()
        adapter=QueueAdapter([result([bridge],[leaf])]);checker=FinalChecker()
        paused=run(state,graph,store,Executor({'method':adapter}),checker,pause_after=1)
        self.assertEqual(paused.status,'incomplete');self.assertEqual(paused.b.actions,4)
        self.assertEqual(paused.round_index,1);self.assertEqual(paused.O,(leaf,))
        self.assertEqual(store.read_json('run.json')['stop_reason'],'checkpoint_paused')
        self.assertEqual(checker.final_calls,[])
        replay=RecordingChecker();fresh,g=resume(store,replay)
        final=run(fresh,g,store,Executor({'method':QueueAdapter([result([proof])])}),FinalChecker())
        self.assertEqual(final.status,'original_theorem_proved')
        self.assertEqual(final.b.actions,3);self.assertEqual(final.round_index,2)
        self.assertEqual(len(replay.seen),1)

    def test_empty_obligations_at_pause_do_not_claim_original_acceptance(self):
        store,state,graph,bridge,proof,leaf=self.fixture()
        checker=FinalChecker()
        paused=run(state,graph,store,Executor({'method':QueueAdapter([result([bridge],[leaf]),result([proof])])}),
                   checker,pause_after=2)
        self.assertEqual(paused.O,());self.assertEqual(paused.status,'incomplete')
        self.assertEqual(checker.final_calls,[])
        self.assertFalse(store.read_json('run.json')['original_identity_proved'])
        fresh,g=resume(store,RecordingChecker());new_checker=FinalChecker()
        final=run(fresh,g,store,Executor({'method':QueueAdapter([])}),new_checker)
        self.assertEqual(final.status,'original_theorem_proved')
        self.assertEqual(len(new_checker.final_calls),1)
        self.assertEqual(final.b.actions,paused.b.actions)

    def test_cli_pause_limits_are_explicit_and_positive(self):
        p=parser()
        self.assertEqual(p.parse_args(['run','--identity','FQI-GAUSS-ALTERNATING','--pause-after','1']).pause_after,1)
        self.assertEqual(p.parse_args(['resume','--run-dir','/tmp/run','--pause-after','2']).pause_after,2)
        self.assertIsNone(p.parse_args(['resume','--run-dir','/tmp/run']).pause_after)
        with self.assertRaises(SystemExit):p.parse_args(['resume','--run-dir','/tmp/run','--pause-after','0'])


if __name__ == '__main__':unittest.main()
