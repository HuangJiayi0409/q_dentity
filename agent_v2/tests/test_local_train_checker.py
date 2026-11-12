"""Mixed CAS/generated Train plumbing; fixed test terms, not model performance."""
from dataclasses import replace
import json
import os
from pathlib import Path
import tempfile
import unittest

from agent_v2.models import Budget, Candidate, Cost, ExecutionResult, FailureSignature, JointAction, initial_state
from agent_v2.storage import RunStore, load_train
from agent_v2.executor import _candidate_request, assemble_term, verify_and_update
from agent_v2.local_tasks import make_task, candidate_for, dependency_name
from agent_v2.local_proof_checker import LocalLeanChecker


class MixedLocalTrainCheckerTests(unittest.TestCase):
    def test_cas_generated_endpoint_dependencies_replay_and_original(self):
        from agent_v2.formal_frontend import analyze_source
        from agent_v2.telescoping_closure import closure_blueprint, make_closure_candidate
        from agent_v2.telescoping_translation import local_proof
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        evidence_root = Path(os.environ.get('AGENT_V2_LOCAL_CHECK_EVIDENCE', tmp.name))
        store = RunStore.create(evidence_root)
        source = load_train('FQI-SRC-AP-3.3.9', store)
        front = analyze_source(source.to_dict(), store.root)
        source = replace(source, proposition=front['original_proposition'])
        front = analyze_source(source.to_dict(), store.root)
        plan = closure_blueprint(front)
        checker = LocalLeanChecker()
        state, _ = initial_state(source, Budget(1800, 10))
        action = JointAction('mixed-check', 'identity', 'original', 'original', 'LLM', 'llm', {})
        context = {'source': source.to_dict(), 'source_sha256': source.sha256, 'run_dir': str(store.root), 'seconds': 300}

        def apply(candidate, stage):
            nonlocal state
            result = ExecutionResult('symbolic_constructed', (candidate,), candidate.replaces,
                FailureSignature('construction', 'fixed_checker_test', 'Fixed plumbing test, no model.', None),
                Cost(0, 1), {}, (), (), False)
            state, diagnostics = verify_and_update(state, action, result, checker,
                dict(context, attempt_dir=str(store.path(stage))))
            store.path(stage + '.json').write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2))
            errors = [p.read_text() for p in store.path(stage).rglob('stdout.jsonl') if '"severity":"error"' in p.read_text()]
            self.assertIn(candidate.id, [c.id for c in state.C], (diagnostics, errors))

        local = Candidate(plan['local_id'], front['local_proposition'], local_proof(front),
                          'AgentV2Candidate.proof', source.sha256)
        apply(local, 'cas')
        approved = {c.id: c.to_dict() for c in state.C}
        bridge = make_closure_candidate(front, 'bridge', approved, action.id)
        apply(bridge, 'bridge')
        # These short terms are authored in the test, never external model output.
        lower = make_task(state, state.r, plan['obligation_ids']['zero_endpoint'])
        checker.register_task(lower)
        apply(candidate_for(lower, 'by\n  intro K inst q m n h_domain\n  exact FiniteQBenchmark.gaussian_above q (Nat.lt_succ_self m)'), 'generated_lower')
        upper = make_task(state, state.r, plan['obligation_ids']['upper_endpoint'])
        checker.register_task(upper)
        apply(candidate_for(upper, 'by\n  intro K inst q m n h_domain\n  simpa only [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]'), 'generated_upper')
        self.assertEqual(state.O, ())
        replay_checker = LocalLeanChecker(tasks=[t.to_dict() for t in checker.tasks.values()])
        for certificate in (state.C[0], state.C[-1]):
            request = {'id': certificate.id, 'proposition': certificate.proposition, 'proof_term': certificate.proof_term,
                'theorem': 'AgentV2Candidate.proof', 'source_sha256': source.sha256, 'dependencies': list(certificate.dependencies)}
            replay = replay_checker.check_partial(request, dict(context,
                attempt_dir=str(store.path('replay-' + certificate.id)), prior_evidence=certificate.to_dict()['evidence'],
                approved_certificates={c.id: c.to_dict() for c in state.C}))
            self.assertTrue(replay['accepted'], replay)
        report = {'state': state.to_dict(), 'proof_term': assemble_term(state), 'seconds': 300, 'run_dir': str(store.root)}
        final = replay_checker.accept_original(report, source.to_dict(), store.path('original'))
        store.path('final.json').write_text(json.dumps(final, ensure_ascii=False, indent=2))
        self.assertTrue(final['accepted'], final)
        self.assertEqual(final['evidence']['audit']['universe_parameter_count'], 1)


if __name__ == '__main__': unittest.main()
