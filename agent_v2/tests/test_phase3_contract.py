"""Phase-three production boundaries; mocks in this file are interface-only."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from agent_v2.models import Candidate


class Phase3ContractTests(unittest.TestCase):
    def test_core_request_rejects_even_a_scoped_formal_candidate(self):
        from agent_v2.cas_adapter import MethodAdapter
        from agent_v2.method_registry import builtin_registry
        from agent_v2.tests.test_executor import result
        candidate=Candidate('untrusted','True','by exact True.intro',
                            'AgentV2Candidate.proof','0'*64)
        raw=result([candidate]).to_dict()
        raw['raw_result']['execution_scope']='local_certificate_only'
        with self.assertRaisesRegex(ValueError,'core request'):
            MethodAdapter._annotate(raw,builtin_registry().get('coefficient'),core_request=True)

    def test_standalone_execution_retains_its_nonformal_level_after_method_upgrade(self):
        from agent_v2.cas_adapter import MethodAdapter
        from agent_v2.symbolic_methods import example_request
        with tempfile.TemporaryDirectory() as directory:
            result=MethodAdapter().execute_request('coefficient',example_request('coefficient'),
                Path(directory)/'actual-core',30)
        self.assertEqual(result['status'],'symbolic_constructed')
        self.assertEqual(result['raw_result']['capability_level'],'L2')
        self.assertEqual(result['raw_result']['registered_method_capability_level'],'L3')
        self.assertFalse(result['C_partial'] or result['O_res'])

    def test_l3_cannot_export_a_candidate_from_an_unscoped_symbolic_result(self):
        from agent_v2.cas_adapter import MethodAdapter
        from agent_v2.method_registry import builtin_registry
        from agent_v2.tests.test_executor import result
        candidate=Candidate('untrusted','True','by exact True.intro',
                            'AgentV2Candidate.proof','0'*64)
        spec=replace(builtin_registry().get('coefficient'),capability_level='L3',local_lean=True)
        with self.assertRaisesRegex(ValueError,'scope'):
            MethodAdapter._annotate(result([candidate]).to_dict(),spec)

    def test_recurrence_retained_request_records_current_method_version(self):
        from agent_v2.method_registry import builtin_registry
        from agent_v2.recurrence_adapter import RecurrenceAdapter
        from agent_v2.storage import RunStore,load_train
        with tempfile.TemporaryDirectory() as directory:
            store=RunStore.create(Path(directory)/'runs')
            source=load_train('FQI-GAUSS-ALTERNATING',store)
            outcome=RecurrenceAdapter().execute(source.identity,'recurrence',source.to_dict(),
                                                store.path('attempt'),0.000001)
            self.assertEqual(outcome['status'],'budget_exhausted')
            self.assertEqual(store.read_json('attempt/method_request.json')['version'],
                             builtin_registry().get('recurrence').version)

    def test_production_method_action_rejects_multiple_candidates(self):
        from agent_v2.cas_adapter import MethodAdapter
        from agent_v2.method_registry import builtin_registry
        from agent_v2.tests.test_executor import result
        candidate = Candidate('one', 'True', 'by exact True.intro',
                              'AgentV2Candidate.proof', '0' * 64)
        with self.assertRaisesRegex(ValueError, 'one candidate'):
            MethodAdapter._annotate(result([candidate, replace(candidate,id='two')]).to_dict(),
                                   builtin_registry().get('recurrence'))

    def test_cli_initializes_five_task_contract_with_only_local_executable(self):
        from agent_v2 import cli
        from agent_v2.method_registry import builtin_registry
        from agent_v2.storage import RunStore
        from agent_v2.method_tasks import TASKS
        registry = builtin_registry()
        registry._methods['recurrence'] = replace(registry.get('recurrence'),
            version='2.0', scopes=('local','full'), tasks=tuple(TASKS))
        captured = {}
        def capture_run(state,graph,*args,**kwargs):
            captured.update(graph=graph,state=state)
            return replace(state,status='incomplete')
        with tempfile.TemporaryDirectory() as directory:
            store=RunStore.create(Path(directory))
            with patch('agent_v2.method_registry.builtin_registry',return_value=registry), \
                 patch('agent_v2.loop.run',side_effect=capture_run):
                args=cli.parser().parse_args(['run','--identity','FQI-GAUSS-ALTERNATING',
                    '--method','recurrence','--scope','full','--max-steps','5','--seconds','1800'])
                self.assertEqual(cli.train_run(args,store),'incomplete')
            self.assertEqual(store.read_json('closure_contract.json')['tasks'],list(TASKS))
        self.assertEqual(len(captured['graph'].outlets),1)
        outlet=next(iter(captured['graph'].outlets.values()))
        self.assertEqual(outlet.parameters['task'],'local')
        self.assertEqual(outlet.parameters['scope'],'full')
        self.assertNotIn('produces_certificate',outlet.parameters)
        self.assertEqual(captured['state'].b.actions,5)


if __name__ == '__main__': unittest.main()
