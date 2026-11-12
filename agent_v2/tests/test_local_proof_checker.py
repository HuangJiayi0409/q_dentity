"""Real generated Lean proofs, original assembly, and untrusted input rejection."""
from dataclasses import replace
from pathlib import Path
import unittest

from agent_v2.tests import test_local_tasks as fixtures


class LocalProofCheckerTests(unittest.TestCase):
    def setUp(self):
        fixtures.LocalTaskTests.setUp(self)
        from agent_v2.local_proof_checker import LocalLeanChecker
        self.checker = LocalLeanChecker()
        self.context = {'source': self.source.to_dict(), 'source_sha256': self.source.sha256,
            'run_dir': str(self.run), 'attempt_dir': str(self.run/'check'), 'seconds': 120}

    def check(self, task, term, **context):
        from agent_v2.executor import _candidate_request
        self.checker.register_task(task)
        return self.checker.check_partial(_candidate_request(self.candidate_for(task, term)), dict(self.context, **context))

    def test_command_injection_and_executable_tactics_rejected(self):
        task = self.make_task(self.state, 'original', 'original')
        for term in ('by sorry', 'by run_tac IO.println "x"', 'by native_decide',
                     'by exact True.intro\naxiom evil : False', 'by exact (by_elab return Lean.mkSorry (Lean.mkConst ``True) true)',
                     'by exact True.intro\nimport Mathlib'):
            with self.subTest(term=term):
                result = self.check(task, term)
                self.assertFalse(result['accepted'], result)
                self.assertEqual(result['status'], 'incomplete', result)
        self.assertFalse((self.run/'check').exists())

    def test_registered_candidate_cannot_omit_source_or_change_schema(self):
        from agent_v2.executor import _candidate_request
        task = self.make_task(self.state, 'original', 'original')
        self.checker.register_task(task)
        request = _candidate_request(self.candidate_for(task, 'by constructor <;> trivial'))
        context = dict(self.context, seconds=0)
        omitted = dict(context); del omitted['source']
        for candidate, ctx in [(request, omitted), (dict(request, schema_version=2), context)]:
            result = self.checker.check_partial(candidate, ctx)
            self.assertEqual(result['status'], 'integrity_error', result)

    def test_real_closed_lemma_negative_replay_and_original(self):
        from agent_v2.executor import assemble_term, verify_and_update
        from agent_v2.models import JointAction, ExecutionResult, FailureSignature, Cost, Obligation
        action = JointAction('local-test', 'identity', 'original', 'original', 'LLM', 'llm', {})
        children = (Obligation('left', 'subgoal', 'True', 'Synthetic.statement', self.source.sha256),
                    Obligation('right', 'subgoal', 'True', 'Synthetic.statement', self.source.sha256))
        bridge = self.make_task(self.state, 'original', 'original', children=children)
        bad = self.check(bridge, 'by exact True.intro')
        self.assertFalse(bad['accepted'], bad)
        self.assertEqual(bad['sigma']['code'], 'lean_check_failed', bad)

        def apply(state, task, term):
            candidate = self.candidate_for(task, term); self.checker.register_task(task)
            result = ExecutionResult('symbolic_constructed', (candidate,), candidate.replaces,
                FailureSignature('construction', 'generated_test', 'Synthetic generated proof.', None), Cost(0, 1), {}, (), (), False)
            updated, diagnostics = verify_and_update(state, action, result, self.checker, self.context)
            if candidate.id not in [c.id for c in updated.C]:
                diagnostics += [p.read_text() for p in (self.run/'check').rglob('stdout.jsonl')]
            self.assertIn(candidate.id, [c.id for c in updated.C], diagnostics)
            return updated

        state = apply(self.state, bridge, 'fun h₁ h₂ => And.intro h₁ h₂')
        self.assertEqual([o.id for o in state.O], ['left', 'right'])
        state = apply(state, self.make_task(state, state.r, 'left'), 'by exact True.intro')
        from agent_v2.local_tasks import dependency_name
        dependency = state.C[-1].id
        state = apply(state, self.make_task(state, state.r, 'right', dependencies=(dependency,)),
                      'by exact ' + dependency_name(dependency))
        cert = state.C[0]
        replay = self.check(bridge, cert.proof_term, prior_evidence=cert.to_dict()['evidence'])
        self.assertTrue(replay['accepted'], replay)
        bad_evidence = cert.to_dict()['evidence']; bad_evidence['proof_term'] = 'by rfl'
        self.assertFalse(self.check(bridge, cert.proof_term, prior_evidence=bad_evidence)['accepted'])
        report = {'state': state.to_dict(), 'proof_term': assemble_term(state), 'run_dir': str(self.run), 'seconds': 120}
        checked = self.checker.accept_original(report, self.source.to_dict(), self.run/'final')
        self.assertTrue(checked['accepted'], checked)
        self.assertEqual(checked['evidence']['audit']['theorem'], self.source.theorem)


if __name__ == '__main__': unittest.main()
