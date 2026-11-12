"""Synthetic integration fixtures; outcomes below are not live model results."""
from pathlib import Path
from dataclasses import replace
from unittest.mock import patch
import time
import tempfile
import unittest

from agent_v2.graph import Graph
from agent_v2.models import Budget, Candidate, initial_state
from agent_v2.storage import RunStore, freeze_source
from agent_v2.tests.test_executor import result
from agent_v2.tests.test_loop import FinalChecker, QueueAdapter


class FakeModel:
    def __init__(self, responses):
        self.responses = list(responses); self.calls_used = 0; self.last_result = None
    def generate(self, kind, payload, **kwargs):
        self.calls_used += 1
        self.last_result = {'status':'ok', 'content':self.responses.pop(0), 'usage':None,
                            'model_calls':1, 'artifacts':[]}
        return self.last_result


class TaskChecker(FinalChecker):
    def __init__(self, final=True):
        super().__init__(final); self.tasks = {}
    def register_task(self, task): self.tasks[task.id] = task


class AutonomousLoopTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); root = Path(self.temp.name)
        src = root/'Source.lean'; src.write_text('import Init\ntheorem demo : True := by sorry\n')
        self.base = RunStore.create(root/'runs')
        self.source = freeze_source(src, 'synthetic', 'demo', self.base, proposition='True')
        self.state, rep = initial_state(self.source, Budget(100, 6))
        self.graph = Graph(self.source.sha256); self.graph.add_node(rep)

    def tearDown(self): self.temp.cleanup()

    def setup_run(self, responses, caps=None, cas=()):
        from agent_v2.autonomous import AutonomousRuntime, AutonomousStore, default_config
        model, checker = FakeModel(responses), TaskChecker()
        runtime = AutonomousRuntime(default_config(), caps or {}, model, checker, [])
        runtime.executor.method_adapter = QueueAdapter(cas)
        return AutonomousStore(self.base.root, runtime), runtime

    def test_local_cas_continues_to_model_and_original(self):
        from agent_v2.autonomous import run
        partial = Candidate('cas', 'True ∧ True', 'by constructor <;> trivial',
                            'AgentV2Candidate.proof', self.source.sha256)
        caps = {'telescoping': {'version':'2.0','local_proposition':partial.proposition,
                               'local_lean':True,'estimated_seconds':1}}
        store, runtime = self.setup_run([{'kind':'prove','proof_term':'by trivial'}], caps,
                                        [result([partial])])
        final = run(self.state, self.graph, store)
        self.assertEqual(final.status, 'original_theorem_proved')
        self.assertEqual(final.round_index, 2)
        self.assertEqual(runtime.model.calls_used, 1)
        self.assertEqual(len(final.C), 2)
        saved = RunStore(store.root).load_checkpoint()
        self.assertIn('autonomous', saved)
        self.assertEqual(saved['autonomous']['model_calls'], 1)

    def test_decomposition_navigates_and_closes_each_real_leaf(self):
        from agent_v2.autonomous import run
        store, runtime = self.setup_run([
            {'kind':'decompose','children':['True ∧ True','True'], 'proof_term':'by intros; trivial'},
            {'kind':'prove','proof_term':'by constructor <;> trivial'},
            {'kind':'prove','proof_term':'by trivial'}])
        final = run(self.state, self.graph, store)
        self.assertEqual(final.status, 'original_theorem_proved')
        actions = [store.read_json(f'rounds/{n}/action.json') for n in (1,2,3)]
        self.assertNotEqual(actions[1]['T'], 'identity')
        self.assertNotEqual(actions[2]['T'], 'identity')
        self.assertEqual(actions[2]['source'], actions[1]['target'])
        self.assertEqual(final.O, ())

    def test_pause_keeps_model_counts_and_registry_in_atomic_checkpoint(self):
        from agent_v2.autonomous import run
        store, runtime = self.setup_run([{'kind':'lemma','proposition':'True ∧ True',
                                         'proof_term':'by constructor <;> trivial'}])
        final = run(self.state, self.graph, store, pause_after=1)
        saved = RunStore(store.root).load_checkpoint()
        self.assertEqual(final.O, self.state.O)
        self.assertEqual(saved['autonomous']['model_calls'], 1)
        self.assertEqual(len(saved['autonomous']['tasks']), 1)
        self.assertEqual(store.read_json('run.json')['stop_reason'], 'checkpoint_paused')

    def test_preexecution_budget_exhaustion_is_not_integrity_error(self):
        from agent_v2.autonomous import run
        store,runtime=self.setup_run([])
        state=replace(self.state,b=Budget(.05,6))
        from agent_v2.autonomous import _legal
        def slow_legal(*args):
            result=_legal(*args)
            time.sleep(.06)
            return result
        with patch('agent_v2.autonomous._legal',slow_legal):
            final=run(state,self.graph,store)
        self.assertEqual(final.status,'budget_exhausted')
        self.assertEqual(runtime.model.calls_used,0)
        self.assertEqual(store.read_json('run.json')['stop_reason'],'wall_budget_exhausted')

    def test_final_prework_is_in_shared_deadline(self):
        from agent_v2.autonomous import run
        from agent_v2.graph_builder import sync_residual_graph
        from agent_v2.storage import verify_source
        store,runtime=self.setup_run([{'kind':'prove','proof_term':'by trivial'}])
        sync_residual_graph(self.state,self.graph,{},seconds=30)
        self.graph.legal_candidates(self.state,True)
        def slow_verify(*args):
            verify_source(*args)
            time.sleep(.25)
        with patch('agent_v2.autonomous.verify_source',slow_verify):
            final=run(replace(self.state,b=Budget(.4,6)),self.graph,store)
        self.assertEqual(final.status,'budget_exhausted')
        self.assertEqual(runtime.model.calls_used,1)
        self.assertEqual(runtime.checker.final_calls,[])

    def test_call_limit_wins_when_last_failed_route_is_also_duplicate(self):
        from agent_v2.autonomous import run
        store,runtime=self.setup_run([{'invalid':'proposal'}])
        runtime.config['max_model_calls']=1
        final=run(self.state,self.graph,store)
        self.assertEqual(runtime.model.calls_used,1)
        self.assertEqual(final.status,'budget_exhausted')
        self.assertEqual(store.read_json('run.json')['stop_reason'],'model_call_limit')


if __name__ == '__main__': unittest.main()
