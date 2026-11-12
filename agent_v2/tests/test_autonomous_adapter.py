"""Control-contract fixtures only; mocked clients/checkers are not proof evidence."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from agent_v2.models import Budget, JointAction, initial_state
from agent_v2.storage import RunStore, freeze_source


class ProposalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        source = root / 'Source.lean'
        source.write_text('import Init\ntheorem demo : True := by sorry\n')
        self.store = RunStore.create(root / 'runs')
        self.state, self.rep = initial_state(freeze_source(source, 'synthetic', 'demo', self.store,
                                                          proposition='True'), Budget(60, 4))
        self.action = JointAction('a', 'identity', 'original', 'original', 'LLM', 'llm',
                                  {'autonomous': True, 'goal_id': 'original', 'seconds': 30})

    def tearDown(self): self.temp.cleanup()

    def test_proposal_cannot_mutate_state_before_lean(self):
        from agent_v2.graph_proposals import bind_proposal
        before = self.state.to_dict()
        task, candidate, children = bind_proposal(self.state, self.action, {
            'kind': 'decompose', 'children': ['True', 'True ∧ True'],
            'proof_term': 'by intros; trivial'})
        self.assertEqual(before, self.state.to_dict())
        self.assertEqual(candidate.closes, 'original')
        self.assertEqual(task.proposition, '(True) → (True ∧ True) → (True)')
        self.assertEqual(len(children), 2)
        self.assertTrue(all(c.origin_action == 'a' for c in children))

    def test_unknown_fields_and_unbounded_children_rejected(self):
        from agent_v2.graph_proposals import bind_proposal
        from agent_v2.models import ContractError
        for response in [
            {'kind':'prove','proof_term':'by trivial','source':'changed'},
            {'kind':'decompose','proof_term':'by trivial','children':['True']*4},
            {'kind':'lemma','proof_term':'by trivial','proposition':'False','children':['True']},
        ]:
            with self.subTest(response=response), self.assertRaises(ContractError):
                bind_proposal(self.state, self.action, response)

    def test_selected_task_requires_current_graph_target(self):
        from agent_v2.graph_proposals import bind_proposal
        from agent_v2.models import ContractError
        action = replace(self.action, theta={'goal_id':'foreign'})
        with self.assertRaises(ContractError):
            bind_proposal(self.state, action, {'kind':'prove','proof_term':'by trivial'})

    def test_prompt_exposes_dependency_names_not_proof_scripts(self):
        from agent_v2.autonomous_adapter import prompt_context
        from agent_v2.models import VerifiedCertificate
        cert = VerifiedCertificate('c', 'True', 'SECRET_OLD_PROOF', self.state.G.sha256, (),
                                  {'source_sha256':self.state.G.sha256,'proposition':'True'})
        state = replace(self.state, C=(cert,))
        payload = prompt_context(state, self.action, self.rep, {}, [], [])
        self.assertNotIn('SECRET_OLD_PROOF', str(payload))
        self.assertIn('AgentV2Dependency', str(payload))


if __name__ == '__main__': unittest.main()
